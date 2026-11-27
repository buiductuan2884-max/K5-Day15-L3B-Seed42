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

Đã đọc __ dòng đầu và từ điển cột. Các *kiểu* hành vi thấy được (trước khi định nghĩa thứ cần đếm):
- __
- __

## 3. Kết quả

| Đếm gì | x / N | % | Ghi chú |
|---|---|---|---|
| | | | |
| | | | |

Ghi dạng "x/N (y%)". "Nhiều bạn…" không phải số.

## 4. ≥5 ví dụ cụ thể (mã dòng / mã đã ẩn danh, không đoán ai là ai)

1.
2.
3.
4.
5.

## 5. Giới hạn của data

Data cho biết người ta **làm gì**, không cho biết **vì sao**. Thiếu gì, lệch về phía nào: __
→ Kiểm lại bằng phỏng vấn / khảo sát nào: __
