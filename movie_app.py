import streamlit as st
import requests

# 配置DeepSeek API（通过secrets安全存储，不泄露）
DEEPSEEK_API_KEY = st.secrets["DEEPSEEK_API_KEY"]
API_URL = "https://api.deepseek.com/v1/chat/completions"

# 页面标题
st.title("🎬 电影解说文案生成器")
st.subheader("输入电影名，一键生成3种风格解说文案")

# 1. 用户输入
movie_name = st.text_input("请输入电影名称：", placeholder="例如：《肖申克的救赎》")
style = st.selectbox("选择解说风格：", ["幽默风", "深情风", "专业风"])

# 2. 生成文案按钮
if st.button("生成解说文案") and movie_name:
    with st.spinner("正在生成文案..."):
        # 构造不同风格的提示词
        style_prompt = {
            "幽默风": "用轻松搞笑、网感十足的语气，写一段300字左右的电影解说文案，包含剧情简介、精彩片段分析、个人感悟，适合短视频口播",
            "深情风": "用细腻深情、有感染力的语气，写一段300字左右的电影解说文案，包含剧情简介、精彩片段分析、个人感悟，适合情感向短视频",
            "专业风": "用专业影评的严谨语气，写一段300字左右的电影解说文案，包含剧情简介、镜头语言分析、主题深度解读，适合干货向短视频"
        }
        
        # 构造API请求
        headers = {
            "Authorization": f"Bearer {DEEPSEEK_API_KEY}",
            "Content-Type": "application/json"
        }
        data = {
            "model": "deepseek-chat",
            "messages": [
                {"role": "system", "content": style_prompt[style]},
                {"role": "user", "content": f"电影：{movie_name}"}
            ],
            "temperature": 0.7,
            "max_tokens": 600
        }
        
        # 调用API
        try:
            response = requests.post(API_URL, headers=headers, json=data, timeout=30)
            if response.status_code == 200:
                result = response.json()
                script = result["choices"][0]["message"]["content"]
                # 显示结果
                st.success("✅ 文案生成完成！")
                st.text_area("生成的解说文案：", value=script, height=300)
                # 一键复制按钮
                st.code(script, language="text")
                st.info("👆 点击右上角复制按钮，直接复制文案使用")
            else:
                st.error(f"生成失败：{response.text}")
        except Exception as e:
            st.error(f"网络/API错误：{str(e)}")

# 3. 项目说明
with st.expander("📖 项目说明"):
    st.write("""
    本工具基于DeepSeek大模型API开发，支持3种风格的电影解说文案生成：
    - 幽默风：适合搞笑类、吐槽类短视频
    - 深情风：适合情感类、治愈类短视频
    - 专业风：适合干货类、影评类短视频
    生成的文案可直接用于视频剪辑、自媒体创作，一键复制，高效便捷。
    """)
