"""check_citations.py - STUDENT IMPLEMENTS `check`.   Runs INSIDE the sandbox (standard library only).

research.py uploads this file to the sandbox and the lead agent runs it with the `execute` tool:
    python3 /tmp/work/research/check_citations.py [report.md] [sources.json]
It must exit 0 and print "OK: ..." when the report is consistent, else print each problem and exit 1.
"""
import json
import sys

REPORT = "/tmp/work/report/report.md"
SOURCES = "/tmp/work/research/sources.json"


import re

_GROUP = re.compile(r"\[(\d+(?:\s*[,–-]\s*\d+)*)\](?!\()")   # [3]  [1, 2]  [1-3]  [2-3]; not [3](link)
_CODE = re.compile(r"(```.*?```|`[^`\n]*`)", re.DOTALL)
_REF_HEADING = re.compile(r"(?m)^##[ \t]+References[ \t]*$")


def _group_numbers(group):
    numbers = []
    for part in re.split(r"\s*,\s*", group):
        span = re.fullmatch(r"(\d+)\s*[–-]\s*(\d+)", part)
        if span:
            a, b = int(span.group(1)), int(span.group(2))
            numbers.extend(range(a, b + 1) if 0 <= b - a <= 200 else [a, b])
        elif part.isdigit():
            numbers.append(int(part))
    return numbers


def check(report_text, sources):
    """Return a list of problem strings (empty list = OK)."""
    problems = []
    if not sources or not isinstance(sources, list):
        return ["no sources in sources.json"]

    seen_urls = set()
    source_by_n = {}
    for entry in sources:
        if not isinstance(entry, dict):
            problems.append(f"source entry is not an object: {entry!r}")
            continue
        n = entry.get("n")
        if not isinstance(n, int):
            problems.append(f"source {entry} has non-integer n: {n!r}")
            continue
        if n in source_by_n:
            problems.append(f"duplicate source number in sources.json: [{n}]")
        else:
            source_by_n[n] = entry

        url = entry.get("url")
        if not isinstance(url, str) or not (url.startswith("http://") or url.startswith("https://")):
            problems.append(f"source [{n}] url must start with http:// or https://: {url!r}")
        elif url in seen_urls:
            problems.append(f"the same url must not appear twice: {url}")
        else:
            seen_urls.add(url)

    matches = list(_REF_HEADING.finditer(report_text))
    if not matches:
        problems.append("missing '## References' section")
        body = report_text
        ref_lines_raw = []
    else:
        body = report_text[:matches[-1].start()]
        ref_text = report_text[matches[-1].end():]
        ref_lines_raw = [line.strip() for line in ref_text.splitlines() if line.strip()]

    # Extract cited numbers from body (excluding code)
    segments = _CODE.split(body)
    cited = set()
    for i, segment in enumerate(segments):
        if i % 2:
            continue
        for match in _GROUP.finditer(segment):
            for num in _group_numbers(match.group(1)):
                cited.add(num)

    for num in sorted(cited):
        if num not in source_by_n:
            problems.append(f"[{num}] cited but missing from sources.json")

    for s_n in sorted(source_by_n.keys()):
        if s_n not in cited:
            problems.append(f"source [{s_n}] never cited")

    ref_seen = {}
    for line in ref_lines_raw:
        m = re.match(r"^\[(\d+)\]\s*(.*)$", line)
        if not m:
            problems.append(f"reference line does not start with [n]: {line}")
            continue
        ref_num = int(m.group(1))
        if ref_num in ref_seen:
            problems.append(f"reference line [{ref_num}] appears more than once")
        else:
            ref_seen[ref_num] = line

        if ref_num not in source_by_n:
            problems.append(f"reference line [{ref_num}] is not a source")

        urls = re.findall(r"https?://[^\s)\]]+", line)
        if len(urls) == 0:
            problems.append(f"reference line [{ref_num}] has no URL")
        elif len(urls) > 1:
            problems.append(f"reference line [{ref_num}] bundles several sources: {urls}")
        else:
            url_found = urls[0]
            if ref_num in source_by_n:
                expected_url = source_by_n[ref_num].get("url")
                if url_found != expected_url:
                    problems.append(f"reference line [{ref_num}] URL does not match sources.json: {url_found} != {expected_url}")

    for s_n in sorted(source_by_n.keys()):
        if s_n not in ref_seen:
            problems.append(f"source [{s_n}] is missing a reference line")

    return problems


def main(argv):
    report_path = argv[1] if len(argv) > 1 else REPORT
    sources_path = argv[2] if len(argv) > 2 else SOURCES
    try:
        with open(report_path, encoding="utf-8") as f:
            report = f.read()
        with open(sources_path, encoding="utf-8") as f:
            sources = json.load(f)
    except (OSError, ValueError) as exc:
        print(f"cannot read inputs: {exc}")
        return 1
    problems = check(report, sources)
    if problems:
        print("\n".join(problems))
        return 1
    print(f"OK: {len(sources)} sources, all citations resolve")
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv))
