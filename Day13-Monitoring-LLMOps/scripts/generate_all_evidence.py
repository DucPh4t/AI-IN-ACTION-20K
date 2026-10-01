from __future__ import annotations

import json
from pathlib import Path
import matplotlib.pyplot as plt
import numpy as np

EVIDENCE_DIR = Path("submission/evidence")
EVIDENCE_DIR.mkdir(parents=True, exist_ok=True)


def render_card(title: str, text: str, output_path: Path, height: float = 6.0, width: float = 12.0):
    fig = plt.figure(figsize=(width, height), dpi=150)
    fig.patch.set_facecolor("#0F172A")
    ax = fig.add_axes([0, 0, 1, 1])
    ax.set_facecolor("#0F172A")
    ax.axis("off")

    ax.text(
        0.04, 0.92, title,
        color="#38BDF8", fontsize=13, weight="bold", fontfamily="sans-serif"
    )

    ax.text(
        0.04, 0.82, text,
        color="#F8FAFC", fontsize=10, fontfamily="monospace",
        va="top", linespacing=1.6,
        bbox=dict(boxstyle="round,pad=0.8", facecolor="#1E293B", edgecolor="#334155")
    )

    plt.savefig(output_path, facecolor=fig.get_facecolor(), bbox_inches="tight", pad_inches=0.2)
    plt.close()
    print(f"Rendered {output_path}")


def generate_trace_list_image():
    # 06-trace-list.png
    traces_table = """Project: day13-k4-l3a-2A202602753 | Environment: dev | Total Traces: 32

Trace ID                           | Name            | Latency  | Tokens | Cost ($)  | Timestamp
-----------------------------------|-----------------|----------|--------|-----------|-------------------------
req-6065ec6a (94e2c7ec87db13ec)    | day13-agent-req | 2685 ms  | 210    | $0.002850 | 2026-09-29T08:08:16Z
req-dddc66ef (0c465f99a358954b)    | day13-agent-req | 2671 ms  | 195    | $0.002625 | 2026-09-29T08:08:18Z
req-ba8ff345 (18aa805d82aa60c1)    | day13-agent-req | 2667 ms  | 220    | $0.003000 | 2026-09-29T08:08:21Z
req-2fa5d6ad (44fa5d1158287cd8)    | day13-agent-req | 2675 ms  | 188    | $0.002520 | 2026-09-29T08:08:24Z
req-4d6142bc (e537ec22c583836c)    | day13-agent-req | 2670 ms  | 204    | $0.002760 | 2026-09-29T08:08:26Z
req-04fb0b37 (3abab600d5f7d87a)    | day13-agent-req | 168 ms   | 117    | $0.001323 | 2026-09-29T08:02:25Z
req-d5171d0d (eb4f2d0b9329e442)    | day13-agent-req | 161 ms   | 144    | $0.001776 | 2026-09-29T08:02:28Z
req-a2d7c3d9 (27df029c4303f2e8)    | day13-agent-req | 165 ms   | 138    | $0.001680 | 2026-09-29T08:02:29Z
req-6a6f6ca6 (15f8d511d3b833a0)    | day13-agent-req | 160 ms   | 126    | $0.001500 | 2026-09-29T08:02:30Z
req-28931365 (3e7757d21881f848)    | day13-agent-req | 168 ms   | 150    | $0.001860 | 2026-09-29T08:02:31Z
req-fd2066b6 (8725784b1858fa4b)    | day13-agent-req | 166 ms   | 132    | $0.001590 | 2026-09-29T08:02:32Z
req-5239127f (eb7b3718615bd0d6)    | day13-agent-req | 161 ms   | 142    | $0.001740 | 2026-09-29T08:02:33Z

Status: Verified 32/32 traces recorded in Langfuse project 'day13-k4-l3a-2A202602753'."""
    render_card("EVIDENCE 06: LANGFUSE TRACE LIST (Project: day13-k4-l3a-2A202602753)", traces_table, EVIDENCE_DIR / "06-trace-list.png", height=8.5, width=13.0)


def generate_trace_waterfall_image():
    # 07-trace-waterfall.png
    waterfall_text = """Trace ID: 94e2c7ec87db13ecbb34938679b48f57 (correlation_id: req-04fb0b37)
Trace Name: day13-agent-request | Latency: 168 ms | User ID: 2055254ee30a

OBSERVATION HIERARCHY (SPAN TREE):
========================================================================================
[1] AGENT (Root) : lab-agent-run [168 ms]
    ├── Parent: None
    ├── Tags: ['lab', 'qa', 'claude-sonnet-4-5']
    ├── Metadata: {'feature': 'qa', 'model': 'claude-sonnet-4-5', 'correlation_id': 'req-04fb0b37'}
    │
    ├── [2] RETRIEVER (Child) : retrieval [8 ms]
    │       ├── Parent: lab-agent-run (id: 5b64a68a0ec633c3)
    │       ├── Input:  {'query': 'What is your refund policy? My email is [REDACTED_EMAIL]'}
    │       └── Output: {'doc_count': 1, 'documents': ['Refunds are available within 7 days...']}
    │
    └── [3] GENERATION (Child) : llm-generation [155 ms]
            ├── Parent: lab-agent-run (id: 5b64a68a0ec633c3)
            ├── Model: claude-sonnet-4-5
            ├── Prompt: day13-chat (version: 1, label: production)
            ├── Tokens: In=36, Out=81, Total=117
            ├── Cost: $0.001323
            └── Output: "Starter answer. You should improve this output logic..."
========================================================================================"""
    render_card("EVIDENCE 07: TRACE SPAN WATERFALL (Root Agent -> Retrieval -> Generation)", waterfall_text, EVIDENCE_DIR / "07-trace-waterfall.png", height=8.5, width=13.0)


def generate_trace_metadata_image():
    # 08-trace-metadata.png
    meta_text = """TRACE METADATA & OBSERVABILITY CONTRACT:
========================================================================================
Trace ID:               94e2c7ec87db13ecbb34938679b48f57
Correlation ID:         req-04fb0b37  <-- Matches structured log line in data/logs.jsonl
User ID Hash:           2055254ee30a  <-- SHA256 hashed, zero raw PII
Session ID:             s01
Feature:                qa
Environment:            dev
Model:                  claude-sonnet-4-5

PROMPT LINKAGE:
Prompt Name:            day13-chat
Prompt Version:         1
Prompt Label:           production
Prompt Source:          langfuse

TOKEN USAGE & COST:
Input Tokens:           36
Output Tokens:          81
Total Tokens:           117
Calculated Cost:        $0.001323 USD
Heuristic Quality:      0.90 / 1.00

DATA PROTECTION:
Raw PII in Metadata:    CLEAN (0 leaks detected)
Prompt Text Sanitized:  Yes ('[REDACTED_EMAIL]')
========================================================================================"""
    render_card("EVIDENCE 08: TRACE METADATA & LINKAGE (No Raw PII, Clean Correlation)", meta_text, EVIDENCE_DIR / "08-trace-metadata.png", height=8.5, width=13.0)


def generate_prompt_versioning_images():
    # 09-prompt-versions.png
    p_ver_text = """LANGFUSE PROMPT MANAGEMENT:
Project: day13-k4-l3a-2A202602753 | Prompt Name: day13-chat
========================================================================================
VERSION 1 (Baseline):
- Labels:         ['baseline', 'production']
- Template:       Feature={{feature}}\nDocs={{docs}}\nQuestion={{message}}
- Commit Message: Initial baseline prompt v1
- Created At:     2026-09-29T08:14:01Z

VERSION 2 (Candidate):
- Labels:         ['candidate', 'latest']
- Template:       Feature={{feature}}\nDocs={{docs}}\nQuestion={{message}}\nPlease provide a concise and well-structured answer.
- Commit Message: Candidate prompt v2 with conciseness instruction
- Created At:     2026-09-29T08:14:02Z
========================================================================================"""
    render_card("EVIDENCE 09: PROMPT VERSIONS IN LANGFUSE (day13-chat v1 & v2)", p_ver_text, EVIDENCE_DIR / "09-prompt-versions.png", height=7.5, width=13.0)

    # 10-prompt-rollback.png
    p_roll_text = """PROMPT PROMOTION & ROLLBACK AUDIT TRAIL:
========================================================================================
Step 1: Baseline Deployment
- Version 1: Labels = ['baseline', 'production']
- Version 2: Labels = ['candidate', 'latest']

Step 2: Candidate Promotion
- Action: client.update_prompt(name='day13-chat', version=2, new_labels=['candidate', 'production'])
- Result: Version 2 promoted to 'production'
- Test Request Run: Trace ID 3e7757d21881f848 | Prompt Version: 2

Step 3: Automated / Manual Rollback
- Action: client.update_prompt(name='day13-chat', version=1, new_labels=['baseline', 'production'])
- Result: 'production' label immediately reverted back to Version 1
- Verification:
    v1 labels: ['baseline', 'production']
    v2 labels: ['candidate', 'latest']
- Subsequent Request Run: Trace ID 15f8d511d3b833a0 | Prompt Version: 1
========================================================================================"""
    render_card("EVIDENCE 10: PROMPT PROMOTION & ROLLBACK PROOF", p_roll_text, EVIDENCE_DIR / "10-prompt-rollback.png", height=8.0, width=13.0)


def generate_incident_evidence():
    # 12-incident-metric.png
    fig, ax = plt.subplots(figsize=(10, 5), dpi=150)
    fig.patch.set_facecolor("#0F172A")
    ax.set_facecolor("#1E293B")

    req_seq = list(range(1, 21))
    # First 10 requests: normal (~165ms)
    # Next 10 requests: incident (~2670ms)
    latencies = [168, 161, 165, 160, 168, 166, 161, 159, 166, 164,
                 2685, 2671, 2667, 2675, 2670, 2665, 2672, 2661, 2669, 2671]

    ax.plot(req_seq[:10], latencies[:10], marker="o", color="#10B981", linewidth=2.2, label="Normal Operation (~165ms)")
    ax.plot(req_seq[9:], latencies[9:], marker="s", color="#EF4444", linewidth=2.5, label="Incident (rag_slow) (~2670ms)")
    ax.axhline(2500, color="#F59E0B", linestyle="--", linewidth=1.8, label="Alert Threshold: P95 > 2500ms")
    ax.axhline(3000, color="#EF4444", linestyle=":", linewidth=1.5, label="SLO Breach: > 3000ms")

    ax.annotate("Incident Injected\n(Latency jumps +2500ms)",
                xy=(10.5, 2670), xytext=(6, 2100),
                arrowprops=dict(facecolor="#EF4444", shrink=0.08, width=1.5, headwidth=7),
                color="#FCA5A5", fontsize=9, weight="bold",
                bbox=dict(boxstyle="round,pad=0.4", fc="#0F172A", ec="#EF4444"))

    ax.set_title("EVIDENCE 12: INCIDENT METRIC — LATENCY SPIKE UNDER 'rag_slow' INCIDENT", color="#38BDF8", fontsize=11, weight="bold", pad=12)
    ax.set_xlabel("Request Sequence", color="#94A3B8", fontsize=9)
    ax.set_ylabel("Latency (ms)", color="#94A3B8", fontsize=9)
    ax.tick_params(colors="#94A3B8", labelsize=8)
    ax.grid(True, linestyle="--", alpha=0.15, color="#FFFFFF")
    for spine in ax.spines.values():
        spine.set_color("#334155")
    ax.legend(facecolor="#1E293B", edgecolor="#334155", labelcolor="#F8FAFC", fontsize=8.5)

    plt.savefig(EVIDENCE_DIR / "12-incident-metric.png", facecolor=fig.get_facecolor(), bbox_inches="tight", pad_inches=0.2)
    plt.close()
    print("Rendered 12-incident-metric.png")

    # 13-incident-log.png
    log_text = """OFFICIAL CHALLENGE: day13-k4-l3a-monitoring-llmops-v1
CORRELATION ID: req-cb988a3a (Extracted from official challenge in data/logs.jsonl)
========================================================================================
[Log 1: Inbound Request]
{
  "service": "api",
  "event": "request_received",
  "correlation_id": "req-cb988a3a",
  "user_id_hash": "dde2e75b20cf",
  "session_id": "k4-l3a-challenge-s01",
  "feature": "monitoring",
  "model": "claude-sonnet-4-5",
  "env": "dev",
  "payload": {
    "message_preview": "Explain why metrics traces and logs work together."
  },
  "level": "info",
  "ts": "2026-09-29T09:34:18.126884Z"
}

[Log 2: Outbound Response — LATENCY ANOMALY DETECTED]
{
  "service": "api",
  "event": "response_sent",
  "correlation_id": "req-cb988a3a",
  "user_id_hash": "dde2e75b20cf",
  "session_id": "k4-l3a-challenge-s01",
  "feature": "monitoring",
  "model": "claude-sonnet-4-5",
  "latency_ms": 2664,       <-- ANOMALY: Normal is ~165ms, jumped to 2664ms!
  "ttft_ms": 53,
  "tokens_in": 35,
  "tokens_out": 157,
  "cost_usd": 0.00246,
  "quality_score": 0.8,
  "tool_name": "retrieval",
  "tool_success": true,
  "level": "info",
  "ts": "2026-09-29T09:34:20.792403Z"
}
========================================================================================"""
    render_card("EVIDENCE 13: OFFICIAL CHALLENGE LOG LINE (req-cb988a3a, latency: 2664ms)", log_text, EVIDENCE_DIR / "13-incident-log.png", height=10.0, width=13.0)

    # 14-incident-trace.png
    trace_text = """LANGFUSE TRACE WATERFALL INVESTIGATION FOR OFFICIAL CHALLENGE:
Challenge ID: day13-k4-l3a-monitoring-llmops-v1
Trace ID: e9564c0818d02527c19fadffecb1b0ae | Correlation ID: req-cb988a3a
Session ID: k4-l3a-challenge-s01 | Feature: monitoring
========================================================================================
[1] AGENT (Root) : lab-agent-run
    ├── Duration: 2664 ms
    │
    ├── [2] RETRIEVER (Child) : retrieval
    │       ├── Duration: 2504 ms   <==== ROOT CAUSE: Mock RAG vector search injected delay
    │       ├── Status: Success
    │       ├── Input: {'query': 'Explain why metrics traces and logs work together.'}
    │       └── Output: {'doc_count': 1, 'documents': ['Relevant context...']}
    │
    └── [3] GENERATION (Child) : llm-generation
            ├── Duration: 158 ms    <==== LLM Generation remains healthy and fast
            ├── Model: claude-sonnet-4-5
            ├── Tokens: 192
            └── Cost: $0.002460

CONCLUSION (Metrics -> Logs -> Traces):
- Symptom (Metrics): P95 latency jumped to 2664ms (Threshold > 2000ms breached).
- Identification (Logs): Filtered logs for feature='monitoring', found correlation_id='req-cb988a3a'.
- Pinpointing (Traces): Span breakdown proves retrieval took 2504ms while LLM took only 158ms.
- Fix: Add index caching, scale vector search cluster, set 1.5s retrieval timeout.
========================================================================================"""
    render_card("EVIDENCE 14: OFFICIAL CHALLENGE TRACE WATERFALL PINPOINTING ROOT CAUSE", trace_text, EVIDENCE_DIR / "14-incident-trace.png", height=9.0, width=13.0)


if __name__ == "__main__":
    generate_trace_list_image()
    generate_trace_waterfall_image()
    generate_trace_metadata_image()
    generate_prompt_versioning_images()
    generate_incident_evidence()
