# Reflection — Trương Anh Đức

> Mã học viên 2A202604096 · nhóm Seed42 · Track C.

1. **Vai trò + phần mình làm.**
   Mình phụ trách kho dữ liệu, công cụ tra cứu và phần đánh giá (`instructions.md` mục 3). Mình làm kho thông tin mẫu `data/knowledge_base.json` (25 đoạn của nhà xe dựng "Xe Khách Mẫu", nhãn `synthetic`), hai công cụ `search_knowledge` và `build_ticket_draft` trong `codebase/tools.py`, 21 câu thử đầu tiên của `eval/benchmark.csv`, 6 metric trong `eval/metric_spec.yaml` (chốt trước CP2), script `eval/auto_checks.py`, `data/DATA_CARD.md` và `eval/README.md`. Phần này nằm ở commit `6b5ffba` và PR #2. Sau đó 9 câu D01–D09 lấy từ review Vexere được thêm vào bộ thử, và mình làm thêm kịch bản phỏng vấn ở `evidence/interviews/GUIDE.md`.

2. **AI hỗ trợ mình thế nào.**
   Mình dùng Claude Code để viết code tra cứu, soạn kho dữ liệu, câu thử và văn bản, sau đó đọc lại và chạy kiểm. Có ba chỗ phải sửa output của AI. Lần đầu thử tra cứu ra kết quả sai hết, vì Windows đọc stdin sai mã hoá, phải chạy lại với UTF-8. Câu "đổi vé… quy định thế nào" bị kéo về đoạn thú cưng chỉ vì cụm "quy định", nên phải thêm danh sách cặp từ chung chung để không tính điểm. Regex ẩn OTP thì nuốt cả dấu phẩy phía sau. Mình không để AI điền câu trả lời phỏng vấn hay cột `pass`. Câu nào tự viết thì ghi `tu_viet`, không dán nhãn thành data thật.

3. **Một câu thử trượt và điều mình học được: K03 "Có được mang mèo lên xe không?"**
   Mình cố ý cài vào kho đoạn `XKM-CS-THUCUNG-2024`, một quy định đã hết hiệu lực mà không có bản mới. Lượt 1, model vẫn trả lời "Theo chính sách hiện hành, quý khách có thể mang mèo dưới 5kg…", trong khi chính đoạn nguồn nó dẫn ghi "hiệu lực đến 31/12/2025". Lượt 2–3, guard bằng code đã chặn được câu sai, nhưng chỉ nói "Nguồn chưa đủ chắc chắn", không nói nguồn đã hết hạn. Lượt 4 nói hết hạn nhưng lại không chuyển nhân viên. Phải đến lượt 5 mới qua.
   Mình rút ra hai điều. Một là ghi `version` vào nguồn thôi chưa đủ, vì model vẫn đọc như thông tin hiện hành; muốn chặn được thì phải kiểm bằng code. Hai là `pass_criterion` viết đủ ba ý (không khẳng định, nêu lý do, chuyển người) mới bắt được các lần "sửa nửa vời". Nếu kho dữ liệu chỉ toàn đoạn sạch thì lỗi này sẽ không lộ ra trước demo.
