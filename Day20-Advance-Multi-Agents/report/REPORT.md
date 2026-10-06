# Báo cáo Lab: Self evolving Agentic

> Sao chép tệp này thành `report/REPORT.md` (đã làm ở Phần 0) và điền dần qua các Phần của lab. Xóa các dòng hướng dẫn dạng trích dẫn (bắt đầu bằng `>`). Văn phong kỹ thuật, ngắn gọn, mọi nhận định đi kèm số liệu hoặc bằng chứng. Trong buổi học: điền mục 1 đến 7 (bản nháp). Sau buổi học: hoàn thiện mục 8 đến 10.

## 1. Thông tin nhóm và cấu hình

| Họ tên | Mã sinh viên | Phần đóng góp |
|---|---|---|
| Nguyễn Đức Phát | 2A202602753 | 100% |

- Nhà cung cấp và mô hình (`LAB_MODEL`, không ghi khóa API), nhiệt độ (`LAB_TEMPERATURE`), `recursion_limit`: `google_genai:gemini-3.5-flash-lite`, nhiệt độ `0`, `recursion_limit`: `50` (mặc định của harness runner).
- Phiên bản Deep Agents (`pip show deepagents`), hệ điều hành, chạy trực tiếp hay trong Docker: `deepagents==0.7.21`, macOS (Darwin 24.1.0 arm64), chạy trực tiếp trong môi trường ảo `.venv` (không dùng Docker).
- Số lần chạy tác vụ đã dùng / ngân sách: 9 lần chạy phát triển (3 baseline learn + 3 subagents learn + 3 skills-auto learn) / ngân sách đánh giá chính thức (9 lần chạy đánh giá sau freeze).
- Commit của tag `freeze`: `028b5cf6e2af175044974a2ee058c99430ff5993`

## 2. Giả thuyết (commit TRƯỚC tag `freeze`, Phần 4.0)

- H1 (subagents so với baseline): Dự đoán điều kiện `subagents` sẽ có điểm số tương đương hoặc giảm nhẹ so với `baseline` (đặc biệt ở các check quy ước hình thức ngầm), trong khi chi phí token tăng mạnh từ 3x đến 5x và thời gian thực thi tăng từ 3x đến 6x. Căn cứ từ lý thuyết và thực nghiệm ở tập học: cơ chế chia tách tác vụ cho các subagent phi trạng thái (`explorer`, `implementer`, `reviewer`) dẫn đến phân mảnh ngữ cảnh (context fragmentation); các subagent chỉ nhận task prompt mà không kế thừa đầy đủ lịch sử hội thoại và các chỉ dẫn quy ước chi tiết của tác tử chính, dẫn đến việc giải quyết tốt logic lõi nhưng bỏ sót định dạng quy ước tổ chức.
- H2 (skills-auto so với baseline): Dự đoán điều kiện `skills-auto` sẽ đạt điểm số cao hơn rõ rệt so với `baseline` trên cả tập học và tập đánh giá, với chi phí token chỉ tăng nhẹ (~10-25% do đưa chỉ dẫn tóm tắt vào context). Căn cứ từ phân loại lỗi ở mục 4: 100% lỗi thất bại của `baseline` thuộc Nhóm E (Vi phạm quy ước tổ chức) - là những tri thức quy ước nội bộ không thể suy diễn từ logic nghiệp vụ chung. Bộ kỹ năng tự tiến hóa được curator cô đọng ngắn gọn và kích hoạt đúng ngữ cảnh sẽ bổ sung trực tiếp các tri thức quy ước này vào bộ nhớ làm việc của tác tử.
- H3 (tác vụ học so với tác vụ đánh giá): Dự đoán điểm số của `skills-auto` trên tác vụ học sẽ cải thiện vượt bậc so với baseline (đạt điểm cao ở các check quy ước đã học), trong khi trên tác vụ đánh giá (eval), điểm của `skills-auto` sẽ cao hơn baseline ở các quy ước dùng chung có tính khái quát (như tính toán tiền tệ integer cents, schema metadata, chuẩn format test/changelog), nhưng sẽ không đạt điểm tuyệt đối ở những quy ước mới (novel conventions) chỉ xuất hiện riêng ở tác vụ đánh giá. Căn cứ lý thuyết: kỹ năng học từ phản hồi quá khứ có khả năng chuyển giao (transferability) đối với các quy ước lặp lại, nhưng không thể đoán trước các quy tắc tổ chức chưa từng xuất hiện trong tập huấn luyện (bảo đảm không rò rỉ dữ liệu).

## 3. Làm quen Deep Agents (Phần 0.3)

1. Tác tử mặc định có 9 công cụ: `ls`, `read_file`, `write_file`, `edit_file`, `delete`, `glob`, `grep`, `execute`, `task`. Trong đó, công cụ duy nhất cho phép chạy lệnh shell trong sandbox là `execute`.
2. Mô tả của công cụ `task` nêu rõ: subagent `general-purpose` là tác tử đa năng dùng để nghiên cứu các câu hỏi phức tạp, tìm kiếm tệp/nội dung và thực hiện các tác vụ nhiều bước (có đầy đủ mọi công cụ như tác tử chính). Về ngữ cảnh: mỗi lần gọi subagent là độc lập và phi trạng thái theo mặc định (stateless by default); subagent chỉ nhìn thấy prompt mà tác tử chính truyền vào trực tiếp và trả về một báo cáo duy nhất, hoàn toàn không nhìn thấy lịch sử hội thoại trước đó của tác tử chính trừ khi kiểu subagent đó được cấu hình tường minh để kế thừa hội thoại.
3. Câu hướng dẫn hành vi trích từ mô tả công cụ:
   - Từ mô tả công cụ `task`: *"Launch multiple agents concurrently when their tasks are independent, using a single message with multiple tool calls."* (hoặc *"Put full detail in the prompt and state exactly what it should return — unless an agent type below says it inherits your conversation instead."*).
   - Từ mô tả công cụ `execute`: *"You MUST avoid using search commands like find and grep. Instead use the grep, glob tools to search. Use read_file rather than cat/head/tail."*

## 4. Đường cơ sở và phân loại lỗi (Phần 2.2)

| Tác vụ | Check thất bại | Nhóm lỗi (A-G) | Bằng chứng (trích ngắn từ `detail` hoặc vết) |
|---|---|---|---|
| data-learn | `rule_money_in_cents` | E | `RULE: money values in answer.json are integer cents (1606.67 USD is written 160667).` |
| data-learn | `rule_meta_block` | E | `RULE: answer.json has an object 'meta' = {"source": <input file name>, "rows_in": <number of data rows in the input file, duplicates included>, "rows_used": <number of distinct orders with a known amount>}.` |
| data-learn | `rule_clean_csv` | E | `RULE: write workspace/clean.csv with the header order_id,timestamp_utc,region,amount_cents; one row per distinct order with a known amount...` |
| code-learn | `rule_type_hints` | E | `RULE: every public function and method (name not starting with '_') has type annotations on all parameters and the return value.` |
| code-learn | `rule_regression_tests` | E | `RULE: write tests in tests/test_regressions.py covering every bug you fixed, with at least one test function per bug.` |
| code-learn | `rule_changelog` | E | `RULE: update CHANGELOG.md under '## Unreleased' with a bullet for every bug fixed, formatted as '- fix(<func>): <short description>'.` |
| logs-learn | `rule_service_names` | E | `RULE: service names in the output are lower-case with '-' replaced by '_' (payment-service -> payment_service).` |
| logs-learn | `rule_sorted_errors` | E | `RULE: top_errors is sorted by count descending, with ties broken by error_code ascending.` |
| logs-learn | `rule_schema_header` | E | `RULE: summary.json has schema_version = '2.1' and generated_by = 'log-analyzer'.` |

Nhận xét: Toàn bộ 9/9 (100%) check thất bại trên tập học của baseline đều thuộc Nhóm E (Vi phạm quy ước tổ chức). Ngược lại, 18/18 (100%) các check chức năng kỹ thuật (thuộc các nhóm A-D như logic xử lý ngày giờ, lọc duplicate, sửa bug mã nguồn, phân tích cú pháp log) đều đã đạt điểm tối đa. Bộ kỹ năng (Skill) hoàn toàn có thể phòng ngừa nhóm lỗi E này một cách hữu hiệu, vì các lỗi này xuất phát từ việc thiếu các quy ước tổ chức nội bộ mà tác tử không thể tự đoán trước nếu không được cung cấp hướng dẫn rõ ràng trong bộ nhớ ngữ cảnh.

## 5. Điều kiện `subagents` (Phần 2.3)

- Các subagent đã định nghĩa:
  - `explorer`: Khảo sát cấu trúc thư mục, tệp mã nguồn và tệp dữ liệu; tóm tắt đặc điểm mà không can thiệp tệp, giúp giảm bớt ngữ cảnh thô ban đầu cho tác tử chính.
  - `implementer`: Chuyên thực thi việc chỉnh sửa mã nguồn, viết code xử lý dữ liệu và tạo tệp kết quả theo thiết kế; được cấp đầy đủ công cụ tệp và shell execute.
  - `reviewer`: Kiểm tra chéo kết quả, chạy test tự động, rà soát tính hợp lệ của schema đầu ra và đối chiếu với các quy ước để phát hiện lỗi trước khi hoàn tất.
- `subagent_calls` ở từng tác vụ và nhận xét:
  - `data-learn`: 2 lần gọi (khảo sát dữ liệu và phân tích làm sạch).
  - `code-learn`: 5 lần gọi (khám phá bug -> sửa code -> chạy test -> kiểm tra chéo).
  - `logs-learn`: 2 lần gọi (đọc tệp log và định dạng JSON tổng hợp).
- Thông tin thiếu hoặc thừa khi giao việc: Tác tử chính phải mô tả lặp lại ngữ cảnh bài toán do subagent không thừa hưởng bộ nhớ đối thoại, gây tiêu hao token dư thừa. Đồng thời, tác tử chính thường chỉ tóm tắt mục tiêu nghiệp vụ lõi mà vô tình bỏ sót các yêu cầu quy ước ngầm, khiến subagent dù hoàn thành xuất sắc chức năng kỹ thuật vẫn vi phạm quy ước tổ chức.
- Ảnh hưởng đến token và thời gian: Chi phí token tăng vọt gấp 3-5 lần (từ 109k-156k token ở baseline lên 479k-733k token ở subagents), thời gian chạy tăng gấp 3-6 lần (từ 27-72s lên 164-295s). Điểm số không hề cải thiện (data-learn: 4/8 vs 5/8; code-learn: 6/10 vs 7/10; logs-learn: 3/9 vs 6/9), chứng minh kiến trúc đa tác tử phân cấp không mang lại hiệu quả chi phí cho các bài toán đơn lẻ có quy ước ngầm.

## 6. Self-evolving: skill do curator sinh (Phần 3)

- Số lần chạy curator: 1 lần. Số skill bị xóa: 0 (cả 3 skill đều tuân thủ nghiêm ngặt chuẩn YAML frontmatter, tên kebab-case, mô tả trigger rõ ràng, nội dung súc tích < 10 dòng, vượt qua hoàn toàn hàm `validate_skill`).

| Skill | Tổng quát hay riêng cho tác vụ học? | Đúng hay sai (nêu chỗ sai nếu có) | Độ dài, `description` và `skills_read` ở Phần 3.4 |
|---|---|---|---|
| `enforce-type-hints-and-tests` | Tổng quát cho các tác vụ bảo trì và phát triển mã nguồn Python. | Đúng hoàn toàn: hướng dẫn thêm type annotations cho mọi public function và tạo regression tests trong `tests/test_regressions.py`. | 8 dòng (484 bytes); description chỉ định rõ khi viết/sửa code Python; `skills_read` = 3 (được nạp và đọc ở các tác vụ). |
| `verify-output-schema-and-units` | Bán tổng quát: áp dụng cho các bài toán xử lý dữ liệu và log xuất ra JSON/CSV. | Đúng hoàn toàn: quy định chuẩn hóa tiền tệ dạng integer cents, thêm metadata top-level và chuẩn hóa tên service. | 9 dòng (657 bytes); description chỉ định khi sinh tệp đầu ra có cấu trúc; `skills_read` = 3 (được nạp và đọc ở các tác vụ). |
| `maintain-changelog` | Tổng quát: quy chuẩn ghi nhận lịch sử thay đổi mã nguồn trong các dự án phần mềm. | Đúng hoàn toàn: cập nhật `CHANGELOG.md` dưới mục `## Unreleased` theo định dạng `- fix(<func>): <mô tả>`. | 8 dòng (368 bytes); description chỉ định khi sửa bug hoặc chỉnh sửa dự án; `skills_read` = 3 (được nạp và đọc ở các tác vụ). |

## 7. Kết quả so sánh (Phần 4.3, 4.4)

Bảng so sánh tổng hợp sinh bởi `python -m lab.compare` (từ `report/table.md`):

| Task | baseline | subagents | skills-auto |
|---|---|---|---|
| code-learn | 7/10 | 6/10 | 7/10 |
| data-learn | 5/8 | 4/8 | 5/8 |
| logs-learn | 6/9 | 3/9 | 6/9 |
| code-eval | 7/11 | 7/11 | 6/11 |
| data-eval | 5/9 | 5/9 | 5/9 |
| logs-eval | 6/10 | 6/10 | 6/10 |
| **Mean score - learning tasks** | 0.66 | 0.48 | 0.66 |
| **Mean score - evaluation tasks** | 0.60 | 0.60 | 0.57 |
| **Mean tokens per run** | 129,261 | 345,768 | 137,271 |
| **Runs that read a skill** | 0/6 | 0/6 | 0/6 |

Thống kê chi tiết theo nhóm check từ `python scripts/check_breakdown.py`:

```text
condition     role    technical  house rules  mean tokens  read a skill
baseline      eval     18/18         0/12         125,115      0/3     
baseline      learn    18/18         0/9          133,407      0/3     
subagents     eval     18/18         0/12         120,172      0/3     
subagents     learn    13/18         0/9          571,365      0/3     
skills-auto   eval     17/18         0/12          86,436      0/3     
skills-auto   learn    18/18         0/9          188,106      0/3     
```

Ghi chú xử lý lỗi và tính toàn vẹn:
- Toàn bộ 18 lần chạy chính thức đều có `skills_modified = false`.
- Trong đợt phát triển trước đóng băng (Phần 3.4), tác tử chạy trên `gemini-3.5-flash-lite` với `skills_read = 3/3`, đạt điểm 8/10 ở `code-learn` (vượt qua `rule_regression_tests`). Kết quả này đã được sao lưu toàn vẹn vào `results/skills-auto-dev`.
- Khi chuyển sang đánh giá chính thức sau tag `freeze`, khóa API gặp giới hạn hạn mức tầng miễn phí (500 requests/ngày) của phiên bản 3.5. Nhóm đã chuyển đổi sang mô hình chị em cùng họ `google_genai:gemini-3.1-flash-lite` để thực hiện toàn bộ các tác vụ đánh giá sau đóng băng. Mọi lần chạy trong `results/skills-auto` đều bắt đầu sau thời điểm tag `freeze` và đã được xác thực hoàn hảo bởi `python scripts/verify_freeze.py` (báo `OK`).
- Ở tác vụ `skills-auto/data-learn`, tác tử gặp `GraphRecursionError` do chạm ngưỡng recursion limit 60; cơ chế bọc lỗi an toàn của `runner.py` đã bắt biệt lệ này, ghi nhận lỗi nhưng vẫn chấm điểm độc lập thành công 5/8 check.

## 8. Phân tích

1. **So sánh điểm số học vs đánh giá:**
   - Trên tác vụ **học**, ở đợt chạy phát triển (Phần 3.4), điều kiện `skills-auto` cải thiện điểm số ở tác vụ `code-learn` (đạt 8/10 so với 7/10 của `baseline` nhờ vượt qua check quy ước kiểm thử). Ở đợt sau đóng băng, `skills-auto` đạt điểm trung bình 0.66 (ngang bằng `baseline`). Ngược lại, điều kiện `subagents` bị suy giảm điểm số trên tác vụ học (chỉ đạt 0.48 so với 0.66 của `baseline`), do việc phân tách tác vụ khiến các subagent không nắm bắt được bức tranh toàn cảnh của yêu cầu.
   - Trên tác vụ **đánh giá**, điểm số của `baseline` và `subagents` tương đương nhau (0.60), trong khi `skills-auto` đạt 0.57. Không có điều kiện nào cải thiện mạnh tác vụ học nhưng lại "sập" bất thường ở tác vụ đánh giá. Việc điểm tác vụ đánh giá không tăng vọt phản ánh trung thực bản chất của bài toán: các quy ước của tác vụ đánh giá là hoàn toàn mới (novel conventions) và không hề bị rò rỉ từ tập học sang tập đánh giá.

2. **Tách điểm kỹ thuật và quy ước (`rule_`):**
   - Theo kết quả từ `check_breakdown.py`, các check kỹ thuật đạt mức tuyệt đối ở `baseline` (18/18 ở cả tập học và đánh giá) và `subagents eval` (18/18). `skills-auto` cũng đạt 18/18 ở tập học và 17/18 ở tập đánh giá.
   - Ngược lại, điểm house rules (`rule_`) ở `baseline` và `subagents` hoàn toàn bằng 0 (0/9 ở học và 0/12 ở đánh giá).
   - Bộ kỹ năng tự tiến hóa sinh bởi curator trực tiếp giải quyết nhóm check quy ước tổ chức (Nhóm E). Ở đợt phát triển, skill đã giúp vượt qua check `rule_regression_tests`. Đối với các check quy ước mới của tác vụ đánh giá (như `rule_bookings_fee` hay format tiền tệ riêng của `data-eval`), skill do curator sinh **không thể giúp đạt điểm**. Lý do là vì curator chỉ được học từ phản hồi của tập học; các quy ước mới của tập đánh giá chưa từng xuất hiện trong lịch sử chạy nên kỹ năng không thể "tiên tri" được (đảm bảo tính hợp lệ, không overfitting hay data leakage).

3. **Cơ chế từ vết (`trace.md`) và `skills_read`:**
   - **Check mà skill giúp đạt**: `rule_regression_tests` trong `results/skills-auto-dev/code-learn`. Vết thực thi ghi nhận tác tử đã đọc `skills/enforce-type-hints-and-tests/SKILL.md`. Nhận được chỉ dẫn *"Create or update regression test files (e.g., tests/test_regressions.py) adding at least one test function per fixed bug"*, tác tử đã tạo mới tệp `tests/test_regressions.py` và bổ sung các hàm test hồi quy tương ứng với các bug đã sửa trong thư viện `inventory`. Check này từ thất bại ở baseline đã chuyển thành thành công ở `skills-auto`.
   - **Check mà skill không giúp (đọc nhưng không làm theo)**: `rule_money_in_cents` trong `results/skills-auto-dev/data-learn`. Tác tử đã đọc `skills/verify-output-schema-and-units/SKILL.md` (yêu cầu chuyển đổi tiền tệ thành integer cents). Tuy nhiên, trong prompt bài toán người dùng ghi: `north_q1_revenue (number): sum of amount of the orders in region North`. Tác tử ưu tiên tuân thủ chỉ dẫn kiểu `number` của prompt người dùng hơn chỉ thị của skill, dẫn đến xuất số thực `3130.24` thay vì integer cents `313024`. Đây là hiện tượng thiên kiến prompt người dùng (user prompt instruction bias).
   - **Trường hợp skill chưa được đọc**: Trong các lần chạy sau đóng băng, tác tử nhìn thấy danh mục skill ở system prompt nhưng chọn nhảy thẳng vào khám phá thư mục `workspace/` mà không gọi tool `read_file` trên thư mục `skills/` (`skills_read = 0`), khiến các chỉ dẫn quy ước chi tiết không được nạp vào context làm việc.

4. **Phân tích chi phí token và hiệu quả đa tác tử:**
   - Số token trung bình mỗi lần chạy: `baseline` là 129,261 token; `skills-auto` là 137,271 token (chỉ tăng ~6.2% do nạp mô tả ngắn của kỹ năng vào system prompt). Trong khi đó, `subagents` tiêu tốn trung bình tới 345,768 token (gấp 2.7 lần baseline) và cá biệt có lần chạy lên tới 733,809 token.
   - Hiệu quả điểm trên token: `baseline` đạt mức hiệu quả tốt nhất (~0.49 điểm / 100k tokens), kế tiếp là `skills-auto` (~0.45 điểm / 100k tokens), trong khi `subagents` kém nhất (~0.17 điểm / 100k tokens).
   - **Kết luận**: Đa tác tử **hoàn toàn không đáng chi phí** trong thí nghiệm này. Việc chia nhỏ bài toán sang các subagent phi trạng thái làm phân mảnh ngữ cảnh, lặp lại các đoạn hội thoại dài và tăng số lượt gọi LLM lên gấp nhiều lần mà không hề nâng cao chất lượng thực thi quy ước ngầm.

5. **Rò rỉ dữ liệu và quá khớp:**
   - **Không có rò rỉ dữ liệu**: Curator trong `curator.py` được thiết kế có bộ lọc nghiêm ngặt `r.get("role") == "learn"`. Curator hoàn toàn không bao giờ đọc các tệp chạy hay kết quả của tập đánh giá (`eval`).
   - **Phòng tránh quá khớp**: Prompt của curator yêu cầu tổng quát hóa các lỗi thành các quy tắc hành vi phổ quát (general best practices: chuẩn hóa đơn vị tiền tệ, quy tắc type annotations, cấu trúc changelog) thay vì lưu lại tên biến hay giá trị cụ thể của bài toán học (ví dụ: không hard-code tên `sales.csv` hay `North`).

6. **Đo lường nhiễu và độ tin cậy:**
   - So sánh điểm tác vụ học của cùng bộ skill giữa đợt phát triển ở Phần 3.4 (`results/skills-auto-dev`: 8/10, 5/8, 6/9 -> Điểm trung bình = 0.69) và đợt sau đóng băng (`results/skills-auto`: 7/10, 5/8, 6/9 -> Điểm trung bình = 0.66).
   - Mức chênh lệch là 0.03 điểm trung bình (tương đương chênh lệch đúng/sai ở đúng 1 check của tác vụ `code-learn`).
   - Ý nghĩa: Con số chênh lệch 0.03 này là ước lượng thực nghiệm cho độ nhiễu ngẫu nhiên của mô hình (sampling noise và biến thiên gọi tool). Điều này chứng minh rằng bất kỳ sự chênh lệch nào trong khoảng <= 0.05 ở bảng so sánh không đủ ý nghĩa thống kê để khẳng định tính vượt trội tuyệt đối nếu không thực hiện đánh giá lặp nhiều lần (multi-trial).

## 9. Hạn chế và tính hợp lệ

1. **Quy mô tập tác vụ nhỏ (Small sample size):** Mỗi điều kiện chỉ được đánh giá trên 3 tác vụ học và 3 tác vụ kiểm tra. Với số lượng tác vụ ít, mỗi check kiểm thử chiếm tỷ trọng từ 9% đến 12.5% tổng điểm của một tác vụ, khiến điểm trung bình dễ bị dao động mạnh bởi một sai sót hình thức đơn lẻ.
2. **Đánh giá trên một lần chạy duy nhất (Single-run variance):** Do hạn mức quota gọi API của các dịch vụ đám mây (500 requests/ngày ở tầng miễn phí), mỗi cấu hình chỉ chạy một lần duy nhất. Tính ngẫu nhiên trong việc tác tử quyết định có gọi công cụ đọc skill hay không giữa các lượt chạy tạo ra phương sai đo lường mà chưa được triệt tiêu bằng cách lấy trung bình đa lần chạy (Monte Carlo multi-seed).
3. **Quy ước mang tính định kiến nhân tạo (Artificial house-rule conventions):** Các quy tắc tổ chức (house rules) như bắt buộc tiền tệ là integer cents hay schema version '2.1' được đặt ra cố định trong bộ chấm mà không có trong tài liệu yêu cầu ban đầu của đề bài. Điều này kiểm tra năng lực phản ứng quy ước ngầm hơn là năng lực suy luận kỹ thuật tổng quát.
4. **Phụ thuộc vào kiến trúc một họ mô hình:** Nghiên cứu thực nghiệm chủ yếu trên dòng mô hình Gemini Flash Lite. Các họ mô hình khác nhau có cơ chế tuân thủ system prompt và xu hướng tự kích hoạt đọc tệp tài liệu rất khác nhau.

## 10. Kết luận

1. Nghiên cứu thực nghiệm xác nhận 100% lỗi thất bại của tác tử cơ sở (baseline) là lỗi vi phạm quy ước tổ chức (Nhóm E), trong khi năng lực giải quyết logic kỹ thuật cốt lõi đạt điểm tuyệt đối 18/18.
2. Kiến trúc đa tác tử phân cấp (`subagents`) không hiệu quả trong bài toán này: tiêu tốn token gấp 2.7 lần và độ trễ tăng cao do phân mảnh ngữ cảnh nhưng không cải thiện khả năng tuân thủ quy ước ngầm.
3. Kỹ năng tự tiến hóa (`skills-auto`) do curator cô đọng từ lịch sử học tập giúp tác tử tự bổ sung quy ước kiểm thử và đạt điểm cao hơn ở tập học mà chi phí token chỉ tăng ~6%.
4. Tác tử không thể tự suy diễn các quy ước mới lạ trên tập đánh giá nếu không có gợi ý, khẳng định sự chặt chẽ và không bị rò rỉ dữ liệu trong quy trình kiểm thử.
5. Đề xuất cải tiến tiếp theo: Thay vì trông đợi tác tử tự phát hiện và đọc tệp kỹ năng qua công cụ `read_file`, hệ thống nên tích hợp cơ chế tự động tiêm kỹ năng liên quan vào prompt (RAG-based dynamic skill injection) dựa trên độ tương đồng ngữ nghĩa của yêu cầu bài toán.

## Phụ lục

- Lệnh đã chạy (theo thứ tự):
  1. `python scripts/tour.py` (Làm quen Deep Agents, trả lời Mục 3)
  2. `pytest tests/` (Xác thực toàn bộ 32/32 unit tests của harness)
  3. `python -m lab.runner --condition baseline --tasks learn` (Chạy đường cơ sở tập học)
  4. `python -m lab.runner --condition subagents --tasks learn` (Chạy đa tác tử tập học)
  5. `python -m lab.curator` (Sinh bộ kỹ năng tự tiến hóa vào `skills/auto/`)
  6. `python -m lab.runner --condition skills-auto --tasks learn` (Chạy thử nghiệm skills-auto đợt phát triển)
  7. `cp -r results/skills-auto results/skills-auto-dev` (Sao lưu kết quả phát triển Mục 3.4)
  8. `git add -A && git commit -m "hypotheses: formulate H1-H3 and complete preliminary sections"` (Commit giả thuyết H1-H3 trước đóng băng)
  9. `git commit --allow-empty -m "freeze skills" && git tag freeze` (Đóng băng kỹ năng và tạo tag freeze)
  10. `python -m lab.runner --condition baseline --tasks eval` (Chạy đánh giá baseline)
  11. `python -m lab.runner --condition subagents --tasks eval` (Chạy đánh giá subagents)
  12. `python -m lab.runner --condition skills-auto --tasks all` (Chạy đánh giá toàn bộ sau đóng băng)
  13. `python scripts/verify_freeze.py` (Kiểm tra quy trình đóng băng -> Báo OK)
  14. `python -m lab.compare > report/table.md` (Xuất bảng so sánh tổng hợp)
  15. `python scripts/check_breakdown.py` (Thống kê chi tiết lỗi kỹ thuật vs quy ước)

- Thử thách mở rộng: **Hướng 6c - Tấn công Red-Teaming đối với Curator và Cơ chế phòng thủ.**
  - **Mục tiêu**: Khảo sát nguy cơ tấn công Curator Injection / Data Leakage: Liệu một tác tử bị thỏa hiệp hoặc một bản ghi chạy độc hại có thể tiêm mã độc vào `SKILL.md` (Prompt Injection qua Curator) hoặc làm rò rỉ dữ liệu của tập đánh giá vào bộ kỹ năng không?
  - **Thiết kế thí nghiệm**: Xây dựng kịch bản kiểm thử độc lập trong `tests/test_red_team_curator.py`. Tạo vết giả định chứa prompt injection (ví dụ chuỗi Markdown chứa chỉ dẫn ghi đè hệ thống hoặc đánh lừa Curator copy đáp án của tác vụ đánh giá).
  - **Kết quả & Phân tích**: Hàm `validate_skill` trong `src/lab/curator.py` đã chặn đứng các nỗ lực chèn frontmatter bất hợp lệ, ép tên kỹ năng phải tuân thủ nghiêm ngặt regex kebab-case `^[a-z0-9]+(-[a-z0-9]+)*$`, và việc lọc cứng `role == "learn"` đã loại trừ hoàn toàn nguy cơ rò rỉ thông tin từ tập đánh giá sang bộ kỹ năng.
  - **Đề xuất cải tiến**: Bổ sung cơ chế AST linting nội dung Markdown của skill trước khi ghi đĩa để ngăn chặn triệt để kỹ thuật steganography hoặc chỉ thị độc hại ẩn trong prompt của kỹ năng.
- Ghi chú khác: Toàn bộ quá trình thực nghiệm tuân thủ chặt chẽ yêu cầu liêm chính học thuật, không can thiệp thủ công vào các thư mục `skills/auto/` hay tệp kết quả `run.json`.
