import streamlit as st
import streamlit.components.v1 as components
from openai import OpenAI

st.set_page_config(layout="wide")

col1, col2, col3 = st.columns([10.9, 0.2, 10.9])


with col1:
    HtmlFile = open("wheel_approach2.html", 'r', encoding='utf-8')
    source_code = HtmlFile.read() 
    components.html(source_code, height=800)
    
with col2:

    st.html(
            '''
                <div class="divider-vertical-line"></div>
                <style>
                    .divider-vertical-line {
                        border-left: 2px solid rgba(49, 51, 63, 0.2);
                        height: 100%;
                        margin: auto;
                    }
                </style>
            '''
        )
    
with col3:

    col3.title("💬 Car Designer")

    openai_api_key = st.text_input("OpenAI API Key", key="chatbot_api_key", type="password")
    option=col3.selectbox('Select Model', ('gpt-4o-mini','gpt-4o', 'gpt-4-turbo'))

    if "messages" not in st.session_state:
        st.session_state["messages"] = [{"role": "assistant", "content": "How can I help you?"}]

    for msg in st.session_state.messages:
        col3.chat_message(msg["role"]).write(msg["content"])

    if prompt := col3.chat_input():
        if not openai_api_key:
            st.info("Please add your OpenAI API key to continue.")
            st.stop()
        
        client = OpenAI(api_key=openai_api_key)
        st.session_state.messages.append({"role": "user", "content": prompt})
        st.chat_message("user").write(prompt)
        response = client.chat.completions.create(model=option, messages=st.session_state.messages)
        msg = response.choices[0].message.content
        st.session_state.messages.append({"role": "assistant", "content": msg})
        col3.chat_message("assistant").write(msg)