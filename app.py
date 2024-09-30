# Ollama-Streamlit-LangChain-Chat-App
# Streamlit app for chatting with Meta Llama 3.2 using Ollama and LangChain
# Author: Gary A. Stafford
# Date: 2024-09-26
# References:
# https://python.langchain.com/v0.2/docs/integrations/memory/streamlit_chat_message_history/
# https://python.langchain.com/docs/integrations/callbacks/streamlit/

import logging
from typing import Dict, Any

import streamlit as st
from langchain_community.chat_message_histories import StreamlitChatMessageHistory
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_core.runnables.history import RunnableWithMessageHistory
from langchain_ollama import ChatOllama

# Constants
PAGE_TITLE = "Llama 3.2 Chat"
PAGE_ICON = "🦙"
SYSTEM_PROMPT = "You are a friendly AI chatbot having a conversation with a human."
DEFAULT_MODEL = "llama3.2:latest"

# Configure logging
logging.basicConfig(
    level=logging.INFO, format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger(__name__)


def initialize_session_state() -> None:
    defaults: Dict[str, Any] = {
        "model": DEFAULT_MODEL,
        "input_tokens": 0,
        "output_tokens": 0,
        "total_tokens": 0,
        "total_duration": 0,
        "num_predict": 2048,
        "seed": 1,
        "temperature": 0.5,
        "top_p": 0.9,
    }
    for key, value in defaults.items():
        if key not in st.session_state:
            st.session_state[key] = value


def create_sidebar() -> None:
    with st.sidebar:
        st.header("Inference Settings")
        st.session_state.system_prompt = st.text_area(
            label="System",
            value=SYSTEM_PROMPT,
            help="Sets the context in which to interact with the AI model. It typically includes rules, guidelines, or necessary information that help the model respond effectively.",
        )

        st.session_state.model = st.selectbox(
            "Model",
            ["llama3.2:1b", "llama3.2:latest"],
            index=1,
            help="Select the model to use.",
        )
        st.session_state.seed = st.slider(
            "Seed",
            min_value=1,
            max_value=9007199254740991,
            value=round(9007199254740991 / 2),
            step=1,
            help="Controls the randomness of how the model selects the next tokens during text generation.",
        )
        st.session_state.temperature = st.slider(
            "Temperature",
            min_value=0.0,
            max_value=1.0,
            value=0.5,
            step=0.01,
            help="Sets an LLM's entropy. Low temperatures render outputs that are predictable and repetitive. Conversely, high temperatures encourage LLMs to produce more random, creative responses.",
        )
        st.session_state.top_p = st.slider(
            "Top P",
            min_value=0.0,
            max_value=1.0,
            value=0.90,
            step=0.01,
            help="Sets the probability threshold for the nucleus sampling algorithm. It controls the diversity of the model's responses.",
        )
        st.session_state.num_predict = st.slider(
            "Response Tokens",
            min_value=0,
            max_value=8192,
            value=2048,
            step=16,
            help="Sets the maximum number of tokens the model can generate in response to a prompt.",
        )

        st.markdown("---")
        st.text(
            f"""Stats:
- model: {st.session_state.model}
- seed: {st.session_state.seed}
- temperature: {st.session_state.temperature}
- top_p: {st.session_state.top_p}
- num_predict: {st.session_state.num_predict}
        """
        )


def create_chat_model() -> ChatOllama:
    return ChatOllama(
        model=st.session_state.model,
        seed=st.session_state.seed,
        temperature=st.session_state.temperature,
        top_p=st.session_state.top_p,
        num_predict=st.session_state.num_predict,
    )


def create_chat_chain(chat_model: ChatOllama):
    prompt = ChatPromptTemplate.from_messages(
        [
            ("system", st.session_state.system_prompt),
            MessagesPlaceholder(variable_name="chat_history"),
            ("human", "{input}"),
        ]
    )
    return prompt | chat_model


def update_sidebar_stats(response: Any) -> None:
    total_duration = response.response_metadata["total_duration"] / 1e9
    st.session_state.total_duration = f"{total_duration:.2f} s"
    st.session_state.input_tokens = response.usage_metadata["input_tokens"]
    st.session_state.output_tokens = response.usage_metadata["output_tokens"]
    st.session_state.total_tokens = response.usage_metadata["total_tokens"]
    token_per_second = (
        response.response_metadata["eval_count"]
        / response.response_metadata["eval_duration"]
    ) * 1e9
    st.session_state.token_per_second = f"{token_per_second:.2f} tokens/s"

    with st.sidebar:
        st.text(
            f"""
- input_tokens: {st.session_state.input_tokens}
- output_tokens: {st.session_state.output_tokens}
- total_tokens: {st.session_state.total_tokens}
- total_duration: {st.session_state.total_duration}
- token_per_second: {st.session_state.token_per_second}
        """
        )


def main() -> None:
    st.set_page_config(page_title=PAGE_TITLE, page_icon=PAGE_ICON, layout="wide")
    st.markdown(
        """
        <style>
            MainMenu {visibility: hidden;}
            footer {visibility: hidden;}
            header {visibility: hidden;}
        </style>
        """,
        unsafe_allow_html=True,
    )

    st.title(f"{PAGE_TITLE} {PAGE_ICON}")

    st.markdown("##### Chat")

    initialize_session_state()
    create_sidebar()

    chat_model = create_chat_model()
    chain = create_chat_chain(chat_model)

    msgs = StreamlitChatMessageHistory(key="special_app_key")
    if not msgs.messages:
        msgs.add_ai_message("How can I help you?")

    chain_with_history = RunnableWithMessageHistory(
        chain,
        lambda session_id: msgs,
        input_messages_key="input",
        history_messages_key="chat_history",
    )

    for msg in msgs.messages:
        st.chat_message(msg.type).write(msg.content)

    if prompt := st.chat_input("Type your message here..."):
        st.chat_message("human").write(prompt)

        with st.spinner("Thinking..."):
            config = {"configurable": {"session_id": "any"}}
            response = chain_with_history.invoke({"input": prompt}, config)
            logger.info({"input": prompt}, config)
            st.chat_message("ai").write(response.content)
            logger.info(response)
            update_sidebar_stats(response)

    if st.button("Clear Chat History"):
        msgs.clear()
        st.rerun()


if __name__ == "__main__":
    main()
