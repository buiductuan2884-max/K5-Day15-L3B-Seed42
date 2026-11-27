# Chi phí khi dùng thật — Seed42

## Đầu vào và trạng thái đo

- Persona và số phiên trong [personas.yaml](personas.yaml): 50 phiên, seed 42. Tỷ lệ persona 50% / 30% / 20%, tần suất 1 / 2 / 3 phiên mỗi tháng và 1 / 2 / 3 lượt mỗi phiên đều **(tự ước tính)**. Các câu hỏi mô phỏng là tình huống tổng hợp, không phải lời khách thật.
- Quy mô 300 / 700 / 1.000 người dùng mỗi tháng (thấp / cơ sở / cao) đều **(tự ước tính)**; chưa có dữ liệu sử dụng của nhà xe. Không suy ra các số này từ 55/440 review vì số đó chỉ liên quan phàn nàn đổi, hủy và hoàn vé.
- Giá Standard USD trên 1 triệu token, không tính cache: gemini-3.1-flash-lite $0.25 vào / $1.50 ra; gemini-3-flash-preview $0.50 vào / $3.00 ra theo [bảng giá Gemini API](https://ai.google.dev/gemini-api/docs/pricing). Xem ngày 27/11/2026. Giá có thể thay đổi trước lúc chạy.
- **Đã kiểm kết nối model:** một lời gọi Gemini 3.1 Flash-Lite do thành viên nhóm chạy trả JSON với 13 token vào và 9 token ra theo usage của API. Đây chỉ là smoke test, không phải lượt eval hay mẫu mô phỏng chi phí.
- **Token eval thật, chưa phải token mô phỏng:** lượt `run-1@20261128-013111` có 14/30 câu nhận output của Gemini 3.1 Flash-Lite, tổng 9.292 token vào và 2.400 token ra theo usage API. 16 câu lỗi kỹ thuật không có token usage được ghi. Chưa có file `cost/simulate-try.csv` hoặc lượt mô phỏng đầy đủ, nên không dùng số eval thay chi phí phiên/persona.
- **Tỷ lệ đạt lượt 1:** 12/30 (40,0%), gồm 16 lỗi API và 2 câu trả lời trượt; `tu_choi` chỉ 1/6. Đây là tỷ lệ đạt của lượt chạy có lỗi, chưa phải ước lượng chất lượng khi API ổn định. Xem `eval/report.md`. Chưa thể tính chi phí / task thành công đáng tin cậy hay kết luận đáng triển khai.

## Kết quả mô phỏng

Chưa có lượt `cost/simulate-N.csv` hợp lệ. Sau khi có lượt eval được chấm với API ổn định, chạy `python run.py simulate --try --wait 10`, rồi `python run.py simulate --rate-from eval/run-N.csv --wait 10`. Ghi run ID, model, token đo và tỷ lệ đạt; giữ nguyên mọi file run và trace đã sinh.

Nếu đo token bằng model khác hai model trong bảng giá, ghi rõ “đo token trên model X, tính giá model Y”; số token thật có thể khác giữa các model. Chi phí ngoài model (hạ tầng, lưu trữ, nhân viên duyệt) chưa được đo.
