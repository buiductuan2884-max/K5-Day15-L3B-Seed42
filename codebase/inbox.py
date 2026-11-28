"""Hộp phiếu mô phỏng của bản web: khách gửi, màn nhà xe xử lý.

Nằm trong bộ nhớ máy chủ nên dùng chung mọi phiên và mất khi khởi động lại. Không ghi đĩa, không gửi ra ngoài.
Tự kiểm cùng giao diện: python codebase/web.py selfcheck
"""
import copy
import secrets
import threading
import time

from app import WARNING, hide

STATES = ["Mới", "Đang xử lý", "Đã xử lý"]
FULL = "Hộp phiếu thử đã đầy. Báo nhóm để mở lại."
# shortcut: giữ trong bộ nhớ, tối đa 100 phiếu; dùng thật thì cần cơ sở dữ liệu và tài khoản nhân viên.
MAX_TICKETS = 100
MAX_CHARS = 1000

_lock = threading.Lock()
_records = []


def _clean(value, label=""):
    """Phiếu và phản hồi được người khác đọc: có dữ liệu nhạy cảm thì không nhận."""
    value = str(value)
    if hide(value, label) != value:
        raise ValueError(WARNING)
    return value[:MAX_CHARS]


def submit(ticket):
    """Nhận phiếu khách đã xem và bấm gửi. Trả mã phiếu; ValueError nếu bị từ chối."""
    data = {key: _clean(ticket.get(key, "")) for key in ("category", "summary", "requested_resolution")}
    data["evidence_to_attach"] = [_clean(x) for x in ticket.get("evidence_to_attach", [])]
    data["provided_fields"] = {k: _clean(v, k) for k, v in ticket.get("provided_fields", {}).items()}
    data["missing_fields"] = [_clean(x) for x in ticket.get("missing_fields", [])]
    with _lock:
        if len(_records) >= MAX_TICKETS:
            done = next((r for r in _records if r["state"] == STATES[-1]), None)
            if done is None:
                raise ValueError(FULL)
            _records.remove(done)
        # đuôi ngẫu nhiên: sau khi khởi động lại, mã cũ của khách này không trùng phiếu của khách khác
        code = "XKM-" + secrets.token_hex(3).upper()
        _records.append({"code": code, "state": STATES[0], "reply": "", "version": 0, "ticket": data,
                         "sent": time.strftime("%H:%M %d/%m", time.gmtime(time.time() + 7 * 3600))})
    return code


def tickets():
    """Bản sao mọi phiếu, mới nhất trước."""
    with _lock:
        return copy.deepcopy(_records[::-1])


def find(code):
    return next((r for r in tickets() if r["code"] == code), None)


def update(code, state, reply):
    """Nhân viên đổi trạng thái và phản hồi. False nếu phiếu không còn; ValueError nếu bị từ chối."""
    if state not in STATES:
        raise ValueError("Trạng thái không hợp lệ.")
    reply = _clean(reply.strip())
    with _lock:
        for record in _records:
            if record["code"] == code:
                record.update(state=state, reply=reply, version=record["version"] + 1)
                return True
    return False
