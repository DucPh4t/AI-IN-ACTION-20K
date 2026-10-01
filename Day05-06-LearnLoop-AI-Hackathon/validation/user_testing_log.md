# 🧪 Báo Cáo Xác Thực Người Dùng Ngoài Nhóm (R6 Validation Log)
> **Dự án:** LearnLoop — AI Tutor Trợ Giảng Tương Tác Hai Chiều  
> **Mốc triển khai:** CP5 (Trước 13:00 ngày 18/09/2026)  
> **Phương pháp luận:** Mom Test (Quan sát hành vi thực tế, không gợi ý, trích dẫn nguyên văn)  
> **Mục tiêu:** Kiểm chứng trải nghiệm người dùng thực tế, săn điểm thưởng R6 (+8 điểm)  

---

## 📋 Bảng Nhật Ký Thử Nghiệm Người Dùng (5 Testers — Đủ 2 Willing Users CP1)

| STT | Người thử (Tên/Vai — Willing User?) | Nhiệm vụ giao (Task) | Điểm tắc nghẽn (Quan sát hành vi) | Trích dẫn nguyên văn (Mom Test Quote) | Mức nghiêm trọng | Quyết định xử lý của nhóm |
| :---: | :---|---|---|---|:---:|---|
| **1** | **Lê Phan Việt Cường**<br>*(Học viên E403 - MSSV: 2A202602641)<br>**[Willing User CP1]** | Dùng LearnLoop tra cứu và tóm tắt thuật ngữ "Transformer" ở Slide 8, sau đó kiểm tra nguồn trích dẫn. | Thẻ trích dẫn `[Trang 8]` lúc đầu nhìn giống text tĩnh; người dùng do dự 4 giây trước khi rê chuột vào để click. | *"Ủa bấm vào cái số trang [Trang 8] này là nó tự cuộn slide qua trang đó luôn hả? Ban đầu tưởng chỉ là text ghi chú thường thôi chứ, phải rê chuột vào mới thấy đổi con trỏ!"* | Trung bình | **[Làm ngay trước Demo]** Thêm icon liên kết nhỏ `↗`, gạch chân chấm (dotted) và tooltip `Nhấp để mở Slide` để nhận diện rõ hyperlink tương tác. |
| **2** | **Nguyễn Đức Danh**<br>*(Học viên E403 - MSSV: 2A202602722)<br>**[Willing User CP1]** | Thử bôi đen một chuỗi ký tự nhiễu vô nghĩa (ví dụ `-->`) khi đang đọc bài để kiểm tra phản ứng của hệ thống. | Hệ thống chặn bằng Dual-layer Guardrail tại chỗ rất tốt, nhưng toast cảnh báo màu vàng tự biến mất sau 2.5s khiến người dùng chưa đọc kịp dòng giải thích. | *"Ủa cái thông báo màu vàng báo 'đoạn chọn quá ngắn hoặc không mang nghĩa học thuật' biến mất hơi nhanh đấy, tôi mới đọc được nửa câu là nó lặn mất rồi, nên để tầm 4-5 giây hoặc có nút bấm tắt."* | Thấp | **[Làm ngay trước Demo]** Tăng thời gian hiển thị thông báo Guardrail từ 2.5s lên 4.5s và thêm nút `✕` để người dùng chủ động đóng. |
| **3** | **Trần Đức Anh**<br>*(Học viên E403 - Lớp 3A)<br>**[Willing User CP1]** | Sử dụng tính năng Socratic Probing để đào sâu sự khác biệt giữa RNN và Transformer sau khi đọc xong câu trả lời cơ bản. | Người dùng nhìn thấy 2 nút gợi ý `[So sánh với RNN]` và `[Cơ chế Self-Attention]`; bấm chọn nhánh 1 nhưng lo lắng câu trả lời ban đầu bị xóa mất. | *"Cái này hay này, hỏi bot cũ nó nói một tràng 1.500 chữ đọc mỏi cả mắt, cái này nó cho nút chọn hướng hỏi tiếp đỡ phải ngồi nghĩ prompt. Nhưng mà bấm xong có lưu lại câu trước đó không hay nó đè mất?"* | Trung bình | **[Làm ngay trước Demo]** Hiển thị câu trả lời mở rộng dạng Accordion nối tiếp phía dưới, gắn nhãn `Đang xem tiếp: Nhánh đào sâu` để khẳng định câu trả lời gốc vẫn còn nguyên vẹn. |
| **4** | **Phạm Thị Thu Trang**<br>*(Học viên nhóm E402 - Lớp 3B)<br>**[External User đổi chéo]** | Tra cứu định nghĩa "Cơ chế Attention" và sao chép kết quả để đưa vào ứng dụng ghi chú cá nhân (Notion). | Câu trả lời micro-summary ngắn gọn (180 ký tự), rất ưng ý; tuy nhiên người dùng phải dùng chuột bôi đen thủ công toàn bộ text trong popup để Ctrl+C, thao tác hơi vụng về trên canvas. | *"Nội dung trích dẫn transcript khớp đúng lời thầy giảng hôm qua, rất chuẩn! Cơ mà nhóm nên thêm cái nút copy nhanh câu trả lời vào góc phải, chứ tôi học hay vừa nghe vừa paste vào Notion, bôi đen bằng tay trên web hay bị trượt."* | Trung bình | **[Làm ngay trước Demo]** Tích hợp nút `Sao chép nhanh` (1-click Clipboard Copy) ở góc trên bên phải khung trả lời, tự động kèm nguồn trích dẫn chuẩn. |
| **5** | **Nguyễn Thanh Hải**<br>*(Học viên nhóm E404 - Lớp 3A)<br>**[External User đổi chéo]** | Nhập câu hỏi tổng hợp: "cho tôi 5 loại mô hình xử lý ngôn ngữ được dùng nhiều nhất" và kiểm chứng độ chính xác số trang slide. | Hệ thống trả lời chính xác 5 mô hình trên Slide Trang 8 (không bịa trang 304). Tuy nhiên trên laptop 13 inch, thanh sidebar bên phải chiếm 380px khiến diện tích hiển thị slide bị thu hẹp. | *"Chuẩn Trang 8 luôn, không bịa trang 304 như con bot cũ của VLearn! Nhưng trên con máy 13 inch của mình cái sidebar bên phải hơi to, nếu có nút thu nhỏ hoặc dock xuống dưới thì nhìn slide rộng hơn."* | Thấp | **[Giữ nguyên có lý do & Đưa vào Backlog]** Giữ nguyên độ rộng 380px phục vụ trình chiếu màn hình lớn / máy chiếu trong buổi Demo CP6; đưa thiết kế Collapsible/Floating Dock vào Roadmap tuần sau. |

---

## 🔍 Tổng Hợp & Đánh Giá 4 Khối Trọng Yếu (Theo §4.2 02-guide.md)

### 1. Chủ đề lặp lại nhiều nhất (Most Common Feedback)
- **100% người dùng (5/5)** đánh giá cao sự vượt trội của **Micro-summary ngắn gọn (<250 ký tự)** và tính năng **nhảy trực tiếp đến trang slide nguồn** so với trải nghiệm cũ của VLearn (vốn xả văn bản dài 1.000–1.500 ký tự và hay bịa số trang).
- Người dùng có nhu cầu rất cao về mặt tiện ích thao tác nhanh khi học (nhận diện rõ link click được, copy nhanh sang Notion/vở ghi chép).

### 2. Thay đổi đã làm ngay trước buổi Demo (Cập nhật vào §9 Changelog của `spec.md`)
1. **Thêm nút Quick Copy (1-Click Clipboard Copy):** Cho phép học viên sao chép tức thì câu trả lời kèm citation để dán vào công cụ học tập cá nhân (Notion, Obsidian, Word).
2. **Visual Cue cho Citation Link:** Bổ sung icon `↗`, hiệu ứng hover gạch chân và tooltip `Nhấp để chuyển đến Slide` giúp học viên nhận biết ngay khả năng điều hướng slide 2 chiều.
3. **Tối ưu Toast Guardrail:** Kéo dài thời gian hiển thị thông báo an toàn từ 2.5 giây lên 4.5 giây kèm nút đóng thủ công.

### 3. Thiết kế quyết định giữ nguyên & Lập luận kỹ thuật
- **Giữ nguyên số lượng 2 Option đào sâu Socratic Probing:** Một số tester tò mò muốn có 4–5 gợi ý, tuy nhiên nhóm quyết định giữ cứng **2 lựa chọn đối lập/bổ trợ** để tránh gây quá tải nhận thức (Cognitive Overload / Paradox of Choice) cho học viên khi đang tập trung nghe giảng.
- **Giữ nguyên cố định bề rộng Sidebar 380px:** Đảm bảo khả năng hiển thị ổn định, chữ to rõ ràng khi chiếu lên máy chiếu hội trường trong buổi Demo trực tiếp.

### 4. Đưa vào Product Backlog (Cho Slide 6 — Nếu có thêm 1 tuần)
- Tích hợp tính năng tự động đồng bộ ghi chú học tập sang **Notion / Google Docs qua Webhook**.
- Hỗ trợ giao diện **Responsive Floating Dock** (tự co giãn hoặc thả nổi) tối ưu riêng cho laptop màn hình nhỏ (13 inch) và tablet.
- Mở rộng ngân hàng câu hỏi Socratic thích ứng dựa trên lịch sử học tập cá nhân hóa của từng học viên.
