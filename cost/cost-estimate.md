# Chi phí khi dùng thật — Seed42

## Đầu vào và trạng thái đo

- Persona và số phiên trong [personas.yaml](personas.yaml): 50 phiên, seed 42. Tỷ lệ persona 50% / 30% / 20%, tần suất 1 / 2 / 3 phiên mỗi tháng và 1 / 2 / 3 lượt mỗi phiên đều **(tự ước tính)**. Các câu hỏi mô phỏng là tình huống tổng hợp, không phải lời khách thật.
- Quy mô 300 / 700 / 1.000 người dùng mỗi tháng (thấp / cơ sở / cao) đều **(tự ước tính)**; chưa có dữ liệu sử dụng của nhà xe. Không suy ra các số này từ số review đã đếm trong `evidence/`.
- Giá Standard USD trên 1 triệu token, không tính cache: model được chọn `gemini-3.5-flash-lite` $0.30 vào / $2.50 ra; đối chiếu `gemini-3.1-flash-lite` $0.25 vào / $1.50 ra theo [bảng giá Gemini API](https://ai.google.dev/gemini-api/docs/pricing). Xem ngày 28/11/2026. Giá có thể thay đổi trước lúc chạy.
- **Đã kiểm kết nối model:** một lời gọi Gemini 3.1 Flash-Lite do thành viên nhóm chạy trả JSON với 13 token vào và 9 token ra theo usage của API. Đây chỉ là smoke test, không phải lượt eval hay mẫu mô phỏng chi phí.
- **Token eval thật, tách khỏi mô phỏng:** lượt `run-1@20261128-013111` có 14/30 câu nhận output của Gemini 3.1 Flash-Lite, tổng 9.292 token vào và 2.400 token ra theo usage API. 16 câu lỗi kỹ thuật không có token usage được ghi. Lượt thử mô phỏng 10 phiên dùng model 3.5 và được tính riêng bên dưới.
- **Tỷ lệ đạt:** lượt 1 trên Gemini 3.1 Flash-Lite là 12/30 (40,0%) với 16 lỗi API; lượt 2–5 trên Gemini 3.5 Flash-Lite lần lượt là 21/30, 19/30, 28/30 và **30/30**, đều không lỗi API. Lượt 5 qua chuẩn §7 trên bộ câu thử dựng. Không gán chênh lệch giữa lượt 1 và lượt 2 cho một nguyên nhân duy nhất: model và điều kiện gọi API đều thay đổi. Xem `eval/report.md`.

## Kết quả mô phỏng

### Số nộp CP4: `simulate-2@20261128-045850`, tỷ lệ đạt lượt 2

50 phiên thật qua API Gemini 3.5 Flash-Lite, seed 42, `python run.py simulate --rate-from eval/run-2.csv --wait 10`: 0 phiên lỗi, 74.656 token vào, 13.216 token ra. Tỷ lệ đạt **21/30 (70%)** của `run-2@20261128-014202`. Dữ liệu: [simulate-2.csv](simulate-2.csv), tóm tắt tự sinh: [simulate-2-summary.md](simulate-2-summary.md).

| Model dùng để tính giá | Chi phí / phiên | Chi phí / task thành công | Chi phí / câu hỏi đạt | Tháng thấp (300 người) | Tháng cơ sở (700 người) | Tháng cao (1.000 người) |
|---|---:|---:|---:|---:|---:|---:|
| Gemini 3.5 Flash-Lite | $0.0011 | **$0.0016** | $0.00089 | $0.6377 | $1.49 | $2.13 |
| Gemini 3.1 Flash-Lite (áp giá lên token 3.5) | $0.00077 | $0.0011 | $0.00062 | $0.4420 | $1.03 | $1.47 |

Lượt 2 chạy trước các sửa prompt sau đó, còn token đo bằng code hiện tại; dùng tỷ lệ này vì đề yêu cầu và vì nó thận trọng hơn. Phần dưới giữ số theo lượt 5 để đối chiếu.

### Đối chiếu: lượt thử và mô phỏng theo lượt 5

Lượt thử `simulate-try@20261128-015325` đã chạy 10 phiên với Gemini 3.5 Flash-Lite, không có phiên lỗi: tổng **10.285 token vào, 2.313 token ra** theo usage API (trung bình 1.029 / 231 token mỗi phiên). Theo giá Standard đã kiểm, chi phí model cho 10 phiên là **$0.00887**, trung bình **$0.000887 / phiên**. Đây là phép tính lại trên token của lượt thử, vì file tóm tắt tự sinh trước khi cập nhật `cost/personas.yaml` vẫn ghi bảng giá 3.1 Flash-Lite và 3 Flash Preview. Không sửa file tóm tắt đã sinh. Lượt thử này chạy **trước** các sửa prompt dẫn tới eval 4–5, nên token/phiên của phiên bản hiện tại cần đo lại.

Lượt CP4 [`simulate-1@20261128-024823`](simulate-1-summary.md) chạy **50 phiên thật qua API Gemini 3.5 Flash-Lite**, seed 42, bằng `python run.py simulate --rate-from eval/run-5.csv --wait 10`: 0 phiên lỗi, 74.656 token vào và 12.995 token ra theo usage API. Tỷ lệ đạt dùng để tính là **30/30 (100%)** của `run-5@20261128-022132` trên cùng model và bộ câu thử dựng. Đây là tỷ lệ đạt của benchmark, không phải tỷ lệ thành công đo ở 50 hành khách thật. Dữ liệu từng phiên ở [`simulate-1.csv`](simulate-1.csv); trace được giữ nguyên ở `traces/simulate-1.jsonl`.

| Persona | Số phiên | Lượt hỏi / phiên | Token vào / phiên | Token ra / phiên | Gọi model / phiên | Gọi công cụ / phiên |
|---|---:|---:|---:|---:|---:|---:|
| `hoi_thong_tin` | 22 | 1 | 1.046 | 174 | 1,0 | 1,0 |
| `can_lam_ro` | 17 | 2 | 1.570 | 275 | 2,0 | 2,0 |
| `can_nhan_vien` | 11 | 3 | 2.270 | 408 | 3,0 | 6,0 |

Giá sau đây là **giá cấu hình trong `cost/personas.yaml` ngày 28/11/2026**, không phải hóa đơn đã thanh toán. Token được đo trên Gemini 3.5 Flash-Lite; dòng Gemini 3.1 chỉ áp giá khác cho cùng lượng token, nên có thể lệch nếu chạy model đó thật. Chi phí model tính từ token đo được của 50 phiên theo giá cấu hình 3.5 là **$0.0548843**, trung bình **$0.001097686/phiên**; bảng tóm tắt làm tròn.

| Model dùng để tính giá | Chi phí / phiên | Chi phí / task thành công* | Chi phí / câu hỏi đạt* | Tháng thấp (300 người) | Tháng cơ sở (700 người) | Tháng cao (1.000 người) |
|---|---:|---:|---:|---:|---:|---:|
| Gemini 3.5 Flash-Lite | $0.0011 | $0.0011 | $0.00062 | $0.6271 | $1.46 | $2.09 |
| Gemini 3.1 Flash-Lite (áp giá lên token 3.5) | $0.00076 | $0.00076 | $0.00043 | $0.4356 | $1.02 | $1.45 |

\* Chia chi phí theo tỷ lệ benchmark 30/30 và trung bình 1,8 lượt hỏi/phiên; không khẳng định 100% task thật sẽ thành công. Quy mô 300/700/1.000 người và tần suất dùng theo persona là **(tự ước tính)**. §2 của `spec.md` ước tính khoảng 42 phút/tháng trong tập người viết review, còn bảng này tính tiền cho một quy mô người dùng giả định khác; chưa có thời gian tiết kiệm được đo, nên **chưa kết luận hiệu quả kinh tế hay lợi ích trên mỗi người**. Chi phí hạ tầng, lưu trữ và nhân viên duyệt chưa được đo.

Nếu đo token bằng model khác hai model trong bảng giá, ghi rõ “đo token trên model X, tính giá model Y”; số token thật có thể khác giữa các model. Chi phí ngoài model (hạ tầng, lưu trữ, nhân viên duyệt) chưa được đo.
