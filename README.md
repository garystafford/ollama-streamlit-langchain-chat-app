# Ollama Streamlit LangChain Chat App Demo

## Commands

```sh
python3 -m venv ollama_ui
source ollama_ui/bin/activate

python3 -m pip install --upgrade pip

python3 -m pip install -r requirements.txt --upgrade

# monitor gpu performance
python3 -m pip install asitop

python3 --version # Python 3.12.2
```

```sh
xcode-select --install
```

```sh
streamlit run app.py
```

```sh
streamlit run app.py \
    --server.runOnSave true \
    --theme.base "light" \
    --theme.primaryColor "#0081FB" \
    --ui.hideTopBar "true" \
    --client.toolbarMode "minimal"
```

```sh
deactivate
```

```text
Improve the grammar of following statement. Explain what was changed and why. If no changes are necessary, then say so:

There’s not a liberal America and a conservative America; there’s the United States of America. There’s not a Black America and white America and Latino America and Asian America; there’s the United States of America. We are one people, all of us pledging allegiance to the stars and stripes, all of us defending the United States of America. In the end, that’s what this election is about. Do we participate in a politics of cynicism, or do we participate in a politics of hope?
```

```text
I have written a blog post entitled, "Interacting with Meta's Latest Llama 3.2 LLMs Locally Using Ollama, LangChain, and Streamlit: Meta's latest Llama 3.2 1B and 3B models are available from Ollama. Learn how to install and interact with these models locally using Streamlit and LangChain." I want to write a LinkedIn post to promote the blog post. Write a succinct yet impactful post. Don't forget the hashtags and emojis!
```
