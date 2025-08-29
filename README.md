# 🎨 Figma Design Diff Checker

Figma から抽出したデザイン画像をもとに、デザインガイドラインとの **差分を自動検出・レポート化** する Python ツールです。  
このリポジトリには以下の 2 つのプログラムが含まれます：

1. **01_get-png.py**  
   Figma API を利用して「デザインガイドライン」と「デザインカンプ」のフレームを探索・PNG形式で保存  

2. **02_check.py**  
   抽出した PNG を OpenAI API に渡し、ガイドラインとカンプを比較して差分を **Markdown レポート** に出力

---

## 📂 ファイル構成

```bash
├── 01_get-png.py # Figma から PNG を抽出
├── 02_check.py # PNG を比較して差分レポートを生成
├── requirements.txt
├── .env.example
└── README.md
```

---

## 🚀 セットアップ

### 1. リポジトリをクローン

```bash
git clone https://github.com/yourname/figma-design-diff-checker.git
cd figma-design-diff-checker
```

### 2. 必要ライブラリをインストール

```bash
pip install -r requirements.txt
```

requirements.txt の内容:
```bash
requests
python-dotenv
openai
```

### 3. 環境変数を設定
.env を作成し、以下を設定してください。

```bash
# Figma用
FIGMA_TOKEN=あなたのFigmaAPIトークン
FILE_KEY=対象のFigmaファイルキー

# OpenAI用
OPENAI_API_KEY=あなたのOpenAI APIキー
```

## 📌 使い方
### 1. FigmaからPNGを抽出
```bash
python extractor.py
```
成功すると output_<node_id>.png が保存されます。
ガイドライン画像とデザインカンプ画像を、それぞれ guideline.png と design.png にリネームしてください。

### 2. 差分チェックを実行
```bash
python diff_checker.py
```
成功すると、比較レポートが diff_report.md として保存されます。

## 📑 出力例
```bash
✅ ガイドラインID: 12:34
✅ デザインカンプID: 56:78
📂 output_12-34.png を保存しました
📂 output_56-78.png を保存しました
✅ 差分レポートを diff_report.md に保存しました！
```

レポート (diff_report.md) のイメージ：
```markdown
# 差分レポート

## TOP
- Title のフォントサイズが異なります (guideline: 32px / design: 28px)
- ボタンのカラーが異なります (#FF0000 → #F85C5C)

## ABOUT
- "会社概要" テキストのフォントファミリーが unknown
⚠️ 注意事項
抽出対象のフレーム名は guideline, style, ガイドライン / comp, design, カンプ で探索されます。必要に応じて extractor.py 内の keywords を変更してください。
```

diff_checker.py のプロンプトは、使用するデザインに合わせて調整してください。

OpenAI API 利用によりトークン料金が発生します。

## 📝 ライセンス
MIT
