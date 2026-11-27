# Chi phí khi dùng thật — Seed42

## Đầu vào và trạng thái đo

- Persona và số phiên trong [personas.yaml](personas.yaml): 50 phiên, seed 42. Tỷ lệ persona 50% / 30% / 20%, tần suất 1 / 2 / 3 phiên mỗi tháng và 1 / 2 / 3 lượt mỗi phiên đều **(tự ước tính)**. Các câu hỏi mô phỏng là tình huống tổng hợp, không phải lời khách thật.
- Quy mô 300 / 700 / 1.000 người dùng mỗi tháng (thấp / cơ sở / cao) đều **(tự ước tính)**; chưa có dữ liệu sử dụng của nhà xe. Không suy ra các số này từ 55/440 review vì số đó chỉ liên quan phàn nàn đổi, hủy và hoàn vé.
- Giá Standard USD trên 1 triệu token, không tính cache: gemini-3.1-flash-lite $0.25 vào / $1.50 ra; gemini-3-flash-preview $0.50 vào / $3.00 ra theo [bảng giá Gemini API](https://ai.google.dev/gemini-api/docs/pricing). Xem ngày 27/11/2026. Giá có thể thay đổi trước lúc chạy.
- **Đã kiểm kết nối model:** một lời gọi Gemini 3.1 Flash-Lite do thành viên nhóm chạy trả JSON với 13 token vào và 9 token ra theo usage của API. Đây chỉ là smoke test, không phải lượt eval hay mẫu mô phỏng chi phí.
- **Token cho mô phỏng: chưa có.** .env đã chọn Gemini 3.1 Flash-Lite và đã có key cục bộ (không commit); phần retrieval và benchmark trên nhánh Minh vẫn chưa tích hợp. Chế độ fake có token 0 nên không dùng làm bằng chứng chi phí.
- **Tỷ lệ đạt thực đo: chưa có.** Chưa có lượt eval model thật được chấm theo chuẩn §7. Vì vậy chưa thể tính chi phí / task thành công hay kết luận đáng triển khai.

## Kết quả mô phỏng

Chưa có lượt cost/simulate-N.csv hợp lệ. Sau khi tích hợp, chạy python run.py check, python run.py eval --try, python run.py eval, chấm và chạy python run.py score eval/run-N.csv, rồi python run.py simulate --rate-from eval/run-N.csv. Chép kết quả có run ID, model, token đo và tỷ lệ đạt vào đây; giữ nguyên mọi file run và trace đã sinh.

Nếu đo token bằng model khác hai model trong bảng giá, ghi rõ “đo token trên model X, tính giá model Y”; số token thật có thể khác giữa các model. Chi phí ngoài model (hạ tầng, lưu trữ, nhân viên duyệt) chưa được đo.
