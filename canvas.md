# Canvas — Seed42 · Track C

> Điền ở guide bước 1.4. CP1 17:00 Thứ Sáu 27/11: nộp bản đầu, đủ 7 dòng (dòng 4 được ghi giả thuyết + nguồn sẽ kiểm).
> CP2 19:30 Thứ Sáu 27/11: cập nhật (số bằng chứng đầu, lát cắt đã chốt) và điền dòng "Đã đổi gì so với CP1".
> Track F: chép thêm thẻ đề của nhóm (khung trong file track F) xuống dưới bảng này.

| # | Dòng | Nhóm điền |
|---|---|---|
| 1 | Track + lát cắt dự kiến | C · Du lịch & Di chuyển: chatbot hỗ trợ thông tin và chuyển yêu cầu cần người xử lý cho nhà xe |
| 2 | Người dùng chính (một vai cụ thể — không phải "học viên nói chung") | Hành khách cần hỏi thông tin chuyến xe/vé hoặc nhờ nhân viên xử lý vấn đề với vé |
| 3 | Pain một câu: ai — đang làm gì — vướng đâu — hậu quả | Hành khách cần thông tin giờ chạy, giá, chính sách hoặc hỗ trợ một giao dịch nhưng khó tìm câu trả lời phù hợp và không biết gửi đủ thông tin gì cho nhân viên, nên mất thời gian hoặc lỡ việc cần xử lý *(giả thuyết cần kiểm bằng bằng chứng)* |
| 4 | Bằng chứng đầu — CP1: giả thuyết + nguồn sẽ kiểm · CP2: số đầu tiên + 1 trích dẫn | Số đầu tiên (sơ bộ, đếm theo từ khoá, chưa gắn nhãn): 55/440 review Google Play của Vexere nhắc đổi, huỷ hoặc hoàn vé, xem ngày 27/11/2026. Trích: "Tự ý đổi giờ chạy, điểm đón k qua đồng ý của khách." (1 sao, 31/08/2026). Sẽ gắn nhãn 200 review mới nhất |
| 5 | **Lát cắt MỘT CÂU** (1 người dùng · 1 việc · 1 quyết định AI · 1 kết quả) | Một hành khách · hỏi hỗ trợ nhà xe · AI quyết định trả lời bằng thông tin RAG có nguồn hay tạo ticket nháp cần người xử lý · khách nhận câu trả lời hoặc ticket để bổ sung và xác nhận gửi |
| 6 | AI tự làm đến đâu + 1 dòng lý do: sai thì ai chịu gì | AI trả lời giờ/giá/chính sách công khai có nguồn và soạn ticket nháp; nhân viên duyệt việc liên quan đến tiền, hoàn tiền, tranh chấp và giao dịch. AI không tự gửi ticket hoặc xử lý vé. Lý do: sai thông tin hay hứa hoàn tiền có thể khiến khách lỡ chuyến hoặc thiệt tiền |
| 7 | Phân công có tên | Bùi Đức Tuấn: spec, sơ đồ, ngưỡng đạt, slide · Đặng Đức Minh: code, nối model, chi phí · Trương Anh Đức: bằng chứng review, câu thử, metric, DATA_CARD |
| — | *(CP2)* Đã đổi gì so với CP1 | Mở từ sự cố đổi/huỷ/hoàn sang chatbot hỗ trợ chung có RAG; việc tiền và giao dịch luôn tạo ticket nháp cho người duyệt. Bằng chứng review 55/440 chỉ nói về một nhóm vấn đề, chưa chứng minh pain chung của chatbot. |
