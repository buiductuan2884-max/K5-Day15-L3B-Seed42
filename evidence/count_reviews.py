"""Đếm review đã gắn nhãn — Trương Anh Đức. Cách đếm ghi trước ở evidence/data-mining.md mục 1.

    python evidence/count_reviews.py                     (mặc định đọc evidence/review_labels.csv)
    python evidence/count_reviews.py duong/dan/khac.csv

File nhãn: mỗi review một dòng, cột  stt, ngay, so_sao, trich, nhan, ghi_chu
  - trich: tối đa 2 câu nguyên văn, KHÔNG chép tên người viết
  - nhan:  một hoặc nhiều nhãn cách nhau bằng dấu ;  (hoan_tien · doi_huy · nha_xe_doi · thong_tin · ho_tro · khac · chua_thong_nhat)
Mẫu số N = MỌI review đã đọc và gắn nhãn, kể cả review không liên quan (nhãn khac).
Một review có thể mang nhiều nhãn, nên tổng các % có thể vượt 100%. Dòng "có ≥1 nhãn đổi/huỷ/hoàn" đếm mỗi review một lần.
Chỉ dùng thư viện chuẩn. Chỉ đọc, không sửa file.
"""
import csv
import os
import sys

for _stream in (sys.stdout, sys.stderr):
    try:
        _stream.reconfigure(encoding="utf-8", errors="replace")
    except Exception:
        pass

HERE = os.path.dirname(os.path.abspath(__file__))
LABELS = ["hoan_tien", "doi_huy", "nha_xe_doi", "thong_tin", "ho_tro", "khac", "chua_thong_nhat"]
PAIN = {"hoan_tien", "doi_huy", "nha_xe_doi"}
SUPPORT = {"thong_tin", "ho_tro"}


def main(argv):
    path = argv[0] if argv else os.path.join(HERE, "review_labels.csv")
    with open(path, encoding="utf-8-sig", newline="") as f:
        rows = list(csv.DictReader(f))
    n = len(rows)
    if not n:
        print("%s chưa có dòng nào — gắn nhãn xong rồi chạy lại." % path)
        return 0
    counts = {k: 0 for k in LABELS}
    bad, pain_any, by_star = [], 0, {}
    for r in rows:
        labels = {x.strip() for x in (r.get("nhan") or "").split(";") if x.strip()}
        unknown = labels - set(LABELS)
        if not labels or unknown:
            bad.append(r.get("stt") or "?")
        for k in labels & set(LABELS):
            counts[k] += 1
        if labels & PAIN:
            pain_any += 1
            star = (r.get("so_sao") or "?").strip()
            by_star[star] = by_star.get(star, 0) + 1
    print("File: %s · N = %d review đã đọc và gắn nhãn" % (path, n))
    for k in LABELS:
        print("  %-11s %d/%d (%.1f%%)" % (k, counts[k], n, 100.0 * counts[k] / n))
    print("  có ≥1 nhãn đổi/huỷ/hoàn: %d/%d (%.1f%%)" % (pain_any, n, 100.0 * pain_any / n))
    support = sum(bool(SUPPORT & {x.strip() for x in (r.get("nhan") or "").split(";")}) for r in rows)
    print("  có thong_tin hoặc ho_tro: %d/%d (%.1f%%)" % (support, n, 100.0 * support / n))
    check = os.path.join(HERE, "hand_check.csv")
    if not argv and os.path.exists(check):
        with open(check, encoding="utf-8-sig", newline="") as f:
            checked = list(csv.DictReader(f))
        out = {c["stt"] for c in checked if c["pham_vi"] != "trong_pham_vi"}
        fixed = {c["stt"]: c["nhan_sau_kiem"] for c in checked}
        left = [{x.strip() for x in fixed.get(r["stt"], r.get("nhan") or "").split(";")} for r in rows if r["stt"] not in out]
        print("Sau kiểm tay (%d dòng đã xem, bỏ %d dòng ngoài phạm vi, giữ mẫu số %d):" % (len(checked), len(out), n))
        for name, group in (("có ≥1 nhãn đau", PAIN | SUPPORT), ("đổi/huỷ/hoàn", PAIN), ("thong_tin hoặc ho_tro", SUPPORT)):
            x = sum(bool(group & s) for s in left)
            print("  %s: %d/%d (%.1f%%)" % (name, x, n, 100.0 * x / n))
    if by_star:
        print("  trong đó theo số sao: " + " · ".join("%s sao: %d" % kv for kv in sorted(by_star.items())))
    if bad:
        print("⚠️ Dòng thiếu nhãn hoặc nhãn lạ (stt): " + ", ".join(bad))
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
