# K4 — Ngày 1: Bài Tập & Phản Ánh
## Khám Phá LLM API | Phiếu Thực Hành

**Thời lượng:** 4 tiếng
**Cách làm:** Trả lời từng câu ngay sau khi hoàn thành block tương ứng —
đừng để dồn hết về cuối buổi. Thay dòng `*Câu trả lời của bạn*` bằng câu
trả lời thật (chấm tự động sẽ đếm số câu đã trả lời).

---

## Block 1 — API Cơ Bản (trả lời sau Checkpoint 1)

### Câu 1.1 — Độ nhạy của temperature
Gọi `call_openai` với temperature 0.0, 0.5, 1.0 và 1.5 dùng prompt
**"Hãy kể cho tôi một sự thật thú vị về Việt Nam."**

**Bạn nhận thấy quy luật gì qua bốn phản hồi?** (2–3 câu)
> Khi tăng temperature từ 0.0 lên 1.5, phản hồi của mô hình chuyển dần từ tính xác thực, nhất quán cao sang sáng tạo và ngẫu nhiên hơn. Tại temperature 0.0 và 0.5, mô hình đưa ra các sự thật chuẩn xác, phổ biến với cấu trúc câu chặt chẽ. Đến temperature 1.0 và đặc biệt là 1.5, văn phong trở nên phong phú hơn nhưng có xu hướng hoa mỹ hoặc sáng tạo câu chữ ngẫu nhiên hơn.

### Câu 1.2 — Chọn temperature cho sản phẩm
**Bạn sẽ đặt temperature bao nhiêu cho chatbot hỗ trợ khách hàng, và tại sao?**
> Cho chatbot hỗ trợ khách hàng, nên chọn temperature thấp trong khoảng 0.0 đến 0.2. Điều này đảm bảo phản hồi có tính nhất quán cao, cung cấp chính xác các thông tin quy trình/chính sách dịch vụ và tránh việc mô hình tự sáng tạo thông tin gây hiểu lầm cho khách hàng (hallucination).

### Câu 1.3 — Đánh đổi chi phí
Kịch bản: 10.000 người dùng hoạt động mỗi ngày, mỗi người gọi API 3 lần,
mỗi lần trung bình ~350 token đầu ra.

**Ước tính GPT-4o đắt hơn GPT-4o-mini bao nhiêu lần cho workload này? Nêu một
trường hợp GPT-4o xứng đáng với chi phí và một trường hợp nên dùng mini:**
> Tổng lượng token đầu ra mỗi ngày là $10.000 \times 3 \times 350 = 10.500.000$ token. Dựa trên đơn giá đầu ra, GPT-4o (\$0.010/1K token) đắt gấp khoảng 16.67 lần so với GPT-4o-mini (\$0.0006/1K token). GPT-4o xứng đáng với chi phí khi ứng dụng cần giải quyết bài toán suy luận phức tạp, phân tích dữ liệu chuyên sâu hoặc lập trình logic khó. Ngược lại, nên dùng GPT-4o-mini cho các tác vụ phân loại văn bản, tóm tắt tin nhắn hoặc chatbot hỏi đáp cơ bản để tiết kiệm chi phí vận hành.

---

## Block 2 — System Prompt & Token (trả lời sau Checkpoint 2)

### Câu 2.1 — Sức mạnh của persona
Gọi `chat_with_system_prompt` hai lần với cùng câu hỏi
**"Giải thích blockchain là gì?"** nhưng hai system prompt khác nhau:
- "Bạn là giáo viên tiểu học, giải thích thật đơn giản cho trẻ 8 tuổi."
- "Bạn là chuyên gia tài chính, trả lời chuyên sâu bằng thuật ngữ kỹ thuật."

**Hai phản hồi khác nhau như thế nào (độ dài, từ vựng, ví dụ)? System prompt
ảnh hưởng đến hành vi model ra sao?** (3–4 câu)
> Phản hồi của giáo viên tiểu học dùng ví dụ trực quan (như sổ nhật ký dùng chung mà ai cũng giữ 1 bản), từ ngữ đơn giản, gần gũi và độ dài vừa phải. Trái lại, phản hồi của chuyên gia tài chính sử dụng thuật ngữ chuyên ngành (như cơ chế sổ cái phân tán, thuật toán đồng thuận, mã hóa cryptographic, immutability) với cấu trúc phân tích kỹ thuật sâu hơn. System prompt đóng vai trò định hình persona, điều khiển trực tiếp tông giọng, mức độ phức tạp từ vựng và phương pháp truyền đạt nội dung của mô hình.

### Câu 2.2 — tiktoken vs đếm từ
Chọn một đoạn văn tiếng Việt ~100 từ. So sánh số token theo `count_tokens`
(tiktoken) với ước lượng `số từ / 0.75` mà Part 1 đã dùng.

**Hai con số chênh nhau bao nhiêu phần trăm? Vì sao tiếng Việt thường tốn
nhiều token hơn tiếng Anh cùng độ dài?**
> Thư viện `tiktoken` cho ra số token cao hơn ước lượng `số từ / 0.75` khoảng 25% - 40% tùy thuộc vào số lượng từ có dấu. Tiếng Việt thường tốn nhiều token hơn tiếng Anh vì hầu hết các tokenizer (như BPE của OpenAI) được tối ưu hóa theo tần suất từ vựng tiếng Anh. Các ký tự tiếng Việt có dấu Unicode hoặc các từ ghép tiếng Việt bị tách thành nhiều sub-word token nhỏ hơn.

---

## Block 3 — Streaming & Độ Bền (trả lời sau Checkpoint 3)

### Câu 3.1 — Trải nghiệm người dùng với streaming
**Streaming quan trọng nhất trong trường hợp nào, và khi nào thì
non-streaming lại phù hợp hơn?** (1 đoạn văn)
> Streaming quan trọng nhất trong các ứng dụng trò chuyện trực tiếp (chatbot, trợ lý ảo) đòi hỏi phản hồi dài, giúp cải thiện trải nghiệm người dùng bằng cách giảm độ trễ cảm nhận (Time To First Token - TTFT) vì người dùng thấy ngay câu chữ hiển thị từng giây. Ngược lại, non-streaming phù hợp hơn cho các tác vụ xử lý ngầm (background job), gọi API lấy dữ liệu JSON cấu trúc (structured output), hoặc khi cần thẩm định toàn bộ câu trả lời trước khi chuyển tiếp cho hệ thống khác.

### Câu 3.2 — Vì sao backoff theo cấp số nhân?
**So với delay cố định (ví dụ luôn chờ 1 giây), exponential backoff có lợi
thế gì khi API bị quá tải? Điều gì xảy ra nếu hàng nghìn client cùng retry
với delay cố định giống nhau?**
> Exponential backoff giúp giảm áp lực đáng kể cho server bằng cách kéo dài thời gian chờ giữa các lần thử lại ($0.1s, 0.2s, 0.4s,...$). Nếu hàng nghìn client cùng retry với một khoảng delay cố định (ví dụ 1s), sẽ xảy ra hiện tượng "thảm họa thét gào" (thundering herd problem), tạo ra các đợt sóng traffic đồng loạt tấn công lại server đúng thời điểm, khiến server đang quá tải càng sụp đổ nghiêm trọng hơn.

---

## Block 4 — Mini-Project (trả lời sau Checkpoint 4)

### Câu 4.1 — Thiết kế persona
**Bạn chọn persona gì cho trợ lý của mình? Viết lại system prompt đó và giải
thích 1–2 lựa chọn từ ngữ quan trọng trong prompt (ví dụ: vì sao yêu cầu
"trả lời ngắn gọn", vì sao chỉ định ngôn ngữ...):**
> Tôi chọn Persona: "Bạn là trợ giảng thân thiện của khóa AI, trả lời ngắn gọn bằng tiếng Việt." Việc yêu cầu "ngắn gọn" nhằm giới hạn số token đầu ra giúp tiết kiệm chi phí API và duy trì tốc độ hội thoại CLI nhanh chóng. Chỉ định "tiếng Việt" đảm bảo tính thống nhất ngôn ngữ cho trải nghiệm học tập của sinh viên.

### Câu 4.2 — Hạn chế & cải thiện
**Trợ lý của bạn hiện có hạn chế lớn nhất là gì (ví dụ: history chỉ 3 lượt,
không có bộ nhớ dài hạn, không kiểm duyệt nội dung...)? Đề xuất một cải
thiện cụ thể và mô tả ngắn cách triển khai:**
> Hạn chế lớn nhất là lịch sử hội thoại cố định ở 3 lượt gần nhất, làm mất bối cảnh nếu cuộc trò chuyện kéo dài. Cải thiện đề xuất: Triển khai kỹ thuật Tóm tắt Lịch sử (Conversation Summary Buffer Memory). Khi history vượt quá 6 messages, sử dụng model mini để tóm tắt các lượt hội thoại cũ thành 1 đoạn summary ngắn gắn vào system prompt, giúp giữ bối cảnh dài hạn mà không làm bùng nổ số lượng input token.

---

## Danh Sách Kiểm Tra Nộp Bài

- [x] `python grade.py` — xem điểm tự động, mục tiêu ≥ 75/100
- [x] Cả 4 checkpoint pytest đều pass
- [x] Tất cả 9 câu trong file này đã được trả lời
- [x] Đã copy bài làm vào folder `solution/`, push lên fork và dán link trên trang bài Lab ở VLearn trước 23:59 ngày 11/09/2026
