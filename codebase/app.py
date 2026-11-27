"""Chat dòng lệnh: khách hỏi → answer() trong agent.py → in câu trả lời, hoặc ticket nháp để khách sửa.

Chạy bằng: python run.py   (macOS/Linux có thể là python3, Windows có thể là py)
Tự kiểm phần ticket, không cần model: python codebase/app.py selfcheck
Không gửi, không lưu gì: bản chạy thử chưa có hộp tiếp nhận thật.
"""
import os
import re
import sys
import unicodedata

for _stream in (sys.stdout, sys.stderr, sys.stdin):
    try:
        _stream.reconfigure(encoding="utf-8", errors="replace")
    except Exception:
        pass

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

SCOPE = """Trợ lý hỗ trợ khách đi xe (bản chạy thử, dữ liệu mẫu)
- Hỏi được: giờ chạy, tuyến, điểm đón trả, giá niêm yết, chính sách công khai.
- Việc về tiền, đổi / huỷ vé, khiếu nại: trợ lý chỉ soạn ticket nháp cho nhân viên.
- Đừng gửi mật khẩu, OTP, số thẻ.
Gõ câu hỏi rồi Enter. Thoát: Ctrl+C (hoặc Enter 2 lần với dòng trống)."""

# shortcut: chặn số thẻ, mã đi sau từ khoá và mật khẩu dễ thấy; mật khẩu toàn chữ thường không có "là / :" vẫn lọt.
SENSITIVE = re.compile(
    # số thẻ 13–19 chữ số
    r"\b(?:\d[ .-]{0,3}){12,18}\d\b"
    # từ khoá rồi tới mã (kể cả viết rời từng số) trong cùng một vế câu; bỏ qua số tiền
    # otp, pin, cvv, cvc: mã 3 chữ số cũng tính; bỏ qua khi số là tiền, phần trăm, số lần hay thời gian
    r"|\b(?:cvv|cvc|otp|pin)(?![a-z])[^\d,;.?!\n]{0,25}(?<!\d)(?:\d[ .-]?){2}\d(?![ .-]?\d|[.,]\d)"
    r"(?!\s*(?:%|đồng|vnđ|vnd|đ|d|k|lần|phút|giờ)(?!\w))"
    r"|\b(?:otp|pin|mật khẩu|mat khau|password)(?![a-z])[^\d,;.?!\n]{0,25}"
    r"(?<!\d)(?!\d{1,3}(?:\.\d{3})+(?!\d))(?:\d[ .-]?){3,}\d(?![\d.,]*\s*(?:đồng|vnđ|vnd|đ|d)(?!\w))"
    # "mật khẩu là x", "mật khẩu: x"
    r"|\b(?:mật khẩu|mat khau|password|pass|mk)\s*(?:là|la|:|=)\s*(?!gì|gi\b|sao|cái|cai)\S+"
    # "mật khẩu abc123", "mật khẩu abcXYZ"
    r"|\b(?:mật khẩu|mat khau|password)\s+(?:của (?:mình|tôi|em)\s+)?(?=\S*\d|\S*(?-i:[a-z][A-Z]))\S{4,}",
    re.IGNORECASE)
WARNING = "Tin này có vẻ chứa số thẻ, OTP hoặc mật khẩu nên không được nhận. Hãy bỏ phần đó rồi gõ lại."


def is_sensitive(text):
    return bool(SENSITIVE.search(unicodedata.normalize("NFC", str(text))))


def hide(value, label=""):
    """Che giá trị nhạy cảm do model trả về; nhãn ô được xét cùng để bắt ô kiểu "ma_otp"."""
    value = str(value)
    return "[đã ẩn]" if is_sensitive(value) or is_sensitive("%s %s" % (label.replace("_", " "), value)) else value


def ticket_fields(ticket):
    """Các ô khách sửa được: (nhãn, nhóm, khoá)."""
    rows = [("Loại vấn đề", "top", "category"), ("Tóm tắt", "top", "summary"),
            ("Yêu cầu mong muốn", "top", "requested_resolution"),
            ("Bằng chứng đính kèm (cách nhau bằng dấu ;)", "top", "evidence_to_attach")]
    rows += [(k, "provided_fields", k) for k in ticket["provided_fields"]]
    rows += [(k, "missing_fields", k) for k in ticket["missing_fields"]]
    return rows


def normalize_ticket(raw):
    """Bản sao đủ khoá, để ticket thiếu hoặc sai kiểu không làm sập màn hình."""
    provided, missing, evidence = (raw.get(k) for k in ("provided_fields", "missing_fields", "evidence_to_attach"))
    return {"status": "draft",
            "category": hide(raw.get("category") or ""),
            "summary": hide(raw.get("summary") or ""),
            "requested_resolution": hide(raw.get("requested_resolution") or ""),
            "evidence_to_attach": [hide(x) for x in evidence] if isinstance(evidence, list) else [],
            "provided_fields": {str(k): hide(v, str(k)) for k, v in provided.items()} if isinstance(provided, dict) else {},
            "missing_fields": [str(x) for x in missing] if isinstance(missing, list) else []}


def set_field(ticket, row, value):
    """Ghi giá trị khách nhập. Ô còn thiếu đã điền thì chuyển sang thông tin đã có."""
    _, group, key = row
    if group == "top":
        ticket[key] = [x.strip() for x in value.split(";") if x.strip()] if key == "evidence_to_attach" else value
    else:
        ticket["provided_fields"][key] = value
        if key in ticket["missing_fields"]:
            ticket["missing_fields"].remove(key)


def show_ticket(ticket):
    print("\n--- TICKET NHÁP (chưa gửi cho ai) ---")
    for n, (label, group, key) in enumerate(ticket_fields(ticket), 1):
        if group == "missing_fields":
            value = "(còn thiếu)"
        else:
            value = ticket[key] if group == "top" else ticket[group][key]
            value = "; ".join(value) if isinstance(value, list) else value
        print("%2d. %s: %s" % (n, label, value or "(trống)"))


def edit_ticket(raw, ask=input):
    """Khách xem, sửa, rồi gửi thử. Trả ticket sau khi sửa."""
    ticket = normalize_ticket(raw)
    while True:
        show_ticket(ticket)
        choice = ask("Số ô muốn sửa · 'gui' để gửi thử · Enter để đóng: ").strip().lower()
        if not choice:
            print("Đã đóng. Ticket không được lưu hay gửi.")
            return ticket
        if choice in ("gui", "gửi"):
            if ticket["missing_fields"]:
                print("Còn thiếu: %s." % ", ".join(ticket["missing_fields"]))
            if ask("Gõ 'co' để xác nhận gửi thử: ").strip().lower() in ("co", "có"):
                print("MÔ PHỎNG: chưa có hộp tiếp nhận thật, ticket KHÔNG được gửi đi đâu.")
                return ticket
            continue
        rows = ticket_fields(ticket)
        if not (choice.isdecimal() and 1 <= int(choice) <= len(rows)):
            print("Không có ô đó.")
            continue
        value = ask("%s: " % rows[int(choice) - 1][0]).strip()
        if is_sensitive(value):
            print(WARNING)
        elif value:
            set_field(ticket, rows[int(choice) - 1], value)


def _where(e):
    """File (trong codebase/) gây lỗi khi nạp: SyntaxError có e.filename, lỗi khác lấy khung cuối của traceback."""
    import traceback
    path = getattr(e, "filename", None) or (traceback.extract_tb(e.__traceback__)[-1].filename if e.__traceback__ else "")
    if not path:
        return "codebase/"
    p = os.path.abspath(path)
    base = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    return os.path.relpath(p, base).replace(os.sep, "/") if p.startswith(base) else path


def main() -> int:
    try:
        import tracing
        from agent import answer
    except Exception as e:  # lỗi cú pháp, thiếu thư viện… trong codebase/
        print("Không nạp được codebase/ — lỗi ở %s: %s: %s" % (_where(e), type(e).__name__, e))
        print("Sửa lỗi rồi chạy lại. Cách nối model: docs/connect-model.md")
        return 1
    print(SCOPE)
    blank = 0
    while True:
        try:
            text = input("> ").strip()
            if not text:
                blank += 1
                if blank >= 2:
                    return 0
                continue
            blank = 0
            if is_sensitive(text):
                print(WARNING)
                continue
            tracing.begin("app")
            try:
                result = answer(text)
            except NotImplementedError as e:
                tracing.end()
                print("Chưa nối model: %s" % e)
                return 1
            except Exception as e:  # lỗi gọi model: báo rồi cho hỏi tiếp
                tracing.end()
                print("[lỗi] %s: %s" % (type(e).__name__, e))
                continue
            s, _ = tracing.end()
            result = result if isinstance(result, dict) else {"output": result}
            print(hide(result.get("output") or "Chưa có câu trả lời. Bạn hỏi lại rõ hơn giúp mình."))
            print("   (model: %s · gọi model %d lần · công cụ %d lần · token vào %d / ra %d)"
                  % (", ".join(s["models"]) or "—", s["model_calls"], s["tool_calls"], s["tokens_in"], s["tokens_out"]))
            if isinstance(result.get("ticket_draft"), dict):
                edit_ticket(result["ticket_draft"])
        except (EOFError, KeyboardInterrupt):
            print()
            return 0


def selfcheck() -> int:
    assert is_sensitive("OTP của mình là 123456")
    assert is_sensitive("thẻ 4111 1111 1111 1111")
    assert is_sensitive("mật khẩu: abcxyz")
    assert not is_sensitive("huỷ vé 300.000đ, còn 15 tiếng, chuyến 8h ngày 28/11")
    for text in ("mật khẩu abcXYZ", "OTP: 1 2 3 4 5 6", "mã OTP của mình vừa nhận là 482913", "password abc123",
                 "cvv 123", "OTP 123456 đi", "mật khẩu: 300000", "otp482913", "mk: 123456", "ma cvc 123",
                 "so the 4111  1111  1111  1111", "otp 482913 k thay ve",
                 "mình chuyển rồi mà chưa được vé, mã 123, otp 345 check hộ với", "mã pin 345", "OTP của mình là 3 4 5"):
        assert is_sensitive(text), text
    for text in ("Không hỏi OTP; giá vé 300000đ có đúng không?", "OTP không có, vé giá 300.000 đồng",
                 "Quên mật khẩu thì làm sao?", "mật khẩu là gì", "mật khẩu wifi trên xe", "gọi 1900 888 686",
                 "quên mật khẩu 100 lần rồi", "khong nhan duoc OTP, goi 19006067 khong ai nghe",
                 "OTP xong bị trừ 350.000 mất tiền", "mật khẩu là cái gì",
                 "pin còn 100% mà không mở được vé", "OTP gửi 100 lần không tới", "mã vé 123, chưa nhận được OTP"):
        assert not is_sensitive(text), text
    hidden = normalize_ticket({"summary": "OTP 123456", "provided_fields": {"ma_otp": "654321", "gia_ve": "300000"}})
    assert hidden["summary"] == "[đã ẩn]"
    assert hidden["provided_fields"] == {"ma_otp": "[đã ẩn]", "gia_ve": "300000"}
    raw = {"summary": "Xin hoàn tiền", "missing_fields": ["ngay_di"], "provided_fields": None}
    inputs = iter(["9", "5", "otp 998877", "5", "28/11", "4", "ảnh vé; tin nhắn", "gui", "co"])
    t = edit_ticket(raw, ask=lambda _: next(inputs))
    assert t["status"] == "draft" and t["missing_fields"] == []
    assert t["provided_fields"] == {"ngay_di": "28/11"}
    assert t["evidence_to_attach"] == ["ảnh vé", "tin nhắn"]
    assert raw["missing_fields"] == ["ngay_di"]  # không sửa ticket gốc
    print("selfcheck OK")
    return 0


if __name__ == "__main__":
    sys.exit(selfcheck() if sys.argv[1:] == ["selfcheck"] else main())
