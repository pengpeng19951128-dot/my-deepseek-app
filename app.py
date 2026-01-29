import streamlit as st
from openai import OpenAI

st.set_page_config(page_title="DeepSeek助手", layout="centered")
st.title("🤖 我的私人 AI 助手")

with st.sidebar:
    st.header("设置")
    api_key = st.text_input("请输入 DeepSeek API Key:", type="password")

if "messages" not in st.session_state:
    st.session_state.messages = []

for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

if prompt := st.chat_input("输入问题..."):
    if not api_key:
        st.error("请填入 Key")
    else:
        st.session_state.messages.append({"role": "user", "content": prompt})
        with st.chat_message("user"):
            st.markdown(prompt)
        try:
            client = OpenAI(api_key=api_key, base_url="https://api.deepseek.com")
            with st.chat_message("assistant"):
                response_placeholder = st.empty()
                full_response = ""
                completion = client.chat.completions.create(
                    model="deepseek-chat",
                    messages=[{"role": m["role"], "content": m["content"]} for m in st.session_state.messages],
                    stream=True
                )
                for chunk in completion:
                    if chunk.choices[0].delta.content:
                        full_response += chunk.choices[0].delta.content
                        response_placeholder.markdown(full_response + "▌")
                response_placeholder.markdown(full_response)
            st.session_state.messages.append({"role": "assistant", "content": full_response})
        except Exception as e:
            st.error(f"出错了：{str(e)}")
