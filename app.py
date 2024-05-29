import streamlit as st
from openai import OpenAI


def APIINPUT():
    st.header("API Key 를 입력하세요")
    API = st.text_input("API", type="password")
    if API:
        st.session_state.API = API

def chating():
    st.header("무엇이든 물어보세요.")
    prompt = st.text_input("질문?")
    
    if prompt and 'API' in st.session_state:
        client = OpenAI(api_key=st.session_state.API)
        response = client.chat_completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "You are a helpful assistant."},
                {"role": "user", "content": prompt}
            ]
        )
        with st.chat_message("AI"):
            st.write(response.choices[0].message.content)
    elif not prompt:
        st.write("질문을 입력하세요.")
    else:
        st.write("API Key를 먼저 입력하세요.")

def drawing():
    
    st.header("무엇이든 그려보세요.")
    pprompt = st.text_input("프롬프트?")

    from openai import OpenAI
    client = OpenAI(api_key=API)
    response = client.images.generate(model="dall-e-3",prompt=pprompt)
    image_url = response.data[0].url
    st.markdown("![alt text](image_url)") # 웹 이미지 보여주기
    st.image(image_url)
  


page = st.sidebar.selectbox("페이지 선택", ["API", "챗봇", "그림"])


if page == "API":
    APIINPUT()
elif page == "챗봇":
    chating()
elif page == "그림":
    drawing()