# Khảo sát: lần gần nhất đặt vé xe khách

- Câu hỏi đầy đủ: [create_form.gs](create_form.gs) (script tạo đúng Google Form đã gửi).
- Người trả lời đúng đối tượng: có đặt vé xe khách trong 6 tháng qua (câu 1 lọc), không phải thành viên nhóm.
- Ngưỡng: ít nhất 20 người. Dưới khoảng 10 người chỉ ghi x/n, không ghi %.
- Kênh đã gửi: ____ · Giờ mở: ____ · Giờ chốt: ____

## Cách đếm, ghi trước khi mở form

Mẫu số N = số người trả lời "Có" ở câu 1.

| Số | Cách tính |
|---|---|
| Có việc phải xử lý | người chọn ít nhất một mục khác "Không cần gì thêm" ở câu 4, chia N |
| Thời gian mỗi lần | phân bố câu 6 trong nhóm có việc phải xử lý; báo khoảng chứa trung vị |
| Không xong | "Xong một phần" cộng "Không xong" ở câu 7, chia nhóm có việc phải xử lý |
| Số lần | phân bố câu 8 |

Giả thuyết bị coi là yếu nếu dưới 20% người trả lời có việc phải xử lý.

Bản xuất đã xoá cột nhận ra người trả lời lưu ở `results.csv`.
