"""Lấy review mới nhất trên Google Play của một app. Chỉ dùng thư viện chuẩn.

    python evidence/fetch_reviews.py com.vexere.vexere 200

Ghi evidence/raw-<app>.json (đã .gitignore): ngày, số sao, nội dung. KHÔNG lấy tên người viết.
"""
import datetime
import json
import os
import sys
import urllib.parse
import urllib.request

app, count = sys.argv[1], int(sys.argv[2])
inner = json.dumps([None, [2, 2, [count], None, [None, None]], [app, 7]])  # sắp xếp 2 = mới nhất
body = urllib.parse.urlencode({"f.req": json.dumps([[["oCPfdb", inner, None, "generic"]]])}).encode()
req = urllib.request.Request(
    "https://play.google.com/_/PlayStoreUi/data/batchexecute?hl=vi&gl=VN", data=body,
    headers={"Content-Type": "application/x-www-form-urlencoded;charset=utf-8", "User-Agent": "generic-client"})
raw = urllib.request.urlopen(req, timeout=30).read().decode("utf-8")
payload = json.loads(raw.split("\n", 2)[2])[0][2]
if not payload:
    sys.exit("Google Play không trả dữ liệu; định dạng yêu cầu có thể đã đổi.")
rows = [{"ngay": datetime.datetime.fromtimestamp(r[5][0], datetime.timezone(datetime.timedelta(hours=7))).strftime("%Y-%m-%d"),
         "so_sao": r[2], "noi_dung": r[4] or ""} for r in json.loads(payload)[0]][:count]
out = os.path.join(os.path.dirname(os.path.abspath(__file__)), "raw-%s.json" % app)
with open(out, "w", encoding="utf-8") as f:
    json.dump(rows, f, ensure_ascii=False, indent=1)
print("%d review, từ %s đến %s → %s" % (len(rows), rows[-1]["ngay"], rows[0]["ngay"], os.path.basename(out)))
