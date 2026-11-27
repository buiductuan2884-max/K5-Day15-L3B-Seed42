"""Ghép nhãn của hai model thành evidence/review_labels.csv và in độ khớp.

    python evidence/merge_labels.py

Đọc: evidence/raw-<app>.json (chạy fetch_reviews.py), evidence/labels_claude.csv, evidence/labels_openai.csv.
Luật chốt: một nhãn được tính khi CẢ HAI model cùng gắn. Dòng không có nhãn chung ghi chua_thong_nhat.
Mọi dòng lệch ghi cả hai ý kiến ở ghi_chu để người kiểm tay quyết.
"""
import csv
import json
import os
import re
import sys

sys.stdout.reconfigure(encoding="utf-8", errors="replace")
HERE = os.path.dirname(os.path.abspath(__file__))
APP = "com.vexere.vexere"
LABELS = ["hoan_tien", "doi_huy", "nha_xe_doi", "thong_tin", "ho_tro", "khac"]


def read(name):
    out = {}
    with open(os.path.join(HERE, name), encoding="utf-8-sig") as f:
        for line in f:
            m = re.match(r"\s*(\d+)\s*,\s*(.+?)\s*$", line)
            if m:
                out[int(m.group(1))] = {x.strip() for x in m.group(2).split(";") if x.strip()}
    return out


def quote(text):
    text = re.sub(r"[\w.+-]+@[\w-]+\.[\w.]+", "[email]", " ".join(text.split()))
    text = re.sub(r"(?<!\d)(?:\+?84|0)(?:[ .-]?\d){8,10}(?!\d)", "[sdt]", text)
    return " ".join(re.split(r"(?<=[.!?])\s+", text)[:2])[:220]


def main():
    path = os.path.join(HERE, "raw-%s.json" % APP)
    rows = json.load(open(path, encoding="utf-8")) if os.path.exists(path) else None
    if rows is None:
        sys.exit("Thiếu %s — chạy fetch_reviews.py trước." % os.path.basename(path))
    a, b = read("labels_claude.csv"), read("labels_openai.csv")
    n = len(rows)
    for name, d in (("claude", a), ("openai", b)):
        missing = [i for i in range(1, n + 1) if i not in d]
        unknown = [i for i, v in d.items() if v - set(LABELS)]
        assert not missing and not unknown, (name, missing[:10], unknown[:10])
    same = 0
    with open(os.path.join(HERE, "review_labels.csv"), "w", encoding="utf-8-sig", newline="") as f:
        w = csv.writer(f)
        w.writerow(["stt", "ngay", "so_sao", "trich", "nhan", "ghi_chu"])
        for i, r in enumerate(rows, 1):
            agreed = sorted(a[i] & b[i], key=LABELS.index)
            note = ""
            if a[i] == b[i]:
                same += 1
            else:
                note = "lech: claude=%s | openai=%s" % ("+".join(sorted(a[i])), "+".join(sorted(b[i])))
            w.writerow([i, r["ngay"], r["so_sao"], quote(r["noi_dung"]), ";".join(agreed) or "chua_thong_nhat", note])
    print("N = %d · khớp hoàn toàn %d/%d (%.1f%%)" % (n, same, n, 100.0 * same / n))
    print("nhãn        claude  openai  cả hai  ít nhất một")
    for k in LABELS:
        x = sum(k in a[i] for i in range(1, n + 1))
        y = sum(k in b[i] for i in range(1, n + 1))
        both = sum(k in a[i] and k in b[i] for i in range(1, n + 1))
        print("%-11s %5d  %6d  %6d  %6d" % (k, x, y, both, x + y - both))
    for tag, sel in (("thong_tin hoặc ho_tro", {"thong_tin", "ho_tro"}), ("đổi/huỷ/hoàn/nhà xe đổi", {"hoan_tien", "doi_huy", "nha_xe_doi"})):
        both = sum(bool(a[i] & sel) and bool(b[i] & sel) for i in range(1, n + 1))
        either = sum(bool(a[i] & sel) or bool(b[i] & sel) for i in range(1, n + 1))
        print("%s: cả hai %d/%d (%.1f%%) · ít nhất một %d/%d (%.1f%%)" % (tag, both, n, 100.0 * both / n, either, n, 100.0 * either / n))


if __name__ == "__main__":
    main()
