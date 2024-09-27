# Ollama-Streamlit-LangChain-Chat-App
# Streamlit app for chatting with Meta Llama 3.2 using Ollama and LangChain
# Author: Gary A. Stafford
# Date: 2024-09-26
# References:
# https://python.langchain.com/v0.2/docs/integrations/memory/streamlit_chat_message_history/
# https://python.langchain.com/docs/integrations/callbacks/streamlit/

import streamlit as st
from langchain_community.chat_message_histories import StreamlitChatMessageHistory
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_core.runnables.history import RunnableWithMessageHistory
from langchain_ollama import ChatOllama

# Set page configuration
st.set_page_config(page_title="Llama 3.2 Chat", page_icon="🦙", layout="wide")

# Main chat interface
st.title("Chat with Llama 3.2 🦙")

with st.sidebar:
    st.header("Inference Settings")

    model = st.selectbox("Model", ["llama3.2:1b", "llama3.2:latest"], index=1)

    seed = st.slider("Seed", min_value=1, max_value=9007199254740991, value=1, step=1)
    temperature = st.slider(
        "Temperature", min_value=0.0, max_value=1.0, value=0.5, step=0.05
    )
    max_tokens = st.slider(
        "Max Tokens", min_value=100, max_value=128000, value=5000, step=100
    )

    st.session_state.model = model
    st.session_state.seed = seed
    st.session_state.temperature = temperature
    st.session_state.max_tokens = max_tokens

chat = ChatOllama(
    model=st.session_state.model,
    seed=st.session_state.seed,
    temperature=st.session_state.temperature,
    max_tokens=st.session_state.max_tokens,
)

msgs = StreamlitChatMessageHistory(key="special_app_key")

if len(msgs.messages) == 0:
    msgs.add_ai_message("How can I help you?")

prompt = ChatPromptTemplate.from_messages(
    [
        ("system", "You are an AI chatbot having a conversation with a human."),
        MessagesPlaceholder(variable_name="chat_history"),
        ("human", "{input}"),
    ]
)

chain = prompt | chat

chain_with_history = RunnableWithMessageHistory(
    chain,
    lambda session_id: msgs,  # Always return the instance created earlier
    input_messages_key="input",
    history_messages_key="chat_history",
)

for msg in msgs.messages:
    st.chat_message(msg.type).write(msg.content)

if prompt := st.chat_input("Type your message here..."):
    st.chat_message("human").write(prompt)

    with st.spinner("Thinking..."):
        # As usual, new messages are added to StreamlitChatMessageHistory when the Chain is called.
        config = {"configurable": {"session_id": "any"}}
        response = chain_with_history.invoke({"input": prompt}, config)
        st.chat_message("ai").write(response.content)

# Add a button to clear chat history
if st.button("Clear Chat History"):
    msgs.clear()
    st.rerun()
