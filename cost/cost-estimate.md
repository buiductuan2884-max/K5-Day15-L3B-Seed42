# Chi phí khi dùng thật — Seed42

## Đầu vào và trạng thái đo

- Persona và số phiên trong [personas.yaml](personas.yaml): 50 phiên, seed 42. Tỷ lệ persona 50% / 30% / 20%, tần suất 1 / 2 / 3 phiên mỗi tháng và 1 / 2 / 3 lượt mỗi phiên đều **(tự ước tính)**. Các câu hỏi mô phỏng là tình huống tổng hợp, không phải lời khách thật.
- Quy mô 300 / 700 / 1.000 người dùng mỗi tháng (thấp / cơ sở / cao) đều **(tự ước tính)**; chưa có dữ liệu sử dụng của nhà xe. Không suy ra các số này từ 55/440 review vì số đó chỉ liên quan phàn nàn đổi, hủy và hoàn vé.
- Giá chuẩn USD trên 1 triệu token, không tính cache: gpt-5.4-mini $0.75 vào / $4.50 ra theo [trang model OpenAI](https://developers.openai.com/api/docs/models/gpt-5.4-mini); gpt-6.2-sol $2.00 vào / $10.00 ra theo [bảng giá OpenAI](https://developers.openai.com/api/docs/pricing). Xem ngày 27/11/2026. Giá có thể thay đổi trước lúc chạy.
- **Token thực đo: chưa có.** .env chưa cấu hình provider/key và phần retrieval, benchmark, metric của nhóm khác vẫn là bản khung. Chế độ fake có token 0 nên không dùng làm bằng chứng chi phí.
- **Tỷ lệ đạt thực đo: chưa có.** Chưa có lượt eval model thật được chấm theo chuẩn §7. Vì vậy chưa thể tính chi phí / task thành công hay kết luận đáng triển khai.

## Kết quả mô phỏng

Chưa có lượt cost/simulate-N.csv hợp lệ. Sau khi tích hợp, chạy python run.py check, python run.py eval --try, python run.py eval, chấm và chạy python run.py score eval/run-N.csv, rồi python run.py simulate --rate-from eval/run-N.csv. Chép kết quả có run ID, model, token đo và tỷ lệ đạt vào đây; giữ nguyên mọi file run và trace đã sinh.

Nếu đo token bằng model khác hai model trong bảng giá, ghi rõ “đo token trên model X, tính giá model Y”; số token thật có thể khác giữa các model. Chi phí ngoài model (hạ tầng, lưu trữ, nhân viên duyệt) chưa được đo.
