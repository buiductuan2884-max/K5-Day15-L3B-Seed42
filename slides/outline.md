# Dàn slide → lấy số từ file nào

> Làm ở guide bước 5.1. Luật: **không có bằng chứng thì không có slide** — mỗi trang ≥1 con số / trích dẫn có nguồn / kết quả đo.
> Xuất PDF thành `demo-slides.pdf` ở thư mục gốc repo, nộp tại CP4 14:30 Thứ Bảy 28/11. Nộp PDF, không nộp link.

| # | Trang | Có gì | Số lấy từ | Xong |
|---|---|---|---|---|
| 1 | Người dùng & pain | Ai · việc gì · chỗ đau + số và trích dẫn | `evidence/summary.md` | ☐ |
| 2 | Vì sao chọn bài này | Bảng impact rút gọn + hướng bị loại | `spec.md` §2 | ☐ |
| 3 | Giải pháp | Lát cắt một câu · sơ đồ · AI tự làm đến đâu, vì sao | `spec.md` §4 | ☐ |
| 4 | Demo live | 1 trường hợp thường + 1 trường hợp khó (lấy từ bộ câu thử); mạng hỏng → video dự phòng | `eval/benchmark.csv` | ☐ |
| 5 | **Đánh giá thế nào** | Dataset · bộ câu thử · metric · lượt 1 → lượt 2 so với chuẩn "đạt" (kèm run ID) · lỗi chính | `eval/README.md`, `eval/report.md` | ☐ |
| 6 | **Chi phí khi dùng thật** | Chi phí / task thành công · 3 kịch bản · so với impact | `cost/cost-estimate.md` | ☐ |
| 7 | Kết luận | Go / iterate / stop — dẫn số ở trang 1, 5, 6 | — | ☐ |
| 8 | Nếu có thêm 1 tuần | 2–3 việc, trỏ về lỗi còn lại / phản hồi người dùng | `eval/report.md` mục 4 · `validation/log.md` | ☐ |

**Trước khi lên:** tải repo về một máy khác (hoặc thư mục mới), chạy theo mục "Chạy trong 3 phút" của `README.md` · `.env` có trên máy demo, đã gọi thử 1 câu trong vòng 1 giờ trước giờ demo · video dự phòng mở được bằng cửa sổ ẩn danh · biết bản chạy thử sẽ làm gì với **1 câu thử lạ** của giám khảo.

Ai nói trang nào (mỗi người ≥1 phần):

| Trang | Người nói |
|---|---|
| 1, 2, 3, 7 | Bùi Đức Tuấn |
| 4, 6 | Đặng Đức Minh |
| 5, 8 | Trương Anh Đức |

## Nội dung nháp

Chỗ ghi `[chờ ...]` điền khi có số thật.

**1. Người dùng và pain.** Hành khách đặt vé xe qua app. 49/200 review Vexere mới nhất nêu vấn đề (thông tin hoặc hỗ trợ 29, đổi, huỷ, hoàn 28, trùng 8); hai model gắn nhãn, kiểm tay một phần; bỏ 3 review vé máy bay còn 46/200. Trích: "lúc cần gọi thì không có nhân viên trực tổng đài" (1 sao, 21/11/2026).

**2. Vì sao chọn.** Hướng rộng gồm trọn nhóm đổi, huỷ, hoàn và thêm 21/200 review về thông tin, hỗ trợ. Loại: chỉ tra thông tin (16/200, không chuyển được việc cần người), gỡ lỗi đăng nhập (phải sửa hệ thống thật). Impact theo thời gian: [chờ hỏi ≥3 người].

**3. Giải pháp.** Khách hỏi → tra dữ liệu có nguồn → LLM chọn trả lời, hỏi thêm, hoặc ticket nháp. Việc về tiền, giao dịch, tranh chấp do nhân viên quyết. Sơ đồ ở `spec.md` §4.

**4. Demo.** Ca thường: hỏi giờ chạy một tuyến mẫu. Ca khó: xin hoàn tiền một vé → ticket nháp, khách sửa. Mạng hỏng: video dự phòng.

**5. Đánh giá.** Chuẩn đạt theo `spec.md` §7. [chờ số câu thử, metric, lượt 1 → lượt 2, lỗi chính]

**6. Chi phí.** [chờ mô phỏng: chi phí / task thành công, 3 kịch bản] · [chờ impact đo được].

**7. Kết luận.** [chờ lượt 2: go, iterate hay stop]

**8. Thêm 1 tuần.** Nút chọn nhanh khi trợ lý hỏi lại. [chờ lỗi còn lại và phản hồi người dùng thử]
