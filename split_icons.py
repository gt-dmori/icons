import os
from PIL import Image

input_dir = "images_5x5"
output_dir = "output"
os.makedirs(output_dir, exist_ok=True)

TRANSPARENT_THRESHOLD = 128  # アルファ値がこの値未満なら透明とみなす

def is_fully_transparent(img):
    """画像がすべて透明（閾値128未満）か判定"""
    arr = img.getdata()
    return all(pixel[3] < TRANSPARENT_THRESHOLD for pixel in arr)

def get_non_transparent_centroid(img):
    """透明でないピクセルの重心を求める"""
    arr = img.load()
    w, h = img.size
    xs, ys = [], []
    for y in range(h):
        for x in range(w):
            if arr[x, y][3] >= TRANSPARENT_THRESHOLD:
                xs.append(x)
                ys.append(y)
    if not xs or not ys:
        return w // 2, h // 2  # 全部透明なら中央
    cx = sum(xs) / len(xs)
    cy = sum(ys) / len(ys)
    return cx, cy

def find_transparent_lines(img):
    """縦横のすべて透明なラインのインデックスを返す（閾値128未満で透明判定）"""
    img = img.convert("RGBA")
    arr = img.load()
    w, h = img.size

    # 横方向
    transparent_rows = []
    for y in range(h):
        if all(arr[x, y][3] < TRANSPARENT_THRESHOLD for x in range(w)):
            transparent_rows.append(y)

    # 縦方向
    transparent_cols = []
    for x in range(w):
        if all(arr[x, y][3] < TRANSPARENT_THRESHOLD for y in range(h)):
            transparent_cols.append(x)

    return transparent_rows, transparent_cols

def find_split_points(transparent_indices, size):
    """連続した透明ラインの中央を区切り線とする"""
    if not transparent_indices:
        return [0, size]
    splits = []
    start = transparent_indices[0]
    for i in range(1, len(transparent_indices)):
        if transparent_indices[i] != transparent_indices[i-1] + 1:
            end = transparent_indices[i-1]
            splits.append((start, end))
            start = transparent_indices[i]
    splits.append((start, transparent_indices[-1]))
    # 画像端も分割点に追加
    points = [0]
    for s, e in splits:
        points.append((s + e) // 2)
    points.append(size)
    return points

def process_image(filepath):
    img = Image.open(filepath).convert("RGBA")
    w, h = img.size
    rows, cols = find_transparent_lines(img)
    row_splits = find_split_points(rows, h)
    col_splits = find_split_points(cols, w)

    basename = os.path.splitext(os.path.basename(filepath))[0]
    total = 0
    print(f"{basename}: {len(row_splits)-1}行 × {len(col_splits)-1}列 = {(len(row_splits)-1)*(len(col_splits)-1)}分割")
    print(f"  row_splits: {row_splits}")
    print(f"  col_splits: {col_splits}")
    count = 1
    for i in range(len(row_splits)-1):
        for j in range(len(col_splits)-1):
            left, upper = col_splits[j], row_splits[i]
            right, lower = col_splits[j+1], row_splits[i+1]
            if right - left <= 0 or lower - upper <= 0:
                continue
            icon = img.crop((left, upper, right, lower))
            # アスペクト比維持で128x128にリサイズ
            icon.thumbnail((128, 128), Image.LANCZOS)
            out_img = Image.new("RGBA", (128, 128), (0, 0, 0, 0))
            # 重心を求めてオフセット
            cx, cy = get_non_transparent_centroid(icon)
            offset_x = int(64 - cx)
            offset_y = int(64 - cy)
            out_img.paste(icon, (offset_x, offset_y), icon)
            # すべて透明なら保存しない
            if is_fully_transparent(out_img):
                continue
            out_name = f"{basename}{count:02d}.png"
            out_path = os.path.join(output_dir, out_name)
            out_img.save(out_path)
            count += 1
            total += 1
    print(f"  => {total}個のアイコンを保存")

# メイン処理
for fname in os.listdir(input_dir):
    if fname.lower().endswith((".png", ".jpg", ".jpeg")):
        process_image(os.path.join(input_dir, fname))

print("分割・リサイズ完了！") 