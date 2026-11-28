# Khai báo dùng AI

README của nhóm có mục "Dùng AI vào việc gì" (2–3 dòng, bắt buộc). Ghi chi tiết vào bảng dưới đây.

> Luật của đề: dùng AI để làm bài thoải mái, nhưng **ai không giải thích được phần có tên mình thì phần đó nhận 0 điểm**. Khai thiếu không bị trừ; giấu mới bị.

| Việc | Công cụ AI | AI làm gì | Người kiểm/sửa gì | Ai phụ trách |
|---|---|---|---|---|
| Code bản chạy thử | | | | |
| Prompt / thiết kế lời gọi mô hình | | | | |
| Đào data (viết script thu và ghép nhãn, gắn nhãn) | Claude (Claude Code), gpt-6.1-sol | Viết script; hai model gắn nhãn độc lập 200 review, khớp 177/200; phản biện luận điểm | Chưa kiểm tay | Bùi Đức Tuấn |
| Rà câu hỏi phỏng vấn / khảo sát | | Chỉ rà câu dẫn dắt | | |
| Viết câu thử (benchmark) | | | Mỗi câu thử có `source`; câu thử AI viết được ghi rõ | |
| Sinh data `synthetic` (nếu có) | | | Seed __ · kiểm tay __ dòng | |
| Chấm cột `pass` bằng LLM (nếu có) | | | Kiểm tra thủ công __ câu thử, khớp __/__ | |
| Slide, văn bản | Claude (Claude Code) | Soạn nháp spec, canvas, dàn slide, giao diện dòng lệnh | Người phụ trách đọc và duyệt | Bùi Đức Tuấn |
| Web demo (`codebase/web.py`, `codebase/inbox.py`) và reflection cá nhân | Claude (Claude Code) | Viết giao diện chat web, màn nhà xe xử lý phiếu và phần tự kiểm; soạn nháp reflection của Tuấn | Tuấn chọn thiết kế, dùng thử web, sửa reflection | Bùi Đức Tuấn |

**Không dùng AI để:** tạo người được phỏng vấn, trích dẫn, câu trả lời khảo sát; sửa kết quả các lượt đã chạy (`eval/run-*.csv`, `cost/simulate-*.csv`, `traces/`).
