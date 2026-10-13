# Nhóm thực hiện K4 Track 3B

Tên nhóm: GOHOME

Repo chung: https://github.com/DucPh4t/K4-L3-DAY24-GOHOME-Eval-Guard

Trưởng nhóm/người nộp: Nguyễn Đức Phát - 2A202602753

Ngày lab/deadline áp dụng: 2026-10-12 23:59:00 — Asia/Ho_Chi_Minh (UTC+07:00)

Commit dùng để chấm: HEAD

Mỗi nhóm nộp một repo. Điền đủ thành viên và một mục INDIVIDUAL cho từng người.
Thêm/xóa rows để khớp nhóm thật; mẫu ba rows không ép nhóm phải có ba người.

## Thành viên và phân công

| STT | Họ và tên | MSSV | Vai trò / công việc thật | Bằng chứng |
|---|---|---|---|---|
| 1 | Nguyễn Đức Phát | 2A202602753 | Trưởng nhóm, Tích hợp Pipeline RAG Day 18, Chạy batch thực nghiệm & Báo cáo Blueprint (Task 13) | `scripts/setup_answers.py`, `doc/reports/blueprint.md`, Commit & nộp repo |
| 2 | Nguyễn Thành Duy | 2A202602804 | Phase A: RAGAS Evaluation (Tasks 1-4) & Phân cụm lỗi | `src/phase_a_ragas.py`, `artifacts/ragas_50q.json`, `doc/reports/failure_clusters.md` |
| 3 | Nguyễn Xuân Khuê | 2A202602999 | Phase B: LLM-as-a-Judge, Swap-and-Average & Đo Bias (Tasks 5-8) | `src/phase_b_judge.py`, `artifacts/judge_results.json`, `doc/reports/bias_report.md` |
| 4 | Lê Minh Sang | 2A202602864 | Phase C: Guardrails Stack (Presidio PII + NeMo Rails) & Latency Benchmark (Tasks 9-12) | `src/phase_c_guard.py`, `artifacts/guard_results.json` |

Người tích hợp/chạy batch/nộp link: Nguyễn Đức Phát - 2A202602753 (Chạy pipeline, sinh artifacts và nộp repo).

## Môi trường và chuẩn bị trước lớp

OS/Python/compiler: macOS Darwin arm64, Python 3.11.17, Apple Clang / Homebrew C++ toolchain.
Virtualenv/dependencies/imports: Đã tạo .venv Python 3.11, pip install -r requirements/requirements.txt, tất cả imports (ragas, nemoguardrails, presidio_analyzer, spacy) thành công.
Models/Qdrant/50 answers đã chuẩn bị: Qdrant v1.9.7 docker container chạy tại localhost:6333, sinh 50 câu hỏi từ hybrid retrieval + reranker sang artifacts/answers_50q.json.
Nếu cài full NeMo chưa thành công, ghi lỗi thực tế; không dùng unit test pass hoặc pip resolve để khẳng định runtime đã chạy.

## INDIVIDUAL

### NguyenDucPhat-2A202602753

- Phần được giao và phần thực tế đã làm: Trưởng nhóm, tích hợp 5 module RAG Day 18 vào src/, cấu hình môi trường Qdrant và sinh 50 answers, xây dựng báo cáo kiến trúc Blueprint (Task 13), kiểm tra chất lượng checker tổng thể.
- Bằng chứng: Module RAG trong src/, artifacts/answers_50q.json, doc/reports/blueprint.md, lịch sử git commits.
- Cách kiểm tra: python scripts/setup_answers.py --live và python scripts/check_lab.py --with-tests PASS 100%.
- Điều đã học: Cách kết nối pipeline RAG production với hệ thống eval tự động và cơ chế CI/CD guardrail gates.
- Giới hạn/cách xử lý: Đảm bảo metadata format version 2 lưu đầy đủ model IDs tách biệt theo từng vai trò generation/evaluator/judge/guard.
- Nguồn/AI hỗ trợ nếu có: AI pair programming hỗ trợ refactor code và kiểm tra schemas.

### NguyenThanhDuy-2A202602804

- Phần được giao và phần thực tế đã làm: Phụ trách Phase A (Tasks 1-4), hiện thực group_by_distribution, run_ragas_50q với m4 evaluator models, bottom_10 theo cây chẩn đoán và cluster_analysis theo ma trận worst_metric x distribution.
- Bằng chứng: src/phase_a_ragas.py, artifacts/ragas_50q.json, doc/reports/failure_clusters.md.
- Cách kiểm tra: pytest tests/test_phase_a.py và python scripts/run_experiments.py --phase a --live.
- Điều đã học: Hiểu sâu 4 metric cốt lõi của RAGAS và cách phân cụm failure modes thay vì chỉ nhìn điểm trung bình tổng quát.
- Giới hạn/cách xử lý: Xử lý các câu hỏi adversarial bị bẫy version chính sách cũ/mới và phân tích context recall.
- Nguồn/AI hỗ trợ nếu có: AI pair programming hỗ trợ kiểm tra tính toán ma trận phân cụm lỗi.

### NguyenXuanKhue-2A202602999

- Phần được giao và phần thực tế đã làm: Phụ trách Phase B (Tasks 5-8), hiện thực pairwise_judge, swap_and_average để khử position bias, tính Cohen's Kappa so với human labels và trích xuất bias_report (position bias & verbosity bias).
- Bằng chứng: src/phase_b_judge.py, artifacts/judge_results.json, doc/reports/bias_report.md.
- Cách kiểm tra: pytest tests/test_phase_b.py và python scripts/run_experiments.py --phase b --live.
- Điều đã học: Kỹ thuật LLM-as-a-Judge, tác động của Position Bias trong pairwise so sánh và tầm quan trọng của hệ số Cohen's Kappa trong calibration.
- Giới hạn/cách xử lý: Tuyệt đối không đưa human_label hoặc human_note vào prompt để tránh data leakage.
- Nguồn/AI hỗ trợ nếu có: AI pair programming hỗ trợ xây dựng prompt JSON judge chuẩn.

### LeMinhSang-2A202602864

- Phần được giao và phần thực tế đã làm: Phụ trách Phase C (Tasks 9-12), hiện thực Presidio PII scan (CCCD/CMND, VN phone, email), NeMo guardrails input/output rails, chạy adversarial test suite và đo P95 latency tuần tự input layers.
- Bằng chứng: src/phase_c_guard.py, artifacts/guard_results.json, bảng số liệu benchmark latency.
- Cách kiểm tra: pytest tests/test_phase_c.py và python scripts/run_experiments.py --phase c --live --latency-samples 20.
- Điều đã học: Kiến trúc guardrails 2 tầng (layer 1 regex/pattern nhanh, layer 2 LLM/Colang sâu) và cách đo P95 latency chuẩn xác loại bỏ warm-up.
- Giới hạn/cách xử lý: Cân bằng giữa tỷ lệ chặn tấn công (>=15/20) và không chặn nhầm câu hỏi hợp lệ (clean controls 8/8 allowed).
- Nguồn/AI hỗ trợ nếu có: AI pair programming hỗ trợ cấu hình Presidio PatternRecognizer và Colang 1.0.

## Cập nhật sau khi nộp

Bản nộp đầu tiên đúng hạn trước 23:59 ngày làm lab, không có cập nhật sau deadline.
