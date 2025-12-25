import re, csv
from pathlib import Path

md = Path("/Users/hideyuki/Documents/zen-content/memo/articles_list_sorted.md")
out = Path("/Users/hideyuki/Documents/zen-content/memo/articles_list_sorted.csv")

lines = md.read_text(encoding="utf-8").splitlines()
# ヘッダ行と区切り行を探す
start = 0
for i, ln in enumerate(lines):
    if ln.startswith("| タイトル"):
        start = i
        break
# データはヘッダの2行後から
data_lines = lines[start+2:]

rows = []
for ln in data_lines:
    ln = ln.strip()
    if not ln or not ln.startswith("|"):
        continue
    # 先頭末尾の | を除去し、" | " で分割（セル内のパイプは基本的に存在しない前提）
    cells = [c.strip() for c in re.split(r'\s\|\s', ln.strip("|"))]
    rows.append(cells)

with out.open("w", newline="", encoding="utf-8") as f:
    writer = csv.writer(f)
    # ヘッダを書き込む（元ヘッダから取得）
    header = [h.strip() for h in re.split(r'\s\|\s', lines[start].strip("|"))]
    writer.writerow(header)
    writer.writerows(rows)

print("wrote", out)