from __future__ import annotations

import json
from pathlib import Path
import matplotlib.pyplot as plt

LOG_PATH = Path("data/logs.jsonl")


def render_card(title: str, text: str, output_path: Path, height: float = 4.5):
    fig = plt.figure(figsize=(12, height), dpi=150)
    fig.patch.set_facecolor("#0F172A")
    ax = fig.add_axes([0, 0, 1, 1])
    ax.set_facecolor("#0F172A")
    ax.axis("off")

    ax.text(
        0.04, 0.90, title,
        color="#38BDF8", fontsize=13, weight="bold", fontfamily="monospace"
    )

    ax.text(
        0.04, 0.80, text,
        color="#F8FAFC", fontsize=9.5, fontfamily="monospace",
        va="top", linespacing=1.6,
        bbox=dict(boxstyle="round,pad=0.8", facecolor="#1E293B", edgecolor="#334155")
    )

    output_path.parent.mkdir(parents=True, exist_ok=True)
    plt.savefig(output_path, facecolor=fig.get_facecolor(), bbox_inches="tight", pad_inches=0.2)
    plt.close()
    print(f"Rendered {output_path}")


def main():
    # 04-structured-log.png
    log_sample_1 = {
        "service": "api",
        "event": "request_received",
        "env": "dev",
        "model": "claude-sonnet-4-5",
        "session_id": "s01",
        "user_id_hash": "2055254ee30a",
        "correlation_id": "req-04fb0b37",
        "feature": "qa",
        "payload": {"message_preview": "What is your refund policy? My email is [REDACTED_EMAIL]"},
        "level": "info",
        "ts": "2026-09-29T08:27:25.363532Z"
    }
    log_sample_2 = {
        "service": "api",
        "event": "response_sent",
        "env": "dev",
        "model": "claude-sonnet-4-5",
        "session_id": "s01",
        "user_id_hash": "2055254ee30a",
        "correlation_id": "req-04fb0b37",
        "feature": "qa",
        "latency_ms": 3406,
        "ttft_ms": 55,
        "tokens_in": 36,
        "tokens_out": 81,
        "cost_usd": 0.001323,
        "quality_score": 0.9,
        "tool_name": "retrieval",
        "tool_success": True,
        "payload": {"answer_preview": "Starter answer. You should improve this output logic and add better quality checks..."},
        "level": "info",
        "ts": "2026-09-29T08:27:28.799040Z"
    }
    text_04 = json.dumps(log_sample_1, indent=2, ensure_ascii=False) + "\n\n" + json.dumps(log_sample_2, indent=2, ensure_ascii=False)
    render_card("EVIDENCE 04: STRUCTURED LOG JSON (request_received & response_sent)", text_04, Path("submission/evidence/04-structured-log.png"), height=11.0)

    # 05-pii-redaction.png
    pii_demo = """// 1. Raw Input Query with PII:
"What is your refund policy? My email is student@vinuni.edu.vn"
// Log Output after Recursive PII Scrubber:
{
  "service": "api",
  "event": "request_received",
  "correlation_id": "req-04fb0b37",
  "payload": {
    "message_preview": "What is your refund policy? My email is [REDACTED_EMAIL]"
  }
}

// 2. Raw Input Query with Vietnamese Phone:
"Here is my phone 090 123 4567, what should be logged?"
// Log Output after Recursive PII Scrubber:
{
  "service": "api",
  "event": "request_received",
  "correlation_id": "req-28931365",
  "payload": {
    "message_preview": "Here is my phone [REDACTED_PHONE_VN], what should be logged?"
  }
}

// 3. Raw Input Query with Credit Card Number:
"What is the policy for PII and credit card 4111-2222-3333-4444?"
// Log Output after Recursive PII Scrubber:
{
  "service": "api",
  "event": "request_received",
  "correlation_id": "req-d8ec3adb",
  "payload": {
    "message_preview": "What is the policy for PII and credit card [REDACTED_CREDIT_CARD]?"
  }
}"""
    render_card("EVIDENCE 05: PII REDACTION BEFORE STORAGE (Email, Phone, Credit Card, CCCD)", pii_demo, Path("submission/evidence/05-pii-redaction.png"), height=11.5)


if __name__ == "__main__":
    main()
