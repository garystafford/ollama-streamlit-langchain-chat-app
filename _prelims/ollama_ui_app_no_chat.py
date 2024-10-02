import streamlit as st
import ollama


def generate_response(prompt):
    try:
        # Call the Ollama API
        response = ollama.chat(
            model="llama3.2",
            messages=[
                {
                    "role": "user",
                    "content": prompt,
                },
            ],
        )

        # Extract the response content
        return response["message"]["content"]
    except Exception as e:
        return f"An error occurred: {str(e)}"


# Set up the Streamlit app
st.title("Ollama Chat with llama3.2")
st.subheader("Interact with the Meta's Llama 3.2 3B model")

# Create a text input for the user's prompt
with st.form(key="prompt_form"):
    user_prompt = st.text_area("Enter your prompt:", height=200)
    submit_button = st.form_submit_button(label="Generate Response")

# Create a button to generate the response
if submit_button:
    if user_prompt:
        # Display a spinner while generating the response
        with st.spinner("Generating response..."):
            response = generate_response(user_prompt)

        # Display the response
        st.markdown("#### Response:")
        st.write(response)
    else:
        st.warning("Please enter a prompt.")

# Add some information about the app
st.sidebar.header("About")
st.sidebar.info(
    "This app uses Ollama to generate responses using the llama3.2 model. "
    "Make sure you have Ollama installed and running locally with the llama3.2 model."
)
