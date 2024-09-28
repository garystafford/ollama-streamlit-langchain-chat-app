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
import logging

logger = logging.getLogger(__name__)
logging.basicConfig(
    level=logging.INFO, format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)

# Set page configuration
st.set_page_config(page_title="Llama 3.2 Chat", page_icon="🦙", layout="wide")

# Main chat interface
st.title("Chat with Llama 3.2 🦙")

if "model" not in st.session_state:
    st.session_state["model"] = "llama3.2:latest"

if "input_tokens" not in st.session_state:
    st.session_state["input_tokens"] = 0

if "output_tokens" not in st.session_state:
    st.session_state["output_tokens"] = 0

if "total_tokens" not in st.session_state:
    st.session_state["total_tokens"] = 0

if "total_duration" not in st.session_state:
    st.session_state["total_duration"] = 0

if "num_predict" not in st.session_state:
    st.session_state["num_predict"] = 512

if "seed" not in st.session_state:
    st.session_state["seed"] = 1

if "temperature" not in st.session_state:
    st.session_state["temperature"] = 0.5

if "top_p" not in st.session_state:
    st.session_state["top_p"] = 0.9

with st.sidebar:
    st.header("Inference Settings")

    model = st.selectbox("Model", ["llama3.2:1b", "llama3.2:latest"], index=1)
    seed = st.slider("Seed", min_value=1, max_value=9007199254740991, value=1, step=1)
    temperature = st.slider(
        "Temperature", min_value=0.0, max_value=1.0, value=0.5, step=0.01
    )
    top_p = st.slider("Top P", min_value=0.0, max_value=1.0, value=0.90, step=0.01)
    num_predict = st.slider(
        "Response Tokens", min_value=0, max_value=8192, value=512, step=8
    )

    st.session_state.model = model
    st.session_state.seed = seed
    st.session_state.temperature = temperature
    st.session_state.top_p = top_p
    st.session_state.num_predict = num_predict

    st.markdown("---")
    st.text(
        f"""
• model: {st.session_state.model}
• seed: {st.session_state.seed}
• temperature: {st.session_state.temperature}
• top_p: {st.session_state.top_p}
• num_predict: {st.session_state.num_predict}
        """
    )

chat = ChatOllama(
    model=st.session_state.model,
    seed=st.session_state.seed,
    temperature=st.session_state.temperature,
    top_p=st.session_state.top_p,
    num_predict=st.session_state.num_predict,
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

        # https://github.com/ollama/ollama/blob/main/docs/api.md
        logger.info(response)
        total_duration = response.response_metadata["total_duration"] / 1000000000
        st.session_state.total_duration = f"{total_duration:.2f} s"

        st.session_state.input_tokens = response.usage_metadata["input_tokens"]
        st.session_state.output_tokens = response.usage_metadata["output_tokens"]
        st.session_state.total_tokens = response.usage_metadata["total_tokens"]

        token_per_second = (
            response.response_metadata["eval_count"]
            / response.response_metadata["eval_duration"]
            * 1000000000
        )
        st.session_state.token_per_second = f"{token_per_second:.2f} tokens/s"

        with st.sidebar:
            st.text(
                f"""
• input_tokens: {st.session_state.input_tokens}
• output_tokens: {st.session_state.output_tokens}
• total_tokens: {st.session_state.total_tokens}
• total_duration: {st.session_state.total_duration}
• token_per_second: {st.session_state.token_per_second}
                """
            )

# Add a button to clear chat history
if st.button("Clear Chat History"):
    msgs.clear()
    st.rerun()
