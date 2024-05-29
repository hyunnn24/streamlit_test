import streamlit as st

st.header("API Key 를 입력하세요")
st.text_input("API", type="password")

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