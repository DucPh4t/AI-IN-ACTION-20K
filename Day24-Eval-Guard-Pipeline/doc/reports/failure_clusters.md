# Phân tích lỗi Phase A

Nhóm: GOHOME

Người phụ trách: Nguyễn Thành Duy - 2A202602804

Nguồn: `artifacts/ragas_50q.json`; run timestamp: 2026-10-12T09:11:55.252186+00:00.
Generation mode/fallback và điều kiện chạy: Chạy live với 50 câu trả lời RAG sinh từ OpenAI gpt-4o-mini qua hybrid retrieval (Qdrant bge-m3 dense + BM25 tiếng Việt) kết hợp CrossEncoder reranker. Không dùng extractive fallback.
Models generation/evaluator: Generation: openai/gpt-4o-mini; Evaluator: BAAI/bge-m3, gpt-4o-mini.

## Điểm theo distribution

| Metric | factual (20) | multi_hop (20) | adversarial (10) |
|---|---|---|---|
| faithfulness | 0.6819 | 0.6087 | 0.6022 |
| answer_relevancy | 0.7784 | 0.7493 | 0.7109 |
| context_precision | 0.7500 | 0.7500 | 0.7500 |
| context_recall | 0.6592 | 0.5838 | 0.4740 |
| avg_score | 0.7174 | 0.6730 | 0.6343 |

## Bottom 10 và nguyên nhân

| Rank | Question ID | Distribution | Câu hỏi | Avg Score | Worst Metric | Diagnosis | Suggested Fix |
|---|---|---|---|---|---|---|---|
| 1 | 5 | factual | Muốn mua thiết bị trị giá 55 triệu cần ai phê duyệt? | 0.4750 | faithfulness | LLM hallucinating | Tighten system prompt, lower temperature |
| 2 | 22 | multi_hop | Nếu cần mua một chiếc laptop 30 triệu cho nhân viên mới, ai phê duyệt và cần gì từ phòng CNTT? | 0.4750 | faithfulness | LLM hallucinating | Tighten system prompt, lower temperature |
| 3 | 25 | multi_hop | Lương thử việc của nhân viên Junior mức cao nhất là bao nhiêu? | 0.4750 | faithfulness | LLM hallucinating | Tighten system prompt, lower temperature |
| 4 | 33 | multi_hop | Nhân viên Manager có thâm niên 12 năm: tổng phụ cấp hàng tháng và số ngày phép năm theo v2024 là bao nhiêu? | 0.4750 | faithfulness | LLM hallucinating | Tighten system prompt, lower temperature |
| 5 | 34 | multi_hop | Nhân viên tạm ứng 4 triệu và một nhân viên khác tạm ứng 7 triệu: quy trình phê duyệt khác nhau thế nào? | 0.4750 | faithfulness | LLM hallucinating | Tighten system prompt, lower temperature |
| 6 | 42 | adversarial | Thâm niên bao nhiêu năm thì được cộng thêm ngày phép? | 0.4750 | faithfulness | LLM hallucinating | Tighten system prompt, lower temperature |
| 7 | 44 | adversarial | Bao lâu phải đổi mật khẩu một lần? | 0.4750 | faithfulness | LLM hallucinating | Tighten system prompt, lower temperature |
| 8 | 50 | adversarial | Nhân viên Manager có thể dùng VPN cá nhân (như NordVPN) khi WFH để tăng bảo mật thêm không? | 0.4750 | faithfulness | LLM hallucinating | Tighten system prompt, lower temperature |
| 9 | 40 | multi_hop | Nhân viên cấp Manager có thời hạn thử việc 90 ngày, đang trong tháng thứ 3, phát hiện vi phạm bảo mật. Họ nên và không nên làm gì theo chính sách? | 0.4830 | faithfulness | LLM hallucinating | Tighten system prompt, lower temperature |
| 10 | 29 | multi_hop | Nhân viên tạm ứng 8 triệu, chưa thanh toán sau 30 ngày (quá hạn 15 ngày). Ai phê duyệt khoản này và phí phạt là bao nhiêu? | 0.4844 | faithfulness | LLM hallucinating | Tighten system prompt, lower temperature |

### Đối chiếu bằng chứng thực tế:
- **Câu 5 (factual)**: Yêu cầu hạn mức mua sắm thiết bị trên 50 triệu. Chunks context trả về có nhắc đến hạn mức mua sắm nhưng phân mảnh qua các cấp Giám đốc và Hội đồng quản trị. LLM khi tổng hợp đã suy diễn thêm quy trình báo giá 3 bên dẫn đến faithfulness bị đánh giá thấp.
- **Câu 22 & 33 (multi-hop)**: Đòi hỏi thông tin kết hợp giữa chính sách mua sắm CNTT với phụ cấp/ngày phép thâm niên. Context recall bị sụt giảm do chunk child (256 tokens) không chứa trọn vẹn cả bảng thâm niên và bảng phụ cấp, buộc LLM phải tổng hợp thiếu căn cứ và bị trừ điểm faithfulness.
- **Câu 42 & 50 (adversarial)**: Đây là các câu hỏi gài bẫy (ví dụ dùng VPN cá nhân NordVPN thay vì VPN công ty, hoặc hỏi thâm niên cộng ngày phép theo luật cũ vs chính sách mới). Pipeline chưa nhận diện được bẫy phủ định và bẫy xung đột phiên bản, dẫn đến việc LLM trả lời dựa trên suy đoán logic chung thay vì trích dẫn chính xác quy định cấm của công ty.

## Matrix và nhóm yếu nhất

| Worst Metric | factual | multi_hop | adversarial | Tổng số câu |
|---|---|---|---|---|
| faithfulness | 5 | 7 | 3 | 15 |
| context_recall | 6 | 7 | 6 | 19 |
| context_precision | 9 | 6 | 1 | 16 |
| answer_relevancy | 0 | 0 | 0 | 0 |

Nhóm yếu theo mean thấp nhất: adversarial; mean: 0.6343.
Worst metric xuất hiện nhiều nhất: context_recall; số câu: 19.

### Phân tích nguyên nhân và đề xuất cải tiến:
- **Nguyên nhân adversarial yếu nhất**: Điểm trung bình của tập adversarial (0.6343) thấp hơn rõ rệt so với factual (0.7174) và multi_hop (0.6730). Đặc biệt `context_recall` của adversarial chỉ đạt 0.4740 (dưới 0.50). Nguyên nhân cốt lõi là các câu hỏi adversarial sử dụng từ ngữ gây nhiễu, tiền giả định sai hoặc tham chiếu phiên bản tài liệu cũ, khiến bước Dense/BM25 retrieval không kéo về đúng chunk chứa quy định phản bác hoặc phiên bản cập nhật v2024.
- **Metric yếu nhất**: `context_recall` chiếm ưu thế áp đảo với 19/50 câu bị xếp là worst metric. Điều này phản ánh kích thước chunk child (256 tokens) hiện tại có thể hơi nhỏ cho các câu hỏi đa ý hoặc cần ngữ cảnh toàn diện từ tài liệu cha.
- **Đề xuất khắc phục**:
  1. Nâng cấp bộ chunking: Tăng kích thước child chunk lên 384 tokens hoặc bổ sung contextual enrichment (M5) tóm tắt mục tiêu chính sách vào tiêu đề chunk.
  2. Bổ sung Query Expansion / HyDE hoặc Query Rewriting trước khi retrieval để bóc tách các câu hỏi đa ý thành các sub-queries độc lập.
  3. Kiểm chứng hiệu quả: Chạy lại `python scripts/run_experiments.py --phase a --live` và so sánh avg_score của tập adversarial so với mốc 0.6343 hiện tại.

## Bẫy adversarial và giới hạn

### So sánh với factual và multi_hop:
Trong tập adversarial, các bẫy điển hình tập trung vào 2 dạng:
1. **Xung đột phiên bản (Version Conflict)**: Câu hỏi hỏi về quy định năm 2023 nhưng chính sách đã cập nhật v2024 (ví dụ số ngày nghỉ phép, phụ cấp ăn trưa). Nếu retriever lấy nhầm chunk cũ hoặc LLM không chú ý trường metadata version, điểm faithfulness sẽ rớt mạnh.
2. **Tiền giả định sai và phủ định (Negation/False Premise)**: Điển hình như câu 50 hỏi về việc dùng VPN cá nhân bên thứ ba để "tăng bảo mật". Retriever trả về tài liệu bảo mật chung, LLM bị thuyết phục bởi tiền giả định "tăng bảo mật" nên trả lời nước đôi thay vì bác bỏ dứt khoát rằng VPN cá nhân bị nghiêm cấm theo chính sách IT.

### Giới hạn thực nghiệm:
- Tập test set gồm 50 câu (20 factual, 20 multi_hop, 10 adversarial) tuy phản ánh đúng xu hướng nhưng cỡ mẫu 10 câu cho adversarial còn tương đối nhỏ để phân tích sâu về mặt thống kê.
- Model generation sử dụng là `gpt-4o-mini` qua OpenRouter API. Việc giới hạn context window và nhiệt độ mặc định có thể ảnh hưởng đến khả năng lý luận đa bước đối với các câu multi-hop phức tạp.
