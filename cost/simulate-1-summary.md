# Tóm tắt mô phỏng simulate-1@20261128-024823

Do `python run.py simulate` sinh ra — không sửa tay. Chép bảng sang `cost/cost-estimate.md`.

| Persona | Số phiên mô phỏng | Lượt hỏi / phiên | Token vào / phiên | Token ra / phiên | Gọi model / phiên | Gọi công cụ / phiên |
|---|---:|---:|---:|---:|---:|---:|
| hoi_thong_tin | 22 | 1 | 1046 | 174 | 1.0 | 1.0 |
| can_lam_ro | 17 | 2 | 1570 | 275 | 2.0 | 2.0 |
| can_nhan_vien | 11 | 3 | 2270 | 408 | 3.0 | 6.0 |

Tỉ lệ đạt dùng để tính: 30/30 (100%) — lượt run-5@20261128-022132

- Tỉ lệ đạt lấy từ lượt nhóm chọn: eval/run-5.csv (--rate-from).

| Model (giá) | Chi phí / phiên | Chi phí / task thành công | Chi phí / câu hỏi đạt | Chi phí / tháng — thấp (300 người) | Chi phí / tháng — cơ sở (700 người) | Chi phí / tháng — cao (1.000 người) | Chi phí / người / tháng (cơ sở) |
|---|---:|---:|---:|---:|---:|---:|---:|
| gemini-3.5-flash-lite (vào 0.3 · ra 2.5 $/1M) | $0.0011 | $0.0011 | $0.00062 | $0.6271 | $1.46 | $2.09 | $0.0021 |
| gemini-3.1-flash-lite (vào 0.25 · ra 1.5 $/1M) | $0.00076 | $0.00076 | $0.00043 | $0.4356 | $1.02 | $1.45 | $0.0015 |

- Chi phí / task thành công = chi phí / phiên ÷ tỉ lệ đạt. Chi phí / câu hỏi đạt = chi phí / phiên ÷ số lượt hỏi trung bình mỗi phiên (1.8) ÷ tỉ lệ đạt — tỉ lệ đạt đo theo từng câu thử.
- Token đo trên model: gemini-3.5-flash-lite. Giá tính theo từng model trong bảng — model khác bộ tách token thì số token thật có thể lệch; ghi rõ "đo trên model X, tính giá model Y" trong cost/cost-estimate.md.
- Phiên lỗi (không tính vào trung bình): 0/50.
