# 03 — Individual Reflection

> Viết bằng lời của bạn (Phase 7 trong `01-worksheet.md`). Có thể dùng AI gợi ý câu hỏi tự soi, không dùng AI viết thay. 8-12 câu, có chuyện cụ thể.

## Thông tin cá nhân

- Họ và tên: Nguyễn Đức Phát
- Mã học viên: 2A202602753
- Nhóm: Nhóm 6 thành viên (Phát, Nam, Đạt, Nhân, Chinh, Tài)
- Candidate problem nhóm chọn: Tổng hợp và chuẩn hóa báo cáo lỗ hổng Pentest từ 4-5 thành viên thành 1 báo cáo hoàn chỉnh (Bùi Gia Chinh)

---

## 1. Tôi đã tham gia vào phần nào?

Ghi việc cụ thể + kết quả cụ thể. Không ghi chung chung kiểu "tham gia thảo luận".

| Hoạt động | Tôi đã làm gì? (việc cụ thể) | Kết quả / ảnh hưởng tới nhóm |
|---|---|---|
| **Scan cá nhân** | Tự scan 10 problems trải dài 4 lăng kính, bấm giờ đo thời gian sửa CV, ôn thi slide và xem YouTube | Đạt +3 điểm bonus scan rộng, chuẩn bị sẵn 3 Card chi tiết |
| **Pitch Problem Card** | Trình bày Card #1 (Đối chiếu CV với JD) trong 90 giây, giải thích quy trình 50' $\rightarrow$ 10' | Nhóm đánh giá cao tính gần gũi và đưa vào shortlist top 2 |
| **Challenge bài của bạn khác** | Đặt câu hỏi cho Chinh về rủi ro vi phạm hợp đồng bảo mật (NDA) khi đưa PoC lỗ hổng lên cloud | Buộc nhóm phải đưa ra giải pháp On-premise / Local LLM |
| **Gom trùng / cluster** | Cùng nhóm phân loại 18 candidates của 6 thành viên thành 4 cụm chuyên đề rõ ràng | Giúp nhóm nhìn ra bức tranh tổng thể và không bị rối ý |
| **Chọn candidate problem** | Đề xuất chọn bài Pentest của Chinh vì có tính thực chiến doanh nghiệp cao hơn bài cá nhân | Cả 6 người đồng thuận 100% chọn bài #13 làm đề tài nhóm |
| **Validation / research** | Cùng Đạt làm bảng phỏng vấn nhanh 6 bạn trong lab về nỗi đau format tài liệu kỹ thuật | Thu thập được số liệu khảo sát thực tế và 2 quote phỏng vấn sâu |
| **Workflow nhóm** | Đảm nhận vai trò thiết kế workflow Before (220') và After (55'), vẽ diagram trực quan | Tạo ra sơ đồ phân định rõ máy (Rule), AI và người (Human boundary) |
| **Problem Statement** | Cùng Nhân và Chinh viết PS v0 và tinh chỉnh lên v1, siết chặt các điều kiện Boundary | Đưa ra định nghĩa rõ ràng: không tự đổi CVSS, không gửi data ra ngoài |
| **Rule / Workflow / Agent** | Lập luận phản biện việc dùng Agent, định hình giải pháp Pipeline Workflow 5 bước | Giúp nhóm tiết kiệm tài nguyên tính toán và an toàn dữ liệu |
| **Decision** | Cùng nhóm thống nhất quyết định GO kèm điều kiện triển khai Local LLM trên hạ tầng nội bộ | Thiết lập kịch bản pilot nhỏ nhất và điều kiện rollback cụ thể |

**Dấu tay rõ nhất của tôi trong artifact cuối (1-2 câu):**

```text
Dấu tay rõ nhất của tôi là việc xây dựng sơ đồ Workflow Before/After phân tầng rõ rệt (Rule ở khâu parse, AI ở khâu format và Human ở khâu duyệt), đồng thời kiên quyết thiết lập ranh giới bảo mật (On-Premise LLM) để bảo vệ dữ liệu khách hàng theo đúng chuẩn NDA.
```

---

## 2. Bảng dùng AI (mỗi dòng 1 phase có dùng AI — 2 cột cuối bắt buộc)

| Phase | Tôi dùng AI để làm gì? | AI hữu ích ở đâu? | AI sai / hời hợt ở đâu? | Tôi sửa gì bằng nhận định của mình? |
|---|---|---|---|---|
| **Scan** | Gợi ý thêm các góc nhìn phản biện theo 4 lăng kính | Giúp liên kết việc học và sinh hoạt thành các con số đo lường | Gợi ý những bài toán viển vông như "Chatbot làm bài tập thay" | Loại bỏ ý kiến vi phạm liêm chính học thuật, giữ lại các pain đo được |
| **Problem Card** | Đóng vai PM khó tính để phản biện điểm nghẽn của từng card | Chỉ ra rủi ro AI hallucination khi viết CV có thể làm sai sự thật | Đánh giá sơ sài về giải pháp thay thế phi AI (Non-AI alternative) | Bổ sung phương án tạo sẵn 3 template CV cố định để so sánh |
| **Workflow** | Tạo ảnh trực quan hóa quy trình Before / After theo cấu trúc pipeline | Sinh sơ đồ quy trình dạng đồ họa rất đẹp, rõ ràng từng mốc thời gian | Hay tự ý chèn thêm các bước tự động hóa không có người duyệt | Bổ sung hộp thoại Human Boundary bắt buộc người phải review trước khi xuất file |
| **Research** | Tìm kiếm thông tin về các công cụ quản lý báo cáo pentest quốc tế | Giới thiệu được các nền tảng lớn như PlexTrac, Dradis | Không nắm rõ bảng giá bản quyền và chính sách NDA thực tế tại VN | Nhóm tự tra cứu trang chủ chính thức và bổ sung phân tích chi phí license |
| **Problem Statement** | Rà soát xem các field trong bảng PS có bị câu chữ chung chung không | Bắt bẻ các từ ngữ mơ hồ như "làm nhanh hơn", "tối ưu hơn" | Gợi ý metric chất lượng chung chung kiểu "đạt độ hài lòng 90%" | Đổi thành metric kỹ thuật đo được: 0 lỗi severity, 0 finding trùng lặp |
| **Rule / Workflow / Agent** | Thử prompt hỏi xem bài toán này nên dùng Agent hay Workflow | Liệt kê được ưu nhược điểm của từng cấp độ tự động hóa | Rất thích gợi ý làm Multi-Agent tự trị cho "hiện đại và ngầu" | Nhóm kiên quyết hạ xuống Workflow vì an toàn thông tin không cho phép Agent tự do |
| **Decision** | Gợi ý cấu trúc của một kế hoạch Pilot và điều kiện Rollback | Đưa ra khung kiểm thử 3 số đo rất bài bản | Viết điều kiện rollback quá chung chung kiểu "khi hệ thống không ổn" | Sửa thành con số cụ thể: Rollback nếu AI làm sai lệch nội dung PoC quá 15% |

---

## 3. Reflection câu hỏi mở

**Reflection (10 câu kể chuyện trải nghiệm thực tế trong lab):**

```text
Trải nghiệm làm việc nhóm trong buổi lab Day 02 hôm nay mang lại cho tôi rất nhiều bài học thực chiến giá trị. Ban đầu khi bước vào Phase 3, mỗi thành viên đều mang theo những bài toán rất hay từ bối cảnh riêng của mình, từ bài toán so khớp CV của tôi, bài toán crawl dữ liệu của Nam cho đến đề xuất hệ thống ReproScout multi-agent rất học thuật của Nhân. Có những lúc nhóm suýt bị cuốn theo tâm lý "solution-first", muốn làm một hệ thống Multi-Agent phức tạp với nhiều agent tự động tra cứu CVE và sửa code để bài nộp trông ấn tượng hơn. Tuy nhiên, sau khi tôi và nhóm cùng đào sâu phân tích bài toán báo cáo Pentest của Chinh, chúng tôi nhận ra rằng trong môi trường doanh nghiệp an ninh mạng, sự ổn định, tính bảo mật dữ liệu và trách nhiệm giải trình quan trọng hơn sự màu mè công nghệ rất nhiều. 

Việc đưa một Agent tự trị vào để nó tự ý thay đổi mức độ nghiêm trọng (Severity) hoặc tự gửi mail cho khách hàng là một thảm họa về bảo mật nếu xảy ra ảo giác. Tôi đã học được cách lùi lại một bước: thay vì cố đấm ăn xôi làm Agent, nhóm đã đồng thuận hạ giải pháp xuống mức Workflow kết hợp Rule-based validation và Local LLM chạy trên máy chủ nội bộ. Điều khó nhất với tôi khi tham gia hoàn thiện Problem Statement không phải là tính toán thời gian, mà là xác định ranh giới (Boundary) — làm rõ hệ thống được phép làm gì và tuyệt đối KHÔNG được phép làm gì. Nhờ sự phản biện qua lại giữa các góc nhìn khác nhau của cả 6 bạn, sản phẩm cuối cùng của nhóm không chỉ là một ý tưởng AI trên giấy, mà là một giải pháp kỹ thuật có tính khả thi cao, bảo vệ được thỏa thuận bảo mật NDA và giải quyết đúng điểm nghẽn của người dùng thật.
```

---

## 4. Tự kiểm cuối bài (check trước khi nộp repo)

- [x] [12đ] Cá nhân có 10 problems (vượt chuẩn 5+) + top 3 Problem Cards chi tiết.
- [x] [12đ] Tôi đã pitch rõ bài CV + challenge nhóm đúng trọng tâm về vấn đề NDA/Local LLM.
- [x] Nhóm có nhật ký hội tụ đầy đủ từ 18 candidates về 1 bài (Gom cụm, Shortlist, Chấm điểm).
- [x] [15đ] Nhóm có sơ đồ workflow trước/sau đầy đủ thời gian, bottleneck, human boundary, fallback.
- [x] [20đ] Nhóm có PS v0/v1 với metric trước/sau + boundary làm/không làm cụ thể.
- [x] [15đ] Nhóm có so sánh chi tiết No AI / Rule / Workflow / Agent và lý giải vì sao hạ cấp độ.
- [x] [10đ] Nhóm có quyết định GO với điều kiện On-premise + kịch bản pilot và rollback rõ ràng.
- [x] [10đ] Reflection này ghi nhận vai trò thật + bảng dùng AI chi tiết + 10 câu reflection sâu sắc.
- [x] [6đ] Tôi tự giải thích được toàn bộ mạch problem $\rightarrow$ workflow $\rightarrow$ metric $\rightarrow$ boundary $\rightarrow$ độ phù hợp AI.

