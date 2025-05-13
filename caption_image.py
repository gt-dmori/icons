from PIL import Image
from transformers import BlipProcessor, BlipForConditionalGeneration
import os

# 画像ファイル名
image_path = "images_5x5/ChatGPT Image 2025年5月13日 21_51_39.png"

# スクリプトのあるディレクトリに画像がある前提
script_dir = os.path.dirname(os.path.abspath(__file__))
img_full_path = os.path.join(script_dir, image_path)

try:
    if not os.path.exists(img_full_path):
        raise FileNotFoundError(f"画像ファイルが見つかりません: {img_full_path}")

    # モデルとプロセッサのロード
    processor = BlipProcessor.from_pretrained("Salesforce/blip-image-captioning-base")
    model = BlipForConditionalGeneration.from_pretrained("Salesforce/blip-image-captioning-base")

    # 画像の読み込み
    img = Image.open(img_full_path)

    # 英語キャプション生成
    inputs = processor(img, return_tensors="pt")
    out = model.generate(**inputs, max_length=10)
    caption_en = processor.decode(out[0], skip_special_tokens=True)

    print("英語キャプション:", caption_en)

except FileNotFoundError as e:
    print(e)
    exit(1)
except Exception as e:
    print(f"エラーが発生しました: {e}")
    exit(1) 