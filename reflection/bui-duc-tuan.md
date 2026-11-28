# Reflection — Bùi Đức Tuấn

> Mã học viên 2A202603902 · nhóm Seed42 · Track C.

1. **Vai trò + phần tôi làm.**
   Tôi là đội trưởng, phụ trách giao diện chat (`codebase/app.py`, `codebase/web.py`), `spec.md`, `canvas.md`, `README.md`, slide và phần đào 200 review trong `evidence/`.
   Tôi lúc đầu định chọn edtech nhưng sau thảo luận thì có chốt hướng vé xe, đặt câu hỏi bài toán có quá dễ không để đội nghĩ lại, chọn chuẩn đạt từ 80% kèm hai điều kiện an toàn và chọn thiết kế cho web demo, slide.
   Mốc đối chiếu: `7309952` (CP1), `41a8828` (CP2), `53f3ad5` (web demo và slide), `e0e4981` (sửa bộ lọc OTP).

2. **AI hỗ trợ tôi thế nào.**
   Tôi dùng Claude Code để viết giao diện, script thu review và soạn nháp spec, canvas, slide, cả bản reflection này; Claude Sonnet và gpt-6.1-sol gắn nhãn độc lập 200 review, khớp 177/200 (`docs/ai-usage.md`).
   Bản UI và slide đầu bị tôi loại vì font xấu, trông đại trà kiểu AI làm, nên tôi gửi ảnh mẫu để làm lại. Số đếm theo từ khoá 55/440 bị bỏ khỏi bằng chứng, và tôi yêu cầu số liệu phải có nguồn kiểm lại được.
   Tôi test tay thì `otp 345` vẫn bị gửi sang model dù đã có bộ lọc; sau đó bộ lọc được sửa để chặn mã 3 chữ số (`e0e4981`, `spec.md` §10).
   Nhãn review mới kiểm tay một phần nhỏ (`evidence/hand_check.csv`), nên đội chỉ coi đó là tín hiệu.

3. **Một câu thử trượt và điều tôi học được: K06** "Vé mình 280 nghìn đi Đà Lạt, huỷ trước 1 ngày rưỡi thì được hoàn bao nhiêu tiền?"
   Lượt 1 câu này qua, nhưng model định báo 252.000đ và lớp kiểm trong code đã thay trước khi hiển thị. Lượt 2 và 3 lại trượt vì nói đã chuyển yêu cầu trong khi mới có phiếu nháp.
   Sau khi sửa lời dặn và lớp kiểm (`5c92396`), lượt 4 và 5 qua; lượt 5 nêu mức chung 90% và để nhân viên xử lý vé cụ thể.
   Tôi học được rằng qua một lượt chưa chắc lượt sau vẫn qua, nên phải chạy nhiều lượt và đọc cả trace.
   Lẽ ra nên làm từ đầu một chatbot hiểu rõ hoàn cảnh của khách rồi mới tạo phiếu, như một tư vấn viên; bản hiện tại còn xử lý từng câu riêng.
