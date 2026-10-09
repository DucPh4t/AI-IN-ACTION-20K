"""tools.py - STUDENT IMPLEMENTS.  Source tools for the research agents.   Guide: GUIDE.md, part 1.

Rules for every tool:
  * runs on the HOST (not in the sandbox): API keys must never enter the sandbox;
  * returns a STRING (JSON text of compact records) and NEVER raises:
        "NO RESULTS"  when the source answers with nothing,
        "ERROR: ..."  when the source keeps failing after the retries (the agent then tries another source);
  * the docstring is the tool description the LLM reads: keep it precise (what it does, what it returns, when to use it).
Try your tools without any agent:   python tools.py
"""
import json
import os
import random
import re
import time
import xml.etree.ElementTree as ET

import httpx
from langchain_core.tools import tool

# ---- constants (given) ----
ARXIV_URL = "https://export.arxiv.org/api/query"  # https only: http answers 301
HF_DAILY_URL = "https://huggingface.co/api/daily_papers"
HF_SEARCH_URL = "https://huggingface.co/api/papers/search"
EXA_URL = "https://mcp.exa.ai/mcp"

_LAST_ARXIV_CALL = 0.0


class RetryableError(Exception):
    """Given. Raise it inside a call to ask with_retry to wait and try again (retry_after in seconds, optional)."""

    def __init__(self, message, retry_after=None):
        super().__init__(message)
        self.retry_after = retry_after


def _clean_text(text):
    if not text:
        return ""
    return " ".join(str(text).split())


def _redact(text):
    if not text:
        return ""
    key = os.getenv("EXA_API_KEY", "").strip()
    if key and key in text:
        return text.replace(key, "[REDACTED]")
    return text


# ---- TODO 1: retry helper ----
def with_retry(fn, *, attempts=5, base=1.0, cap=30.0):
    """Call fn(); when it raises RetryableError, wait and call it again.

    Exponential backoff with random jitter, respects Retry-After, capped at `cap` seconds.
    Raises on the final attempt without sleeping.
    """
    for attempt in range(attempts):
        try:
            return fn()
        except RetryableError as e:
            if attempt == attempts - 1:
                raise
            if e.retry_after is not None:
                try:
                    delay = float(e.retry_after)
                except (ValueError, TypeError):
                    delay = base * (2 ** attempt)
            else:
                backoff = base * (2 ** attempt)
                jitter = random.uniform(0, 0.5 * backoff)
                delay = backoff + jitter
            delay = min(delay, cap)
            time.sleep(delay)


def _http_get_with_retry(url, params=None, timeout=30.0, attempts=5, cap=30.0):
    def _call():
        try:
            with httpx.Client(timeout=timeout, follow_redirects=True) as client:
                resp = client.get(url, params=params)
                if resp.status_code == 429 or 500 <= resp.status_code <= 504:
                    retry_after = resp.headers.get("Retry-After")
                    delay = float(retry_after) if retry_after and retry_after.replace(".", "", 1).isdigit() else None
                    raise RetryableError(f"HTTP {resp.status_code}", retry_after=delay)
                resp.raise_for_status()
                return resp
        except (httpx.TransportError, httpx.TimeoutException) as exc:
            raise RetryableError(f"Network error: {exc}")

    return with_retry(_call, attempts=attempts, cap=cap)


# ---- TODO 2: arXiv ----
@tool
def arxiv_search(query: str, max_results: int = 10) -> str:
    """Search arXiv papers by keywords, newest first. Returns a JSON list of {id, url, published, title, summary}."""
    global _LAST_ARXIV_CALL
    try:
        terms = re.findall(r"[\w\-]+", query)
        if not terms:
            return "NO RESULTS"

        # Respect arXiv rate limit: at least 3 seconds between requests
        elapsed = time.time() - _LAST_ARXIV_CALL
        if elapsed < 3.0:
            time.sleep(3.0 - elapsed)
        _LAST_ARXIV_CALL = time.time()

        clamped_results = max(1, min(max_results, 30))
        search_query = " AND ".join(f"all:{t}" for t in terms)
        params = {
            "search_query": search_query,
            "sortBy": "submittedDate",
            "sortOrder": "descending",
            "max_results": clamped_results,
        }

        # arXiv gets higher cap (60s) and 5 attempts
        resp = _http_get_with_retry(ARXIV_URL, params=params, attempts=5, cap=60.0)
        _LAST_ARXIV_CALL = time.time()

        root = ET.fromstring(resp.text)
        ns = {"atom": "http://www.w3.org/2005/Atom"}
        entries = root.findall("atom:entry", ns)
        if not entries:
            return "NO RESULTS"

        records = []
        for entry in entries:
            id_elem = entry.find("atom:id", ns)
            if id_elem is None or not id_elem.text:
                continue
            raw_id = id_elem.text.strip().split("/abs/")[-1]
            paper_id = re.sub(r"v\d+$", "", raw_id)
            url = f"https://arxiv.org/abs/{paper_id}"

            pub_elem = entry.find("atom:published", ns)
            published = pub_elem.text.strip()[:10] if pub_elem is not None and pub_elem.text else ""

            title_elem = entry.find("atom:title", ns)
            title = _clean_text(title_elem.text) if title_elem is not None else ""

            sum_elem = entry.find("atom:summary", ns)
            summary = _clean_text(sum_elem.text)[:600] if sum_elem is not None else ""

            records.append({
                "id": paper_id,
                "url": url,
                "published": published,
                "title": title,
                "summary": summary,
                "source": "arxiv",
            })

        if not records:
            return "NO RESULTS"
        return json.dumps(records, ensure_ascii=False)
    except Exception as exc:
        return f"ERROR: {type(exc).__name__}: {exc}"


# ---- TODO 3: Hugging Face ----
@tool
def hf_daily_papers(limit: int = 30, date: str = "", keyword: str = "") -> str:
    """Hugging Face Daily Papers = what is trending in AI research. Returns a JSON list of
    {id, url, published, title, summary, upvotes, github, stars, source} sorted by upvotes. `date` is YYYY-MM-DD (empty = latest).
    `keyword` filters title/summary; there is no topic search on this endpoint (use hf_search_papers for a topic)."""
    try:
        clamped_limit = max(1, min(limit, 100))
        params = {"limit": clamped_limit}
        if date.strip():
            params["date"] = date.strip()

        resp = _http_get_with_retry(HF_DAILY_URL, params=params, attempts=5, cap=30.0)
        items = resp.json()
        if not isinstance(items, list) or not items:
            return "NO RESULTS"

        records = []
        kw = keyword.strip().lower()
        for item in items:
            if not isinstance(item, dict):
                continue
            paper = item.get("paper") if isinstance(item.get("paper"), dict) else item
            paper_id = paper.get("id") or item.get("id")
            if not paper_id:
                continue

            title = _clean_text(paper.get("title") or item.get("title") or "")
            summary = _clean_text(paper.get("summary") or item.get("summary") or "")[:600]
            published = str(paper.get("publishedAt") or item.get("publishedAt") or "")[:10]
            upvotes = paper.get("upvotes") or item.get("upvotes") or 0
            github = paper.get("githubRepo") or item.get("githubRepo") or ""
            stars = paper.get("githubStars") or item.get("githubStars") or 0
            url = f"https://huggingface.co/papers/{paper_id}"

            if kw:
                haystack = f"{title} {summary}".lower()
                if kw not in haystack:
                    continue

            records.append({
                "id": str(paper_id),
                "url": url,
                "published": published,
                "title": title,
                "summary": summary,
                "upvotes": int(upvotes) if str(upvotes).isdigit() else 0,
                "github": str(github),
                "stars": int(stars) if str(stars).isdigit() else 0,
                "source": "hf-daily",
            })

        if not records:
            return "NO RESULTS"
        records.sort(key=lambda r: r.get("upvotes", 0), reverse=True)
        return json.dumps(records, ensure_ascii=False)
    except Exception as exc:
        return f"ERROR: {type(exc).__name__}: {exc}"


@tool
def hf_search_papers(query: str, limit: int = 10) -> str:
    """Search Hugging Face papers by topic. Returns a JSON list of
    {id, url, published, title, summary, upvotes, github, stars, source}."""
    try:
        q = query.strip()
        if not q:
            return "NO RESULTS"
        clamped_limit = max(1, min(limit, 50))
        params = {"q": q, "limit": clamped_limit}

        resp = _http_get_with_retry(HF_SEARCH_URL, params=params, attempts=5, cap=30.0)
        items = resp.json()
        if not isinstance(items, list) or not items:
            return "NO RESULTS"

        records = []
        for item in items:
            if not isinstance(item, dict):
                continue
            paper = item.get("paper") if isinstance(item.get("paper"), dict) else item
            paper_id = paper.get("id") or item.get("id")
            if not paper_id:
                continue

            title = _clean_text(paper.get("title") or item.get("title") or "")
            summary = _clean_text(
                paper.get("ai_summary") or item.get("ai_summary") or paper.get("summary") or item.get("summary") or ""
            )[:600]
            published = str(paper.get("publishedAt") or item.get("publishedAt") or "")[:10]
            upvotes = paper.get("upvotes") or item.get("upvotes") or 0
            github = paper.get("githubRepo") or item.get("githubRepo") or ""
            stars = paper.get("githubStars") or item.get("githubStars") or 0
            url = f"https://huggingface.co/papers/{paper_id}"

            records.append({
                "id": str(paper_id),
                "url": url,
                "published": published,
                "title": title,
                "summary": summary,
                "upvotes": int(upvotes) if str(upvotes).isdigit() else 0,
                "github": str(github),
                "stars": int(stars) if str(stars).isdigit() else 0,
                "source": "hf-search",
            })

        if not records:
            return "NO RESULTS"
        return json.dumps(records, ensure_ascii=False)
    except Exception as exc:
        return f"ERROR: {type(exc).__name__}: {exc}"


# ---- TODO 4: web search / fetch through the Exa MCP endpoint ----
def _call_exa_mcp(tool_name: str, arguments: dict) -> str:
    """Internal helper to call Exa MCP tool over JSON-RPC HTTP with retry and key redaction."""
    exa_key = os.getenv("EXA_API_KEY", "").strip()
    endpoint = f"{EXA_URL}?exaApiKey={exa_key}" if exa_key else EXA_URL
    headers = {
        "Content-Type": "application/json",
        "Accept": "application/json, text/event-stream",
    }
    if exa_key:
        headers["Authorization"] = f"Bearer {exa_key}"

    payload = {
        "jsonrpc": "2.0",
        "id": 1,
        "method": "tools/call",
        "params": {
            "name": tool_name,
            "arguments": arguments,
        },
    }

    def _post():
        try:
            with httpx.Client(timeout=20.0) as client:
                resp = client.post(endpoint, json=payload, headers=headers)
                if resp.status_code == 429 or 500 <= resp.status_code <= 504:
                    retry_after = resp.headers.get("Retry-After")
                    delay = float(retry_after) if retry_after and retry_after.replace(".", "", 1).isdigit() else 2.0
                    raise RetryableError(f"Exa HTTP {resp.status_code}", retry_after=min(delay, 5.0))

                # Parse response: could be SSE event-stream or plain JSON
                text = resp.text.strip()
                data = None
                for line in text.splitlines():
                    if line.startswith("data:"):
                        try:
                            data = json.loads(line[5:].strip())
                            break
                        except ValueError:
                            pass
                if data is None:
                    try:
                        data = resp.json()
                    except ValueError:
                        raise RetryableError(f"Invalid Exa response: {text[:200]}")

                # Check JSON-RPC errors
                if "error" in data:
                    err = data["error"]
                    err_msg = str(err.get("message", ""))
                    if "rate limit" in err_msg.lower() or err.get("code") == -32000:
                        raise RetryableError(f"Exa rate limit: {err_msg}", retry_after=2.0)
                    raise RuntimeError(f"Exa RPC error: {err_msg}")

                result = data.get("result", {})
                # Check rate limit signaled in _meta or text
                meta = result.get("_meta", {})
                if meta.get("rate_limited") or "rate limit" in str(meta).lower():
                    raise RetryableError("Exa rate limit signaled in meta", retry_after=2.0)

                contents = result.get("content", [])
                text_parts = []
                for item in contents:
                    if isinstance(item, dict) and item.get("type") == "text":
                        t = item.get("text", "")
                        if "rate limit" in t.lower() and "dashboard.exa.ai" in t:
                            raise RetryableError("Exa rate limit signaled in content text", retry_after=2.0)
                        text_parts.append(t)

                return "\n\n".join(text_parts).strip()
        except (httpx.TransportError, httpx.TimeoutException) as exc:
            raise RetryableError(f"Exa network error: {exc}", retry_after=2.0)

    attempts = 3 if exa_key else 2
    return with_retry(_post, attempts=attempts, base=1.0, cap=5.0)


@tool
def web_search(query: str, objective: str = "", num_results: int = 5) -> str:
    """Search the web (Exa). Describe the ideal page in natural language. Returns clean text of the top results with URLs."""
    try:
        q = query.strip()
        if not q:
            return "NO RESULTS"
        obj = objective.strip() or f"find academic research and survey papers about {q}"
        clamped_n = max(1, min(num_results, 10))
        text = _call_exa_mcp("web_search_exa", {"query": q, "objective": obj, "numResults": clamped_n})
        if not text:
            return "NO RESULTS"
        return _redact(text)
    except Exception as exc:
        return f"ERROR: {type(exc).__name__}: {_redact(str(exc))}"


@tool
def web_fetch(url: str) -> str:
    """Read the full content of one web page (e.g. an arXiv abstract page) as markdown. Long pages are truncated."""
    try:
        u = url.strip()
        if not (u.startswith("http://") or u.startswith("https://")):
            return "ERROR: ValueError: invalid URL (must start with http:// or https://)"
        text = _call_exa_mcp("web_fetch_exa", {"urls": [u]})
        if not text:
            return "NO RESULTS"
        truncated = text[:12000]
        return _redact(truncated)
    except Exception as exc:
        return f"ERROR: {type(exc).__name__}: {_redact(str(exc))}"


# ---- TODO 5: registry (the researcher subagent gets exactly these) ----
SOURCE_TOOLS = [arxiv_search, hf_daily_papers, hf_search_papers, web_search, web_fetch]


if __name__ == "__main__":
    for name, fn, args in [
        ("arxiv_search", arxiv_search, {"query": "world model", "max_results": 3}),
        ("hf_daily_papers", hf_daily_papers, {"limit": 20}),
        ("hf_search_papers", hf_search_papers, {"query": "world model", "limit": 3}),
        ("web_search", web_search, {"query": "survey paper on world models", "num_results": 2}),
        ("web_fetch", web_fetch, {"url": "https://arxiv.org/abs/1803.10122"}),
    ]:
        try:
            print(f"== {name}\n{fn.invoke(args)[:400]}\n")
        except NotImplementedError as exc:
            print(f"== {name}: not implemented yet ({exc})\n")
