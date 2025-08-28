import os
import base64
from openai import OpenAI
from dotenv import load_dotenv

# .env ファイルを読み込む
load_dotenv()

# 環境変数から API キーを取得
api_key = os.getenv("OPENAI_API_KEY")

if not api_key:
    raise ValueError("OPENAI_API_KEY が設定されていません。.env を確認してください。")

# OpenAI クライアントを初期化
client = OpenAI(api_key=api_key)

def encode_image(image_path):
    with open(image_path, "rb") as f:
        return base64.b64encode(f.read()).decode("utf-8")

# PNGファイル（保存済みのガイドライン＆デザインカンプ）
guideline_img = encode_image("guideline.png")
design_img = encode_image("design.png")

prompt = """
あなたはデザインチェックAIです。
1. guideline.png から色とフォントのルールを抽出

2. design.png から以下の情報を抽出
- sectionName: セクション名（TOP / NEWS / ABOUT / CONTACT）
- elements: 各UI要素の配列。要素ごとに以下の情報を含めてください。
  - type: 要素の種類（title, text, button, input, line, logo, menu など）
  - content: テキストがある場合はその文字列。なければ null
  - fontFamily: フォントファミリー。わからない場合は "unknown"
  - fontSize: フォントサイズ。わからない場合は "unknown"
  - color: カラーコード（例: "#FFFFFF"）。わからない場合は "unknown"
### 注意事項
- 不明な場合は必ず "unknown" と出力してください
- デザインをセクション（TOP / NEWS / ABOUT / CONTACT）ごとに分けて出力してください
- 各セクションの主要なUI要素のみを対象にしてください

3. 両者を比較し、差分を **Markdown** 形式で出力してください。
"""

response = client.chat.completions.create(
    model="gpt-4o-mini",  # 画像対応モデル
    messages=[
        {"role": "system", "content": "あなたは厳密なデザイン監査AIです。"},
        {
            "role": "user",
            "content": [
                {"type": "text", "text": prompt},
                {"type": "image_url", "image_url": {"url": f"data:image/png;base64,{guideline_img}"}},
                {"type": "image_url", "image_url": {"url": f"data:image/png;base64,{design_img}"}},
            ],
        },
    ],
)

report = response.choices[0].message.content

# Markdownファイルに保存
with open("diff_report.md", "w", encoding="utf-8") as f:
    f.write(report)

print("✅ 差分レポートを diff_report.md に保存しました！")