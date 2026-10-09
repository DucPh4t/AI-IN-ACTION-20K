"""research.py - STUDENT IMPLEMENTS.  The main script.   Guide: GUIDE.md, part 3.

Usage:  python research.py "survey about world model"
Result: reports/<slug>.md   reports/<slug>.sources.json   reports/<slug>.meta.json
"""
import json
import os
import re
import sys
import time
from collections import Counter
from pathlib import Path

from agents import FINALIZER_PATH, REPORT_PATH, SOURCES_PATH, VALIDATOR_PATH, WORKDIR, build_lead_agent
from model import make_model
from sandbox import download, open_sandbox, upload

ROOT = Path(__file__).parent
REPORTS = ROOT / "reports"
VALIDATOR_SOURCE = ROOT / "check_citations.py"
FINALIZER_SOURCE = ROOT / "finalize_citations.py"   # provided: uploaded next to your validator


def slugify(topic):
    """Turn a topic into a safe file name: lower case, runs of non-word characters become one "-", max 60 chars,
    never empty (fall back to "topic"). The topic is user input: "../../x" must not escape reports/.
    """
    s = str(topic or "").strip().lower()
    s = re.sub(r"[^\w]+", "-", s).strip("-")
    s = s[:60].rstrip("-")
    return s or "topic"


def build_prompt(topic):
    """The user message sent to the lead agent."""
    return (
        f"Conduct an in-depth academic research survey on the topic: '{topic}'.\n\n"
        f"Requirements:\n"
        f"1. Plan with write_todos and split into >= 3 focused sub-questions.\n"
        f"2. Delegate sub-questions to the `researcher` subagent with the `task` tool in parallel.\n"
        f"3. Ensure at least 3 distinct source families among (arxiv, hf-daily, hf-search, web) are present in notes. Instruct researchers to query arxiv_search, hf_search_papers, and hf_daily_papers.\n"
        f"4. Consolidate sources into {SOURCES_PATH}. Verify that {SOURCES_PATH} includes papers from all 3 source families (arxiv, hf-search, and hf-daily).\n"
        f"5. Write the body of {REPORT_PATH} following the required sections (TL;DR, Background, thematic sections, Trends and open problems) with inline [n] citations. Cite papers across all 3 source families. Do NOT write ## References.\n"
        f"6. Execute {FINALIZER_PATH} to generate references and renumber citations.\n"
        f"7. Execute {VALIDATOR_PATH} to verify citations until it prints OK.\n"
        f"8. Delegate spot-check of key citations to `citation-checker` subagent."
    )


def summarize(messages, elapsed, model_name):
    """Return {"model", "elapsed_s", "subagent_calls", "tool_calls": {name: count}, "tokens": {"input", "output"}}.

    Walk the lead's messages; for every message with tool_calls count call["name"] (subagent_calls = the
    count of "task"); add the input/output token counts from each message's usage_metadata when present.
    (Lead messages only: subagent tokens are not included, so this undercounts the real cost.)
    elapsed_s rounded to 0.1.
    """
    tool_counts = Counter()
    input_tokens = 0
    output_tokens = 0

    for msg in messages:
        # Extract tool calls
        calls = []
        if hasattr(msg, "tool_calls") and msg.tool_calls:
            calls = msg.tool_calls
        elif isinstance(msg, dict) and msg.get("tool_calls"):
            calls = msg.get("tool_calls")

        for call in calls:
            name = call.get("name") if isinstance(call, dict) else getattr(call, "name", "")
            if name:
                tool_counts[name] += 1

        # Extract token usage metadata if present
        usage = None
        if hasattr(msg, "usage_metadata") and msg.usage_metadata:
            usage = msg.usage_metadata
        elif isinstance(msg, dict) and msg.get("usage_metadata"):
            usage = msg.get("usage_metadata")
        elif hasattr(msg, "response_metadata") and isinstance(msg.response_metadata, dict):
            usage = msg.response_metadata.get("token_usage") or msg.response_metadata.get("usage")

        if isinstance(usage, dict):
            input_tokens += int(usage.get("input_tokens") or usage.get("prompt_tokens") or 0)
            output_tokens += int(usage.get("output_tokens") or usage.get("completion_tokens") or 0)

    subagent_calls = tool_counts.get("task", 0)

    return {
        "model": model_name,
        "elapsed_s": round(float(elapsed), 1),
        "subagent_calls": subagent_calls,
        "tool_calls": dict(tool_counts),
        "tokens": {
            "input": input_tokens,
            "output": output_tokens,
        },
    }


def save_outputs(backend, topic, messages, elapsed, model_name, reports_dir=REPORTS):
    """Download the report from the sandbox and write the three files into reports_dir. Return the report path.

    Files: <slug>.sources.json, <slug>.meta.json and <slug>.md
    """
    files = download(backend, [REPORT_PATH, SOURCES_PATH])
    report_bytes = files.get(REPORT_PATH)
    sources_bytes = files.get(SOURCES_PATH)

    if not report_bytes or not report_bytes.strip():
        raise RuntimeError(f"Report at {REPORT_PATH} is missing or empty in the sandbox")
    if not sources_bytes:
        raise RuntimeError(f"Sources file at {SOURCES_PATH} is missing in the sandbox")

    try:
        sources_json = json.loads(sources_bytes.decode("utf-8"))
        if not isinstance(sources_json, list):
            raise ValueError("sources.json must be a JSON array")
    except Exception as exc:
        raise RuntimeError(f"sources.json is invalid JSON: {exc}")

    reports_dir = Path(reports_dir)
    reports_dir.mkdir(parents=True, exist_ok=True)
    slug = slugify(topic)

    # Calculate distinct source families
    source_families = sorted(list({
        str(s.get("source", "")).strip() for s in sources_json if isinstance(s, dict) and s.get("source")
    }))

    summary_stats = summarize(messages, elapsed, model_name)
    meta_info = {
        "topic": topic,
        **summary_stats,
        "n_sources": len(sources_json),
        "source_families": source_families,
    }

    sources_target = reports_dir / f"{slug}.sources.json"
    meta_target = reports_dir / f"{slug}.meta.json"
    report_target = reports_dir / f"{slug}.md"

    sources_target.write_bytes(sources_bytes)
    meta_target.write_text(json.dumps(meta_info, indent=2, ensure_ascii=False), encoding="utf-8")
    report_target.write_bytes(report_bytes)

    return report_target


def main(topic):
    """Return the process exit code (0 ok, 1 failed run, 2 no topic)."""
    topic_clean = str(topic or "").strip()
    if not topic_clean:
        print("Usage: python research.py '<topic>'", file=sys.stderr)
        return 2

    model = make_model()
    model_name = os.getenv("LAB_MODEL", "model")
    start = time.monotonic()

    with open_sandbox() as backend:
        backend.execute(f"mkdir -p {WORKDIR}/research/notes {WORKDIR}/report")
        upload(
            backend,
            {
                VALIDATOR_PATH: VALIDATOR_SOURCE.read_bytes(),
                FINALIZER_PATH: FINALIZER_SOURCE.read_bytes(),
            },
        )
        agent = build_lead_agent(backend, model)
        result = agent.invoke(
            {"messages": [{"role": "user", "content": build_prompt(topic_clean)}]},
            config={"recursion_limit": 1000},
        )
        messages = result.get("messages", []) if isinstance(result, dict) else []
        elapsed = time.monotonic() - start

        try:
            saved_path = save_outputs(backend, topic_clean, messages, elapsed, model_name, reports_dir=REPORTS)
        except RuntimeError as exc:
            print(f"FAILED: {exc}", file=sys.stderr)
            return 1

    print(f"Report saved to {saved_path}")
    return 0


if __name__ == "__main__":
    sys.exit(main(" ".join(sys.argv[1:])))
