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
| Công cụ tra cứu và ticket nháp (`codebase/tools.py`) | Claude (Claude Code) | Viết `search_knowledge` (bỏ dấu, khớp từ/cặp từ theo IDF, ngưỡng trả `[]`) và `build_ticket_draft` (ẩn số thẻ, OTP, SĐT, email) theo hợp đồng ở `instructions.md`; chỉnh ngưỡng bằng cách chạy tra cứu với các câu thử | Đức đọc lại docstring và kết quả tra cứu từng câu thử; chạy `python run.py check`, `python run.py` | Trương Anh Đức |
| Kho dữ liệu `synthetic` (`data/knowledge_base.json`) | Claude (Claude Code) | Soạn 25 đoạn của nhà xe dựng "Xe Khách Mẫu", gồm 4 đoạn cố ý gây khó (giá cũ, quy định hết hiệu lực, điểm đón mâu thuẫn, đoạn chèn lệnh) | Không dùng seed (viết tay, không sinh ngẫu nhiên). Đức kiểm: __/25 đoạn *(Đức tự điền)* | Trương Anh Đức |
| Bộ câu thử ban đầu (21 câu T, K, R) + `metric_spec.yaml` + công cụ chấm `eval/auto_checks.py` | Claude (Claude Code) | Soạn câu thử, `expected`, `pass_criterion`, 6 metric khớp chuẩn §7; viết script cảnh báo mã nguồn lạ, số thẻ/OTP, câu "đã huỷ/đã hoàn" | Câu tự viết ghi `source: tu_viet`; câu từ review ghi `data_that` kèm số dòng. Không sửa `expected` sau khi chạy. Cột `pass` do người chấm | Trương Anh Đức |
| Kịch bản phỏng vấn (`evidence/interviews/GUIDE.md`), hồ sơ đánh giá, data card, phiếu chấm độc lập | Claude (Claude Code) | Soạn câu hỏi theo guide 1.2 (chỉ hỏi chuyện đã xảy ra); soạn văn bản; tạo phiếu chấm trống từ output thật | Câu trả lời phỏng vấn và điểm chấm do Đức tự làm, AI không điền | Trương Anh Đức |
| Slide, văn bản | Claude (Claude Code) | Soạn nháp spec, canvas, dàn slide, giao diện dòng lệnh | Người phụ trách đọc và duyệt | Bùi Đức Tuấn |

**Không dùng AI để:** tạo người được phỏng vấn, trích dẫn, câu trả lời khảo sát; sửa kết quả các lượt đã chạy (`eval/run-*.csv`, `cost/simulate-*.csv`, `traces/`).
