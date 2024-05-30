import streamlit as st
from openai import OpenAI
import time

def run_and_wait(client, assistant, thread):
    run = client.beta.threads.runs.create(
        thread_id=thread.id,
        assistant_id=assistant.id
    )
    while True:
        run_check = client.beta.threads.runs.retrieve(
            thread_id=thread.id,
            run_id=run.id
        )
        print(run_check.status)
        if run_check.status in ['queued', 'in_progress']:
            time.sleep(2)
        else:
            break
    return run

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
        response = client.chat.completions.create(
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
    
    if 'API' in st.session_state:
        client = OpenAI(api_key=st.session_state.API)
        response = client.images.generate(model="dall-e-3", prompt=pprompt)
        image_url = response.data[0].url
        st.image(image_url)
    else:
        st.write("API Key를 먼저 입력하세요.")

def chatting():
    st.header("Chat with AI")
    user_input = st.text_input("Your message:")
    
    if user_input and 'API' in st.session_state:
        client = OpenAI(api_key=st.session_state.API)
        assistant = client.beta.assistants.create(
            name="streamlit",
            description="you are a helpful assistant",
            model="gpt-4o",
            tools=[{"type": "code_interpreter"}]
        )
        thread = client.beta.threads.create(
            messages=[
                {
                    "role": "user",
                    "content": user_input
                }
            ]
        )
        run = run_and_wait(client, assistant, thread)
        thread_messages = client.beta.threads.messages.list(thread.id)
        for msg in thread_messages.data:
            role = getattr(msg, 'role', 'unknown role')
            content = getattr(msg, 'content', 'no content')
            if isinstance(content, list):
                content = " ".join(content)
            st.write(f"{role}: {content}")

page = st.sidebar.selectbox("페이지 선택", ["API", "챗봇", "그림", "Chat"])

if page == "API":
    APIINPUT()
elif page == "챗봇":
    chating()
elif page == "그림":
    drawing()
elif page == "Chat":
    chatting()