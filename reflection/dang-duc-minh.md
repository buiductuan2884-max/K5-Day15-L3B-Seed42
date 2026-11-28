# Reflection — Đặng Đức Minh

> Mã học viên 2A202603886 · nhóm Seed42 · Track C.

1. **Vai trò + phần mình làm.**
   Mình phụ trách luồng trả lời trong `codebase/agent.py`, kết nối Gemini trong `codebase/ai.py` và mô phỏng chi phí trong `cost/personas.yaml`, `cost/cost-estimate.md` (xem `instructions.md` mục 2).
   Mình nối API với token lấy từ `usage` của nhà cung cấp, kiểm nguồn trước khi trả lời và chỉ tạo ticket nháp cho việc cần nhân viên duyệt; không tự gửi yêu cầu hay xử lý tiền.
   Các mốc có thể đối chiếu: `c0b87f2` (kết nối Gemini), `a4d0f7e` và `5c92396` (sửa luồng an toàn), `86cf3f6` (sửa hai ca còn trượt), `4c5d9ce` (mô phỏng 50 phiên và ghi chi phí).

2. **AI hỗ trợ mình thế nào.**
   Mình dùng Codex để viết và rà code, soạn prompt, phân tích output/trace của các lượt eval và tính lại chi phí từ token API; mình kiểm bằng các lệnh `python run.py check`, `eval`, `score`, `simulate` và các test của agent.
   Bản đầu vẫn để model nói yêu cầu đã được ghi nhận dù công cụ chỉ tạo ticket nháp; mình phải sửa lớp kiểm output và câu chữ để trạng thái hiển thị khớp với hành động thật.
   Mình cũng đổi model được chọn từ Gemini 3.1 sang 3.5 Flash-Lite, giữ nguyên kết quả lượt cũ, ghi rõ thay đổi model và lỗi API để không nhận toàn bộ mức tăng điểm là do một sửa code.

3. **Một câu thử trượt và điều mình học được: D06.**
   Ở lượt 1, câu D06 về hỗ trợ vé bị chấm trượt vì output nói đã ghi nhận yêu cầu, trong khi trace chỉ có `build_ticket_draft` ở trạng thái `draft`.
   Mình bổ sung kiểm tra lời khẳng định đã gửi/đã xử lý và hướng dẫn model giải thích rõ rằng bản nháp còn chờ khách kiểm, nhân viên chưa nhận hay duyệt; kết quả các lượt sau được ghi trong `eval/report.md`.
   Mình học được rằng trả lời an toàn không chỉ là chặn giao dịch thật: câu chữ cũng phải phản ánh đúng trạng thái hệ thống. Lượt 5 đạt 30/30 trên bộ thử dựng, nhưng vẫn cần kiểm với dữ liệu và hành khách thật trước khi triển khai.
