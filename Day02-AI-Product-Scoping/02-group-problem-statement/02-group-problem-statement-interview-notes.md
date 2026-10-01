# Ghi chú phỏng vấn & Kiểm chứng nhanh (Validation Notes)

> Dự án: Tổng hợp và Chuẩn hóa Báo cáo Lỗ hổng Pentest từ nhiều thành viên  
> Nhóm thực hiện: Nhóm 6 thành viên (Phát, Nam, Đạt, Nhân, Chinh, Tài)

---

## 1. Phỏng vấn sâu (Deep Interviews)

### Phỏng vấn 1: Bùi Gia Chinh — Intern An ninh mạng (Chủ bài toán)
- **Thời gian thực hiện:** 12/09/2026
- **Câu hỏi chính:**
  1. *Quy trình hiện tại gom báo cáo từ anh em pentester diễn ra như thế nào?*
     - **Trả lời:** *"Mỗi đợt kết thúc pentest (thường là chiều thứ Sáu hoặc đầu tuần), 4-5 người gửi file qua Slack hoặc up lên Google Drive. Người thì viết file `.docx`, người nộp `.md`, người quăng file `.txt`. Khổ nhất là style hành văn: có bạn viết rất cẩn thận, có bạn chỉ quăng đúng 1 dòng lệnh curl và cái screenshot mờ căm không ghi CVSS hay remediation."*
  2. *Điểm nghẽn tốn thời gian nhất là bước nào?*
     - **Trả lời:** *"Chắc chắn là bước format lại từng finding vào template chung của công ty. Mình phải ngồi gõ lại từng mục: Tổng quan lỗ hổng, Các bước tái hiện (PoC steps), và Biện pháp khắc phục (Remediation). Mỗi finding mất 10-15 phút, một đợt 15-20 finding là ngốn đứt 1.5 đến 2 tiếng chỉ để sửa câu từ."*
  3. *Từng có rủi ro nào xảy ra chưa?*
     - **Trả lời:** *"Đợt tháng trước có 2 bạn cùng test web app và cùng tìm ra 1 lỗi XSS ở trang tìm kiếm nhưng đặt tên khác nhau (một bạn đặt Reflected XSS, một bạn đặt Input Validation Failure). Mình làm tay lúc 10h đêm mỏi mắt quá nên không nhận ra, paste cả hai vào báo cáo. Hôm sau Lead review phát hiện bị trùng và nhắc nhở."*

### Phỏng vấn 2: Đỗ Thành Đạt — Sinh viên CNTT / Dev tham gia dự án phần mềm
- **Thời gian thực hiện:** 12/09/2026
- **Câu hỏi chính:**
  1. *Nếu công ty áp đặt 1 form mẫu cứng bắt buộc tester phải điền đúng 100%, tester có chịu làm không?*
     - **Trả lời:** *"Rất khó. Khi tester đang khai thác lỗ hổng (exploit), người ta chỉ muốn ghi nhanh payload, chụp màn hình bằng chứng rồi chuyển sang test mục khác. Nếu bắt mở form web phức tạp nhập từng trường bắt buộc thì năng suất test bị giảm mạnh, mọi người sẽ phản ứng hoặc điền đối phó."*
  2. *Đạt nghĩ giải pháp nào là hợp lý nhất?*
     - **Trả lời:** *"Cứ để anh em nộp ghi chép thô dạng text/markdown tự do. Cần một công cụ tự động ingest text đó, bóc tách và đưa vào khung chuẩn, sau đó người tổng hợp chỉ cần mở ra review và duyệt nhanh."*

---

## 2. Kết quả Khảo sát nhanh (Quick Survey trong lớp Lab)

- **Cỡ mẫu:** 6 học viên trong phòng lab có kinh nghiệm làm Dev / SecOps / Data.
- **Kết quả khảo sát:**
  - **Câu 1:** Bạn có thường xuyên phải gom tài liệu/báo cáo từ nhiều thành viên thành 1 bản thống nhất không?  
    $\rightarrow$ **6/6 (100%)** trả lời CÓ.
  - **Câu 2:** Bước nào gây nản lòng và tốn thời gian nhất?  
    $\rightarrow$ **5/6 (83.3%)** chọn "Đọc sửa văn phong lệch pha và chuẩn hóa format"; **1/6 (16.7%)** chọn "Chờ mọi người nộp bài".
  - **Câu 3:** Bạn có sẵn sàng để AI hỗ trợ format báo cáo nội bộ không?  
    $\rightarrow$ **6/6 (100%)** đồng ý, với điều kiện bắt buộc: **Không được gửi dữ liệu nhạy cảm của khách hàng lên cloud công khai**.

---

## 3. Nhật ký thời gian thực tế (Log dữ liệu 3 đợt gần nhất)

| Đợt Pentest | Số finding | Thời gian tổng hợp thủ công | Sự cố / Vấn đề phát sinh |
|---|---:|---:|---|
| **Đợt 1 (Tháng 7)** | 14 | 3 giờ 45 phút | Thiếu 3 mã CVSS, phải nhắn tin hỏi lại tester làm trễ 45 phút. |
| **Đợt 2 (Tháng 8)** | 18 | 4 giờ 10 phút | 1 tester nộp thiếu bước PoC, báo cáo bị trễ sang ngày hôm sau. |
| **Đợt 3 (Gần nhất)** | 15 | 3 giờ 15 phút | Bị trùng lặp 2 finding XSS do 2 tester đặt tên khác nhau. |
