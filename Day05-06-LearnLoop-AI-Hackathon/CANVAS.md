# CANVAS CHECKPOINT 1 (CP1) — NHÓM LEARNLOOP
**Lớp:** 3A · **Phòng:** E403 · **Cụm:** Bàn 1  
**Track:** Track A · Đề A1 (Tối ưu AI Tutor hiện có trên VLearn)  
**Repository:** [https://github.com/DucPh4t/K4-3A-E403-LearnLoop](https://github.com/DucPh4t/K4-3A-E403-LearnLoop)

---

## 📋 1. Scaffold Canvas 7 dòng (Theo chuẩn 02-guide.md §1.5 & Rubric CP1)

1. **Hướng & Đề bài:** Track A · Đề A1 — Tối ưu AI Tutor hiện có trên VLearn (Grounding, Citation & Hallucination Defense).
2. **Job executor:** Học viên khóa AI20k đang theo dõi bài giảng và làm bài lab trên VLearn, bôi đen văn bản hoặc mở chat để hỏi đáp kiến thức bài học.
3. **Pain một câu (Ai · Đang làm gì · Vướng đâu · Hậu quả):** Học viên khóa AI20k khi bôi đen hoặc hỏi AI Tutor về khái niệm trong bài học thường xuyên nhận được câu trả lời thiếu căn cứ trích dẫn hoặc tự suy diễn ngoài phạm vi bài giảng, khiến học viên hoang mang, mất 15–30 phút tra cứu đối chiếu lại và dễ hiểu sai kiến thức kiểm tra.
4. **1–2 Bằng chứng đầu tiên (Mining chatlog thật 13.494 turns):**
   - **28% câu trả lời của Tutor hoàn toàn không có trích dẫn nguồn** (không có `[trang N]` hay mã đoạn bài giảng).
   - **Chỉ 28 / 13.494 lượt chat** Tutor đặt câu hỏi ngược làm rõ (`ask_probing_question`) khi đầu vào mơ hồ; còn lại tự bịa hoặc trả lời khuôn mẫu.
5. **Lát cắt MỘT CÂU:**
   > *"Khi học viên khóa AI20k hỏi về nội dung bài giảng trên VLearn, AI Tutor đối soát với transcript và slide đang mở: nếu câu hỏi nằm ngoài tài liệu thì từ chối lịch sự và hướng dẫn nguồn xem thay vì bịa, nếu câu hỏi mơ hồ thì hỏi lại một câu làm rõ trước khi trả lời đúng kích cỡ kèm trích dẫn chính xác mã đoạn."*
6. **Automation dự kiến + 1 dòng lý do:** **Conditional Automation** — AI tự động trả lời khi bằng chứng trong tài liệu đạt độ tin cậy cao; nếu không chắc chắn hoặc ngoài tài liệu thì từ chối thông minh hoặc điều hướng sang TA. *(Lý do cost-of-error: Kiến thức kỹ thuật sai lệch gây hiểu lầm nghiêm trọng cho học viên khi thi và làm dự án).*
7. **Willing users dự kiến (≥3 người) + Phân công có tên:**
   - *Willing users (Phòng E403):* Hoàng Văn Nam, Lê Minh Tuấn, Trần Đức Anh.
   - *Phân công:*
     - Nguyễn Đức Phát (`2A202602753`): Product Lead, điều phối CP1-CP6, AI Spec, Video & Pitch.
     - Chử Trần Phương Nam (`2A202602675`): Tech Lead, kiến trúc Grounding / RAG pipeline, prompt engineering.
     - Đỗ Thành Đạt (`2A202602874`): AI & Evaluation Engineer, Golden Set $\ge 25$ ca, eval script.
     - Nguỵ Khắc Phi Long (`2A202602532`): UX & User Research, mock prototype, thu thập feedback người dùng.

---

## 🧩 2. Canvas 4 Ô Sản Phẩm AI (4-Box AI Product Canvas)

```
┌──────────────────────────────────────────┬──────────────────────────────────────────┐
│ Ô 1: PROBLEM & USER (Nỗi đau & Dữ liệu) │ Ô 2: SOLUTION & SLICE (Giải pháp & Lát)  │
├──────────────────────────────────────────┼──────────────────────────────────────────┤
│ • User: Học viên AI20k trên VLearn.      │ • Lát cắt: Grounded & Calibrated Tutor: │
│ • Pain: 28% câu trả lời không có nguồn;  │   - Bắt buộc gắn badge trích dẫn đoạn.   │
│   tự bịa khi ngoài bài giảng; trả lời    │   - Từ chối lịch sự nếu ngoài tài liệu.  │
│   quá cỡ khi câu hỏi mơ hồ/cộc lốc.      │   - Hỏi lại làm rõ nếu câu hỏi mơ hồ.    │
│ • Bằng chứng: Mining 13.494 chatlog      │ • Mode: Conditional Automation.          │
│   thật (28% 0-citation; 28/13.494 probe).│ • Nguyên tắc: HAX G1, G2, G9, G10.       │
├──────────────────────────────────────────┼──────────────────────────────────────────┤
│ Ô 3: IMPACT & METRICS (Giá trị & Đo lường│ Ô 4: TEAM & VALIDATION (Nhân sự & Test)  │
├──────────────────────────────────────────┼──────────────────────────────────────────┤
│ • Tiết kiệm 15–30 phút/buổi học/học viên │ • Team: Phát (Lead) · Nam (AI Pipeline)  │
│ • Golden Set: 25 test cases đa dạng.     │   · Đạt (Eval & Data) · Long (UX & Test) │
│ • Quality Bar:                           │ • 3 Willing Users (Phòng E403):          │
│   - Citation accuracy: ≥ 90%.            │   1. Hoàng Văn Nam                       │
│   - Zero Hallucination ngoài bài: 100%.  │   2. Lê Minh Tuấn                        │
│   - Probing question rate: ≥ 80%.        │   3. Trần Đức Anh                        │
└──────────────────────────────────────────┴──────────────────────────────────────────┘
```
