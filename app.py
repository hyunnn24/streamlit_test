import streamlit as st

page = st.sidebar.selectbox("페이지 선택", ["챗봇", "페이지 1", "페이지 2"])

if page == "챗봇":
    chating()

st.header("API Key 를 입력하세요")
API=st.text_input("API", type="password")
st.session_state.API

def chating():
  st.header("무엇이든 물어보세요.")
  prompt = st.text_input("질문?")
  


  from openai import OpenAI
  client = OpenAI(api_key=API)
  response = client.chat.completions.create(
    model="gpt-3.5-turbo",
    messages=[
      {"role": "system", "content": "You are a helpful assistant."},
      {"role": "user", "content": prompt}
    ]
  )
  print(response.choices[0].message.content)
  with st.chat_message("AI"):
      st.write(response.choices[0].message.content)

page = st.sidebar.selectbox("페이지 선택", ["챗봇", "페이지 1", "페이지 2"])

if page == "챗봇":
    chating()