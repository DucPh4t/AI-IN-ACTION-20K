# Đánh giá LLM Judge Phase B

Nhóm: GOHOME

Người phụ trách: Nguyễn Xuân Khuê - 2A202602999

Nguồn: `artifacts/judge_results.json`; run timestamp: 2026-10-12T09:26:07.245149+00:00.
Models generation/judge: Generation: openai/gpt-4o-mini; Judge: gpt-4o-mini.

## Năm cặp A/B và hai lượt

Nguồn cố định: A từ `artifacts/answers_50q.json:answer`; B từ `fixtures/human_labels_10q.json:model_answer`; reference từ `fixtures/test_set_50q.json:ground_truth`.
Ids: 1, 5, 12, 21, 41. Không đổi nguồn sau khi xem kết quả judge.

| Question ID | Winner Lượt 1 | Winner Lượt 2 (quy về gốc) | Final Winner | Nhất quán vị trí | Scores Lượt 1 (A/B) | Scores Lượt 2 (A/B) |
|---|---|---|---|---|---|---|
| 1 | B | B | B | Có | 0.0 / 1.0 | 0.0 / 1.0 |
| 5 | B | A | tie | Không | 0.0 / 0.5 | 1.0 / 0.0 |
| 12 | A | A | A | Có | 1.0 / 0.7 | 1.0 / 0.7 |
| 21 | B | B | B | Có | 0.8 / 1.0 | 0.6 / 1.0 |
| 41 | B | B | B | Có | 0.0 / 0.6 | 0.0 / 0.6 |

Position bias count/rate: 1 / 0.2 (20.0%).
Verbosity win rate: 0.5 (50.0%); decisive cases: 4.

### Phân tích chi tiết và đối chiếu nội dung:
- **Câu không nhất quán (ID 5)**:
  - Lượt 1 (A trước, B sau): Judge chọn B thắng với lý do B có thông tin liên quan hơn dù không hoàn toàn chính xác.
  - Lượt 2 (B đưa lên đầu, A xuống sau): Sau khi swap vị trí, Judge đổi ý chọn A thắng với lập luận Answer B chỉ báo không tìm thấy thông tin trong khi Answer A nêu sai người phê duyệt.
  - Do có xung đột kết quả khi hoán đổi thứ tự hiển thị, cơ chế Swap-and-Average đã xử lý hòa (`final_winner = tie`), phản ánh đúng hiện tượng Position Inconsistency do mô hình bị ảnh hưởng bởi thứ tự đọc vào prompt.
- **Hiện tượng Verbosity**:
  - Trong 4 ca phân định thắng thua (`decisive cases`), có 2 ca câu trả lời dài hơn giành chiến thắng (ID 12: A dài hơn và thắng; ID 21: B dài hơn và thắng). Tỷ lệ verbosity win rate là 2/4 = 50.0%.
  - Tỷ lệ 50.0% này cho thấy Judge không bị thiên vị mù quáng vào độ dài văn bản (verbosity bias không chiếm ưu thế tuyệt đối), mà Judge thực sự cân nhắc nội dung thông tin: ở câu 1 và 41, ứng viên thắng vì tính chính xác và bám sát chính sách chứ không đơn thuần vì số lượng từ.

## Calibration đúng model_answer

Helper đánh giá đúng question/model_answer đang có trong fixtures/human_labels_10q.json; không lấy answer mới của pipeline. Prompt chỉ nhận question, answer, reference. Không gửi human_label, human_note hoặc phân bố nhãn human vào prompt.

| Question ID | Model Answer Gốc | Nhãn Judge | Nhãn Human | Agree | Lý do của Judge |
|---|---|---|---|---|---|
| 1 | Nhân viên kết hôn được nghỉ 3 ngày phép có lương, không trừ vào phép năm. | 1 | 1 | Có | Câu trả lời chính xác theo thông tin trong tài liệu tham khảo, nêu rõ số ngày nghỉ và điều kiện không trừ vào phép năm. |
| 5 | Mua thiết bị 55 triệu thuộc thẩm quyền của Giám đốc bộ phận theo quy trình mua sắm. | 0 | 0 | Có | Câu trả lời sai vì không nêu đúng người phê duyệt theo chính sách, cần Tổng Giám đốc chứ không phải Giám đốc phòng ban. |
| 12 | Thưởng Tết áp dụng cho nhân viên chính thức từ đủ 6 tháng, tối thiểu 1 tháng lương. | 1 | 1 | Có | Câu trả lời chính xác theo thông tin trong reference, nêu rõ điều kiện và mức thưởng cho nhân viên chính thức có từ 6 tháng trở lên. |
| 21 | Nhân viên Senior 9 năm có 16 ngày phép và khung lương 30 - 45 triệu. | 1 | 1 | Có | Câu trả lời chính xác theo reference, nêu rõ số ngày phép và khoảng lương cho nhân viên Senior có 9 năm thâm niên. |
| 23 | Nghỉ việc sau 8 tháng khóa học thì phải hoàn trả 100% chi phí đào tạo 25 triệu. | 1 | 1 | Có | Câu trả lời chính xác theo reference, nêu rõ nhân viên phải hoàn trả 25 triệu do chưa đủ 1 năm cam kết. |
| 29 | Trưởng phòng duyệt tạm ứng 8 triệu; phạt 2% một tháng trên số tiền tạm ứng. | 0 | 0 | Có | Câu trả lời sai vì chỉ đề cập Trưởng phòng phê duyệt mà không nhắc đến Kế toán trưởng, và phí phạt được tính cho quá hạn 15 ngày. |
| 33 | Manager thâm niên 12 năm có 16 ngày phép theo v2024 và phụ cấp 3.5 triệu/tháng. | 1 | 1 | Có | Câu trả lời cung cấp đúng số ngày phép và tổng phụ cấp hàng tháng theo thông tin trong tài liệu tham khảo. |
| 41 | Nhân viên chính thức được nghỉ 12 ngày phép một năm theo chính sách nghỉ phép. | 0 | 0 | Có | Câu trả lời dựa trên chính sách cũ (v2023) là sai, vì chính sách hiện hành (v2024) quy định nhân viên được nghỉ 15 ngày phép năm. |
| 46 | Nhân viên thử việc không có ngày phép năm; nếu cần nghỉ phải xin nghỉ không lương và được Trưởng phòng phê duyệt. | 1 | 1 | Có | Câu trả lời chính xác theo reference, nêu rõ rằng nhân viên thử việc không được nghỉ phép năm và phải xin nghỉ không lương nếu cần. |
| 50 | Nhân viên được phép dùng VPN cá nhân nếu đã cài đặt phần mềm diệt virus. | 0 | 0 | Có | Câu trả lời sai vì khẳng định cho phép sử dụng VPN cá nhân, trong khi reference rõ ràng cấm điều này. |

Cohen’s κ: 1.0.
Observed/chance agreement và diễn giải:
- Tỷ lệ đồng thuận quan sát được: P_o = 10 / 10 = 1.0 (100%).
- Tỷ lệ đồng thuận ngẫu nhiên kỳ vọng: P_e = (0.6 * 0.6) + (0.4 * 0.4) = 0.36 + 0.16 = 0.52.
- Hệ số Cohen's kappa: κ = (P_o - P_e) / (1 - P_e) = (1.0 - 0.52) / (1 - 0.52) = 1.0.
- Kết quả κ = 1.0 thể hiện sự tương đồng hoàn hảo (perfect agreement) giữa LLM Judge nhị phân và chuyên gia con người trên tập mẫu thử nghiệm chuẩn 10 câu.

## Giới hạn và cách dùng judge

### Giới hạn mô hình và kích thước mẫu:
1. **Cỡ mẫu nhỏ**: Tập hiệu chuẩn gồm 10 câu hỏi nhị phân và 5 cặp so sánh pairwise. Mặc dù đạt kết quả xuất sắc (κ = 1.0, position bias 20%), tập mẫu chưa thể bao phủ toàn bộ các góc khuất ngôn ngữ và ngữ cảnh phức tạp của các bộ quy định đa dạng.
2. **Khả năng bị ảnh hưởng bởi Position Bias**: Kết quả câu 5 cho thấy khi cả 2 câu trả lời đều có khiếm khuyết hoặc ranh giới đúng/sai mong manh, Judge rất dễ bị ảnh hưởng bởi thứ tự đọc vào prompt (vị trí A trước hay B trước).
3. **Chi phí và độ trễ**: Gọi LLM Judge chạy 2 lượt (Swap-and-Average) tốn gấp đôi token và thời gian so với gọi đơn lẻ, không phù hợp cho online real-time guard mà phù hợp cho offline regression testing.

### Khuyến nghị vận hành LLM Judge:
- **Bắt buộc áp dụng Swap-and-Average**: Khi dùng LLM làm trọng tài đánh giá A/B, không bao giờ tin tưởng kết quả của một lượt chạy đơn lẻ. Luôn đảo vị trí A/B và chỉ chấp nhận kết quả nếu mô hình đưa ra quyết định nhất quán ở cả hai lượt.
- **Không coi Judge là chân lý tuyệt đối**: Trong môi trường production, LLM Judge chỉ đóng vai trò bộ lọc tự động vòng 1 (triage filter). Các trường hợp có điểm số mấp mé ngưỡng hoặc không nhất quán vị trí (`final_winner = tie`) cần được gắn cờ (flagged) để chuyên gia con người (human-in-the-loop) thẩm định lại.
