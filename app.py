import streamlit as st
import json
from openai import OpenAI

# OpenAIクライアント（新方式）
client = OpenAI(api_key="")

# ツールDB（ローカル推薦用）
tool_db = [
    {"name": "ChatGPT", "genre": ["要約", "文章生成"], "speed": "中", "accuracy": "高", "price": "無料枠あり", "url": "https://chat.openai.com"},
    {"name": "Glarity", "genre": ["要約", "動画"], "speed": "高", "accuracy": "中", "price": "無料", "url": "https://glarity.app"},
    {"name": "Devin", "genre": ["コード", "自動化"], "speed": "高", "accuracy": "高", "price": "有料", "url": "https://cognition-labs.com"}
]

# ---------------------- UI ----------------------
st.title("🧭 Navigator - AIツールナビ")

st.markdown("### 🔘 重視する項目を選んでください")
options = st.multiselect("重視項目を選択", ["精度", "速さ", "価格（無料）"])

user_input = st.text_area("💬 やりたいことを教えてください：", placeholder="例：YouTubeを5分に要約したい")

if st.button("🚀 ツールを探す") and user_input:

    # ----------------------------------------
    # ① ChatGPTにジャンル分類させる
    # ----------------------------------------
    with st.spinner("ジャンルを分類中..."):
        genre_response = client.chat.completions.create(
            model="gpt-4",
            messages=[
                {"role": "system", "content": "あなたはAIコンシェルジュです。ユーザーの入力からジャンルを1語で出力してください。"},
                {"role": "user", "content": user_input}
            ]
        )
        genre = genre_response.choices[0].message.content.strip()
    st.success(f"ジャンル：{genre}")

   
    # ----------------------------------------
    # ③ ChatGPTによる「ダイナミック推薦」
    # ----------------------------------------
    st.markdown("---")
    st.markdown("## 🤖 ChatGPTによるおすすめ生成AI")

    with st.spinner("AIが最適なツールを選んでいます..."):
        recommendation_response = client.chat.completions.create(
            model="gpt-4",
            messages=[
                {"role": "system", "content": "あなたは最新の生成AIに詳しい専門家です。ユーザーの目的に対して、今最も適したAIツールを3つ提案してください。出力形式は：\n\nツール名｜特徴（40文字）｜URL"},
                {"role": "user", "content": f"目的：{user_input}"}
            ]
        )
        recommendation_text = recommendation_response.choices[0].message.content.strip()

    st.markdown(recommendation_text)
