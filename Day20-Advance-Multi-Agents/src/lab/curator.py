"""GUIDE Phần 3 - Người tuyển chọn skill (skill curator): tự viết skill từ các lần chạy thất bại.   >>> SINH VIÊN CÀI ĐẶT curate_skills <<<

Pseudo-code: guides/pseudocode/04_curator.md
Kiểm tra:    pytest tests/test_04_curator.py
Chạy thật:   python -m lab.curator
"""
import json
import re
from pathlib import Path

from .model import make_model
from .tasks import ROOT, eval_markers   # có sẵn: định danh của tác vụ đánh giá, tính lúc chạy

# ---- CÓ SẴN, KHÔNG SỬA: kiểm tra và tách khối skill (phần dễ sai và liên quan bảo mật) ----------------
SAFE_NAME = re.compile(r"^[a-z0-9]+(-[a-z0-9]+)*$")


def validate_skill(text: str, expected_name: str | None = None) -> list[str]:
    """Kiểm tra nội dung một SKILL.md. Trả về danh sách vấn đề (rỗng = hợp lệ).

    Quy tắc: có khối YAML frontmatter; `name` chữ thường/số/gạch ngang (tối đa 64 ký tự) và bằng `expected_name`
    nếu được truyền; có `description` (tối đa 1024 ký tự); phần thân tối đa 80 dòng; không chứa chuỗi nào của
    `eval_markers()`. Quy tắc về `name` cũng là biện pháp bảo mật: tên khối do LLM sinh ra được dùng để tạo
    đường dẫn, nên `../evil` không được lọt qua.
    """
    problems = []
    m = re.match(r"^---\n(.*?)\n---\n(.*)$", text.strip() + "\n", re.S)
    if not m:
        return ["missing YAML frontmatter"]
    front, body = m.groups()
    name = re.search(r"^name:\s*(.+)$", front, re.M)
    desc = re.search(r"^description:\s*(.+)$", front, re.M)
    n = name.group(1).strip() if name else ""
    if not SAFE_NAME.fullmatch(n) or len(n) > 64:
        problems.append("invalid name")
    elif expected_name is not None and n != expected_name:
        problems.append("name differs from the block name")
    if not desc or len(desc.group(1).strip()) > 1024:
        problems.append("missing or too long description")
    if len(body.strip().splitlines()) > 80:
        problems.append("body longer than 80 lines")
    low = text.lower()
    for marker in eval_markers():
        if marker in low:
            problems.append(f"mentions evaluation material: {marker}")
    return problems


def parse_skill_blocks(reply: str) -> list[tuple[str, str]]:
    """Tách câu trả lời của LLM thành danh sách (name, nội dung SKILL.md).

    Khuôn dạng: `=== SKILL: <name> ===` ... `=== END ===`. Một khối kết thúc ở điểm nào đến trước trong ba điểm:
    `=== END ===`, tiêu đề `=== SKILL:` kế tiếp, hoặc cuối văn bản (LLM đôi khi quên dòng END).
    """
    pattern = re.compile(r"^=== SKILL: (\S+) ===[ \t]*\n(.*?)(?=^=== END ===|^=== SKILL: |\Z)", re.S | re.M)
    return [(name, text.strip()) for name, text in pattern.findall(str(reply))]
# --------------------------------------------------------------------------------------------------


def curate_skills(results_dir="results", source_condition="baseline", out_dir=None, model=None, max_skills: int = 3) -> list[Path]:
    """Đọc các lần chạy của TÁC VỤ HỌC (role == "learn") trong `source_condition`, nhờ LLM viết skill, ghi file.

    Các bước: nạp run.json + trace.md -> (nếu không có check nào thất bại: in cảnh báo và trả về [] mà KHÔNG gọi LLM)
    -> dựng prompt -> model.invoke(prompt) -> parse_skill_blocks -> validate_skill(text, expected_name=name)
    -> ghi `<out_dir>/<name>/SKILL.md`. Mặc định `out_dir` = <gốc lab>/skills/auto (dùng `ROOT` từ lab.tasks).
    Giữ tối đa `max_skills` skill hợp lệ; skill không hợp lệ bị bỏ qua.
    Prompt chứa, với mỗi check thất bại, TÊN và trường `detail` (lời nhận xét của bot đánh giá: phát biểu quy tắc bị vi phạm)
    cùng phần cuối của vết (trace). Với tác vụ học, `detail` chỉ phát biểu quy tắc, không chứa đáp án.
    Tuyệt đối KHÔNG đưa dữ liệu của tác vụ đánh giá (role == "eval") vào prompt.
    model mặc định: make_model() (lab.model).
    Trả về: danh sách đường dẫn SKILL.md đã ghi.
    """
    if out_dir is None:
        out_dir = ROOT / "skills" / "auto"
    out_dir = Path(out_dir)

    results_path = Path(results_dir) / source_condition
    runs = []

    if results_path.exists():
        for run_file in sorted(results_path.glob("*/run.json")):
            try:
                data = json.loads(run_file.read_text(encoding="utf-8"))
            except Exception:
                continue

            if data.get("role") != "learn":
                continue

            trace_file = run_file.parent / "trace.md"
            trace_text = ""
            if trace_file.exists():
                trace_text = trace_file.read_text(encoding="utf-8")[-6000:]

            checks = data.get("checks", [])
            failed = [
                {"name": c.get("name", ""), "detail": c.get("detail", "")}
                for c in checks if not c.get("passed", False)
            ]
            if failed:
                runs.append({
                    "task": data.get("task", run_file.parent.name),
                    "failed": failed,
                    "trace": trace_text,
                })

    if not runs:
        print("Warning: Không có check nào thất bại ở tác vụ học (no failed checks in learning tasks).")
        return []

    run_summaries = []
    for r in runs:
        failures = "\n".join(f"  - Check: {f['name']} | Feedback: {f['detail']}" for f in r["failed"])
        run_summaries.append(
            f"### Task: {r['task']}\n"
            f"Failed checks:\n{failures}\n\n"
            f"Execution trace snippet:\n{r['trace']}\n"
        )
    runs_context = "\n".join(run_summaries)

    prompt = (
        f"You are an expert AI curator tasked with writing procedural SKILL documents for a coding and data agent.\n"
        f"Below are the failed checks (check names and evaluation bot feedback) and execution traces from previous learning runs.\n"
        f"Identify common procedural pitfalls and rules that were violated, and synthesize up to {max_skills} concise, general SKILLs "
        f"that will prevent these errors on NEW tasks of similar types.\n\n"
        f"Rules for each skill:\n"
        f"1. Be general and procedural: do NOT hardcode specific task IDs, specific file paths, numbers, or specific test values.\n"
        f"2. Each skill must have YAML frontmatter with:\n"
        f"   - name: lowercase letters, digits, hyphens (e.g. verify-data-formatting)\n"
        f"   - description: a single concise sentence describing WHEN to activate/read this skill\n"
        f"3. The body should be a clear, actionable checklist or step-by-step guideline (under 40 lines).\n"
        f"4. Format EACH skill exactly as follows:\n"
        f"=== SKILL: <name> ===\n"
        f"---\n"
        f"name: <name>\n"
        f"description: <description>\n"
        f"---\n"
        f"<body instructions>\n"
        f"=== END ===\n\n"
        f"Learning runs data:\n"
        f"{runs_context}\n"
    )

    actual_model = model or make_model()
    response = actual_model.invoke(prompt)
    reply = response.content if hasattr(response, "content") else str(response)
    if isinstance(reply, list):
        reply = "\n".join(b.get("text", "") for b in reply if isinstance(b, dict) and "text" in b) or str(reply)

    blocks = parse_skill_blocks(reply)
    written = []

    for name, text in blocks:
        if len(written) >= max_skills:
            break
        problems = validate_skill(text, expected_name=name)
        if problems:
            continue
        skill_dir = out_dir / name
        skill_dir.mkdir(parents=True, exist_ok=True)
        skill_file = skill_dir / "SKILL.md"
        skill_file.write_text(text + "\n", encoding="utf-8")
        written.append(skill_file)

    return written


if __name__ == "__main__":
    for p in curate_skills():
        print("wrote", p)
