import streamlit as st
import requests


# Function to call Ollama API
def query_ollama(prompt):
    url = "http://localhost:11434/api/generate"
    data = {"model": "llama3.2", "prompt": prompt, "stream": False}

    try:
        response = requests.post(url, json=data)
        response.raise_for_status()
        result = response.json()
        return result["response"]
    except requests.exceptions.RequestException as e:
        return f"Error: {str(e)}"


# Streamlit app
st.title("Ollama LLM Interface")
st.subheader("Interact with the Meta's Llama 3.2 3B model")

# Input prompt
user_prompt = st.text_area("Enter your prompt:", height=200)

# Button to submit
if st.button("Generate Response"):
    if user_prompt:
        with st.spinner("Generating response..."):
            response = query_ollama(user_prompt)
        st.subheader("Response:")
        st.write(response)
    else:
        st.warning("Please enter a prompt.")

# Instructions
st.sidebar.header("Instructions")
st.sidebar.write(
    """
1. Make sure Ollama is running locally with the llama3.2 model.
2. Enter your prompt in the text area.
3. Click 'Generate Response' to get the AI's response.
"""
)

# Error handling
st.sidebar.header("Troubleshooting")
st.sidebar.write(
    """
If you encounter errors:
- Ensure Ollama is running locally
- Check if the llama3.2 model is available
- Verify your network connection
"""
)
