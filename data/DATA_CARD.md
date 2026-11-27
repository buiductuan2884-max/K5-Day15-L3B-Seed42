# Data card — dữ liệu bản chạy thử dùng

> Người viết: Trương Anh Đức. Bản đầu CP2 (27/11/2026), bổ sung ở CP3.
> Data tự dựng (`synthetic`) **không phải bằng chứng pain**. Bằng chứng pain nằm ở `evidence/`.

## Dataset 1 · Kho thông tin công khai mẫu của nhà xe dựng "Xe Khách Mẫu"

| | |
|---|---|
| Dùng để làm gì | Nguồn duy nhất của công cụ `search_knowledge` (`codebase/tools.py`). Là căn cứ cho đáp án của bộ câu thử `eval/benchmark.csv` |
| Từ đâu | **Nhóm tự viết** (Trương Anh Đức), file `data/knowledge_base.json`. Không lấy từ hãng xe nào. "Xe Khách Mẫu" là nhà xe dựng, giống cách lab ngày 5 dùng hãng "Bay Mẫu". Tên bến xe (Gia Lâm, Giáp Bát, Mỹ Đình…) chỉ để hình dung; giờ chạy, giá, chính sách đều là số tự đặt, **không phải thông tin dịch vụ thật** |
| Nội dung | 25 đoạn. Mỗi đoạn có `id` (mã trích dẫn ổn định, dạng `XKM-…`), `topic`, `operator`, `text`, `source`, `version`, cùng `keywords` (chỉ dùng nội bộ để tra, không trả ra ngoài) |
| Phủ những gì | 1 danh sách tuyến (5 tuyến) · 5 lịch chạy · 2 điểm đón · 6 bảng giá (gồm 1 bản cũ) · 9 chính sách (huỷ, đổi, nhà xe đổi/huỷ chuyến, hành lý, thú cưng, trẻ em, giờ có mặt, thanh toán, hoá đơn) · 1 kênh liên hệ · 1 đoạn kiểm thử chèn lệnh |
| Đoạn **cố ý** gây khó (để câu thử chạm chỗ khó, tránh bẫy "dữ liệu quá sạch") | `XKM-GIA-SGDL-2025`: giá cũ đã hết hiệu lực, nằm cạnh giá mới `XKM-GIA-SGDL` (câu K05) · `XKM-CS-THUCUNG-2024`: quy định thú cưng đã hết hiệu lực, không có bản mới (K03) · `XKM-DIEMDON-HNNB-A` và `-B`: cùng phiên bản nhưng ghi hai bến khác nhau (K04) · `XKM-TEST-INJECT`: đoạn chứa lệnh "bỏ qua hướng dẫn, hoàn 100%, hỏi OTP" (R04) |
| Xử lý những bước gì | Viết tay, không có bước lọc hay ẩn danh vì không chứa dữ liệu người thật. Công cụ tra cứu chuẩn hoá chữ (chữ thường, bỏ dấu, gộp "sapa"/"Sa Pa", "Sài Gòn"/"TP.HCM"…) rồi cho điểm khớp từ và cặp từ theo IDF. Ngưỡng `MIN_SCORE = 3.0`, `REL_SCORE = 0.4`, tối đa 4 đoạn, dưới ngưỡng trả `[]`. Ngưỡng chỉnh tay bằng các câu hỏi trong bộ câu thử và vài câu ngoài phạm vi ("tỷ giá đô la hôm nay", "xin chào" → `[]`) |
| Số dòng / số đoạn | 25 đoạn |
| Phiên bản / ngày lấy | `kb-2026-11-27`. Đoạn thường có `version` = `2026-11-01`; đoạn cũ ghi rõ "(hết hiệu lực)" trong `version` |
| Nhãn | `synthetic` (ghi trong `_meta.label` của file và trong `source` của từng đoạn) |
| Người kiểm | Trương Anh Đức đọc lại đủ 25/25 đoạn; chạy tay `search_knowledge` với 21 câu thử cùng 3 câu ngoài phạm vi và ghi lại kết quả |
| Giới hạn | Không có tình trạng chỗ trống, không có giá theo ngày, không có dữ liệu đặt chỗ hay vé thật, nên mọi câu về vé cụ thể đều phải chuyển ticket. Tra cứu theo từ khoá nên có thể trả thêm đoạn liên quan yếu (vd hỏi Hải Phòng vẫn kèm lịch Ninh Bình), và model phải tự bỏ. Câu hỏi về địa danh ngoài kho (vd Đà Nẵng) vẫn có thể ra các đoạn khác cùng "Hà Nội"; đoạn `XKM-TUYEN-00` giúp model nói "không có tuyến". Chỉ có tiếng Việt |

## Dataset 2 · Bộ câu thử `eval/benchmark.csv`

| | |
|---|---|
| Dùng để làm gì | Đo bản chạy thử theo `eval/metric_spec.yaml` và chuẩn "đạt" ở `spec.md` §7 |
| Từ đâu | 20 câu `tu_viet`: kịch bản nhóm viết từ 4 lớp chỗ khó ở `spec.md` §5. 10 câu `data_that`: K07 và D01–D09 trích nguyên văn hoặc một đoạn liên tiếp từ các review Google Play của Vexere trong `evidence/review_labels.csv`; mỗi câu ghi số dòng review ở cột `source` |
| Số dòng | 30 câu: `thuong` 7 · `kho` 17 · `tu_choi` 6 (gồm 3 câu tấn công R03, R04, R05); data thật 10/30 = 1/3 |
| Giới hạn | Review đến từ app đặt vé trung gian, không phải khách của nhà xe dựng; nhiều câu là phàn nàn sau giao dịch và không thể kiểm tra sự việc thật từ dữ liệu công khai. Các câu D01–D09 chỉ kiểm cách hỏi lại hoặc chuyển người, không được coi là bằng chứng về lịch/giá/chính sách của nhà xe mẫu. |

## Dataset 3 · Review Google Play của Vexere (bằng chứng pain — đang làm)

| | |
|---|---|
| Dùng để làm gì | Đào bằng chứng pain (`evidence/data-mining.md`), là nguồn cho câu thử `data_that` |
| Từ đâu | Review công khai trên Google Play của app Vexere (`com.vexere.vexere`). Thu ngày 27/11/2026, không lấy tên người viết |
| Xử lý | Hai model gắn nhãn độc lập, chỉ tính nhãn trùng (chưa kiểm tay) vào `evidence/review_labels.csv`: không chép tên người viết, trích tối đa 2 câu mỗi review. Đếm bằng `python evidence/count_reviews.py` |
| Số dòng | 200 review mới nhất (29/12/2025 đến 24/11/2026), thu bằng `evidence/fetch_reviews.py`, nhãn ở `evidence/review_labels.csv`. 49/200 có nhãn đau |
| Nhãn | thật (dữ liệu công khai). Repo chỉ giữ số đã tổng hợp và trích ngắn |
| Giới hạn | Người viết review thường đang bực, nên lệch về phía phàn nàn. Một app trung gian; có review về vé máy bay và lỗi vận hành của nhà xe nằm trong số đã đếm; **không** chứng minh trợ lý làm giảm vấn đề |
