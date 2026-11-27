# Đào data — cách đếm và kết quả

> Điền ở guide bước 1.2. Ôn lại: ngày 2, ngày 6 · lab ngày 2, lab ngày 6.
> Không đào data thì xoá file này. Script / công thức đếm để trong repo (vd `evidence/count.py` hoặc ghi công thức Sheets ngay dưới), người khác chạy lại phải ra cùng số.
> Repo chỉ chứa số đã tổng hợp và vài dòng ví dụ — không chép lại nguyên file data.

## 1. Cách đếm — viết TRƯỚC khi chạy

- Data dùng: review Google Play của app Vexere (`com.vexere.vexere`), tiếng Việt, https://play.google.com/store/apps/details?id=com.vexere.vexere&hl=vi&gl=VN. Khoảng ngày ghi sau khi lấy mẫu
- Đếm gì: số review theo nhãn `hoan_tien`, `doi_huy`, `nha_xe_doi`, `khac` · trên tập nào: 200 review mới nhất (sắp theo "Mới nhất") · lọc gì: không lọc, mọi mức sao
- **Mẫu số là gì:** N = mọi review đã đọc và gắn nhãn, kể cả review không liên quan *(lỗi hay gặp nhất là mẫu số sai)*
- Script / công thức: bảng gắn nhãn mỗi review một dòng (nguồn, ngày, số sao, trích tối đa 2 câu, nhãn), không chép tên người viết → `evidence/review_labels.csv` (cột `stt, ngay, so_sao, trich, nhan, ghi_chu`; nhiều nhãn cách nhau bằng `;`). Đếm: `python evidence/count_reviews.py` in x/N và % cho từng nhãn, N = mọi review đã gắn nhãn

**Bổ sung cách đếm, ghi 27/11/2026 18:50, trước khi thu mẫu 200 review mới nhất** (bài toán mở rộng sang hỗ trợ chung):
- Thêm hai nhãn: `thong_tin` = kể thông tin giờ chạy, giá, điểm đón, vé hoặc chính sách bị sai, thiếu, khó tìm · `ho_tro` = kể không liên hệ được, không được phản hồi hoặc không được giải quyết khi cần người hỗ trợ.
- Bốn nhãn cũ giữ nguyên nghĩa: `hoan_tien` = đòi hoặc hỏi tiền hoàn, trừ tiền không đúng · `doi_huy` = muốn đổi, huỷ vé hoặc không làm được · `nha_xe_doi` = nhà xe huỷ chuyến, đổi giờ, đổi điểm đón, không giữ chỗ · `khac` = không thuộc nhãn nào ở trên.
- Giả thuyết "hỗ trợ chung" bị coi là yếu nếu `thong_tin` hoặc `ho_tro` chỉ có dưới 5% review.
- Gắn nhãn: hai model gắn độc lập (Claude và một model OpenAI), ghi tỉ lệ khớp; dòng lệch ghi ở cột `ghi_chu` để người kiểm tay quyết.

## 2. Đọc trước, đếm sau

Trước khi ghi cách đếm đã xem sơ review ở thứ tự mặc định (đếm theo từ khoá, 55/440, không dùng làm bằng chứng nữa). Các kiểu thấy được: huỷ vé không được hoàn · nhà xe tự đổi giờ, điểm đón · không liên hệ được người hỗ trợ · lỗi đăng nhập.

## 3. Kết quả (mẫu 200 review mới nhất, 29/12/2025 đến 24/11/2026, thu ngày 27/11/2026)

Chạy lại: `python evidence/fetch_reviews.py com.vexere.vexere 200` → gắn nhãn → `python evidence/merge_labels.py` → `python evidence/count_reviews.py`.
Review mới đăng sẽ làm mẫu lấy lại khác đi; bảng đã gắn nhãn ở `evidence/review_labels.csv` là bản được đếm.

| Đếm gì | x / N | % | Ghi chú |
|---|---|---|---|
| `hoan_tien` | 21/200 | 10,5% | |
| `doi_huy` | 15/200 | 7,5% | |
| `nha_xe_doi` | 8/200 | 4,0% | Hai model lệch nhiều nhất (18 và 8) |
| `thong_tin` | 16/200 | 8,0% | |
| `ho_tro` | 18/200 | 9,0% | |
| `khac` | 137/200 | 68,5% | Gồm cả lời khen, lỗi đăng nhập |
| `chua_thong_nhat` | 14/200 | 7,0% | Chờ người kiểm tay |
| Có `thong_tin` hoặc `ho_tro` | 29/200 | 14,5% | |
| Có đổi, huỷ, hoàn hoặc nhà xe đổi | 28/200 | 14,0% | |
| Có ít nhất một nhãn đau | 49/200 | 24,5% | Trong 102 review 1 đến 3 sao là 46 |

Hai model gắn nhãn độc lập (Claude Sonnet và gpt-6.1-sol), khớp hoàn toàn 177/200 (88,5%). Nhãn chỉ tính khi cả hai cùng gắn.

**Kiểm tay** (ghi ở `evidence/hand_check.csv`, không sửa nhãn gốc): đã xem một số dòng, xác nhận #10, #117, #183 là vé máy bay, ngoài phạm vi. Sau khi bỏ 3 dòng này (giữ mẫu số 200): có nhãn đau 46/200 (23,0%); đổi, huỷ, hoàn 25/200; thông tin hoặc hỗ trợ 28/200. Cột `trich` chỉ giữ 2 câu đầu, kiểm nhãn phải đọc cả review.

## 4. ≥5 ví dụ cụ thể (số thứ tự trong `review_labels.csv`)

1. #3, 21/11/2026, 1 sao, `ho_tro`: "lúc cần gọi thì không có nhân viên trực tổng đài"
2. #4, 18/11/2026, 1 sao, `hoan_tien`, `doi_huy`: "lừa đảo không hoàn trièn vé và không đổi được vé"
3. #27, 26/09/2026, 1 sao, `thong_tin`: "Điểm trả thiếu, chọn điểm gần nhất thì chạy lên cao tốc không ghé được."
4. #43, 04/09/2026, 1 sao, `hoan_tien`, `doi_huy`: "Đặt xe hủy mà không hoàn tiền và không hỗ trợ đổi chuyến. Bị mất 100% phí xe."
5. #47, 31/08/2026, 1 sao, `nha_xe_doi`: "Tự ý đổi giờ chạy, điểm đón k qua đồng ý của khách."
6. #103, 30/05/2026, 1 sao, `thong_tin`: "mình đặt từ sân bay sân bay nhất đi Chu Lai nó báo cho mình đi Đà Nẵng luôn cấp 100 km"

## 5. Giới hạn của data

Một app đặt vé trung gian, không phải một nhà xe. Người viết review thường đang bực hoặc rất hài lòng (89 review 1 sao, 89 review 5 sao). Data không cho biết mỗi lần mất bao lâu và vì sao khách không tự tìm được câu trả lời. Nhãn do model gắn.
→ Kiểm lại bằng phỏng vấn ít nhất 3 người từng đi xe khách đặt qua app trước CP3.
