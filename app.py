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

    from openai import OpenAI
    client = OpenAI(api_key=st.session_state.API)
    response = client.images.generate(model="dall-e-3",prompt=pprompt)
    image_url = response.data[0].url
    
    st.image(image_url)

def chatting():
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
        if run_check.status in ['queued','in_progress']:
        time.sleep(2)
        else:
        break
    return run

    client = OpenAI(api_key="sk-")

    assistant = client.beta.assistants.create(
    name="assistant",
    description="you are an helpful assistant.",
    model="gpt-4o",
    tools=[{"type": "code_interpreter"}]
    )

    thread = client.beta.threads.create(
    messages=[
        {
        "role": "user",
        "content": prompt
        
        }
    ]
    )


    run = run_and_wait(client, assistant, thread)

    for i,run_step in enumerate(run_steps.data):
    print(f"{i}: {run_step.type}: {run_step.step_details}")
    if run_step.step_details.type == 'tool_calls':
        for tool_call in run_step.step_details.tool_calls:
        print(f"- Tool Call: {tool_call.type}")
        print(f"- Input: {tool_call.code_interpreter.input}")
        print(f"- Output: {tool_call.code_interpreter.outputs}")
  


page = st.sidebar.selectbox("페이지 선택", ["API", "챗봇", "그림","Chat"])


if page == "API":
    APIINPUT()
elif page == "챗봇":
    chating()
elif page == "그림":
    drawing()
elif page == "Chat":
    chatting()