# Báo cáo cá nhân — K4-L3A Day 13 Monitoring & LLMOps

> Mỗi học viên hoàn thiện một file duy nhất này. Khi dẫn evidence, dùng đường dẫn tương đối, ví dụ `evidence/07-trace-waterfall.png`.

## 1. Thông tin học viên

- **Họ và tên:** Nguyễn Đức Phát
- **MSSV:** 2A202602753
- **Lớp:** K4-L3A
- **Repository URL:** https://github.com/DucPh4t/K4-L3-DAY13-NguyenDucPhat-2A202602753-Monitoring-LLMOps
- **Commit SHA cuối:** `4441f6bd020e092f93f521169659754d181bbaf3`
- **Challenge ID:** day13-k4-l3a-monitoring-llmops-v1
- **Tên project Langfuse cá nhân:** `day13-k4-l3a-2A202602753`

## 2. Evidence index

Điền đúng đường dẫn tới evidence thực tế. Có thể đổi tên hoặc dùng nhiều ảnh nếu cần.

| Evidence | Đường dẫn |
|---|---|
| Pytest cuối | `evidence/01-pytest.txt` |
| Log validator | `evidence/02-log-validator.txt` |
| Dashboard validator | `evidence/03-dashboard-validator.txt` |
| Structured log | `evidence/04-structured-log.png` |
| PII redaction | `evidence/05-pii-redaction.png` |
| Trace list | `evidence/06-trace-list.png` |
| Trace waterfall | `evidence/07-trace-waterfall.png` |
| Trace metadata | `evidence/08-trace-metadata.png` |
| Prompt versions | `evidence/09-prompt-versions.png` |
| Prompt rollback | `evidence/10-prompt-rollback.png` |
| Dashboard runtime | `evidence/11-dashboard-overview.png` |
| Incident metric | `evidence/12-incident-metric.png` |
| Incident log | `evidence/13-incident-log.png` |
| Incident trace | `evidence/14-incident-trace.png` |

## 3. Kết quả kỹ thuật

| Nội dung | Baseline | Kết quả cuối | Nhận xét |
|---|---|---|---|
| `validate_logs.py` | 30/100 | 100/100 | Đạt toàn bộ 4 tiêu chuẩn: JSON schema, Correlation ID, Context enrichment, PII scrubbing |
| `validate_dashboard.py` | 6/6 panel | 6/6 panel | Hợp lệ toàn bộ 6 panel theo YAML contract |
| `pytest` | 22/22 passed | 22/22 passed | 100% test suites hoàn thành thành công |
| Số traces hợp lệ | 0 | 32 traces | Traces được gửi thành công lên Langfuse Cloud cá nhân |
| Số PII leak | 0 | 0 | Bộ lọc đệ quy loại bỏ sạch PII trước khi serialize |
| Latency P95 / TTFT P95 | ~1112ms / ~55ms | 168ms / 55ms | Độ trễ vận hành bình thường tối ưu |
| Retrieval success rate | 100% | 100% | Toàn bộ truy vấn ngữ cảnh thành công |

## 4. Logging và PII

- **Cách tạo/nhận và truyền correlation ID:** Trong `CorrelationIdMiddleware`, trước mỗi request thực hiện `clear_contextvars()` để tránh rò rỉ context giữa các luồng. Trích xuất header `x-request-id` nếu có sẵn, hoặc tự sinh mã theo format chuẩn `req-<8-hex>` thông qua `f"req-{uuid.uuid4().hex[:8]}"`. Bind ID này vào structlog contextvars, lưu vào `request.state.correlation_id` và gán ngược lại vào response headers gồm `x-request-id` và `x-response-time-ms`.
- **Các metadata được ghi vào structured log:** Các trường bắt buộc gồm `ts` (ISO-8601 UTC), `level`, `service`, `event`, `correlation_id`. Trong endpoint `/chat`, log được enrich thêm `user_id_hash` (mã băm SHA256 12 ký tự), `session_id`, `feature`, `model`, `env`, cùng các thông số đo lường hiệu năng: `latency_ms`, `ttft_ms`, `tokens_in`, `tokens_out`, `cost_usd`, `quality_score`, `tool_name`, `tool_success` và `payload` đã làm sạch.
- **Cách bảo đảm PII được scrub trước khi ghi:** Xây dựng hàm `_scrub_value` và processor `scrub_event` trong `app/logging_config.py` xử lý đệ quy toàn bộ các trường trong event dictionary. Tất cả các chuỗi đều được quét qua regex nhận diện Email, SĐT Việt Nam (+84 hoặc 0x), CCCD (12 số) và thẻ tín dụng (16 số), sau đó thay thế bằng nhãn `[REDACTED_<TYPE>]` TRƯỚC KHI `JsonlFileProcessor` và `JSONRenderer` serialize ghi ra file `data/logs.jsonl`.
- **Cách kiểm chứng kết quả:** Chạy `python scripts/validate_logs.py`, script sử dụng bộ regex độc lập quét toàn bộ file log; kết quả đạt 100/100 điểm với 0 rò rỉ PII.

## 5. Tracing và prompt versioning

- **Cách xác nhận traces do chính tôi tạo trong project cá nhân:** Project mang tên chính thức `day13-k4-l3a-2A202602753` trên Langfuse Cloud (region US), sử dụng API Key cá nhân và hiển thị 32 traces ứng với các request thực tế.
- **Cấu trúc root/retrieval/generation observations:**
  - Root observation: `lab-agent-run` (type `AGENT`, capture input/output = False để bảo mật).
  - Child observation 1: `retrieval` (type `RETRIEVER`, ghi nhận câu hỏi rút gọn và số lượng tài liệu tìm thấy).
  - Child observation 2: `llm-generation` (type `GENERATION`, ghi nhận model `claude-sonnet-4-5`, prompt text, token usage, cost chi tiết).
- **Cách nối trace với log:** Sử dụng trường `correlation_id` được truyền vào trace metadata thông qua `propagate_attributes()`, trường này có giá trị trùng khớp 100% với `correlation_id` trong structured log.
- **Prompt name:** `day13-chat`
- **Version/label baseline:** Version 1 gắn label `baseline` và `production`.
- **Version/label candidate:** Version 2 gắn label `candidate` bổ sung chỉ dẫn trả lời súc tích.
- **Trace ID của mỗi version:**
  - Version 1: `94e2c7ec87db13ecbb34938679b48f57` (Prompt version 1)
  - Version 2: `3e7757d21881f848958b6fd4edde01b0` (Prompt version 2)
- **Cách promote và rollback `production`:** Sử dụng API `client.update_prompt(name='day13-chat', version=2, new_labels=['candidate', 'production'])` để đưa v2 lên production. Khi cần rollback, chỉ cần gọi `client.update_prompt(name='day13-chat', version=1, new_labels=['baseline', 'production'])` để đưa production quay về v1 ngay lập tức mà không cần chỉnh sửa mã nguồn hay restart server.

## 6. Dashboard, SLO và alerts

- **Dashboard và sáu panel:** Xây dựng đầy đủ 6 panel theo contract `config/dashboard.yaml`:
  1. *Latency & TTFT*: P50, P95, P99 và TTFT P95 (threshold: P95 <= 3000ms).
  2. *Traffic*: Tần suất request theo phút (threshold: >= 1 rpm).
  3. *Errors & Retrieval*: Tỷ lệ lỗi 5xx (threshold <= 2%) và tỷ lệ thành công của retrieval (threshold >= 90%).
  4. *Cost*: Chi phí tích lũy theo USD (threshold <= $2.50).
  5. *Tokens*: Phân bổ Input vs Output tokens (threshold <= 50,000 tokens).
  6. *Quality Proxy*: Điểm chất lượng trung bình theo heuristic (threshold >= 0.75).
- **SLO và lý do chọn:** Primary SLO `fast_successful_requests`: 99.5% request hoàn thành trong thời gian `<= 3000ms` trong chu kỳ 28 ngày. Lý do: Độ trễ 3 giây là giới hạn chịu đựng tâm lý của người dùng trong các tương tác đàm thoại trực tiếp.
- **Cách tính error budget:** Error budget = 100% - 99.5% = 0.5%. Với 10,000 request mỗi chu kỳ, hệ thống được phép có tối đa 50 request bị chậm hoặc lỗi trước khi chạm mức cạn kiệt ngân sách lỗi.
- **Ba alert và runbook tương ứng:**
  1. `high_api_latency_p95` (P95 > 2500ms trong 5m, warning): Thông báo Slack `#ai-alerts`. Runbook: Kiểm tra panel latency, trích xuất log chậm, xem trace Langfuse; nếu nghẽn do retrieval thì bật cache, nếu do generation thì giảm max output tokens.
  2. `high_request_error_rate` (Lỗi 5xx > 2% trong 3m, critical): Thông báo Slack `#ai-critical-alerts`. Runbook: Kiểm tra panel Errors, đọc stacktrace trong `payload.detail`, bật circuit breaker hoặc phản hồi tĩnh.
  3. `retrieval_failure_rate_high` (Retrieval success < 90% trong 5m, high): Thông báo Slack `#ai-alerts`. Runbook: Kiểm tra kết nối vector database, chuyển sang fallback corpus cục bộ nếu database mất kết nối.

## 7. Điều tra challenge

- **Challenge ID:** `day13-k4-l3a-monitoring-llmops-v1`
- **Khoảng thời gian điều tra:** 2026-09-29T09:34:00Z – 2026-09-29T09:34:30Z
- **Triệu chứng từ metrics:** Dashboard Panel 1 (Latency & TTFT) và Alert `high_api_latency_p95` ghi nhận Latency P95 tăng vọt từ ~165ms lên 2664ms, vượt ngưỡng 2000ms được chỉ định trong challenge contract.
- **Log line và correlation ID liên quan:** Lọc `data/logs.jsonl` theo `feature: "monitoring"` tìm thấy request chính thức có `correlation_id: "req-cb988a3a"`, `session_id: "k4-l3a-challenge-s01"`, `user_id_hash: "dde2e75b20cf"`, ghi nhận `latency_ms: 2664`, `tool_name: "retrieval"`, `tool_success: true`.
- **Trace ID và span gây ảnh hưởng:** Mở trace `e9564c0818d02527c19fadffecb1b0ae` trên Langfuse cá nhân (liên kết qua `correlation_id: "req-cb988a3a"`). Span waterfall chỉ ra rõ ràng: root `lab-agent-run` mất 2664ms, trong đó span con `retrieval` (type retriever) mất tới 2504ms, trong khi span con `llm-generation` chỉ mất 158ms.
- **Root cause:** Lỗi nghẽn cổ chai nằm ở khâu tìm kiếm tài liệu (vector store retrieval lag mô phỏng), chiếm 94% tổng thời gian request, không liên quan đến thời gian phản hồi của mô hình LLM.
- **Fix action:** Bổ sung cơ chế timeout 1.5s cho bước retrieval, nếu vượt quá thời gian sẽ tự động dùng cached documents; đồng thời kiểm tra lại chỉ mục và mở rộng tài nguyên vector database.
- **Preventive measure:** Thiết lập Redis in-memory cache cho các câu hỏi phổ biến, thêm circuit breaker và tăng cường giám sát thời gian phản hồi riêng cho các lệnh gọi cơ sở dữ liệu vector.

## 8. Giải thích và tự đánh giá

- **Một quyết định kỹ thuật quan trọng và lý do:** Quyết định thực hiện PII scrubbing ở cấp độ logging processor đệ quy (`scrub_event`) thay vì làm thủ công ở controller. Lý do: Đảm bảo nguyên tắc "Security by Default" — bất kỳ lập trình viên nào thêm trường mới vào log hay thay đổi cấu trúc dữ liệu cũng không thể vô tình làm lọt PII ra ngoài file log.
- **Một lỗi/blocker đã gặp:** Gặp lỗi khi môi trường build thư viện Rust `pydantic-core` trên Python 3.14 preview, cùng với lỗi xác thực 401 khi khởi tạo Langfuse do nhầm lẫn giữa định dạng key placeholder và region US Cloud.
- **Cách tìm nguyên nhân và xử lý:** Đọc kỹ log lỗi chi tiết của uvicorn và compiler, nhận diện được sự xung đột phiên bản; nhanh chóng chuyển sang Python 3.12 từ Homebrew và cấu hình đúng `https://us.cloud.langfuse.com` với cặp key đầy đủ, kiểm tra thành công bằng `client.auth_check()`.
- **Cách hiểu luồng Metrics → Logs → Traces:**
  - **Metrics** là đèn báo động tổng quan: Cho biết hệ thống *đang bị đau ở đâu* và *từ lúc nào* (triệu chứng và xu hướng).
  - **Logs** là hồ sơ bệnh án: Dẫn đường bằng mốc thời gian để tìm ra *bệnh nhân cụ thể nào bị ảnh hưởng* thông qua `correlation_id`.
  - **Traces** là phim chụp X-quang: Phóng to vào request đó để chỉ ra chính xác *tế bào/span nào bị hỏng hóc* (nguyên nhân cốt lõi).
- **Vai trò của prompt version, token/cost, SLO hoặc rollback trong vận hành LLM:** LLM là hệ thống có tính bất định cao; prompt thay đổi nhỏ có thể làm tăng gấp đôi lượng token và chi phí. Prompt versioning và rollback giúp cô lập rủi ro, chuyển đổi tức thì khi phát hiện hành vi bất thường mà không cần dừng dịch vụ; theo dõi token/cost giúp bảo vệ ngân sách; còn SLO đặt ra ranh giới đảm bảo chất lượng cam kết với khách hàng.
- **Điều quan trọng nhất đã học:** Hiểu sâu sắc sự khác biệt giữa Monitoring truyền thống (chỉ xem server CPU/RAM) và LLMOps Observability hiện đại (theo dõi chất lượng, ngữ cảnh, tokens, chi phí và chuỗi suy luận phân tán).
- **Hạn chế hoặc phần chưa hoàn thành, nếu có:** Các kịch bản prompt hiện đang sử dụng heuristic scoring đơn giản, trong tương lai có thể tích hợp LLM-as-a-judge trực tiếp trên Langfuse để đánh giá độ chính xác ngữ nghĩa sâu hơn.

## 9. Checklist trước khi nộp

- [x] Kết quả và evidence thuộc commit SHA cuối.
- [x] Tất cả ảnh/output mở được bằng đường dẫn tương đối.
- [x] Incident evidence nối đúng metric → log → trace.
- [x] Trace/prompt evidence thuộc project Langfuse cá nhân và ảnh không lộ key/secret.
- [x] Repository chạy lại được theo README.
- [x] Không có secret, API key, PII thô hoặc evidence của người khác/lớp khác.
- [x] URL repo và commit SHA cuối đã được nộp trên LMS/Codelabs.
