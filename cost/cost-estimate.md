# Chi phí khi dùng thật — Seed42

## Đầu vào và trạng thái đo

- Persona và số phiên trong [personas.yaml](personas.yaml): 50 phiên, seed 42. Tỷ lệ persona 50% / 30% / 20%, tần suất 1 / 2 / 3 phiên mỗi tháng và 1 / 2 / 3 lượt mỗi phiên đều **(tự ước tính)**. Các câu hỏi mô phỏng là tình huống tổng hợp, không phải lời khách thật.
- Quy mô 300 / 700 / 1.000 người dùng mỗi tháng (thấp / cơ sở / cao) đều **(tự ước tính)**; chưa có dữ liệu sử dụng của nhà xe. Không suy ra các số này từ 55/440 review vì số đó chỉ liên quan phàn nàn đổi, hủy và hoàn vé.
- Giá Standard USD trên 1 triệu token, không tính cache: model được chọn `gemini-3.5-flash-lite` $0.30 vào / $2.50 ra; đối chiếu `gemini-3.1-flash-lite` $0.25 vào / $1.50 ra theo [bảng giá Gemini API](https://ai.google.dev/gemini-api/docs/pricing). Xem ngày 28/11/2026. Giá có thể thay đổi trước lúc chạy.
- **Đã kiểm kết nối model:** một lời gọi Gemini 3.1 Flash-Lite do thành viên nhóm chạy trả JSON với 13 token vào và 9 token ra theo usage của API. Đây chỉ là smoke test, không phải lượt eval hay mẫu mô phỏng chi phí.
- **Token eval thật, tách khỏi mô phỏng:** lượt `run-1@20261128-013111` có 14/30 câu nhận output của Gemini 3.1 Flash-Lite, tổng 9.292 token vào và 2.400 token ra theo usage API. 16 câu lỗi kỹ thuật không có token usage được ghi. Lượt thử mô phỏng 10 phiên dùng model 3.5 và được tính riêng bên dưới.
- **Tỷ lệ đạt:** lượt 1 trên Gemini 3.1 Flash-Lite là 12/30 (40,0%) với 16 lỗi API; lượt 2 và 3 trên Gemini 3.5 Flash-Lite lần lượt là 21/30 (70,0%) và 19/30 (63,3%), đều không lỗi API nhưng đều chưa qua chuẩn §7 vì thấp hơn 80% và `tu_choi` không đạt 100%. Không gán chênh lệch giữa lượt 1 và lượt 2 cho một nguyên nhân duy nhất: model và điều kiện gọi API đều thay đổi. Xem `eval/report.md`.

## Kết quả mô phỏng

Lượt thử `simulate-try@20261128-015325` đã chạy 10 phiên với Gemini 3.5 Flash-Lite, không có phiên lỗi: tổng **10.285 token vào, 2.313 token ra** theo usage API (trung bình 1.029 / 231 token mỗi phiên). Theo giá Standard đã kiểm, chi phí model cho 10 phiên là **$0.00887**, trung bình **$0.000887 / phiên**. Đây là phép tính lại trên token của lượt thử, vì file tóm tắt tự sinh trước khi cập nhật `cost/personas.yaml` vẫn ghi bảng giá 3.1 Flash-Lite và 3 Flash Preview. Không sửa file tóm tắt đã sinh.

Chưa có lượt `cost/simulate-N.csv` ≥50 phiên, nên chưa dùng 10 phiên thử để kết luận chi phí theo persona hoặc tháng. Bước CP4: chạy `python run.py simulate --rate-from eval/run-3.csv --wait 10` sau khi cấu hình giá mới; chi phí / task thành công sẽ dùng tỷ lệ đạt thực đo 19/30 của cùng model, nhưng chỉ nên coi là kịch bản vì chất lượng chưa qua chuẩn.

Nếu đo token bằng model khác hai model trong bảng giá, ghi rõ “đo token trên model X, tính giá model Y”; số token thật có thể khác giữa các model. Chi phí ngoài model (hạ tầng, lưu trữ, nhân viên duyệt) chưa được đo.
