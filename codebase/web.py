"""Web demo: chat Streamlit nối answer(). Bản dòng lệnh `python run.py` giữ nguyên.

Nút ở góc trái đổi giữa hai giao diện: khách hỏi, và màn nhà xe xử lý phiếu khách gửi (inbox.py).
Phía khách có hai chế độ xem chung một cuộc trò chuyện: "Khách hàng", và "Trace / log" hiện thêm các bước xử lý.

Chạy:      python -m streamlit run codebase/web.py
Tự kiểm:   python codebase/web.py selfcheck      (không cần Streamlit, không gọi model)
Gửi phiếu là mô phỏng: phiếu chỉ nằm trong bộ nhớ máy chủ, chưa có hộp tiếp nhận thật của nhà xe.
"""
import hmac
import html
import json
import os
import re
import sys
import threading
import time

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)

import inbox  # noqa: E402
from app import WARNING, hide, is_sensitive, normalize_ticket, set_field  # noqa: E402

KB_PATH = os.path.join(HERE, "..", "data", "knowledge_base.json")
HERO_PATH = os.path.join(HERE, "assets", "hero.png")
STATUS = {"answer": "Đã trả lời có nguồn", "clarify": "Cần thêm thông tin", "ticket": "Chuyển nhân viên",
          "blocked": "Đã chặn, không gửi cho trợ lý", "error": "Chưa gọi được trợ lý", "fake": "Chế độ thử, chưa nối model"}
SUGGESTIONS = ["Xe đi Hải Phòng mấy giờ?", "Giá vé đi Sa Pa bao nhiêu?", "Huỷ trước 2 ngày hoàn bao nhiêu phần trăm?",
               "Xe đổi giờ, hoàn tiền cho mình"]
VIEWS = ["Khách hàng", "Trace / log"]
SETTINGS = ("MODEL_PROVIDER", "MODEL_NAME", "API_KEY", "APP_PASSCODE", "STAFF_PASSCODE", "MAX_CALLS")
# shortcut: đếm trong bộ nhớ, khởi động lại là về 0; cần giới hạn bền thì đặt hạn mức ở trang nhà cung cấp key.
DEFAULT_MAX_CALLS = 200
FIELD_NAMES = {"summary": "Tóm tắt", "category": "Loại việc", "requested_resolution": "Bạn muốn được giải quyết thế nào",
               "evidence_to_attach": "Bằng chứng đính kèm (cách nhau bằng dấu ;)"}


def classify(result, model_names=()):
    """Từ kết quả answer() suy ra trạng thái, lời đáp và mã nguồn. answer() chỉ trả output và ticket_draft."""
    output = hide(result.get("output") or "Chưa có câu trả lời. Bạn hỏi lại rõ hơn giúp mình.")
    if isinstance(result.get("ticket_draft"), dict):
        return "ticket", output, []
    message, sep, tail = output.partition("\nNguồn:")
    if sep:
        return "answer", message.strip(), re.findall(r"\[([A-Z0-9][A-Z0-9-]+)\]", tail)
    if "fake" in model_names:
        return "fake", output, []
    return "clarify", output, []


def load_sources(path=KB_PATH):
    """Mã nguồn → đoạn dữ liệu. File thiếu hoặc lạ thì trả rỗng, trang vẫn chạy."""
    try:
        with open(path, encoding="utf-8") as f:
            data = json.load(f)
        items = data if isinstance(data, list) else next(v for v in data.values() if isinstance(v, list))
        return {x["id"]: x for x in items if isinstance(x, dict) and "id" in x}
    except (OSError, ValueError, StopIteration):
        return {}


def ask(text):
    """Một lượt hỏi. Tin nhạy cảm dừng ở đây, không tới model."""
    if is_sensitive(text):
        return {"user": "(nội dung đã ẩn)", "kind": "blocked", "reply": WARNING, "events": []}
    import tools
    import tracing
    from agent import answer
    # khung trace là biến chung của cả tiến trình: mỗi lúc một người hỏi, không lẫn dấu vết sang người khác
    with tracing.__dict__.setdefault("web_lock", threading.Lock()):
        used = tracing.__dict__.get("web_calls", 0)
        if used >= max_calls():
            return {"user": text, "kind": "error", "events": [],
                    "reply": "Bản chạy thử đã hết lượt hỏi cho phiên máy chủ này. Báo nhóm để mở lại."}
        tracing.__dict__["web_calls"] = used + 1
        return run_turn(text, answer, tools, tracing)


def max_calls():
    try:
        return int(os.environ.get("MAX_CALLS") or DEFAULT_MAX_CALLS)
    except ValueError:
        return DEFAULT_MAX_CALLS


def run_turn(text, answer, tools, tracing):
    tracing.begin("web")
    started = time.perf_counter()
    try:
        result = answer(text)
    except Exception as e:  # không in nội dung lỗi cho khách: có thể chứa chi tiết yêu cầu gửi nhà cung cấp
        _, events = tracing.end()
        return {"user": text, "kind": "error", "events": events, "found": found_ids(tools, text),
                "reply": "Gọi trợ lý chưa được (%s). Kiểm tra mạng và file .env rồi hỏi lại." % type(e).__name__}
    summary, events = tracing.end()
    kind, reply, ids = classify(result, summary["models"])
    turn = {"user": text, "kind": kind, "reply": reply, "ids": ids, "events": events, "found": found_ids(tools, text),
            "meta": "%s · %d token vào, %d ra · %.1f giây" % (
                ", ".join(summary["models"]) or "không gọi model", summary["tokens_in"], summary["tokens_out"],
                time.perf_counter() - started)}
    if kind == "ticket":
        turn["ticket"] = normalize_ticket(result["ticket_draft"])
    return turn


def found_ids(tools, text):
    """Tra lại ngoài khung trace để hiện đủ mã đoạn tìm được (trace chỉ giữ bản rút gọn)."""
    try:
        return [p["id"] for p in tools.search_knowledge(text)]
    except Exception:
        return []


def trace_steps(turn):
    """Các bước đã chạy của một lượt, theo đúng thứ tự: (tên bước, chi tiết, ổn hay không)."""
    if turn["kind"] == "blocked":
        return [("Lọc dữ liệu nhạy cảm", "Phát hiện OTP, mật khẩu hoặc số thẻ. Dừng, không gọi công cụ hay model.", False)]
    steps = [("Lọc dữ liệu nhạy cảm", "Không thấy dữ liệu nhạy cảm theo mẫu.", True)]
    for e in turn.get("events", []):
        took = "%.2f giây" % e.get("latency_s", 0)
        error = e.get("error")
        if e["kind"] == "tool":
            detail = error or took
            if e["name"] == "search_knowledge":
                found = turn.get("found") or []
                detail = "%s · %s" % (", ".join(found) if found else "không tìm thấy đoạn nào", took)
            steps.append(("Công cụ " + e["name"], error or detail, not error))
        elif e["kind"] == "model":
            choice = re.search(r'"decision"\s*:\s*"(\w+)"', e.get("output", ""))
            detail = error or "%s · %d token vào, %d ra · %s · model chọn: %s" % (
                e.get("model") or "?", e.get("tokens_in", 0), e.get("tokens_out", 0), took,
                choice.group(1) if choice else "không đọc được")
            steps.append(("Gọi model", detail, not error))
        elif e["kind"] == "note":
            steps.append(("Chốt chặn của luồng", e.get("text", ""), False))
    steps.append(("Kết quả", STATUS[turn["kind"]], turn["kind"] != "error"))
    return steps


CSS = """
@import url('https://fonts.googleapis.com/css2?family=Be+Vietnam+Pro:wght@400;500;600;700;800&family=Dancing+Script:wght@600&display=swap');
html, body, .stApp, .stApp p, .stApp label, .stApp input, .stApp textarea, .stApp button {font-family:'Be Vietnam Pro','Segoe UI',sans-serif}
.stApp {background:radial-gradient(90% 55% at 100% 0%, #c9e27a 0%, rgba(201,226,122,0) 60%),
        linear-gradient(180deg,#12896f 0%,#0f9d8a 38%,#0b7a68 100%) fixed}
header[data-testid="stHeader"] {background:transparent}
.block-container {max-width:760px;padding-top:3.8rem;padding-bottom:8rem}
.st-key-switch {position:fixed;top:.6rem;left:1rem;z-index:1000001;width:auto !important}
.st-key-staff div[data-testid="stForm"] {margin-left:0}
.card {color:#12302a;font-size:14px;line-height:1.55;overflow-wrap:anywhere}
.stApp .card > b {display:inline;color:#0b6b57}
.card .state {float:right;border-radius:999px;padding:2px 11px;font-size:12px;font-weight:700;background:#fdecc8;color:#6d4600}
.card .state.s1 {background:#dbe9ff;color:#174a94}.card .state.s2 {background:#dff3c4;color:#245314}
.card p {margin:6px 0}.card small {color:#4d6b63}
.hero {text-align:center;color:#fff;margin-bottom:18px}
.hero h1 {font-size:clamp(30px,5vw,46px);font-weight:800;line-height:1.18;text-transform:uppercase;color:#fff;margin:0;padding:0}
.hero .script {font-family:'Dancing Script',cursive;font-size:30px;margin:4px 0 0;color:#fff}
.top {display:flex;align-items:center;gap:12px;background:#ffffff;border-radius:999px;padding:10px 18px 10px 10px;
      box-shadow:0 10px 28px rgba(4,52,44,.22);margin-bottom:18px}
.orb {width:42px;height:42px;border-radius:50%;flex:none;
      background:radial-gradient(circle at 32% 28%,#f4ffd0 0 8%,#b6e34f 24%,#18a98a 58%,#075a4d 100%)}
.top b {display:block;font-size:17px;color:#0d2f29;line-height:1.3}
.top small {font-size:13px;color:#3f6159}
.top small::before {content:"";display:inline-block;width:8px;height:8px;border-radius:50%;background:#2fbf6b;margin-right:6px}
.top small.off::before {background:#e0a100}
.me {display:flex;justify-content:flex-end;margin:14px 0 8px}
.me div {max-width:82%;background:linear-gradient(135deg,#b9e04c,#8fd13f);color:#0b2a1c;font-weight:600;
         padding:12px 18px;border-radius:22px 22px 6px 22px;box-shadow:0 6px 16px rgba(4,52,44,.2);overflow-wrap:anywhere}
.bot {display:flex;gap:10px;align-items:flex-start;margin:6px 0}
.bot .orb {width:34px;height:34px}
.bubble {max-width:86%;background:#fff;color:#12302a;padding:13px 18px;border-radius:6px 22px 22px 22px;
         box-shadow:0 6px 18px rgba(4,52,44,.18);overflow-wrap:anywhere;white-space:pre-line}
.chip {display:inline-flex;align-items:center;gap:7px;background:rgba(255,255,255,.95);border-radius:999px;
       padding:4px 13px;font-size:13px;font-weight:700;margin:2px 0 4px 44px;color:#0b6b57}
.chip::before {content:"";width:8px;height:8px;border-radius:50%;background:currentColor}
.chip.clarify {color:#1c5bb0}.chip.ticket,.chip.fake {color:#8a5a00}.chip.blocked,.chip.error {color:#b3261e}
.src {margin:4px 0 6px 44px;background:#fff;border-radius:20px;padding:12px 16px;max-width:86%;color:#12302a;
      box-shadow:0 6px 18px rgba(4,52,44,.16)}
.src b {display:block;color:#0b6b57;font-size:14px}
.src p {margin:4px 0;font-size:14px;line-height:1.55}
.src small {color:#4d6b63}
.meta {margin:2px 0 0 44px;font-size:12px;color:#effdf6}
.stButton button {border-radius:999px;border:0;background:#fff;color:#0d4a3d;font-weight:600;font-size:14px;
                  padding:7px 15px;box-shadow:0 4px 12px rgba(4,52,44,.18)}
.stButton button:hover {background:#eef9d3;color:#0d4a3d}
div[data-testid="stForm"] {background:#fff;border:0;border-radius:22px;padding:18px 20px;margin-left:44px;
                           box-shadow:0 8px 22px rgba(4,52,44,.2)}
div[data-testid="stForm"] h3 {font-size:16px;color:#0d2f29;padding:0 0 2px}
.stFormSubmitButton button {border-radius:999px;background:#0b6b57;color:#fff;border:0;font-weight:700;padding:8px 20px}
.stFormSubmitButton button:hover {background:#095546;color:#fff}
div[data-testid="stBottom"] > div {background:transparent}
div[data-testid="stChatInput"] {border-radius:999px;box-shadow:0 10px 28px rgba(4,40,34,.35)}
div[data-testid="stChatInput"] > div {border-radius:999px;background:#fff;border:0}
.foot {text-align:center;color:#effdf6;font-size:13px;margin-top:14px}
div[data-testid="stButtonGroup"], div[data-testid="stSegmentedControl"] {width:100%;display:flex;justify-content:center}
button[data-variant^="segmented_control"] {background:#ffffff !important;border:0 !important;color:#0d4a3d !important;
        font-weight:700;padding:6px 22px}
button[data-variant^="segmented_control"][aria-checked="true"] {background:#b9e04c !important;color:#0b2a1c !important}
.trace {margin:8px 0 6px 44px;background:#08342c;color:#e8fff6;border-radius:18px;padding:12px 16px;font-size:13px;
        box-shadow:0 8px 20px rgba(2,28,23,.35)}
.trace ol {list-style:none;margin:0;padding:0}
.trace li {position:relative;padding:0 0 10px 22px;margin:0;line-height:1.5;overflow-wrap:anywhere}
.trace li::before {content:"";position:absolute;left:0;top:5px;width:10px;height:10px;border-radius:50%;background:#b9e04c}
.trace li.bad::before {background:#ffb454}
.trace li:not(:last-child)::after {content:"";position:absolute;left:4px;top:17px;bottom:0;width:2px;background:#2b6a5b}
.trace li b {display:block;font-size:13px;color:#fff}
.trace li span {color:#b8e6d6;font-family:Consolas,monospace;font-size:12px}
.trace summary {cursor:pointer;color:#b9e04c;font-weight:600}
.trace pre {background:#04251f;color:#d8fff1;border-radius:10px;padding:10px;font-size:11px;max-height:260px;overflow:auto;white-space:pre-wrap}
@media (max-width:640px) {.trace {margin-left:0}.chip,.src,.meta {margin-left:0}div[data-testid="stForm"] {margin-left:0}}
"""


def esc(value):
    # đổi xuống dòng thành mã: dòng trống làm Markdown cắt khối HTML và đọc phần sau thành link, ảnh
    return html.escape(str(value)).replace("\r", "").replace("\n", "&#10;")


def show_trace(st, turn):
    steps = "".join('<li class="%s"><b>%s</b><span>%s</span></li>' % ("" if ok else "bad", esc(name), esc(detail))
                    for name, detail, ok in trace_steps(turn))
    raw = esc(json.dumps(turn.get("events", []), ensure_ascii=False, indent=1))
    # một chuỗi liền, không dòng trống, để Markdown không cắt khối HTML
    st.markdown('<div class="trace"><ol>%s</ol><details><summary>Log gốc</summary><pre>%s</pre></details></div>'
                % (steps, raw.replace(chr(10), "&#10;")), unsafe_allow_html=True)


def show_turn(st, n, turn, sources, traced):
    st.markdown('<div class="me"><div>%s</div></div>' % esc(turn["user"]), unsafe_allow_html=True)
    st.markdown('<div class="chip %s">%s</div><div class="bot"><span class="orb"></span><div class="bubble">%s</div></div>'
                % (turn["kind"], STATUS[turn["kind"]], esc(turn["reply"])), unsafe_allow_html=True)
    for sid in dict.fromkeys(turn.get("ids") or []):
        item = sources.get(sid, {})
        st.markdown('<div class="src"><b>Nguồn %s</b><p>%s</p><small>%s · bản %s</small></div>'
                    % (esc(sid), esc(item.get("text", "Không tìm thấy đoạn này trong dữ liệu.")),
                       esc(item.get("source", "")), esc(item.get("version", ""))), unsafe_allow_html=True)
    if turn.get("code"):
        show_sent(st, n, turn["code"])
    elif "ticket" in turn:
        show_ticket(st, n, turn)
    if traced:
        if turn.get("meta"):
            st.markdown('<div class="meta">%s</div>' % esc(turn["meta"]), unsafe_allow_html=True)
        show_trace(st, turn)


def show_ticket(st, n, turn):
    ticket = turn["ticket"]
    with st.form("ticket%d" % n):
        st.markdown("### Phiếu nháp cho nhân viên (chưa gửi)")
        fields = [(("top", key), label, "; ".join(ticket[key]) if key == "evidence_to_attach" else ticket[key])
                  for key, label in FIELD_NAMES.items()]
        fields += [(("provided_fields", key), key, old) for key, old in ticket["provided_fields"].items()]
        fields += [(("missing_fields", key), "%s (còn thiếu)" % key, "") for key in ticket["missing_fields"]]
        columns = st.columns(2)
        values = {}
        for i, (place, label, old) in enumerate(fields):
            values[place] = columns[i % 2].text_input(label, old, key="t%d-%s-%s" % ((n,) + place))
        st.caption("Bản chạy thử: phiếu chỉ vào hộp mô phỏng của nhóm. Đừng nhập thông tin thật.")
        if st.form_submit_button("Gửi phiếu cho nhà xe (mô phỏng)"):
            if any(hide(v, key) != v for (_, key), v in values.items()):
                st.error(WARNING)
                return
            for (group, key), value in values.items():
                if group != "missing_fields" or value.strip():
                    set_field(ticket, (key, group, key), value.strip())
            try:
                turn["code"] = inbox.submit(ticket)
            except ValueError as e:
                st.error(str(e))
                return
            st.rerun()


def card(record):
    """Một phiếu dạng thẻ HTML; mọi chữ do người hoặc model nhập đều được thoát."""
    t = record["ticket"]
    rows = [("Loại việc", t["category"]), ("Muốn được giải quyết", t["requested_resolution"]),
            ("Bằng chứng", "; ".join(t["evidence_to_attach"]))] + list(t["provided_fields"].items())
    rows.append(("Còn thiếu", ", ".join(t["missing_fields"])))
    body = "".join("<br><small>%s:</small> %s" % (esc(k), esc(v)) for k, v in rows if v)
    return ('<div class="card"><span class="state s%d">%s</span><b>Phiếu %s</b> <small>· gửi %s</small>'
            '<p>%s%s</p></div>' % (inbox.STATES.index(record["state"]), esc(record["state"]), esc(record["code"]),
                                   esc(record["sent"]), esc(t["summary"] or "(không có tóm tắt)"), body))


def show_sent(st, n, code):
    """Phía khách: phiếu đã gửi, trạng thái và phản hồi của nhà xe."""
    record = inbox.find(code)
    if record is None:
        st.markdown('<div class="src"><p>Phiếu %s không còn trong hộp thử (máy chủ đã khởi động lại).</p></div>'
                    % esc(code), unsafe_allow_html=True)
        return
    st.markdown('<div class="src">%s<p><b>Nhà xe phản hồi</b>%s</p></div>'
                % (card(record), esc(record["reply"] or "Chưa có phản hồi.")), unsafe_allow_html=True)
    st.button("Xem cập nhật", key="refresh%d" % n)   # bấm là trang chạy lại và đọc lại hộp


def staff_page(st):
    """Màn nhà xe: xem phiếu, đổi trạng thái, phản hồi. Không đổi, huỷ hay hoàn vé nào."""
    if os.environ.get("APP_PASSCODE") and not os.environ.get("STAFF_PASSCODE"):
        st.info("Màn nhà xe đang khoá. Bản công khai cần đặt STAFF_PASSCODE trong Secrets.")
        return
    if not passcode_ok(st, "STAFF_PASSCODE", "Mã nhân viên nhà xe"):
        return
    records = inbox.tickets()
    waiting = sum(r["state"] == inbox.STATES[0] for r in records)
    st.markdown('<div class="top"><span class="orb"></span><span><b>Bàn xử lý phiếu · Xe Khách Mẫu</b>'
                '<small>%d phiếu mới / %d phiếu · mô phỏng, mất khi máy chủ khởi động lại</small></span></div>'
                % (waiting, len(records)), unsafe_allow_html=True)
    picked = st.segmented_control("Lọc trạng thái", ["Tất cả"] + inbox.STATES, default="Tất cả", key="filter",
                                  label_visibility="collapsed")
    st.button("Tải phiếu mới")
    shown = [r for r in records if picked in (None, "Tất cả", r["state"])]
    if not shown:
        st.markdown('<div class="foot">Chưa có phiếu nào ở mục này.</div>', unsafe_allow_html=True)
    with st.container(key="staff"):
        for r in shown:
            key = "%s-%d" % (r["code"], r["version"])   # phiếu đổi thì ô nhập lấy lại giá trị mới
            with st.form("staff-" + key):
                st.markdown(card(r), unsafe_allow_html=True)
                state = st.selectbox("Trạng thái", inbox.STATES, inbox.STATES.index(r["state"]), key="state-" + key)
                reply = st.text_area("Phản hồi cho khách", r["reply"], max_chars=500, key="reply-" + key)
                if st.form_submit_button("Lưu"):
                    try:
                        inbox.update(r["code"], state, reply)
                    except ValueError as e:
                        st.error(str(e))
                    else:
                        st.rerun()


def load_secrets(st):
    """Trên Streamlit Cloud, cấu hình nằm ở mục Secrets; chép sang biến môi trường trước khi nạp ai.py."""
    try:
        for key in SETTINGS:
            if key in st.secrets:
                os.environ.setdefault(key, str(st.secrets[key]))
    except Exception:  # chạy trên máy không có file secrets: dùng .env như cũ
        pass


def passcode_ok(st, setting="APP_PASSCODE", label="Mã truy cập bản chạy thử"):
    """Có đặt mã thì phải nhập đúng mới vào: APP_PASSCODE giữ tiền của key, STAFF_PASSCODE giữ phiếu của khách."""
    code = os.environ.get(setting, "")
    if not code or st.session_state.get("ok_" + setting):
        return True
    with st.form("gate_" + setting):
        typed = st.text_input(label, type="password")
        if st.form_submit_button("Vào"):
            if hmac.compare_digest(typed.strip().encode("utf-8"), code.encode("utf-8")):
                st.session_state["ok_" + setting] = True
                st.rerun()
            st.error("Mã chưa đúng.")
    return False


def page():
    import streamlit as st
    st.set_page_config(page_title="Trợ lý Xe Khách Mẫu", page_icon="🚌", layout="centered")
    st.markdown("<style>%s</style>" % CSS, unsafe_allow_html=True)
    load_secrets(st)
    if not passcode_ok(st):
        return
    import ai
    staff = st.session_state.get("is_staff", False)
    if st.button("💬 Khách hàng" if staff else "🧑‍💼 Nhà xe", key="switch",
                 help="Đổi giữa giao diện khách và giao diện nhà xe"):
        st.session_state["is_staff"] = not staff
        st.rerun()
    if staff:
        staff_page(st)
        return
    live = ai.MODEL_PROVIDER != "fake"
    turns = st.session_state.setdefault("turns", [])
    if not turns:
        if os.path.exists(HERO_PATH):
            st.image(HERO_PATH, use_container_width=True)
        st.markdown('<div class="hero"><h1>Hỏi nhà xe<br>trả lời có nguồn</h1>'
                    '<div class="script">Xin chào, bạn muốn đi đâu hôm nay?</div></div>', unsafe_allow_html=True)
    st.markdown('<div class="top"><span class="orb"></span><span><b>Trợ lý Xe Khách Mẫu</b><small class="%s">%s</small></span></div>'
                % ("" if live else "off",
                   "Đang sẵn sàng · dữ liệu mẫu" if live else "Chế độ thử, chưa nối model · dữ liệu mẫu"),
                unsafe_allow_html=True)
    # một cuộc trò chuyện, hai cách xem: chỉ vẽ một chế độ mỗi lần nên không trùng ô nhập của phiếu
    view = st.segmented_control("Chế độ xem", VIEWS, default=VIEWS[0], key="view", label_visibility="collapsed")
    sources = load_sources()
    for n, turn in enumerate(turns):
        show_turn(st, n, turn, sources, view == VIEWS[1])
    picked = None
    if not turns:
        cols = st.columns(2)
        for i, text in enumerate(SUGGESTIONS):
            if cols[i % 2].button(text, key="s%d" % i, use_container_width=True):
                picked = text
        st.markdown('<div class="foot">Tiền và vé của bạn do nhân viên quyết định. Đừng gửi mật khẩu, OTP, số thẻ.</div>',
                    unsafe_allow_html=True)
    elif st.button("Cuộc trò chuyện mới"):
        st.session_state["turns"] = []
        st.rerun()
    typed = st.chat_input("Hỏi giờ chạy, giá vé, chính sách…")
    text = (typed or picked or "").strip()
    if text:
        with st.spinner("Đang tra nguồn…"):
            turns.append(ask(text[:1000]))
        st.rerun()


def selfcheck():
    assert classify({"output": "x", "ticket_draft": {}})[0] == "ticket"
    kind, reply, ids = classify({"output": "Có chuyến 06:00.\nNguồn: [XKM-LICH-HNHP] Bảng giờ (phiên bản 2026-11-01)"})
    assert (kind, reply, ids) == ("answer", "Có chuyến 06:00.", ["XKM-LICH-HNHP"])
    assert classify({"output": "Tuyến nào?"})[0] == "clarify"
    assert classify({"output": "thử"}, ["fake"])[0] == "fake"
    blocked = ask("OTP của mình là 482913")
    assert blocked["kind"] == "blocked" and "482913" not in json.dumps(blocked)
    assert len(trace_steps(blocked)) == 1
    steps = trace_steps({"kind": "ticket", "found": ["XKM-CS-HUY"], "events": [
        {"kind": "tool", "name": "search_knowledge", "latency_s": 0.01},
        {"kind": "model", "model": "m", "tokens_in": 5, "tokens_out": 2, "latency_s": 0.4,
         "output": '{"decision": "ticket_draft"}'},
        {"kind": "note", "text": "chặn"}]})
    assert [x[0] for x in steps] == ["Lọc dữ liệu nhạy cảm", "Công cụ search_knowledge", "Gọi model",
                                     "Chốt chặn của luồng", "Kết quả"]
    assert "XKM-CS-HUY" in steps[1][1] and "ticket_draft" in steps[2][1]
    os.environ["MAX_CALLS"] = "0"
    assert ask("Xe đi Hải Phòng mấy giờ?")["kind"] == "error"   # hết lượt: không gọi model
    del os.environ["MAX_CALLS"]
    assert "XKM-LICH-HNHP" in load_sources()
    assert load_sources("khong-co-file.json") == {}
    ticket = normalize_ticket({"summary": "<b>x</b>", "missing_fields": ["ngay_di"]})
    code = inbox.submit(ticket)
    assert inbox.find(code)["state"] == "Mới" and "<b>x" not in card(inbox.find(code))
    assert "\n" not in esc("a\n\n[b](c)") and "\r" not in esc("a\r\rb")
    assert inbox.update(code, "Đã xử lý", "Nhân viên sẽ gọi lại") and not inbox.update("XKM-KHONG", "Mới", "")
    for bad in (lambda: inbox.submit({"provided_fields": {"ma_otp": "654321"}}),
                lambda: inbox.update(code, "Đã xử lý", "OTP 482913"), lambda: inbox.update(code, "Khác", "")):
        try:
            bad()
        except ValueError:
            continue
        raise AssertionError("hộp phiếu phải từ chối")
    assert len(inbox.tickets()) == 1 and inbox.find(code)["reply"] == "Nhân viên sẽ gọi lại"
    for _ in range(inbox.MAX_TICKETS):   # đầy: bỏ phiếu đã xử lý trước, không bỏ phiếu đang chờ
        inbox.submit(ticket)
    assert inbox.find(code) is None and len(inbox.tickets()) == inbox.MAX_TICKETS
    try:
        inbox.submit(ticket)
    except ValueError as e:
        assert str(e) == inbox.FULL
    else:
        raise AssertionError("hộp đầy phiếu chờ thì không nhận thêm")
    print("web selfcheck OK")
    return 0


if __name__ == "__main__":
    if sys.argv[1:] == ["selfcheck"]:
        sys.exit(selfcheck())
    page()
