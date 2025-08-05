import streamlit as st

# openai 라이브러리 임포트 (app.py 상단에서 import 권장)
from openai import OpenAI


st.title("🧠 심리상담 챗봇 (Solar Pro2)")

# Upstage Solar Pro2 API 키와 엔드포인트
client = OpenAI(
    api_key= st.secrets["OPENAI_API_KEY"],
    base_url="https://api.upstage.ai/v1"
)

if "messages" not in st.session_state:
    st.session_state.messages = [
        {"role": "assistant", "content": "안녕하세요. 심리상담 챗봇입니다. 무엇이든 편하게 말씀해 주세요."}
    ]

# 이전 대화 출력
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# 사용자 입력 받기
if prompt := st.chat_input("고민이나 궁금한 점을 입력해 주세요."):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    # Upstage Solar Pro2로 메시지 전송 (스트리밍)
    with st.chat_message("assistant"):
        stream = client.chat.completions.create(
            model="solar-pro2",
            messages=[
                {"role": m["role"], "content": m["content"]}
                for m in st.session_state.messages
            ],
            stream=True,
        )
        response_text = ""
        response_area = st.empty()
        for chunk in stream:
            if chunk.choices[0].delta.content is not None:
                response_text += chunk.choices[0].delta.content
                response_area.markdown(response_text + "▌")
        response_area.markdown(response_text)
    st.session_state.messages.asppend({"role": "assistant", "content": response_text})

