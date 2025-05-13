import os
import re

def make_icon_list(output_dir="output", docs_dir="docs", icons_per_row=20):
    os.makedirs(docs_dir, exist_ok=True)
    html_file = os.path.join(docs_dir, "icon_list.html")
    github_base_url = "https://raw.githubusercontent.com/gt-dmori/icons/main/output/"

    # ファイル名で数字部分を抽出してソート
    def extract_number(filename):
        m = re.search(r'(\d+)', filename)
        return int(m.group(1)) if m else 0

    # PNGファイルを数字順にソート
    files = [f for f in os.listdir(output_dir) if f.lower().endswith(".png")]
    files.sort(key=extract_number)

    with open(html_file, "w", encoding="utf-8") as f:
        f.write("<html><head><meta charset='utf-8'><title>Icon List</title></head><body>\n")
        f.write("<h1>Icon List</h1>\n")
        f.write("<table>\n<tr>\n")
        for idx, filename in enumerate(files):
            img_url = github_base_url + filename
            f.write(f"<td><a href='{img_url}' target='_blank'><img src='{img_url}' width='64' height='64'></a></td>\n")
            if (idx + 1) % icons_per_row == 0:
                f.write("</tr>\n<tr>\n")
        f.write("</tr>\n</table>\n")
        f.write("</body></html>\n")

    print(f"icon_list.html を {docs_dir} に作成しました。")

if __name__ == "__main__":
    make_icon_list() 