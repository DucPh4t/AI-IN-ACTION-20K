# Blueprint CI/CD cho RAG và guardrails

Nhóm: GOHOME

Người phụ trách: Nguyễn Đức Phát - 2A202602753

Đây là **đề xuất CI/CD**, không phải workflow đã được triển khai/chạy.
Nguồn kết quả: artifacts/ragas_50q.json, judge_results.json, guard_results.json.
Run timestamp: 2026-10-12T09:41:49.475260+00:00; guard models: gpt-4o-mini.
Models generation/evaluator/judge từ A/B: Generation: openai/gpt-4o-mini (answers_50q.json, ragas_50q.json, judge_results.json); Evaluator: BAAI/bge-m3, gpt-4o-mini (ragas_50q.json); Judge: gpt-4o-mini (judge_results.json); Guard: gpt-4o-mini (guard_results.json).

## Kiến trúc và failure action

Input → Presidio → NeMo input → RAG → NeMo output → response.
Request thực dừng sớm khi bị chặn; khác phép đo input layers chạy đủ hai tầng.

### Data Flow và Failure Action:
1. **Tầng 1 - Presidio PII Scanner (Input Guard)**:
   - Dữ liệu người dùng gửi vào sẽ đi qua Presidio trước tiên để quét số CCCD (12 số), CMND (9 số), số điện thoại di động Việt Nam (đầu số 03-09), và địa chỉ email.
   - Failure Action: Nếu phát hiện PII nhạy cảm, request bị chặn ngay lập tức (short-circuit), trả về thông báo từ chối an toàn theo quy định bảo mật dữ liệu, không chuyển tiếp request đến các tầng sau để tiết kiệm chi phí và bảo vệ quyền riêng tư.
2. **Tầng 2 - NeMo Guardrails Input Rail (Topic & Jailbreak Guard)**:
   - Nếu câu hỏi không chứa PII, NeMo Guardrails sẽ kiểm tra xem câu hỏi có thuộc phạm vi chính sách nội bộ (HR/IT policy) hay không, đồng thời chặn các nỗ lực tấn công prompt injection, jailbreak (DAN), hoặc mạo danh cấp quản lý/CEO.
   - Failure Action: Nếu vi phạm hoặc ngoài phạm vi, NeMo kích hoạt flow từ chối chuẩn mực từ `rails.co` và kết thúc luồng xử lý.
3. **Tầng 3 - Production RAG Core Pipeline**:
   - Truy vấn hợp lệ được đưa vào RAG core: Hybrid search (Dense BAAI/bge-m3 trên Qdrant + BM25 tiếng Việt có tách từ underthesea), sau đó qua CrossEncoder reranker (top 3 chunks liên quan nhất), kết hợp contextual metadata từ M5 enrichment để sinh câu trả lời bằng LLM (`gpt-4o-mini`).
4. **Tầng 4 - NeMo Guardrails Output Rail (Hallucination & Leakage Guard)**:
   - Câu trả lời sinh ra từ LLM được kiểm tra lại bởi NeMo output rail nhằm đảm bảo không rò rỉ dữ liệu lương cá nhân cụ thể, mật khẩu quản trị hoặc thông tin tuyệt mật bị hallucinate.
   - Failure Action: Nếu phát hiện nội dung độc hại hoặc rò rỉ, output rail sẽ thay thế bằng câu từ chối chuẩn hoặc che giấu thông tin nhạy cảm trước khi trả về người dùng.
5. **Quản lý Secrets và Fallback**:
   - Toàn bộ API keys (OpenAI, HuggingFace, Qdrant) được nạp qua biến môi trường (.env / GitHub Secrets), tuyệt đối không commit vào mã nguồn.
   - Khi API gọi ngoài gặp sự cố mạng hoặc lỗi hạn mức, pipeline kích hoạt extractive fallback trích xuất câu trả lời trực tiếp từ top chunks để duy trì tính liên tục của dịch vụ.

## Phạm vi và số đo latency

Bắt buộc Task 12: **input_layers_sequential**, Presidio + NeMo input, không
short-circuit. Engines tạo trước đo; có hai warm-up thật không tính vào mẫu.
Percentile nội suy tuyến tính từ raw samples; tổng từ tổng từng sample.

Số mẫu timed: 20; warm-up: 2;
phương pháp: linear.

| Layer / scope | P50 ms | P95 ms | P99 ms | Tình trạng |
|---|---|---|---|---|
| Presidio | 11.69 | 13.98 | 14.14 | Đã đo thực tế trong Task 12 |
| NeMo input | 1029.55 | 2158.95 | 2267.86 | Đã đo thực tế trong Task 12 |
| Input guard sequential | 1042.73 | 2166.66 | 2280.49 | Đã đo thực tế trong Task 12 |
| RAG | chưa đo | chưa đo | chưa đo | Ngoài phạm vi bắt buộc |
| NeMo output | chưa đo | chưa đo | chưa đo | Ngoài phạm vi bắt buộc |
| Full guard / short-circuit request | chưa đo | chưa đo | chưa đo | Không suy từ input_guard_ms |

Input-layer budget target: 500ms; kết quả thực tế/budget_ok: P95 = 2166.66ms / False.

### Phân tích Bottleneck và Kế hoạch đo lường:
- **Bottleneck**: Presidio chạy local bằng regex và quy tắc tiếng Việt cực kỳ nhanh chóng (P50 = 11.69ms, P95 = 13.98ms, chiếm dưới 1% tổng thời gian). Điểm nghẽn lớn nhất nằm ở NeMo input rail (P95 = 2158.95ms) do mỗi lần kiểm tra phải gọi mạng ra OpenAI API để chạy prompt `self_check_input`.
- **Giải pháp tối ưu**: Để đạt ngân sách dưới 500ms trong môi trường production, cần thay thế LLM API của NeMo bằng mô hình phân loại cục bộ chạy trên GPU (chẳng hạn như mô hình DeBERTa/RoBERTa phân loại intent/jailbreak với ONNX Runtime hoặc vLLM cục bộ), giảm thời gian phản hồi xuống dưới 50ms.
- **Các thành phần ngoài phạm vi**: Các thành phần RAG, NeMo output rail và full request chưa được đo trong Task 12 nên được giữ nguyên trạng thái "chưa đo" theo đúng quy chuẩn báo cáo khoa học.

## CI gates đề xuất

- RAGAS faithfulness ≥0.75, avg_score ≥0.65 trên 50 câu.
- Attacks ≥18/20 cho CI đề xuất; clean 8/8 allowed; output cases đúng.
- Full guard P95 <500ms chỉ áp dụng sau khi thực sự đo full guard.

Mốc bắt buộc lab vẫn attacks ≥15/20; bonus ≥18/20 kèm clean controls đạt.

### Đề xuất cấu hình CI Workflow (GitHub Actions):
- **Cấu hình pipeline kiểm tra tự động**:
  ```yaml
  name: Production Eval & Guardrail Quality Gate
  on: [push, pull_request]
  jobs:
    evaluation-gate:
      runs-on: ubuntu-latest
      steps:
        - uses: actions/checkout@v4
        - uses: actions/setup-python@v5
          with:
            python-version: '3.11'
        - name: Install dependencies
          run: pip install -r requirements.txt -c constraints-core.txt
        - name: Run Lab Validation & Quality Gate
          env:
            OPENAI_API_KEY: "$SECRET_OPENAI_KEY"
          run: python scripts/check_lab.py --with-tests
  ```
- **Cơ chế chặn thất bại**: Script `check_lab.py` trả về exit code khác 0 (`exit 1`) ngay khi phát hiện bất kỳ vi phạm nào về schema JSON, placeholder chưa điền, bài test pytest trượt, hoặc tỷ lệ phát hiện tấn công không đạt mốc quy định.

## Monitoring và cải tiến

### Chiến lược giám sát Production:
1. **Metrics & Cảnh báo**:
   - Giám sát tỷ lệ chặn (Block Rate) hàng giờ: nếu vượt quá 15% tổng lượng truy vấn thì phát cảnh báo khẩn cấp (có nguy cơ false positive cao).
   - Giám sát độ trễ P95: nếu vượt ngưỡng 1500ms thì cảnh báo nghẽn mạng API.
2. **Lấy mẫu & Human-in-the-Loop**:
   - Lấy mẫu ngẫu nhiên 2% các câu hỏi bị chặn và 2% câu hỏi được thông qua mỗi ngày để chuyên gia nhân sự và kỹ sư bảo mật đánh giá thủ công.
3. **Quản lý dữ liệu và quyền riêng tư**:
   - Toàn bộ log lưu vết được ẩn danh hóa (anonymized) trước khi ghi vào kho log tập trung (Elasticsearch / CloudWatch).

RAGAS mean/worst distribution: mean 0.6749, worst distribution adversarial (0.6343).
Cohen’s κ: 1.0.
Attacks passed: 19/20; clean false_positive_rate: 0.0 (0/8 câu sạch bị chặn nhầm).

### Các hành động cải tiến cụ thể:
1. **Cải thiện độ hồi quy ngữ cảnh cho Adversarial (context_recall 0.4740)**: Tích hợp kỹ thuật Query Rewriting để bóc tách các câu hỏi chứa tiền giả định sai trước khi đưa vào retriever, giúp nâng cao context recall của nhóm adversarial lên trên 0.65.
2. **Tối ưu hóa độ trễ Guardrail**: Chuyển đổi tầng NeMo input rail từ mô hình LLM đám mây sang mô hình phân loại jailbreak/off-topic cục bộ (như Llama-Guard hoặc mô hình ONNX classifier), đưa độ trễ P95 từ 2166ms xuống dưới 100ms.
3. **Nâng cấp độ phân giải Chunking**: Tăng kích thước chunk con (child size) từ 256 lên 384 tokens trong `m1_chunking.py` để bảo tồn trọn vẹn ngữ cảnh của các bảng biểu thâm niên và quy định phê duyệt phức tạp.
4. **Mở rộng tập kiểm thử tự động**: Xây dựng thêm bộ 50 câu kiểm thử adversarial chuyên sâu về xung đột phiên bản chính sách nội bộ (v2023 so với v2024) vào bộ CI test suite định kỳ.
