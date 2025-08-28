import os
import requests
from dotenv import load_dotenv

load_dotenv()

FIGMA_TOKEN = os.environ["FIGMA_TOKEN"]
FILE_KEY = os.environ["FILE_KEY"]

headers = {
    "X-Figma-Token": FIGMA_TOKEN
}

# 1. ファイル構造を取得
url = f"https://api.figma.com/v1/files/{FILE_KEY}"
response = requests.get(url, headers=headers)
data = response.json()

def find_node_id(node, keywords):
    """ノード名にkeywordsが含まれるものを探す"""
    if any(k.lower() in node["name"].lower() for k in keywords):
        return node["id"]
    if "children" in node:
        for child in node["children"]:
            nid = find_node_id(child, keywords)
            if nid:
                return nid
    return None

# 2. ガイドライン用ノードを探索
guideline_id = find_node_id(data["document"], ["guideline", "style", "ガイドライン"])
# 3. デザインカンプ用ノードを探索
camp_id = find_node_id(data["document"], ["comp", "design", "カンプ"])

print("✅ ガイドラインID:", guideline_id)
print("✅ デザインカンプID:", camp_id)

# 4. PNG書き出し
if guideline_id and camp_id:
    url = f"https://api.figma.com/v1/images/{FILE_KEY}?ids={guideline_id},{camp_id}&format=png"
    res = requests.get(url, headers=headers).json()
    for node_id, img_url in res["images"].items():
        img_data = requests.get(img_url).content
        filename = f"output_{node_id.replace(':','-')}.png"
        with open(filename, "wb") as f:
            f.write(img_data)
        print(f"📂 {filename} を保存しました")
else:
    print("❌ 対象のノードが見つかりませんでした")