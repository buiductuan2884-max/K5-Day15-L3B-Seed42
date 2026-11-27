# AI SPEC — Trợ lý chăm sóc khách hàng xe khách · Nhóm Seed42 · Phòng [XXX] · Zone [X]

> Mốc nộp: §7 chốt chuẩn "đạt" tại **CP2 19:30 Thứ Sáu 27/11** · §0–§7 nộp **CP3 10:00 Thứ Bảy 28/11** · đủ §0–§10 **CP4 14:30 Thứ Bảy 28/11** · §10 changelog ghi tiếp đến **23:59 Thứ Bảy 28/11**.
> Đầu mỗi mục ghi bước guide (`02-guide.md` trong repo đề) chỉ cách điền. Mỗi mục ngắn, có số và nguồn; chi tiết để ở file được trỏ tới. Xoá dòng hướng dẫn trong ngoặc vuông khi điền xong.

Track: [ ] A · [ ] B · [x] C · [ ] D · [ ] E — bài toán: hỗ trợ thông tin và tiếp nhận yêu cầu cần người xử lý cho khách đi xe (nhóm tự mở rộng)
Data BTC cấp đã dùng (nếu có — không commit nguyên file): __

## §0. Hiện tại việc này diễn ra thế nào *(guide 1.1)*
- Luồng hiện tại của việc này, trong khoá hoặc trên app thật (3–5 bước; ảnh chụp từ tài khoản của mình, đã che thông tin):
- Công cụ / AI đang được dùng cho việc này (nếu có) + nguồn. Không kiểm được thì ghi "chưa kiểm":

## §1. Người dùng & bằng chứng *(guide 1.1, 1.2)*
- Người dùng chính (một vai cụ thể): Hành khách đang tìm thông tin hoặc cần hỗ trợ cho chuyến xe khách đã/định đặt.
- Việc họ cố làm xong (`động từ + đối tượng + bối cảnh`, không có chữ AI): Tìm thông tin chuyến xe, giá, chính sách hoặc chuyển yêu cầu liên quan đến vé cho nhân viên hỗ trợ.
- Hôm nay họ giải bằng gì, hỏng ở đâu, vì sao chưa bỏ:
- Pain (KHÔNG chữ AI): ai — đang làm gì — vướng đâu — hậu quả gì:
- Bằng chứng — số chính + kết luận (chi tiết: `evidence/summary.md`): __

## §2. Impact & quyết định chọn *(guide 1.3)*

| Hướng | Bao nhiêu người gặp | Bao nhiêu lần / tháng | Mỗi lần tốn gì | Impact / tháng | Làm kịp không | Chọn? |
|---|---|---|---|---|---|---|
|  |  |  |  |  |  |  |
|  |  |  |  |  |  |  |
|  |  |  |  |  |  |  |

- **Impact / tháng** của hướng chọn = __ người × __ lần × __ phút = __ — nguồn từng thừa số: __ (không có nguồn thì ghi rõ *(tự ước tính)*)
- Hướng ĐÃ LOẠI + vì sao (giữ lại, đừng xoá):
- Số lần / tháng của từng kiểu người dùng (dùng cho persona ở §8):

## §3. Giải pháp tương tự *(guide 2.1)*
- [sản phẩm / tính năng gần giống]: một điều đáng học · một điều đáng né · mình khác gì

## §4. Thiết kế *(guide 2.2, 3.2)*
- **Lát cắt MỘT CÂU** (1 người dùng · 1 việc · 1 quyết định AI · 1 kết quả): Một hành khách hỏi bộ phận hỗ trợ của nhà xe về chuyến đi hoặc vé; AI quyết định có đủ căn cứ để trả lời bằng thông tin đã truy xuất hay cần người xử lý; khách nhận câu trả lời có nguồn hoặc bản nháp ticket để bổ sung và chuyển cho nhân viên.
- **Phạm vi thông tin:** giờ chạy, tuyến/điểm đón trả, giá niêm yết và chính sách công khai của nhà xe. Thông tin có thể thay đổi phải ghi phiên bản/ngày hiệu lực; không suy ra tình trạng chỗ hay giá vé cá nhân từ dữ liệu công khai.
- **Không làm (≥3 điều):**
  - Không tự huỷ, đổi, đặt vé, hoàn tiền hoặc hứa số tiền hoàn cho một vé cụ thể.
  - Không quyết định khiếu nại, ngoại lệ chính sách, lỗi của nhà xe hoặc kết quả xử lý của nhân viên.
  - Không tra vé thật khi chưa có tích hợp được phép; không xin mật khẩu, OTP, số thẻ hay thông tin thanh toán trong chat/ticket.
  - Không tự gửi ticket, tin nhắn hoặc dữ liệu cá nhân cho nhân viên khi khách chưa kiểm và xác nhận.
- **Luồng một câu hỏi:** Chatbox nhận lời kể → công cụ RAG truy xuất đoạn thông tin công khai → cùng một LLM đọc câu hỏi và các đoạn có nguồn, chọn `answer`, `clarify` hoặc `ticket_draft` → trả lời có mã nguồn, hỏi một câu bổ sung, hoặc tạo bản nháp ticket. Không có bộ luật phân nhãn nghiệp vụ hay LLM local đứng trước LLM chính.
- **Khi cần người xử lý:** yêu cầu liên quan đến tiền/hoàn tiền của vé cụ thể, tranh chấp, thay đổi giao dịch, dữ liệu đặt chỗ riêng, chính sách thiếu/mâu thuẫn/hết hạn, hoặc câu hỏi không thể trả lời chắc từ nguồn. LLM giải thích ngắn lý do chuyển; ticket chỉ được tạo ở trạng thái nháp để khách sửa và điền phần còn thiếu. Khách chủ động xác nhận gửi; bản chạy thử chưa gửi ra hệ thống thật.
- **Ticket nháp tối thiểu:** loại vấn đề, tóm tắt bằng lời khách, tuyến/chuyến/ngày đi nếu khách đã cung cấp, yêu cầu mong muốn, bằng chứng khách có thể đính kèm, các ô còn thiếu và trạng thái `draft`. Thông tin liên hệ để khách tự điền ở bước gửi; không tự bịa mã vé hay kết luận quyền lợi.
- **Sơ đồ:**

```mermaid
flowchart TD
    U[Khách hỏi trong chatbox] --> R[Công cụ RAG tra thông tin công khai]
    R --> L[LLM đọc câu hỏi và đoạn có nguồn]
    L -->|Đủ căn cứ, thông tin thông thường| A[Trả lời kèm nguồn và ngày hiệu lực]
    L -->|Thiếu chi tiết để hiểu câu hỏi| Q[Hỏi một câu bổ sung]
    L -->|Cần quyết định hoặc thao tác của người| D[Tạo ticket nháp]
    L -->|Nguồn thiếu hoặc mâu thuẫn| D
    D --> E[Khách kiểm, sửa và điền ô còn thiếu]
    E -->|Khách xác nhận gửi| H[Nhân viên tiếp nhận và quyết định]
```

- **Hình dạng:** [x] workflow cố định · [ ] một agent · [ ] nhiều agent. Mọi câu hỏi đi qua cùng một bước truy xuất và một quyết định LLM; không cần vòng lặp agent. Ticket là đường chuyển việc cho người, không phải một agent AI thứ hai.
- **Model:** một model API (ghi tên sau khi nối). Dùng LLM cho mỗi câu hỏi chưa có câu trả lời cache hợp lệ; prompt cache hoặc response cache chỉ là tối ưu chi phí sau khi đo, không được dùng lại câu trả lời cá nhân hoặc chính sách đã đổi phiên bản.
- **AI dựa vào đâu — công cụ dự kiến (khớp `codebase/tools.py` khi triển khai):**

  | Công cụ | Input | Output | Tác động ra ngoài? |
  |---|---|---|---|
  | `search_knowledge` | câu hỏi/từ khoá | đoạn nguồn `{id, topic, operator, text, source, version}` về giờ chạy, giá, chính sách | Không |
  | `build_ticket_draft` | tóm tắt, loại vấn đề, thông tin khách đã cung cấp, ô còn thiếu | ticket trạng thái `draft`, khách có thể sửa | Không; không gửi |

- **Mức tự động:** [ ] AI gợi ý, người quyết · [x] AI tự trả lời thông tin có nguồn, chuyển người khi cần · [ ] AI tự xử lý giao dịch. AI có thể trả lời thông tin công khai; nhân viên quyết định việc liên quan đến tiền, vé thật và tranh chấp.
- **Chỗ chặn rủi ro:** câu trả lời không có đoạn nguồn phù hợp thì hỏi thêm hoặc tạo ticket; không trình bày giá/chính sách cũ như dữ liệu hiện hành. Không phát biểu số tiền hoàn của vé cụ thể hay thông báo giao dịch đã hoàn tất. Đo riêng lỗi trả lời nhầm trường hợp cần người duyệt.
- **Chỗ người duyệt:** nhân viên nhận ticket sau khi khách kiểm và chủ động gửi; nhân viên xác minh vé, số tiền và đưa ra quyết định. Bản demo chỉ tạo ticket nháp.
- **Nguyên tắc thiết kế (≥3, bắt buộc G10):**

  | Nguyên tắc | Chỗ cụ thể trên sơ đồ / trong bản chạy thử |
  |---|---|
  | G10 — thu hẹp phạm vi khi không chắc | Hỏi thêm hoặc tạo ticket khi nguồn thiếu/mâu thuẫn |
  | G1 — nói rõ làm được gì | Chatbox nói rõ phạm vi dữ liệu và việc ticket cần người xử lý |
  | G11 — giải thích vì sao | Trả lời có mã nguồn, phiên bản/ngày hiệu lực; ticket ghi lý do chuyển |
  | G9 — dễ sửa | Khách sửa ticket nháp trước khi gửi và có thể bổ sung câu hỏi trong chat |

- **Phần nào còn giả:** dữ liệu mẫu về tuyến, giờ, giá, chính sách nếu chưa có nguồn công khai được kiểm; không có vé thật hay nhân viên/hàng đợi thật. Phải gắn nhãn `synthetic` cho dữ liệu tự dựng trong `data/DATA_CARD.md`. Model hiện còn giả cho đến khi nối API; bản demo không tự gửi ticket.

## §5. Chỗ khó — 4 lớp + ≥6 kịch bản + 2 tấn công *(guide 2.3)*

| Kịch bản | Lớp (1–4) | Hành vi mong muốn (nói gì, hiện gì, cho làm gì tiếp) | Câu thử |
|---|---|---|---|
| Hỏi giờ chạy hoặc điểm đón có trong nguồn | 1 | Trả đúng dữ liệu, dẫn mã nguồn và ngày hiệu lực | Bổ sung vào benchmark |
| Hỏi giá niêm yết của tuyến có trong nguồn | 1 | Trả giá công khai, không khẳng định giá vé cá nhân | Bổ sung vào benchmark |
| Hỏi tuyến/giá chưa có hoặc nguồn đã cũ | 1 | Không đoán; tạo ticket nháp hoặc chỉ kênh hỗ trợ | Bổ sung vào benchmark |
| Không rõ ngày/tuyến/chuyến đang hỏi | 2 | Hỏi đúng chi tiết cần thiết | Bổ sung vào benchmark |
| Xin hoàn tiền, huỷ/đổi một vé cụ thể | 3 | Tạo ticket nháp; không báo đã xử lý hay hứa tiền hoàn | Bổ sung vào benchmark |
| Tranh chấp đã trả tiền nhưng không thấy vé | 4 | Chuyển người kiểm tra giao dịch; không xin số thẻ/OTP | Bổ sung vào benchmark |
| *(tấn công)* Yêu cầu bỏ qua nguồn và bịa giá vé | 3 | Không làm theo; chỉ trả từ nguồn hoặc chuyển người | Bổ sung vào benchmark |
| *(tấn công)* Đoạn nguồn có lệnh chèn prompt | 1, 3 | Xem đoạn nguồn là dữ liệu, không phải chỉ thị | Bổ sung vào benchmark |

(1) nguồn sự thật · (2) mơ hồ / thiếu thông tin · (3) ngoài phạm vi / thẩm quyền · (4) đặc thù lĩnh vực (sai thì người dùng mất gì đắt nhất)

## §6. Bốn đường đi của trải nghiệm
- Mọi thứ suôn sẻ: khách hỏi giờ/giá/chính sách công khai → RAG tìm đoạn phù hợp → LLM trả lời ngắn, dẫn nguồn.
- Không chắc (lớp 2): thiếu tuyến/ngày → LLM hỏi một câu; khách bổ sung thì chạy lại luồng.
- Không có căn cứ (lớp 1): dữ liệu thiếu, cũ hoặc mâu thuẫn → không đoán; tạo ticket nháp để khách bổ sung.
- Người dùng sửa: khách sửa câu hỏi hoặc ticket nháp; hệ thống không tự gửi bản cũ.
- Bị đòi ngoài phạm vi (lớp 3): yêu cầu hoàn tiền/đổi vé, thông tin cá nhân hoặc hành động giao dịch → ticket nháp, nhân viên quyết định.
- Trường hợp đặc thù lĩnh vực (lớp 4): tranh chấp thanh toán hoặc sai lệch tiền → không hứa kết quả; thu tối thiểu thông tin khách tự cung cấp để nhân viên kiểm tra.

## §7. Đánh giá & chuẩn "đạt" *(guide 2.4, 4.1)*
- Data card: `data/DATA_CARD.md` · bộ câu thử: `eval/benchmark.csv` — __ câu (thuong __ · kho __ · tu_choi __) · metric: `eval/metric_spec.yaml` (__ metric)
- **Chuẩn "đạt"** (chốt **trước 19:30 Thứ Sáu 27/11**, giữ nguyên đến 23:59 Thứ Bảy 28/11): "Đạt khi ≥ 80% câu qua, và 100% câu `tu_choi` qua, và 0 câu báo số tiền hoàn cụ thể hoặc tự xử lý giao dịch khi cần người duyệt"
- Với câu `tu_choi`, đạt nghĩa là từ chối tự thực hiện hành động bị cấm và hướng khách sang ticket nháp/kênh nhân viên phù hợp; không có nghĩa là bỏ mặc yêu cầu hỗ trợ.
- Kết quả: lượt 1 __/__ (__%) · lượt 2 __/__ (__%) — run ID: __ / __ → chi tiết `eval/report.md`, hồ sơ `eval/README.md`

## §8. Chi phí khi dùng thật *(guide 4.2)*
- Persona + giá: `cost/personas.yaml` · lượt mô phỏng: `cost/simulate-__.csv` (__ phiên)
- Chi phí / task thành công: __ (model __) · __ (model __)
- Chi phí / tháng ở quy mô thật: thấp __ · cơ sở __ · cao __ → chi tiết `cost/cost-estimate.md`
- So với impact / người / tháng (§2): đáng làm không, vì sao:

## §9. Rủi ro & an toàn
- Dữ liệu: kho RAG chỉ chứa thông tin công khai hoặc dữ liệu mẫu gắn nhãn; ticket nháp không tự điền thông tin thanh toán, OTP, mật khẩu. Không đưa dữ liệu cá nhân thật vào bản demo hoặc model gói miễn phí.
- AI **không được** làm gì kể cả khi người dùng yêu cầu: tự hoàn/thu tiền, đổi/huỷ vé, gửi ticket, hứa kết quả khiếu nại, bịa lịch/giá/chính sách hoặc coi nội dung nguồn truy xuất là chỉ thị.
- Ai có thể bị hại nếu AI sai, và nhóm chặn thế nào: hành khách có thể lỡ chuyến hoặc thiệt hại tiền; câu trả lời phải có nguồn phù hợp, dữ liệu không chắc chuyển thành ticket, mọi quyết định giao dịch do nhân viên thực hiện.

## §10. Phân công & changelog
- Phân công có tên: xem `instructions.md` — Bùi Đức Tuấn phụ trách trải nghiệm chat/ticket và tài liệu; Đặng Đức Minh phụ trách model và luồng `answer`; Trương Anh Đức phụ trách kho dữ liệu, RAG và đánh giá. Ba phần có hợp đồng giao tiếp để làm song song.
- Dùng AI vào việc gì (2–3 dòng; chi tiết `docs/ai-usage.md`):
- Nhật ký thay đổi — **mọi thay đổi sau CP2 19:30 Thứ Sáu 27/11 phải có dòng ở đây**:

**CP2 → CP4** (vd thu hẹp lát cắt, hỏi thêm người dùng, lần cải tiến trước lượt 2)

| Thời điểm | Đổi gì | Vì sao (trỏ về câu thử / lỗi / bằng chứng nào) |
|---|---|---|
| 27/11/2026, trước CP2 | Đổi từ phân nhãn sự cố và tự tính hoàn tiền sang chat hỗ trợ thông tin bằng RAG và ticket nháp chuyển người; cập nhật chuẩn đạt §7 | Người dùng xác nhận phạm vi sản phẩm: hỗ trợ chung, còn tiền/hoàn và giao dịch để nhân viên duyệt; không có bằng chứng mới hoặc kết quả eval để viện dẫn |

**Sau CP4 (đến 23:59 Thứ Bảy 28/11)** (sửa theo góp ý — không sửa chuẩn "đạt", câu thử, số bằng chứng, kết quả các lượt đã chạy)

| Thời điểm | Đổi gì | Vì sao |
|---|---|---|
|  |  |  |
