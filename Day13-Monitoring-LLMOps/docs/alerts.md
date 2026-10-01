# Template Alert và Runbook

Mỗi alert phải dựa trên triệu chứng người dùng hoặc SLO, không dựa trực tiếp vào tên implementation nội bộ.

## Alert 1

- Tên: high_api_latency_p95
- Severity: warning
- Duration: 5m
- Kênh thông báo: Slack (#ai-alerts)
- SLI/SLO liên quan: Primary SLO - fast_successful_requests (latency <= 3000ms, threshold cảnh báo P95 > 2500ms)
- Điều kiện và thời gian duy trì: Latency P95 > 2500ms duy trì liên tục trong 5 phút.
- Ảnh hưởng tới người dùng: Người dùng trải nghiệm phản hồi chậm trễ khi gửi tin nhắn hoặc yêu cầu hỏi đáp tới hệ thống.
- Ba bước kiểm tra đầu tiên:
  1. Kiểm tra panel Latency & TTFT trên Dashboard xem độ trễ tăng ở khâu retrieval hay generation.
  2. Lọc file `data/logs.jsonl` tìm các log `response_sent` có `latency_ms > 2500` và trích xuất `correlation_id`.
  3. Mở Langfuse tìm trace tương ứng theo `correlation_id`, kiểm tra span waterfall xem span nào bị nghẽn (ví dụ `retrieval` bị timeout/sleep hay LLM output tokens bị spike).
- Mitigation tạm thời:
  1. Nếu do retrieval bị nghẽn hoặc external database lag, bật chế độ fallback retrieval hoặc giảm top-k documents.
  2. Nếu do LLM generation chậm, kiểm tra prompt độ dài đầu ra, giảm max_tokens hoặc restart replica.
- Owner: oncall-ai-engineer

## Alert 2

- Tên: high_request_error_rate
- Severity: critical
- Duration: 3m
- Kênh thông báo: Slack (#ai-critical-alerts)
- SLI/SLO liên quan: Error Budget & Service Availability (guardrail error_rate_pct <= 2%)
- Điều kiện và thời gian duy trì: Tỷ lệ lỗi 5xx trên tổng số request > 2% duy trì trong 3 phút.
- Ảnh hưởng tới người dùng: Người dùng nhận mã lỗi HTTP 500 khi gọi endpoint `/chat`, yêu cầu bị gián đoạn.
- Ba bước kiểm tra đầu tiên:
  1. Mở panel Errors trên Dashboard để phân tích `error_type` (RuntimeError, Timeout, ConnectionError).
  2. Tìm log `request_failed` gần nhất trong `data/logs.jsonl` để đọc stacktrace và thông điệp lỗi trong `payload.detail`.
  3. Mở Langfuse trace để xác định dịch vụ phụ trợ nào (vector store, LLM gateway) đang từ chối kết nối.
- Mitigation tạm thời:
  1. Kiểm tra status của incident flags trên `/health`, tắt kịch bản lỗi giả định nếu đang chạy test.
  2. Kích hoạt circuit breaker hoặc fallback answer tĩnh cho người dùng thay vì trả về lỗi 500.
- Owner: oncall-ai-engineer

## Alert 3

- Tên: retrieval_failure_rate_high
- Severity: high
- Duration: 5m
- Kênh thông báo: Slack (#ai-alerts)
- SLI/SLO liên quan: Retrieval Guardrail (retrieval_success_rate_pct >= 90%)
- Điều kiện và thời gian duy trì: Tỷ lệ tìm kiếm tri thức thất bại (`tool_success == false`) vượt quá 10% trong 5 phút.
- Ảnh hưởng tới người dùng: AI trả lời dựa trên fallback knowledge hoặc ảo giác, chất lượng câu trả lời bị suy giảm nghiêm trọng (`quality_score < 0.75`).
- Ba bước kiểm tra đầu tiên:
  1. Kiểm tra panel Errors & Retrieval Success trên Dashboard để xác định thời điểm bắt đầu sụt giảm.
  2. Lọc log có `tool_name == "retrieval"` và `tool_success == false` để kiểm tra nguyên nhân (vector DB down, token limit, timeout).
  3. Kiểm tra kết nối mạng tới vector store/corpus retrieval service.
- Mitigation tạm thời:
  1. Chuyển hướng truy vấn sang fallback corpus cục bộ hoặc in-memory cache.
  2. Restart vector store proxy service nếu phát hiện rò rỉ connection pool.
- Owner: oncall-ai-engineer
