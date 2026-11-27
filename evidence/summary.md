# Tổng hợp bằng chứng pain — CP3

> Nguồn chính: 200 review Google Play mới nhất của app Vexere (29/12/2025–24/11/2026), cách lấy, gắn nhãn và đếm ở [data-mining.md](data-mining.md). Đây là người dùng app trung gian, không phải khách của nhà xe mẫu.

## 1. Nguồn đã dùng

| Nguồn | Trạng thái | File |
|---|---|---|
| Đào data | 200 review, có cách đếm và ví dụ; hai model gắn nhãn, mới kiểm tay 4 dòng | [data-mining.md](data-mining.md), [review_labels.csv](review_labels.csv), [hand_check.csv](hand_check.csv) |
| Phỏng vấn | Chưa thực hiện; nhóm xác nhận ngày 28/11/2026 | — |
| Khảo sát | Chưa có câu trả lời; [bộ câu hỏi](survey/questions.md) chưa tạo thành số liệu | — |

## 2. Số chính và cách hiểu

- 49/200 review (24,5%) mang ít nhất một nhãn vấn đề; 29/200 (14,5%) nhắc thông tin hoặc hỗ trợ, 28/200 (14,0%) nhắc đổi, hủy, hoàn hoặc nhà xe đổi chuyến. Hai nhóm chồng nhau ở 8 review. Đây là nhãn **hai model cùng đồng ý**; độ khớp toàn bộ hai bộ nhãn là 177/200 (88,5%), chưa phải kết quả kiểm tay toàn bộ.
- Kiểm tay đã xác nhận ba dòng trong nhóm vấn đề (#10, #117, #183) là vé máy bay, ngoài lát cắt xe khách. Bỏ ba dòng đó và giữ mẫu số 200 còn **46/200 (23,0%)** review nêu ít nhất một vấn đề trong phạm vi rộng. 14/200 dòng chưa thống nhất nhãn vẫn cần người xem.
- Review không đo số người dùng thật của nhà xe, số lần gặp vấn đề mỗi tháng, thời gian mất mỗi lần, hay tác động của trợ lý. Không dùng 46/200 làm tỷ lệ toàn bộ hành khách gặp pain.

## 3. Năm ví dụ nguyên văn, bỏ tên

1. “lúc cần gọi thì không có nhân viên trực tổng đài” — [review #3](review_labels.csv), 21/11/2026, nhãn `ho_tro`.
2. “Điểm trả thiếu, chọn điểm gần nhất thì chạy lên cao tốc không ghé được.” — [review #27](review_labels.csv), 26/09/2026, nhãn `thong_tin`.
3. “Đặt xe hủy mà không hoàn tiền và không hỗ trợ đổi chuyến. Bị mất 100% phí xe.” — [review #43](review_labels.csv), 04/09/2026, nhãn `hoan_tien;doi_huy`.
4. “Tự ý đổi giờ chạy, điểm đón k qua đồng ý của khách.” — [review #47](review_labels.csv), 31/08/2026, nhãn `hoan_tien;doi_huy;nha_xe_doi;ho_tro`.
5. “tôi nhập địa điểm đón và trả rồi, nhưng app trả lại địa chỉ mặc định mà ko có cảnh báo nào trên app, thông tin vé qua email cũng ko có địa điểm đón và trả.” — [review #114](review_labels.csv), 29/04/2026, nhãn `thong_tin`.

Mỗi trích dẫn là toàn bộ hoặc một đoạn liên tiếp trong cột `trich` của dòng được nêu; bảng giữ số thứ tự, ngày, nhãn và không giữ tên người viết.

## 4. Các nguồn có khớp nhau không

Chưa có phỏng vấn hoặc khảo sát để đối chiếu. Review cho thấy có phàn nàn về thông tin chuyến và khả năng tiếp cận hỗ trợ, đồng thời có nhiều vấn đề giao dịch cần người kiểm tra. Không thể từ review kết luận khách muốn dùng trợ lý này, cách họ sẽ dùng, hoặc nó tiết kiệm bao nhiêu thời gian.

## 5. Kết luận

Giả thuyết về **sự tồn tại** của pain thông tin/hỗ trợ được mẫu review ủng hộ ở mức mô tả; giả thuyết “không biết gửi đủ thông tin cho nhân viên” và lợi ích của ticket nháp **chưa được kiểm**. Trước khi tính impact theo phút hoặc quyết định triển khai, cần hỏi hành khách thật và đo thời gian xử lý, đồng thời kiểm tay các nhãn còn mâu thuẫn.
