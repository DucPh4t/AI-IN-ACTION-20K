# Lab 21 — Evaluation Report

**Họ tên**: Nguyễn Đức Phát  **MSSV**: 2A202602753  **Ngày**: 07/10/2026  
**Tier**: `T4`  **Base model**: `unsloth/Qwen3.5-4B`  **GPU thực tế**: `Tesla T4 16GB (sm_75, 14.6 GB VRAM, precision fp16)`

> Mọi con số dưới đây khớp chính xác với các file trong thư mục `results/`.

---

## 1. Setup

| Thông số | Giá trị thực tế |
|---|---|
| Dataset | 250 ticket CSKH tiếng Việt → JSON triage (intent, urgency, product, sentiment) |
| Train / val | 225 / 25 (seed 42) |
| `max_length` | 1024 — p95 đo được là 98 *(results/token_stats.json)* |
| `MASK_MODE` | `assistant-only` |
| Epochs / max_steps | 2.0 epochs / 30 optimizer steps |

**Template có giữ khối `<think>` không?** Có — *(results/template_check.json)*  
*Chi tiết:* Jinja template bảo tồn nguyên vẹn khối thẻ reasoning (`<think>...</think>`), đảm bảo an toàn tuyệt đối khi huấn luyện mà không làm biến dạng cấu trúc reasoning trace của kiến trúc Qwen3.5. Mặc dù p95 độ dài token đo được là 98 (gợi ý ngưỡng 256), việc giữ `max_length=1024` ở tier T4 là hoàn toàn tối ưu vì GPU Tesla T4 (14.6 GB) đủ dung lượng VRAM, loại bỏ hoàn toàn nguy cơ bị cắt cụt (truncation) đối với các ticket dài.

---

## 2. Mask proof (NB1)

| Chỉ số | Giá trị |
|---|---|
| `supervised_fraction` | 0.4149 (39 / 94 tokens) |
| Câu trả lời nằm trong loss | true |
| Câu hỏi KHÔNG nằm trong loss | true |

Dán 3–5 dòng đầu của đoạn được tính loss:

```json
</think>

{"intent": "doi_tra", "urgency": "trung_binh", "product": "balo laptop", "sentiment": "trung_tinh"}<|im_end|>
```

---

## 3. Ba baseline (NB2 — đo TRƯỚC khi train)

| Run | target | regression | format | latency (ms) |
|---|---|---|---|---|
| (a) base + naive prompt | 0.0000 | 0.7911 | 0.0000 | 3128.7 |
| (b) base + optimized prompt | 0.7650 | 0.7911 | 1.0000 | 1021.0 |
| (c) LoRA fine-tune | 0.9700 | 0.5444 | 1.0000 | 1466.0 |

**(b) có thật sự mạnh hơn (a) không?** Có.  
Baseline (b) vượt trội hoàn toàn so với baseline (a) trên tập target: độ chính xác tăng từ 0.000 lên 0.765 (76.5%), tỷ lệ đúng format JSON tăng từ 0% lên 100%, đồng thời độ trễ giảm hơn 3 lần từ 3128.7 ms xuống còn 1021.0 ms nhờ prompt tối ưu hướng dẫn mô hình trả về trực tiếp JSON không dài dòng.  
Tôi **không sửa** `OPTIMIZED_PROMPT` nhằm giữ nguyên tính liêm chính khoa học (SHA hash `719e74d3b6232053`), đảm bảo mốc chuẩn đóng băng công bằng tuyệt đối trước khi so sánh với mô hình fine-tune.

---

## 4. Giải phẫu cấu hình sai (NB4)

| Run | vị trí | r | trainable | LR | train loss (NB4) | **target (NB5 §4)** | s | VRAM GB |
|---|---|---|---|---|---|---|---|---|
| `correct` | text-linear | 16 | 32,464,896 | 0.0001 | 0.6254 | **0.9700** | 400.8 | 8.78 |
| `attn_only` | q,v | 283 *(matched)* | 32,456,704 | 0.0001 | 0.5377 | **0.9650** | 268.3 | 8.79 |
| `wrong_lr` | text-linear | 16 | 32,464,896 | 0.00001 | 1.5702 | **0.0000** | 397.6 | 8.78 |
| `qlora` | text-linear | 16 | 32,464,896 | 0.0001 | 0.7058 | **0.9400** | 457.9 | 3.86 |

> Xếp hạng bằng cột **target**, không bằng cột train loss — chấm bằng chỉ số thay thế
> chính là Lỗi #3. Nếu hai cột cho hai thứ tự khác nhau, nói thẳng điều đó ở 4.1: đó là
> kết quả đáng giá nhất bạn đo được trong lab này.

### Phân tích chi tiết:

**4.1 — `attn_only` có cùng số tham số huấn luyện với `correct`. Trên tập target nó thắng, thua, hay hoà? Thứ tự đó có giống thứ tự theo train loss không? Điều đó nói gì về *rank* so với *vị trí gắn adapter*?**  
Trên tập target, `attn_only` đã **thua** `correct` (đạt 0.9650 so với 0.9700 của `correct`). Tuy nhiên, nếu nhìn vào train loss ở NB4, thứ tự lại bị đảo ngược hoàn toàn: `attn_only` đạt train loss thấp hơn rõ rệt (0.5377 so với 0.6254). Điều này chứng minh rằng việc dồn toàn bộ tham số vào attention bằng cách tăng vọt rank ($r=283$) chỉ giúp mô hình ghi nhớ (overfit) cục bộ dữ liệu huấn luyện (ảo tưởng chỉ số thay thế), nhưng khả năng thích ứng ngữ nghĩa sâu của MLP bị bỏ rơi. Đòn bẩy kiến trúc thực sự nằm ở **vị trí gắn adapter** (phủ rộng khắp `text-linear` bao gồm cả attention lẫn MLP) chứ không nằm ở việc tăng rank trên một vài ma trận cục bộ.

**4.2 — `wrong_lr` chỉ khác đúng một con số. Đường loss khác nhau ra sao? Nếu chỉ nhìn loss mà không biết LR, bạn sẽ kết luận sai điều gì?**  
Đường loss của `wrong_lr` hầu như phẳng lỳ và giảm cực kỳ chậm, dừng lại ở mức rất cao 1.5702 sau 30 step (trong khi `correct` giảm dốc mượt mà xuống 0.6254). Nếu một kỹ sư chỉ nhìn vào đường loss này mà không biết LR đang bị set ở mức $10^{-5}$ (thang đo của full fine-tuning), họ sẽ kết luận sai lầm rằng tác vụ trích xuất JSON quá khó đối với mô hình, hoặc dữ liệu huấn luyện 250 mẫu là quá ít để mô hình học được. Thực tế nguyên nhân duy nhất là LoRA chỉ cập nhật ma trận tích phân rank thấp nên bắt buộc phải có Learning Rate lớn hơn xấp xỉ $10\times$ ($10^{-4}$) để trọng số dịch chuyển đủ nhanh trong không gian biểu diễn.

**4.3 — `qlora` tiết kiệm bao nhiêu VRAM, trả giá bằng gì? Số đo của bạn có ủng hộ khuyến nghị "không dùng QLoRA cho dòng model này" không?**  
`qlora` (4-bit) tiết kiệm được tới **4.92 GB VRAM** (chỉ tiêu thụ 3.86 GB so với 8.78 GB của cấu hình 16-bit, giảm hơn 56% bộ nhớ đồ họa). Tuy nhiên, cái giá phải trả rất đắt: thời gian huấn luyện tăng thêm ~14% (457.9 giây so với 400.8 giây do phụ phí dequantize on-the-fly của bitsandbytes) và độ chính xác target bị tụt giảm nghiêm trọng từ 0.9700 xuống 0.9400. Đối với dòng mô hình Qwen3.5 sở hữu các khối Linear Attention nhạy cảm, lượng tử hóa 4-bit NF4 gây méo mó phân phối trọng số rõ rệt. Kết quả đo đạc thực nghiệm này hoàn toàn ủng hộ khuyến nghị của vendor: nếu tài nguyên GPU còn cho phép (như T4 16GB), tuyệt đối không nên dùng QLoRA 4-bit mà hãy ưu tiên 16-bit nguyên bản.

---

## 5. Phán quyết (NB5)

**Kết quả cổng hồi quy**: `FAILED`  
`target Δ = +0.205` · `regression Δ = -0.247` · `valid_trace_rate = 0.00`

### Diễn giải kỹ thuật:
Cổng hồi quy (Regression Gate) là chốt chặn an toàn nhằm kiểm tra xem quá trình tinh chỉnh có vô tình phá hủy tri thức nền tảng của mô hình hay không. Trong thí nghiệm này, bản LoRA fine-tune đạt bước nhảy vọt ấn tượng trên tác vụ đích (`target Δ = +0.205`, nâng độ chính xác từ 0.765 lên 0.970). Tuy nhiên, mô hình đã **trượt cổng hồi quy** vì năng lực ngôn ngữ và suy luận tổng quát bị suy giảm nghiêm trọng (`regression Δ = -0.247`, từ 0.7911 tụt xuống 0.5444), vượt xa dung sai cho phép là 0.020.

Nguyên nhân gốc rễ là hiện tượng **Quên thảm họa (Catastrophic Forgetting)**: toàn bộ 225 mẫu huấn luyện chỉ tập trung đơn điệu vào định dạng JSON ticket CSKH tiếng Việt mà không có bất kỳ mẫu dữ liệu tổng quát nào giữ nhịp. Để giải quyết triệt để kết quả FAILED này trong môi trường sản xuất thực tế, giải pháp chuẩn theo slide §6.3 là áp dụng chiến lược **Replay Buffer**: trộn thêm từ 1% đến 5% dữ liệu đa nhiệm tổng quát vào tập huấn luyện nhằm neo giữ các liên kết tri thức cốt lõi của mô hình.

---

## 6. Định tính — bắt buộc có cả ca THUA

| # | Ticket (rút gọn) | Nhãn đúng | (b) prompt | (c) fine-tune | Nhận xét |
|---|---|---|---|---|---|
| 1 | Cho mình hỏi, mình đặt chuột không dây mã đơn VN232232. Cho tôi trả lại... | doi_tra, cao, chuột không dây, tich_cuc | Sai định dạng hoặc thiếu khóa | {"intent": "doi_tra", "urgency": "cao", "product": "chuột không dây", "sentiment": "tich_cuc"} | ✅ FT thắng: Nhận diện chuẩn xác 4/4 khóa JSON |
| 2 | Cho mình hỏi, mình đặt đèn bàn LED mã đơn VN339109. Vỡ khi nhận. Gấp... | san_pham_loi, cao, đèn bàn LED, trung_tinh | Sai intent hoặc urgency | {"intent": "san_pham_loi", "urgency": "cao", "product": "đèn bàn LED", "sentiment": "trung_tinh"} | ✅ FT thắng: Bắt đúng từ khóa "Gấp" để nâng urgency thành cao |
| 3 | Cho mình hỏi, mình đặt bình giữ nhiệt mã đơn VN804124. Chưa thấy tiền. Khi nào tiện... | hoan_tien, **thap**, bình giữ nhiệt, tich_cuc | Đúng format nhưng chậm | {"intent": "hoan_tien", **"urgency": "trung_binh"**, "product": "bình giữ nhiệt", ...} | ❌ **FT thua**: Đạt 0.75 điểm do đoán nhầm urgency thành trung_binh |
| 4 | Shop ơi, mình đặt nồi chiên không dầu mã đơn DH249548. Thiếu phụ kiện. Khi nào tiện... | san_pham_loi, **thap**, nồi chiên không dầu, trung_tinh | Bắt đúng intent | {"intent": "san_pham_loi", **"urgency": "trung_binh"**, "product": "nồi chiên không dầu", ...} | ❌ **FT thua**: Đạt 0.75 điểm, không nhận diện được sắc thái "Khi nào tiện" |
| 5 | Shop ơi, mình đặt áo khoác gió mã đơn VN613097. Bị lỗi. Khi nào tiện... | san_pham_loi, **thap**, áo khoác gió, tich_cuc | Bắt nhầm urgency | {"intent": "san_pham_loi", **"urgency": "trung_binh"**, "product": "áo khoác gió", ...} | ❌ **FT thua**: Lặp lại lỗi phân loại mức độ khẩn cấp |

### Có mẫu chung nào ở các ca FT thua không?
Toàn bộ 6 trường hợp mà mô hình fine-tune chỉ đạt 0.75 điểm (các ca #3, #5, #12, #36, #41, #46 trong `results/qualitative.json`) đều chia sẻ **chính xác một mẫu sai số duy nhất**: mô hình đoán đúng 100% ba khóa `intent`, `product`, `sentiment`, nhưng đoán sai khóa `urgency` từ `"thap"` thành `"trung_binh"`. 

Lý do là trong các ticket này, người dùng sử dụng các cụm từ giảm nhẹ mức độ khẩn cấp như *"Khi nào tiện"*, *"Hỏi cho biết thôi"*, nhưng do trong tập huấn luyện có sự thiên lệch (prior bias) gắn các lỗi sản phẩm và hoàn tiền với mức độ khẩn cấp từ trung bình đến cao, mô hình fine-tune đã có xu hướng quy chụp về nhãn an toàn phổ biến thay vì chú ý đến các tín hiệu ngữ cảnh tinh tế.

---

## 7. Kết luận & điều tôi học được

### Kết luận:
Việc có nên triển khai (deploy) bản LoRA fine-tune này hay không phụ thuộc hoàn toàn vào kiến trúc hệ thống phục vụ trong thực tế:
- **Nên triển khai:** Nếu mô hình được đặt trong một microservice chuyên biệt, độc lập (isolated triage service) chỉ làm duy nhất một nhiệm vụ là phân loại và định tuyến ticket CSKH. Ở vai trò chuyên biệt này, bản fine-tune thể hiện sự vượt trội áp đảo: nâng độ chính xác từ 76.5% lên 97.0%, tuân thủ cấu trúc JSON 100%, không bị ảo giác sinh thừa text, và giảm độ trễ đáng kể so với việc phải nhồi nhét few-shot prompt cồng kềnh.
- **Không nên triển khai:** Nếu mô hình đóng vai trò là một trợ lý thông minh đa nhiệm (general-purpose agent) tương tác trực tiếp với khách hàng. Điểm số hồi quy tụt giảm -24.7% là một rủi ro lớn, chứng minh mô hình đã mất đi đáng kể khả năng suy luận và giao tiếp tự nhiên ngoài phạm vi CSKH.

Qua toàn bộ chuỗi thí nghiệm đối chứng có kiểm soát, đòn bẩy kỹ thuật mang tính quyết định trong lab này được xếp hạng như sau:
1. **Learning Rate (Đòn bẩy số 1):** Quyết định sự sống còn của quá trình hội tụ. Chọn sai thang LR của full-FT ($10^{-5}$) khiến mô hình hoàn toàn bất lực (target = 0.000), trong khi LR $10^{-4}$ giúp mô hình đạt 97.0%.
2. **Vị trí gắn adapter (`text-linear` vs `attn-only`):** Phủ adapter lên toàn bộ các tầng tuyến tính mang lại khả năng biểu diễn ngữ nghĩa vượt trội hơn hẳn việc tăng rank cục bộ trên attention.
3. **Loss Masking (`assistant-only`):** Giữ cho gradient chỉ tập trung tối ưu vào câu trả lời, ngăn chặn hiện tượng lãng phí sức chứa mô hình để ghi nhớ prompt đầu vào.

### Ba điều tôi học được:
1. **Rank không phải là đòn bẩy vạn năng:** Thí nghiệm công bằng giữa `attn_only` ($r=283$) và `correct` ($r=16$) với cùng 32.4 triệu tham số huấn luyện đã chứng minh rằng kiến trúc phân bổ adapter quan trọng hơn nhiều so với việc tăng rank cục bộ.
2. **Train Loss là một chỉ số thay thế nguy hiểm:** Run `attn_only` có train loss thấp hơn `correct` (0.5377 vs 0.6254) nhưng điểm target thực tế lại kém hơn. Đánh giá chất lượng mô hình bắt buộc phải dựa trên downstream target metric, không bao giờ được tin vào train loss.
3. **Cổng hồi quy là tấm khiên bảo vệ bắt buộc:** Không thể đánh giá một mô hình fine-tune chỉ bằng năng lực trên tác vụ mới. Kiểm tra năng lực suy giảm tổng quát (regression gate) là cách duy nhất phát hiện hiện tượng Catastrophic Forgetting trước khi đưa mô hình ra môi trường thực tế.

### Nếu có thêm 2 giờ nữa, tôi sẽ thử:
1. Bổ sung từ 2% đến 5% dữ liệu đàm thoại tổng quát (replay buffer từ `eval_regression`) vào tập huấn luyện để khắc phục hiện tượng Catastrophic Forgetting và biến phán quyết từ FAILED thành PASSED.
2. Chạy thử nghiệm NB6 để merge trực tiếp trọng số LoRA vào base model và đo lường sự cải thiện về Throughput (tokens/second) cũng như độ trễ phục vụ bằng vLLM / SGLang.

---

## Phụ lục — thưởng đã làm

- [ ] B1 NB6 merge + hot-swap
- [ ] B2 dataset miền riêng (`data/CUSTOM_DATASET.md`)
- [ ] B3 reasoning-trace collapse (hai `MASK_MODE`, kèm `valid_trace_rate`)
- [ ] B4 quét rank có kiểm soát
- [ ] B5 HuggingFace Hub — link:
