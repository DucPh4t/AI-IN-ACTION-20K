# 02 — Group Problem Statement (Bản nộp nhóm)

> Làm chung 1 bản, mỗi thành viên copy vào repo cá nhân. Đi theo Phase 3 → 6 trong `01-worksheet.md`. Nhóm chỉ chọn **candidate problem** ở Phase 3, viết Problem Statement sau khi validate + vẽ workflow.

## Thành viên nhóm

| STT | Họ và tên | Mã học viên | Vai trò trong nhóm (VD: facilitator, workflow, research, writer) |
|-----|-----------|-------------|---------------------------------------------------------------|
| 1   | Nguyễn Đức Phát | 2A202602753 | Facilitator / Workflow Designer |
| 2   | Chu Trần Phương Nam | 2A202602675 | Technical Research / Data Analyst |
| 3   | Đỗ Thành Đạt | 2A202602874 | Solution Architect / Documentation Writer |
| 4   | Trần Đại Nhân | 2A202602642 | AI Research Engineer / Benchmark Specialist |
| 5   | Bùi Gia Chinh | 2A202602693 | Security Analyst / Compliance Specialist |
| 6   | Nguyễn Tú Tài | 2A202602455 | Software Engineer / Research Assistant |

**Candidate problem nhóm chọn (1 câu):**

```text
Mỗi đợt pentest, tôi (intern an ninh mạng) mất 3-4 tiếng để tổng hợp và chuẩn hóa báo cáo lỗ hổng từ 4-5 thành viên team thành 1 báo cáo hoàn chỉnh gửi cho Lead và Khách hàng, vì mỗi người viết theo style khác nhau và hay thiếu field quan trọng.
```

## Phase 3 — Group Convergence: từ 9-12 candidates về 1

### 3.1. Trình bày top 3 mỗi người (mỗi candidate 1-2 phút)

| # | Người đưa ra | Candidate problem | Người gặp vấn đề | Điểm nghẽn | Cảm nhận nhanh của nhóm |
|---|---|---|---|---|---|
| 1 | Nguyễn Đức Phát | Đối chiếu CV với JD & gợi ý chỉnh sửa hồ sơ ứng tuyển | Sinh viên xin việc / thực tập | Đọc JD nhặt từ khóa & viết lại gạch đầu dòng kinh nghiệm (35/50') | Rất thiết thực, ai cũng từng gặp, metric và boundary rõ |
| 2 | Nguyễn Đức Phát | Tự động tạo câu hỏi trắc nghiệm & flashcard ôn thi từ slide PDF | Sinh viên ôn thi cuối kỳ | Ngồi gõ câu hỏi trắc nghiệm từ 80 slide lý thuyết (60/120') | Nhu cầu thật mùa thi, input PDF rõ ràng |
| 3 | Nguyễn Đức Phát | Tóm tắt video YouTube bài giảng / podcast tiếng Anh sang tiếng Việt | Người tự học công nghệ | Vừa nghe vừa bấm pause tra từ và gõ note (45/75') | Hay nhưng phụ thuộc chất lượng transcript YouTube |
| 4 | Chu Trần Phương Nam | Trích xuất & đối chiếu số liệu từ paper nghiên cứu | AI Researcher tập sự | Đọc & đối chiếu số liệu bảng benchmark phức tạp (60/120') | Bài toán chuyên sâu lab AI, giá trị học thuật cao |
| 5 | Chu Trần Phương Nam | Tự động sửa bộ bóc tách Scraper khi website bị HTML Drift | Data Engineer | Dò tìm và viết lại selector XPath/CSS thủ công (25/60') | Nỗi đau kinh điển của DE, pipeline bị gián đoạn 4-6h |
| 6 | Chu Trần Phương Nam | Chẩn đoán nguyên nhân biến động chỉ số Dashboard | Data Analyst | Viết & chạy lặp lại SQL qua 4-5 chiều dữ liệu (22/50') | Nghiêng về nghiệp vụ dữ liệu, cần domain knowledge sâu |
| 7 | Đỗ Thành Đạt | Định hướng tài liệu và thứ tự làm trong lab | Học viên lab, sinh viên thực hành | Nối vai trò từng file/folder thành thứ tự hành động (15-20') | Nỗi đau ngay trước mắt, nhưng thiên về Doc/Process fix hơn AI product |
| 8 | Đỗ Thành Đạt | Tra vị trí mặt hàng cho nhân viên siêu thị | Nhân viên bán lẻ / kho | Tìm và xác nhận vị trí sản phẩm khi khách hỏi (1.5-2'/lần) | Bối cảnh bán lẻ hay, nhưng khó tiếp cận dữ liệu layout siêu thị để test |
| 9 | Đỗ Thành Đạt | Tìm các bước trong video hướng dẫn dài | Người học nghề / thực hành quy trình | Định vị timestamp và kiểm tra bước có đủ ngữ cảnh (7/11') | Khá tương đồng bài YouTube, có thể gom chung cụm Multimedia |
| 10 | Trần Đại Nhân | Chẩn đoán thiếu code/config khi reproduce baseline paper (ReproScout) | AI Researcher / SWE | Phát hiện thiếu config / eval protocol / preprocessing giữa chừng (16h/baseline) | Rất chuyên sâu, có benchmark ReproRepo EMNLP 2026, pain thật lab AI |
| 11 | Trần Đại Nhân | Tổng hợp & validate note cuộc họp chia task | Điều phối nhóm / Trưởng dự án | Lọc meeting notes dài và gõ task vào Jira (12-16h/tuần) | Nỗi đau lặp lại của người lead, tốn nhiều thời gian |
| 12 | Trần Đại Nhân | Chẩn đoán xung đột thư viện CUDA/PyTorch và sinh script setup môi trường | AI Research Engineer | Mò lỗi traceback và thử các phiên bản PyTorch/CUDA/cuDNN tương thích (120/180') | Nỗi đau kinh điển của kỹ sư AI khi chạy code mô hình mới |
| 13 | Bùi Gia Chinh | Tổng hợp và chuẩn hóa báo cáo lỗ hổng Pentest từ 4-5 thành viên | Intern an ninh mạng tổng hợp báo cáo | Format lại từng finding do style không đồng nhất (1.5-2h/4h) | Rất thực tế, số liệu rõ, có phân tích bảo mật NDA và tool chuyên dụng |
| 14 | Bùi Gia Chinh | Tự động sinh mô tả & remediation cho từng finding pentest | Pentester | Viết mô tả kỹ thuật và remediation advice (20-30'/finding) | Tốn nhiều thời gian cá nhân (5-10h/đợt), nhưng đã có tool chuyên dụng |
| 15 | Bùi Gia Chinh | Viết Executive Summary non-technical sau đợt pentest | Người viết báo cáo pentest | Dịch ngôn ngữ kỹ thuật sang ngôn ngữ business, hay bị trắng trang (45') | Ảnh hưởng ấn tượng khách hàng nhưng tần suất ít (2 lần/tháng) |
| 16 | Nguyễn Tú Tài | Tìm và lọc paper tiếng Anh cho sinh viên NCKH | Sinh viên NCKH năm 3-4 | Đọc lướt 10-15 abstract để lọc 1-2 bài phù hợp (60/150') | Pain thật sinh viên NCKH, tốn 6-10h/tuần |
| 17 | Nguyễn Tú Tài | Dịch & hiệu đính Related Work tiếng Anh sang tiếng Việt học thuật | Nhóm sinh viên NCKH | Hiệu đính văn phong học thuật, tránh dịch máy thô (20-30'/paper) | Lặp lại giữa 4 người, tốn 6-12h/tuần cả nhóm |
| 18 | Nguyễn Tú Tài | Tự động tổng hợp báo cáo tiến độ đồ án tuần từ commit, chat, Notion | Trưởng nhóm đồ án | Gom thông tin từ 3-4 nguồn rời rạc và làm slide (60-90'/tuần) | Rất phổ biến trong làm việc nhóm, tốn 5-7h/tuần |

### 3.2. Gom trùng / cluster (gom 9-12 ý thành 3-4 cụm)

| Cluster | Candidates included | Pattern chung | Ghi chú |
|---|---|---|---|
| **A. An toàn thông tin & Báo cáo kỹ thuật** | #13, #14, #15 | Gom dữ liệu kỹ thuật từ nhiều thành viên, chuẩn hóa văn phong và xuất báo cáo tuân thủ NDA | Nhu cầu thực tế cao trong doanh nghiệp, đòi hỏi tính bảo mật và độ chính xác tuyệt đối |
| **B. Nghiên cứu Khoa học & AI Reproducibility** | #4, #10, #12, #16, #17 | Đọc hiểu tài liệu học thuật phức tạp, trích xuất benchmark, chẩn đoán code/CUDA và dịch thuật ngữ | Tính kỹ thuật cao, phục vụ trực tiếp cho lab AI và cộng đồng nghiên cứu |
| **C. Xử lý Dữ liệu & Quy trình Vận hành** | #5, #6, #11, #18 | Xử lý sự cố kỹ thuật tự động (crawler drift, biến động metric) và quản lý task/tiến độ sau họp | Giảm tải các công việc thủ công lặp lại trong quy trình của Data/SWE/Project Lead |
| **D. Hỗ trợ Học tập & Phát triển Nghề nghiệp** | #1, #2, #3, #7, #8, #9 | Tối ưu hóa hồ sơ ứng tuyển, ôn thi tài liệu học tập và tra cứu thông tin phân tán | Đối tượng học viên sinh viên năm cuối rất đồng cảm, dễ đo lường |

### 3.3. Shortlist (giữ 2-3 bài trả lời được 7 câu hỏi worksheet)

| Candidate | Vì sao vào shortlist (2-3 ý) | Rủi ro / điều chưa rõ |
|---|---|---|
| **#13: Tổng hợp và chuẩn hóa báo cáo lỗ hổng Pentest (Chinh)** | - Actor cực kỳ rõ (intern an ninh mạng làm việc hàng tuần).<br>- Workflow 6 bước thật, bottleneck chiếm 50% thời gian có log đo đạc.<br>- Metric đo lường kép: vừa đo thời gian vừa đo độ chính xác (0 sai lệch severity).<br>- Ranh giới bảo mật (NDA / Local LLM) giúp bài có chiều sâu phản biện rất tốt. | Phải đảm bảo mô hình AI chạy local hoàn toàn, không được gửi dữ liệu lỗ hổng của khách hàng lên cloud công khai. |
| **#1: Đối chiếu CV với JD & gợi ý chỉnh sửa hồ sơ (Phát)** | - Cả 6 thành viên đều là sinh viên năm cuối/intern, ai cũng gặp nỗi đau này.<br>- Workflow Before/After rõ ràng (50' -> 10'), đã có sơ đồ PNG hoàn chỉnh.<br>- Dễ dàng làm survey và phỏng vấn xác nhận ngay trong phạm vi lớp học. | Đã có một số công cụ thương mại (Jobscan), giải pháp cần tạo ra sự khác biệt cho sinh viên Việt Nam. |
| **#10: Chẩn đoán thiếu code/config khi reproduce baseline paper (Nhân)** | - Đậm chất nghiên cứu học thuật của lab AI.<br>- Có sẵn số liệu ngành (khảo sát Nature 1.576 người) và benchmark ReproRepo EMNLP 2026.<br>- So sánh Multi-agent vs Single prompt rất sâu. | Kiến trúc multi-agent khá nặng nề để xây dựng pilot thực nghiệm trong thời gian ngắn của buổi lab. |

### 3.4. Score để đồng thuận (chấm 1-5, ép nói rõ vì sao cho 5 / cho 3)

| Candidate | Actor rõ | Workflow rõ | Pain có evidence | Impact đo được | Làm trong lab | So sánh R/W/A được | Nhóm hiểu domain | Tổng |
|---|---:|---:|---:|---:|---:|---:|---:|---:|
| **#13: Báo cáo Pentest** | 5 | 5 | 5 | 5 | 4 | 5 | 4 | **33** |
| **#1: CV vs JD** | 5 | 5 | 4 | 4 | 5 | 5 | 5 | **33** |
| **#10: Reproduce Paper** | 4 | 4 | 5 | 4 | 3 | 5 | 4 | **29** |

**Candidate nhóm chọn (1 bài duy nhất):**

```text
Problem #13 — Tổng hợp và chuẩn hóa báo cáo lỗ hổng Pentest từ 4-5 thành viên thành 1 báo cáo hoàn chỉnh (Bùi Gia Chinh đưa ra).
```

**Vì sao chọn (4-5 câu):**

```text
1. Đây là bài toán thực chiến tại doanh nghiệp có bằng chứng rõ ràng nhất trong nhóm: Chinh hiện đang là intern an ninh mạng và trực tiếp chịu trận khâu tổng hợp báo cáo 2 lần/tháng.
2. Quy trình hiện tại có điểm nghẽn đo đạc cụ thể: Bước format lại văn phong từng finding ngốn 1.5 - 2 tiếng (hơn 50% thời gian) do mỗi tester viết một kiểu và hay thiếu field bắt buộc.
3. Bài toán có Success Metric cực kỳ chặt chẽ: Không chỉ đo giảm thời gian (từ 3.5h xuống <1.5h) mà còn đo chất lượng an toàn: 0 finding bị đổi sai severity, 0 finding bị bỏ sót hoặc trùng lặp.
4. Bài toán mở ra góc nhìn phản biện xuất sắc về ranh giới bảo mật thông tin (NDA / Compliance): Ép nhóm phải giải quyết bài toán AI bằng mô hình On-Premise/Local LLM thay vì ỷ lại vào Cloud AI công khai.
5. Cả nhóm 5 người đều có nền tảng CNTT/AI/Data nên nhanh chóng hiểu cấu trúc dữ liệu của báo cáo kỹ thuật và cùng đóng góp giải pháp kiến trúc được ngay.
```

**Vì sao KHÔNG chọn các candidate còn lại (mỗi bài 2-3 câu):**

```text
- Candidate #1 (CV vs JD): Rất hay và ai cũng đồng cảm, nhưng mang tính cá nhân cao (B2C), trong khi bài toán Pentest Report mang tính cộng tác nhóm và nghiệp vụ doanh nghiệp (B2B) với rủi ro và trách nhiệm giải trình cao hơn.
- Candidate #10 (Reproduce paper): Rất học thuật nhưng bài toán chẩn đoán thiếu code/config cần tích hợp quá nhiều nguồn phân tán (PDF, GitHub repo, issue threads); phạm vi quá rộng và khó triển khai pilot kiểm chứng ngay trong lab.
- Candidate #5 (Crawler HTML drift) & #6 (Dashboard anomaly): Phần lớn có thể giải quyết tốt bằng các thuật toán Rule-based / Statistical analysis truyền thống, chưa bắt buộc phải đưa Generative AI vào làm trung tâm.
```

**Disagreement (nếu có — ai lo gì, chốt ra sao):**

```text
- Ai lo gì: Bạn Nhân và bạn Đạt lo ngại rằng việc đưa dữ liệu lỗ hổng bảo mật (PoC, IP hệ thống khách hàng) vào mô hình AI sẽ vi phạm nghiêm trọng thỏa thuận bảo mật (NDA) và có nguy cơ rò rỉ thông tin nhạy cảm.
- Chốt ra sao: Nhóm đồng thuận 100% đặt ra một RÀNG BUỘC CỨNG (Hard Constraint): Hệ thống tuyệt đối KHÔNG sử dụng các API đám mây công khai (như OpenAI, Anthropic web). Thay vào đó, toàn bộ AI workflow bắt buộc phải triển khai cục bộ (Local / On-Premise LLM) sử dụng các mô hình open-weight (như Qwen 2.5 7B / Llama 3 8B) chạy qua Ollama hoặc vLLM trên máy chủ nội bộ của công ty.
```

---

## Phase 4 — Quick Validation + Research

### 4.1. Quick validation (ít nhất 1 cách: interview 2-3 người hoặc survey 5-10 người)

| Nguồn | Số người / mẫu | Tín hiệu xác nhận (kèm quote nguyên văn) | Tín hiệu phản bác | Nhóm sửa problem thế nào |
|---|---:|---|---|---|
| **Interview** | 3 người (Chinh - Intern Pentest, Đạt - Dev/Security, và 1 bạn học viên làm SecOps) | *"Mỗi lần gom bài của 4 ông là 4 font chữ, 4 kiểu hành văn khác nhau. Có ông quăng đúng 1 dòng curl với cái ảnh chụp mờ căm không ghi CVSS, mình phải tự Google viết lại remediation mất cả tối."* (Quote từ Chinh) | *"Nếu bắt anh em điền form cứng bắt buộc thì mọi người lười, chỉ muốn note nhanh khi đang exploit."* | Không bắt tester đổi thói quen; để tester nộp text thô/markdown tự do, AI sẽ làm khâu phân loại và chuẩn hóa văn phong. |
| **Survey / poll** | 6 học viên trong lab VinUni làm mảng Dev/Security | 5/6 người (83.3%) xác nhận khâu format tài liệu kỹ thuật từ nhiều người là công việc gây nản lòng nhất và mất từ 2-4 tiếng mỗi đợt phát hành. | 1 người cho rằng chỉ cần dùng Google Docs chia sẻ chung rồi tự ai nấy sửa là xong. | Làm rõ: Google Docs chung vẫn không giải quyết được việc lệch văn phong và sót trường CVSS/PoC nếu không có bước kiểm duyệt tự động. |
| **Log / ticket thật** | 3 đợt pentest gần nhất của Chinh | Bấm giờ thực tế: Đợt 1 mất 3h45, Đợt 2 mất 4h10 (bị trễ 1 ngày do sót PoC phải hỏi lại), Đợt 3 mất 3h15. Đợt 3 từng bị Lead phát hiện trùng 2 finding XSS ở cùng 1 controller do 2 tester nộp độc lập. | Không có phản bác về số liệu; thời gian trung bình thực tế là 3.7 giờ/đợt. | Đưa tiêu chí "Phát hiện finding trùng lặp" vào thành một tính năng bắt buộc của AI workflow. |

**Insight sau validation (1-2 câu — pain thật nằm ở đâu):**

```text
Pain thật không nằm ở việc dịch thuật ngữ tiếng Anh, mà nằm ở việc xử lý sự "bất đồng nhất về cấu trúc và mức độ chi tiết" giữa các thành viên, và gánh nặng rà soát thủ công để không bỏ sót các trường cốt lõi (CVSS, PoC steps, Remediation) trước khi gửi khách hàng.
```

Bằng chứng đính kèm (nếu có): `02-group-problem-statement-interview-notes.md`

### 4.2. Research giải pháp đã có (ít nhất 2-3 tools/patterns + 1-2 link kiểm được)

| Nguồn / tool / case | Link | Họ giải quyết bước nào? | Điểm mạnh | Khoảng trống / rủi ro | Bài học cho nhóm |
|---|---|---|---|---|---|
| **PlexTrac** | https://plextrac.com/ | Nền tảng quản lý báo cáo tập trung, có sẵn WriteupDB (thư viện mẫu mô tả lỗ hổng) | Chuẩn hóa quy trình doanh nghiệp, quản lý tập trung từ khâu test đến fix | Chi phí bản quyền cực đắt (hàng nghìn USD/năm); tester vẫn phải copy-paste thủ công vào từng ô form | Không cần build lại cả platform cồng kềnh; chỉ cần một công cụ xử lý file thô gọn nhẹ. |
| **Dradis Framework** | https://dradisframework.com/ | Tổng hợp báo cáo từ nhiều tool (Burp, Nessus, Nmap) vào template chung | Open-source bản community, có khả năng merge nhiều nguồn | Phải cài đặt phức tạp; văn phong mô tả thủ công vẫn bị lệch; không có AI hỗ trợ tóm tắt hay phát hiện trùng lặp ngữ nghĩa | Cần tận dụng tư duy cấu trúc hóa finding theo các trường chuẩn OWASP/CWE. |
| **PentestReportAI / PenReport** | https://github.com/topics/penetration-testing-reports | Tự động sinh mô tả lỗ hổng và khuyến nghị remediation từ tên finding | Tốc độ sinh text nhanh, chuẩn văn phong chuyên nghiệp | Đa số gọi API OpenAI công khai (vi phạm NDA khách hàng); chỉ sinh từng finding lẻ, không xử lý gom 4-5 file báo cáo con | Bắt buộc phải chạy mô hình On-premise và giải quyết bài toán "hợp nhất đa nguồn" thay vì chỉ sinh văn bản đơn thuần. |

**Research takeaway (2-3 câu — nên build gì / không build gì):**

```text
Nhóm KHÔNG build lại một hệ thống quản lý kiểm thử đồ sộ như PlexTrac hay Dradis. Nhóm sẽ tập trung xây dựng một "Micro-Workflow Pipeline" chạy On-premise: Tự động phân tích các file markdown/docx thô của thành viên, dùng Rule kiểm tra thiếu field, dùng Local LLM chuẩn hóa văn phong và phát hiện finding trùng lặp, sau đó đưa ra giao diện Review 1 màn hình cho intern duyệt.
```

---

## Phase 5 — Workflow + Problem Statement

### 5.1. Current workflow bản nhóm

File đính kèm: `02-group-problem-statement-workflow.png`

```text
CURRENT STATE — 220 phút (~3.7 tiếng)

[1. Nhận file báo cáo con từ Slack/Drive: 10'] 
→ [2. Đọc lướt từng file, kiểm tra field thiếu: 30'] 
→ [3. Nhắn tin hỏi lại thành viên nếu thiếu PoC/CVSS: 25'] 
→ [4. Copy & Format lại từng finding vào template chung: 105']  <-- BOTTLENECK (ngốn 50% thời gian)
→ [5. Sắp xếp severity, đánh số thứ tự, check trùng lặp: 30'] 
→ [6. Review tổng thể & gửi Lead/Khách hàng: 20']
```

| Bước | Actor | Input | Output | Thời gian / tần suất | Ghi chú (handoff? bottleneck?) |
|---|---|---|---|---|---|
| 1 | Intern tổng hợp | 4-5 file báo cáo con (docx/md/txt) | Thư mục chứa file thô | 10 phút (2 lần/tháng) | Nhận rải rác từ Slack, Drive |
| 2 | Intern tổng hợp | Các file báo cáo thô | Danh sách các chỗ bị thiếu thông tin | 30 phút | Đọc lướt bằng mắt, dễ hoa mắt sót field |
| 3 | Intern & Tester | Tin nhắn Slack/Zalo | Dữ liệu bổ sung từ tester | 25 phút | Chờ tester phản hồi, gây nghẽn tiến độ |
| **4** | **Intern tổng hợp** | **Dữ liệu thô phân tán** | **Các finding đã vào đúng template** | **105 phút** | **BOTTLENECK CHÍNH: Phải sửa câu từ, canh chỉnh format, viết lại remediation** |
| 5 | Intern tổng hợp | Danh sách finding đã format | Báo cáo đã sắp xếp thứ bậc | 30 phút | Dễ nhầm lẫn mức độ nghiêm trọng, sót finding trùng |
| 6 | Lead & Intern | Bản nháp báo cáo tổng | Báo cáo hoàn chỉnh gửi khách hàng | 20 phút | Handoff sang Lead duyệt lần cuối |

**Bottleneck chính (2-3 câu):**

```text
Bước 4 (Copy & Format lại từng finding) là điểm nghẽn nặng nề nhất, chiếm tới 105 phút (~48% toàn bộ thời gian). Nguyên nhân do mỗi pentester có thói quen viết khác nhau (người viết 3 dòng ngắn ngủn, người chép cả trang log), intern phải tự tay gọt giũa lại câu từ và căn chỉnh bố cục sao cho đồng nhất theo bộ nhận diện của công ty.
```

### 5.2. Future workflow bản nhóm

Phải nhìn ra 5 thứ: bước nào máy (Rule), bước nào AI, bước nào người, boundary ở đâu, fallback khi AI sai.

```text
FUTURE STATE — 55 phút (Tiết kiệm 75% thời gian)

[1. Nạp các file thô vào thư mục dự án: 2' - System] 
→ [2. Rule Engine parse & kiểm tra thiếu field CVSS/PoC: 3' - Rule/Máy] 
→ [3. Local LLM chuẩn hóa văn phong theo template & gắn cờ nghi trùng: 5' - AI Workflow] 
→ [4. Intern review bảng kiểm duyệt, xử lý cờ cảnh báo & bấm xuất file: 35' - Human Boundary] 
→ [5. Lead review nhanh & phát hành báo cáo: 10' - Human]

Fallback: Nếu Local LLM parse sai cấu trúc hoặc không nhận diện được finding lạ, hệ thống giữ nguyên text thô ban đầu và đánh dấu đỏ [Cần chỉnh sửa tay] để intern tự điền vào template.
```

**Before/after impact:**

| Metric | Trước | Sau kỳ vọng | Cách đo |
|---|---:|---:|---|
| **Tổng thời gian tổng hợp** | 220 phút (3.7 tiếng) | 55 phút (< 1 tiếng) | Bấm giờ từ lúc nhận file đến khi có bản draft hoàn chỉnh |
| **Thời gian format finding** | 105 phút | 15 phút review | Đo riêng thời gian xử lý bước chuẩn hóa nội dung |
| **Số bước thủ công lặp lại** | 5 bước thủ công | 1 bước review tập trung | Đếm số thao tác copy-paste giữa các cửa sổ |
| **Bottleneck chính** | Format tay từng câu chữ | Duyệt nhanh trên bảng phân tích diff | Khảo sát mức độ mệt mỏi của intern sau mỗi đợt nộp |
| **Risk mới** | Nguy cơ bỏ sót finding do làm tay | AI diễn đạt sai sắc thái kỹ thuật / vi phạm NDA | Đo bằng 0 lỗi severity bị đổi và 100% dữ liệu xử lý Local |

### 5.3. Problem Statement v0 (mỗi field 2-3 câu)

| Field | Nội dung |
|---|---|
| **Actor** | Bùi Gia Chinh (Intern an ninh mạng) chịu trách nhiệm tổng hợp báo cáo; người thụ hưởng kết quả trực tiếp là Team Lead kiểm duyệt và Khách hàng nhận báo cáo đánh giá an toàn. |
| **Workflow** | Cứ mỗi đợt pentest định kỳ (2 tuần/lần), người tổng hợp thu thập 4-5 file báo cáo từ các tester, kiểm tra tính đầy đủ của các trường, format lại văn phong từng finding vào template chuẩn, lọc trùng lặp và gửi Lead phê duyệt. |
| **Bottleneck** | Bước căn chỉnh format và viết lại văn phong từng lỗ hổng ngốn 105 phút trên tổng số 220 phút, do sự bất đồng nhất về cách hành văn và độ chi tiết giữa các thành viên. |
| **Impact** | Tiêu tốn 7-8 giờ công mỗi tháng của intern; nguy cơ chậm tiến độ bàn giao báo cáo cho khách hàng và tiềm ẩn sai sót nghiêm trọng nếu làm sót finding hoặc phân loại sai mức độ rủi ro. |
| **Success Metric** | Giảm thời gian tổng hợp từ 220 phút xuống dưới 60 phút/đợt; đảm bảo chất lượng tuyệt đối: 0 finding bị đổi sai severity so với bản gốc của tester, và 0 trường hợp finding bị trùng lặp lọt qua mắt Lead. |
| **Boundary** | Hệ thống chỉ hỗ trợ trích xuất, chuẩn hóa văn phong và phát hiện bất thường; hệ thống KHÔNG được tự ý thay đổi điểm số CVSS/mức độ nghiêm trọng, KHÔNG tự động gửi email cho khách hàng, và KHÔNG được gửi dữ liệu ra ngoài mạng nội bộ. |

**Câu hỏi AI phản biện v0 (nếu có):**
- Field nào mơ hồ: Field Success Metric ban đầu chỉ ghi "giảm thời gian", chưa làm rõ tiêu chí chất lượng kỹ thuật của ngành an ninh mạng.
- Tôi sửa gì: Bổ sung 2 chỉ số chất lượng cứng: "0 finding bị AI đổi sai severity" và "0 finding trùng lặp bị bỏ sót".

---

## Phase 6 — Rule / Workflow / Agent + Decision

### 6.0. Ma trận độ phù hợp (suy nghĩ nhanh, không thay quyết định cuối)

- Độ mơ hồ: **[x] Thấp (có đúng/sai rõ)** / [ ] Cao — Vì sao: Cấu trúc của một báo cáo lỗ hổng an ninh mạng đã có tiêu chuẩn quốc tế định hình rõ ràng (OWASP, CWE, thang điểm CVSS v3.1 từ 0.0 đến 10.0, các bước PoC và giải pháp khắc phục).
- Độ phức tạp: [ ] Thấp (1-2 bước) / **[x] Cao (3+ bước/nguồn, phụ thuộc nhau)** — Vì sao: Phải nhận nhiều file nguồn từ nhiều người, xử lý bóc tách text, kiểm tra thiếu trường, đối chiếu ngữ nghĩa để tìm finding trùng lặp và kết xuất ra file hoàn chỉnh.

**Bài toán nhóm nằm ở ô nào:**

```text
Ô: [Độ mơ hồ Thấp — Độ phức tạp Cao] → RẤT PHÙ HỢP VỚI MÔ HÌNH "WORKFLOW".
```

**Vì sao (2-3 câu):**

```text
Độ mơ hồ thấp nghĩa là bài toán có quy chuẩn đúng/sai rành mạch, không cần AI phải sáng tạo tùy tiện. Độ phức tạp cao đòi hỏi một chuỗi xử lý tuần tự kết hợp nhiều công cụ: dùng Code/Rule để kiểm tra định dạng và dùng LLM để chuẩn hóa văn phong.
```

### 6.1. So sánh Rule / Workflow / Agent (so trên cùng 1 bài)

| Mức | Phương án cho bài toán nhóm | Khi nào đủ | Rủi ro | Chọn? (Dùng cho bước nào?) |
|---|---|---|---|---|
| **Rule** | Dùng Regex + Script Python đọc file, kiểm tra sự tồn tại của các thẻ `# CVSS`, `# PoC`, `# Remediation` và ghép nối file | Đủ nếu tất cả tester đều tuân thủ 100% cú pháp markdown định sẵn không sai một dấu phẩy | Tester viết sai tiêu đề hoặc viết văn xuôi tự do là script bị gãy hoàn toàn; không thể phát hiện 2 finding trùng lặp nếu dùng từ khác nhau | **CHỌN MỘT PHẦN** (Dùng cho Bước 2: Kiểm tra sự tồn tại của các trường bắt buộc) |
| **Workflow** | Pipeline kết hợp: Rule kiểm tra cấu trúc $\rightarrow$ Local LLM trích xuất & chuẩn hóa văn phong $\rightarrow$ Human duyệt 1 màn hình | Đủ khi cần xử lý văn phong phi cấu trúc nhưng vẫn giữ quy trình tuần tự kiểm soát được | LLM cục bộ có thể tốn tài nguyên phần cứng hoặc dịch sai một số thuật ngữ đặc thù nếu prompt không chặt | **CHỌN LÀM GIẢI PHÁP CHÍNH** (Cân bằng hoàn hảo giữa tự động hóa và an toàn) |
| **Agent** | Cho một AI Agent tự do đọc file, tự quyết định gọi API tra cứu CVE, tự sửa lại điểm CVSS và tự gửi email cho khách hàng | Chỉ nên dùng khi cần tự động hóa hoàn toàn từ quét lỗ hổng đến bàn giao mà không cần con người | RỦI RO CỰC KỲ NGUY HIỂM: Agent có thể hallucinate đổi sai mức nghiêm trọng, rò rỉ dữ liệu hoặc gửi báo cáo chưa hoàn thiện cho khách hàng | **KHÔNG CHỌN** (Vi phạm nguyên tắc an toàn thông tin và trách nhiệm giải trình) |

**5 câu hỏi chốt (trả lời câu đầy đủ):**
1. **Rule có giải được 70-80% case không?**  
   $\rightarrow$ Không, Rule chỉ kiểm tra được file có đủ thẻ tiêu đề hay không, nhưng không thể chuẩn hóa văn phong lộn xộn hoặc nhận diện 2 lỗ hổng trùng lặp được mô tả bằng hai cách diễn đạt khác nhau.
2. **Các bước có đi thẳng một đường không hay phải rẽ nhánh?**  
   $\rightarrow$ Đi thẳng một đường tuần tự (Linear Pipeline): Nạp file $\rightarrow$ Parse cấu trúc $\rightarrow$ AI chuẩn hóa $\rightarrow$ Human duyệt $\rightarrow$ Xuất bản.
3. **Có thật sự cần Agent tự lập kế hoạch + gọi tool không?**  
   $\rightarrow$ Hoàn toàn KHÔNG, quy trình tổng hợp báo cáo đã có sẵn các bước cố định, để Agent tự lập kế hoạch chỉ làm tăng độ trễ và rủi ro sai sót.
4. **Nếu AI sai, ai phát hiện đầu tiên và sửa trong bao lâu?**  
   $\rightarrow$ Người tổng hợp (Chinh) sẽ phát hiện ngay trên giao diện Diff/Preview trong vòng 1-2 phút trước khi bấm Approve xuất file.
5. **Có hạ được từ Agent → Workflow → Rule không?**  
   $\rightarrow$ Có, nhóm đã chủ động hạ từ Agent xuống **Workflow**, trong đó tận dụng Rule tối đa ở khâu tiền xử lý (pre-processing) để giảm tải cho AI.

**Mức chọn:**

```text
[WORKFLOW] — Kết hợp Rule-based Validation và Local LLM Normalization với Human-in-the-loop.
```

**Vì sao chọn (3-4 câu):**

```text
Workflow là điểm cân bằng tối ưu giữa tính linh hoạt của AI và sự an toàn của hệ thống. Nó cho phép xử lý ngôn ngữ tự nhiên không đồng nhất của các tester mà vẫn giữ con người ở vị trí kiểm soát cao nhất (Human boundary). Kiến trúc đường ống (pipeline) cố định giúp dễ dàng kiểm thử, dễ debug và đảm bảo tính nhất quán tuyệt đối của báo cáo.
```

**Vì sao không chọn mức đơn giản hơn (2-3 câu):**

```text
Nếu chỉ dùng Rule thuần túy, nhóm sẽ không giải quyết được cái gốc của điểm nghẽn: tester vẫn sẽ nộp bài với văn phong khác nhau và intern vẫn phải tốn hàng tiếng đồng hồ để viết lại từng câu chữ mô tả. AI là bắt buộc để "dịch" các đoạn ghi chép thô thành văn phong báo cáo chuyên nghiệp.
```

### 6.2. Problem Statement v1 (v0 sửa chặt hơn + 3 field cuối)

| Field | Nội dung |
|---|---|
| **Actor** | Bùi Gia Chinh (Intern an ninh mạng phụ trách tổng hợp); Team Lead và Khách hàng doanh nghiệp nhận báo cáo cuối cùng. |
| **Workflow** | Thu thập các file báo cáo con từ 4-5 tester $\rightarrow$ Kiểm tra các trường kỹ thuật bắt buộc $\rightarrow$ Chuẩn hóa văn phong finding theo chuẩn doanh nghiệp $\rightarrow$ Phát hiện trùng lặp $\rightarrow$ Xuất báo cáo pentest hoàn chỉnh. |
| **Bottleneck** | Khâu căn chỉnh format và viết lại văn phong finding chiếm 105 phút do văn phong không đồng nhất và hay thiếu trường dữ liệu. |
| **Impact** | Tiêu tốn 7-8 tiếng/tháng; nguy cơ trễ deadline giao nộp và rủi ro sai sót chuyên môn ảnh hưởng uy tín công ty. |
| **Success Metric** | - Thời gian tổng hợp giảm từ 220 phút xuống dưới 60 phút/đợt.<br>- Tỷ lệ chính xác severity: 100% (0 finding bị đổi sai mức nghiêm trọng).<br>- Tỷ lệ phát hiện trùng lặp: Đạt $\ge 90\%$ các trường hợp finding trùng scope/vulnerability type. |
| **Boundary** (làm / không làm) | **LÀM:** Parse file thô, chuẩn hóa định dạng văn bản, gợi ý remediation chuẩn theo CWE, gắn cờ cảnh báo thiếu sót / trùng lặp.<br>**KHÔNG LÀM:** Không tự ý thay đổi điểm CVSS/Severity, không tự động gửi báo cáo ra ngoài khi chưa có người duyệt, không kết nối internet công khai. |
| **AI intervention point** | Can thiệp ngay sau bước Rule Parse dữ liệu thô (Bước 2) và trước bước Người kiểm duyệt cuối cùng (Bước 4). |
| **Mức chọn** | **WORKFLOW** — Vì các bước xử lý đi theo một luồng tuyến tính xác định; AI đóng vai trò như một bộ chuyển đổi văn phong và gợi ý ngữ nghĩa dưới sự giám sát chặt chẽ của con người. |
| **Rủi ro & người thật kiểm tra** | **Rủi ro lớn nhất:** Dữ liệu bảo mật khách hàng bị rò rỉ (vi phạm NDA) hoặc AI tự bịa thông tin kỹ thuật sai lệch.<br>**Cách kiểm tra:** Bắt buộc chạy Local LLM trên hạ tầng mạng nội bộ cách ly; Intern đối chiếu trực tiếp bản gốc và bản gợi ý trên giao diện Split-Screen trước khi xuất báo cáo. |

### 6.3. Final decision

| Câu hỏi | Yes / Not Yet / No | Ghi chú (câu đầy đủ) |
|---|---|---|
| Actor + workflow rõ chưa? | **Yes** | Actor là intern an ninh mạng với quy trình 6 bước được bấm giờ thực tế qua 3 đợt pentest. |
| Baseline + metric đo được chưa? | **Yes** | Baseline rõ ràng: 220 phút/đợt $\rightarrow$ Mục tiêu: $<60$ phút/đợt; đo lường thêm bằng 0 lỗi severity. |
| Data/input đủ dùng chưa? | **Yes** | Có sẵn các file báo cáo thô từ các đợt pentest trước đây của Chinh để làm tập test mẫu. |
| AI sai, hậu quả chấp nhận được không? | **Yes** | Chấp nhận được vì AI chỉ đóng vai trò gợi ý bản nháp, con người duyệt 100% trước khi phát hành. |
| Có người review/owner không? | **Yes** | Chinh là người chịu trách nhiệm review trực tiếp (Owner), Team Lead là người duyệt cấp 2. |
| Có cách non-AI đơn giản hơn không? | **Yes (nhưng không đủ)** | Template và Rule script đã được xem xét nhưng chỉ giải quyết được việc kiểm tra thẻ, không chuẩn hóa được văn phong tự do. |

**Decision:**

```text
[GO] — Tiến hành xây dựng giải pháp AI Workflow với điều kiện tiên quyết: Chạy 100% Local / On-Premise.
```

**Lý do (3-4 câu dựa trên bằng chứng):**

```text
1. Vấn đề có thật, lặp lại đều đặn và gây lãng phí 7-8 giờ công mỗi tháng của nhân sự trong team.
2. Workflow phân định rõ ràng giữa tự động hóa (Rule + Local LLM) và trách nhiệm con người (Human boundary), loại bỏ triệt để rủi ro ảo giác.
3. Rào cản lớn nhất về tính bảo mật (NDA) đã được giải quyết thấu đáo bằng phương án kỹ thuật triển khai Local LLM trên máy chủ nội bộ.
4. Nhóm có sẵn dữ liệu thực tế và nhân sự có chuyên môn để kiểm thử đánh giá ngay lập tức.
```

**Nếu Go — pilot nhỏ nhất (data nào, chạy tay ra sao, đo 3 số nào):**

```text
- Data pilot: Sử dụng dữ liệu ẩn danh (anonymized) của 10 finding thô từ đợt pentest tháng trước.
- Cách chạy: Chạy script parse + đưa qua mô hình Local LLM (Llama 3 8B / Qwen 2.5 7B chạy bằng Ollama trên máy tính cá nhân có GPU).
- Đo 3 số cụ thể:
  1. Thời gian xử lý: Toàn bộ quá trình từ nạp file đến khi ra bản draft mất dưới 5 phút.
  2. Tỷ lệ phát hiện trường thiếu: Đạt 100% (cảnh báo đúng các finding thiếu PoC hoặc CVSS).
  3. Độ chính xác văn phong: Tỷ lệ câu chữ được intern giữ lại sử dụng mà không phải viết lại từ đầu đạt >= 80%.
```

**Nếu Not Yet — cần validate gì trước:**

```text
(Không áp dụng vì nhóm chọn GO. Nếu có, cần kiểm tra cấu hình phần cứng tối thiểu để chạy mượt mà Local LLM 7B/8B trong mạng nội bộ công ty).
```

**Nếu No-Go — làm gì thay AI:**

```text
(Không áp dụng vì nhóm chọn GO. Phương án dự phòng nếu không dùng AI là áp dụng chính sách phạt/thưởng để bắt buộc tester điền form mẫu nghiêm ngặt).
```

**Exit / rollback (khi nào dừng AI, quay về cách cũ):**

```text
Dừng sử dụng AI và quay về quy trình thủ công nếu xảy ra 1 trong 2 trường hợp:
1. Mô hình Local LLM xảy ra hiện tượng hallucination làm biến đổi sai lệch thông tin kỹ thuật của PoC quá 15% số finding được test.
2. Công ty ban hành chính sách nghiêm cấm hoàn toàn việc sử dụng bất kỳ công cụ LLM nào (kể cả Local LLM) trong việc xử lý báo cáo kiểm thử.
```

---

### Self-check nộp phần 02 (nhóm)
- [x] Có nhật ký hội tụ 9-14 → 1 (cluster + shortlist + score đầy đủ lý do).
- [x] Có validation (quote phỏng vấn thật, poll lớp học, log 3 đợt pentest) + research (PlexTrac, Dradis, link kiểm chứng).
- [x] Có workflow trước/sau đầy đủ thời gian, handoff, bottleneck, human boundary, fallback.
- [x] Có Problem Statement v0 → v1, metric có trước/sau + cách đo, boundary làm/không làm cụ thể.
- [x] Có so sánh chi tiết Rule / Workflow / Agent và quyết định GO dựa trên bằng chứng kỹ thuật.
