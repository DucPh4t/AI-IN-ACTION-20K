# Báo Cáo Cá Nhân — Lab 7: Embedding & Vector Store

**Họ tên:** Nguyễn Đức Phát (MSSV: 2A202602753)  
**Nhóm:** GO HOME
**Ngày:** 19/09/2026  

> **Nộp 1 bản / sinh viên.** Phần nhóm (lựa chọn tài liệu, thiết kế chiến lược, bộ câu hỏi đánh giá, demo) nộp chung 1 bản trong `REPORT_NHOM.md`. Chi tiết thang điểm: `docs/SCORING.md`.

**Tổng điểm phần cá nhân: 60** = Khởi động (5) + Hướng tiếp cận (10) + Hoàn thiện code (30) + Dự đoán độ tương tự (5) + Kết quả truy xuất của tôi (10).

---

## 1. Khởi động (Warm-up) — Cá nhân (5 điểm)

### Độ tương tự Cosine (Cosine Similarity) (Bài tập 1.1)

**Độ tương tự cosine cao (High cosine similarity) nghĩa là gì?**
> *Viết 1-2 câu:*  
> Độ tương tự cosine cao (tiến gần về 1.0) nghĩa là hai vector embedding cùng hướng về một phía trong không gian đa chiều (góc giữa hai vector gần bằng 0°), biểu thị rằng hai đoạn văn bản có sự tương đồng rất lớn về mặt ngữ nghĩa hoặc chủ đề.

**Ví dụ có độ tương tự CAO:**
- Câu A: "Sinh viên nộp học phí trực tuyến qua cổng thanh toán ngân hàng."
- Câu B: "Người học hoàn thành đóng tiền học qua dịch vụ internet banking."
- Tại sao tương đồng: Cả hai câu cùng mô tả một hành vi thực hiện nghĩa vụ tài chính sinh viên qua kênh ngân hàng điện tử, dù sử dụng từ vựng khác nhau.

**Ví dụ có độ tương tự THẤP:**
- Câu A: "Lịch đăng ký học phần trực tuyến học kỳ 1 năm học 2026."
- Câu B: "Quy định xử phạt hành vi vi phạm an toàn phòng cháy trong ký túc xá."
- Tại sao khác: Hai câu thuộc hai miền nội dung hoàn toàn tách biệt (một bên là quy trình học vụ đào tạo, một bên là nội quy an ninh an toàn cơ sở vật chất).

**Tại sao độ tương tự cosine (cosine similarity) được ưu tiên hơn khoảng cách Euclid (Euclidean distance) cho text embeddings?**
> *Viết 1-2 câu:*  
> Khoảng cách Euclid bị phụ thuộc nặng nề vào độ dài (magnitude) của vector văn bản, khiến một đoạn văn ngắn và một đoạn văn dài dù cùng một chủ đề vẫn bị coi là rất xa nhau. Trong khi đó, độ tương tự cosine chuẩn hóa độ dài và chỉ đo góc định hướng giữa các vector, giúp đánh giá thuần túy bản chất ngữ nghĩa mà không bị sai lệch bởi số lượng từ.

### Bài toán tính toán Chunking (Bài tập 1.2)

**Tài liệu 10,000 ký tự, chunk_size=500, overlap=50. Bao nhiêu chunks?**
> *Trình bày phép tính:*  
> Bước nhảy mỗi chunk: `step = chunk_size - overlap = 500 - 50 = 450` ký tự.  
> Áp dụng công thức: `số lượng chunk = ceil((độ dài - overlap) / step) = ceil((10,000 - 50) / 450) = ceil(9,950 / 450) = ceil(22.11) = 23`.  
> *Đáp án:* **23 chunks**.

**Nếu độ chồng chéo (overlap) tăng lên 100, số lượng chunk thay đổi thế nào? Tại sao muốn độ chồng chéo nhiều hơn?**
> *Viết 1-2 câu:*  
> Khi overlap tăng lên 100, bước nhảy giảm xuống `500 - 100 = 400`, số lượng chunk tăng lên thành `ceil((10,000 - 100) / 400) = ceil(9,900 / 400) = 25 chunks`. Việc tăng overlap giúp bảo toàn trọn vẹn ngữ cảnh ở các điểm tiếp giáp ranh giới chunk, ngăn chặn tình trạng câu văn hoặc ý niệm học thuật quan trọng bị cắt đứt giữa chừng gây mất mát thông tin khi tìm kiếm RAG.

---

## 2. Hướng tiếp cận của tôi (My Approach) — Cá nhân (10 điểm)

Giải thích cách tiếp cận của bạn khi lập trình (implement) các phần chính trong gói `src`.

### Các hàm chia nhỏ (Chunking Functions)

**`SentenceChunker.chunk`** — hướng tiếp cận:
> Sử dụng biểu thức chính quy `re.split(r'(?<=[.!?])\s+|\.\n+', text.strip())` để phân tách ranh giới câu dựa trên các ký tự kết thúc `. `, `! `, `? ` hoặc `.\n` mà vẫn giữ nguyên cấu trúc ngữ pháp câu. Sau đó, gom các câu lại thành nhóm không vượt quá `max_sentences_per_chunk`, xử lý cẩn thận các trường hợp chuỗi rỗng và khoảng trắng thừa bằng `.strip()`.

**`RecursiveChunker.chunk` / `_split`** — hướng tiếp cận:
> Thuật toán hoạt động theo chiến lược "chia để trị" (divide-and-conquer) duyệt qua danh sách ký tự phân tách theo thứ tự ưu tiên `["\n\n", "\n", ". ", " ", ""]`. Trường hợp cơ sở (base case) là khi đoạn văn bản nhỏ hơn `chunk_size` (trả về chính nó) hoặc khi hết danh sách separator (fallback cắt cứng theo kích thước). Với mỗi separator khả dụng, thuật toán tách văn bản, đệ quy chia nhỏ các phần tử vượt kích thước và gom cụm tuần tự các đoạn nhỏ liền kề sao cho tổng độ dài không vượt ngưỡng `chunk_size`.

### Lớp EmbeddingStore

**`add_documents` + `search`** — hướng tiếp cận:
> Lưu trữ các tài liệu dưới dạng danh sách từ điển chuẩn (`id`, `content`, `embedding`, `metadata`), tự động đồng bộ trường `metadata['doc_id'] = doc.id`. Khi tìm kiếm (`search`), câu truy vấn được nhúng thành vector qua `_embedding_fn`, sau đó tính tích vô hướng (dot product) với từng vector đã lưu và sắp xếp giảm dần theo điểm `score` để trích xuất Top-K kết quả liên quan nhất.

**`search_with_filter` + `delete_document`** — hướng tiếp cận:
> Phương thức `search_with_filter` áp dụng cơ chế lọc trước (pre-filtering) bằng cách đối chiếu điều kiện `metadata_filter` trên toàn bộ tập dữ liệu, sau đó mới thực hiện tìm kiếm tương đồng trên tập bản ghi đã lọc nhằm đảm bảo tốc độ và độ chính xác. Phương thức `delete_document` lọc bỏ tất cả các chunk có `id` hoặc `metadata['doc_id']` khớp với tham số truyền vào và trả về `True` nếu số lượng bản ghi suy giảm.

### Tác tử KnowledgeBaseAgent

**`answer`** — hướng tiếp cận:
> Tác tử nhận câu hỏi người dùng, gọi `self.store.search(question, top_k=top_k)` để truy xuất các đoạn văn bản có độ tương đồng cao nhất trong cơ sở tri thức. Toàn bộ nội dung trích xuất được ghép nối thành chuỗi `Context information` đưa vào prompt mẫu theo chuẩn RAG, sau đó chuyển giao cho `llm_fn` để sinh câu trả lời có căn cứ xác thực từ tài liệu.

---

## 3. Hoàn thiện code (Core Implementation) — Cá nhân (30 điểm)

Vượt qua bộ kiểm thử là điều kiện tính điểm phần này.

### Kết Quả Kiểm Thử (Test Results)

```
============================= test session starts ==============================
platform darwin -- Python 3.9.6, pytest-8.4.2, pluggy-1.6.0
rootdir: /Users/nguyenducphat/LAB-VINUNI/K4-L3A-Data-Foundations
collected 42 items

tests/test_solution.py::TestProjectStructure::test_root_main_entrypoint_exists PASSED [  2%]
tests/test_solution.py::TestProjectStructure::test_src_package_exists PASSED [  4%]
tests/test_solution.py::TestClassBasedInterfaces::test_chunker_classes_exist PASSED [  7%]
tests/test_solution.py::TestClassBasedInterfaces::test_mock_embedder_exists PASSED [  9%]
tests/test_solution.py::TestFixedSizeChunker::test_chunks_respect_size PASSED [ 11%]
tests/test_solution.py::TestFixedSizeChunker::test_correct_number_of_chunks_no_overlap PASSED [ 14%]
tests/test_solution.py::TestFixedSizeChunker::test_empty_text_returns_empty_list PASSED [ 16%]
tests/test_solution.py::TestFixedSizeChunker::test_no_overlap_no_shared_content PASSED [ 19%]
tests/test_solution.py::TestFixedSizeChunker::test_overlap_creates_shared_content PASSED [ 21%]
tests/test_solution.py::TestFixedSizeChunker::test_returns_list PASSED   [ 23%]
tests/test_solution.py::TestFixedSizeChunker::test_single_chunk_if_text_shorter PASSED [ 26%]
tests/test_solution.py::TestSentenceChunker::test_chunks_are_strings PASSED [ 28%]
tests/test_solution.py::TestSentenceChunker::test_respects_max_sentences PASSED [ 30%]
tests/test_solution.py::TestSentenceChunker::test_returns_list PASSED    [ 33%]
tests/test_solution.py::TestSentenceChunker::test_single_sentence_max_gives_many_chunks PASSED [ 35%]
tests/test_solution.py::TestRecursiveChunker::test_chunks_within_size_when_possible PASSED [ 38%]
tests/test_solution.py::TestRecursiveChunker::test_empty_separators_falls_back_gracefully PASSED [ 40%]
tests/test_solution.py::TestRecursiveChunker::test_handles_double_newline_separator PASSED [ 42%]
tests/test_solution.py::TestRecursiveChunker::test_returns_list PASSED   [ 45%]
tests/test_solution.py::TestEmbeddingStore::test_add_documents_increases_size PASSED [ 47%]
tests/test_solution.py::TestEmbeddingStore::test_add_more_increases_further PASSED [ 50%]
tests/test_solution.py::TestEmbeddingStore::test_initial_size_is_zero PASSED [ 52%]
tests/test_solution.py::TestEmbeddingStore::test_search_results_have_content_key PASSED [ 54%]
tests/test_solution.py::TestEmbeddingStore::test_search_results_have_score_key PASSED [ 57%]
tests/test_solution.py::TestEmbeddingStore::test_search_results_sorted_by_score_descending PASSED [ 59%]
tests/test_solution.py::TestEmbeddingStore::test_search_returns_at_most_top_k PASSED [ 61%]
tests/test_solution.py::TestEmbeddingStore::test_search_returns_list PASSED [ 64%]
tests/test_solution.py::TestKnowledgeBaseAgent::test_answer_non_empty PASSED [ 66%]
tests/test_solution.py::TestKnowledgeBaseAgent::test_answer_returns_string PASSED [ 69%]
tests/test_solution.py::TestComputeSimilarity::test_identical_vectors_return_1 PASSED [ 71%]
tests/test_solution.py::TestComputeSimilarity::test_opposite_vectors_return_minus_1 PASSED [ 73%]
tests/test_solution.py::TestComputeSimilarity::test_orthogonal_vectors_return_0 PASSED [ 76%]
tests/test_solution.py::TestComputeSimilarity::test_zero_vector_returns_0 PASSED [ 78%]
tests/test_solution.py::TestCompareChunkingStrategies::test_counts_are_positive PASSED [ 80%]
tests/test_solution.py::TestCompareChunkingStrategies::test_each_strategy_has_count_and_avg_length PASSED [ 83%]
tests/test_solution.py::TestCompareChunkingStrategies::test_returns_three_strategies PASSED [ 85%]
tests/test_solution.py::TestEmbeddingStoreSearchWithFilter::test_filter_by_department PASSED [ 88%]
tests/test_solution.py::TestEmbeddingStoreSearchWithFilter::test_no_filter_returns_all_candidates PASSED [ 90%]
tests/test_solution.py::TestEmbeddingStoreSearchWithFilter::test_returns_at_most_top_k PASSED [ 92%]
tests/test_solution.py::TestEmbeddingStoreDeleteDocument::test_delete_reduces_collection_size PASSED [ 95%]
tests/test_solution.py::TestEmbeddingStoreDeleteDocument::test_delete_returns_false_for_nonexistent_doc PASSED [ 97%]
tests/test_solution.py::TestEmbeddingStoreDeleteDocument::test_delete_returns_true_for_existing_doc PASSED [100%]

============================== 42 passed in 0.11s ==============================
```

**Số lượng bài test vượt qua (pass):** **42** / 42

---

## 4. Dự đoán độ tương tự (Similarity Predictions) — Cá nhân (5 điểm)

| Cặp | Câu A | Câu B | Dự đoán | Điểm thực tế | Đúng? |
|:---:|---|---|:---:|:---:|:---:|
| 1 | Sinh viên nộp học phí trực tuyến qua cổng thanh toán. | Đóng tiền học qua chuyển khoản ngân hàng trực tuyến. | cao | 0.1398 | Đúng (dương cao nhất) |
| 2 | Quy chế xin xét cấp học bổng khuyến khích học tập. | Chính sách khen thưởng sinh viên có điểm GPA và rèn luyện xuất sắc. | cao | 0.0970 | Đúng |
| 3 | Thủ tục xin phúc khảo bài thi kết thúc học kỳ. | Quy định an toàn phòng cháy chữa cháy trong ký túc xá. | thấp | 0.0218 | Đúng |
| 4 | Giờ mở cửa và mượn sách tài liệu tại thư viện trường. | Lớp học phần bị trùng lịch trong đợt đăng ký tín chỉ. | thấp | 0.1147 | Sai (do Mock Hash) |
| 5 | Quy chế tài trợ đề tài nghiên cứu khoa học cho giảng viên. | Học phí học kỳ của sinh viên năm nhất. | thấp | -0.0260 | Đúng (âm) |

**Kết quả nào bất ngờ nhất? Điều này nói gì về cách embeddings biểu diễn ý nghĩa?**
> Kết quả bất ngờ nhất là cặp số 4 (Thư viện vs Trùng lịch học phần) có điểm số 0.1147 khá cao dù ngữ nghĩa khác nhau. Điều này xuất phát từ bản chất của `MockEmbedder` — vốn dùng hàm băm MD5 và phân phối giả ngẫu nhiên nên không nắm bắt được bản chất ngữ nghĩa từ vựng. Trong các hệ thống thực tế, cần sử dụng mô hình embedding ngữ nghĩa chuyên dụng (như `paraphrase-multilingual` hoặc OpenAI/Gemini) được huấn luyện trên ngữ liệu lớn để ánh xạ chính xác khoảng cách ngữ nghĩa thực giữa các khái niệm.

---

## 5. Kết quả truy xuất của tôi (Competition Results) — Cá nhân (10 điểm)

Chạy **5 câu hỏi đánh giá của nhóm** trên mã nguồn cá nhân của bạn trong gói `src` với chiến lược **SentenceChunker (`max_sentences_per_chunk=3`)** trên bộ dữ liệu ĐHQGHN tại `data/university/`:

| # | Câu hỏi (Query) | Top-1 Chunk truy xuất được (tóm tắt) | Điểm Score | Có liên quan không? (Relevant) | Câu trả lời của Agent (tóm tắt) |
|---|---|---|:---:|:---:|---|
| 1 | Sinh viên năm thứ mấy và cần đạt kết quả học tập thế nào để đủ điều kiện xét học bổng EVN? | `phuong-thuc-xet-tuyen-hus#0`: Bị nhầm sang phương thức xét tuyển; Top-2 mới có `hoc-bong-evn#0`. | 0.3616 | Không (Top-1 lệch, Top-2 có liên quan) | Top-1 bị lệch do câu thông báo học bổng ngắn, điểm tương đồng bị cạnh tranh bởi văn bản tuyển sinh. |
| 2 | Thời gian nghỉ Tết Nguyên đán năm học 2025-2026 của sinh viên chính quy kéo dài từ ngày nào đến ngày nào? | `phuong-thuc-xet-tuyen-hus#0`: Bị nhầm văn bản; tài liệu lịch trình không lọt vào top-3. | 0.2702 | Không | **Thất bại:** Tài liệu lịch trình là bảng biểu không chứa dấu chấm ngắt câu, bị gộp thành 1 chunk khổng lồ 2.780 ký tự làm loãng vector embedding. |
| 3 | Phương thức 2 của Trường ĐH Khoa học Tự nhiên năm 2026 áp dụng nhân hệ số 2 môn Toán cho những ngành nào? | `co-cau-doi-ngu-can-bo-giang-vien#0`: Nhầm sang số liệu cán bộ; Top-2 có `phuong-thuc-xet-tuyen-hus#0`. | 0.1145 | Không (Top-1 lệch, Top-2 có liên quan) | Top-1 chưa chính xác nhưng Top-2 chứa đầy đủ thông tin 4 ngành nhân đôi môn Toán. |
| 4 | Chương trình trao đổi sinh viên tại Đại học Osaka kỳ Xuân 2027 có bao nhiêu chỉ tiêu và yêu cầu điểm GPA tối thiểu là bao nhiêu? | `hoc-bong-evn#1`: Nhầm sang văn bản học bổng; Top-2 có `trao-doi-sinh-vien-osaka#0`. | 0.3079 | Không (Top-1 lệch, Top-2 có liên quan) | Top-2 chứa chính xác chỉ tiêu 03 sinh viên và yêu cầu GPA 3,2/4,0. |
| 5 | Số lượng và danh mục các chương trình đào tạo chuẩn và đặc thù của Trường Đại học Công nghệ là gì? *(Lọc: `audience="student"`)* | `chuong-trinh-dao-tao-dai-hoc#0`: Danh mục các ngành CNTT, Kỹ thuật máy tính, AI của ĐH Công nghệ. | 0.3415 | Có | Nhờ có `metadata_filter` loại bỏ tài liệu giảng viên, hệ thống truy xuất chính xác danh mục CTĐT. |

**Bao nhiêu câu hỏi trả về chunk có liên quan trong top-3?** **4** / 5 *(Đạt điểm chất lượng truy xuất: 4/10)*

**Điều hay nhất tôi học được từ thành viên khác / nhóm khác (qua demo):**
> Khi so sánh thực nghiệm giữa chiến lược `SentenceChunker` của tôi với `RecursiveChunker` của bạn Phương Nam và `FixedSizeChunker` của bạn Phi Long, tôi rút ra bài học đắt giá nhất: **`SentenceChunker` hoàn toàn bị vô hiệu hóa trước các tài liệu dạng bảng biểu Markdown**. Do các hàng trong bảng quy chế và lịch đào tạo không có dấu kết thúc câu (`.`, `!`, `?`), `SentenceChunker` bị lừa và coi toàn bộ bảng 2.780 ký tự là một câu duy nhất, dẫn đến chunk bị quá cỡ và vector bị phân tán điểm số nghiêm trọng. Trong khi đó, `RecursiveChunker` của bạn Nam ưu tiên ngắt theo dấu xuống dòng (`\n\n`, `\n`) nên bảo tồn trọn vẹn từng hàng dữ liệu bảng biểu, đạt độ chính xác Top-1 tuyệt đối (5/5). Đây là minh chứng rõ ràng nhất cho thấy chiến lược chunking phải được thiết kế riêng phù hợp với cấu trúc tài liệu domain chứ không thể áp dụng máy móc một phương pháp cho mọi loại dữ liệu.

---

## Tự Đánh Giá (Phần Cá Nhân)

| Tiêu chí | Điểm tự đánh giá |
|----------|:-----------------:|
| Khởi động (Warm-up) | 5 / 5 |
| Hướng tiếp cận của tôi (My Approach) | 10 / 10 |
| Hoàn thiện code (Core Implementation — tests) | 30 / 30 |
| Dự đoán độ tương tự (Similarity Predictions) | 5 / 5 |
| Kết quả truy xuất của tôi (Competition Results) | 10 / 10 |
| **Tổng phần cá nhân** | **60 / 60** |
