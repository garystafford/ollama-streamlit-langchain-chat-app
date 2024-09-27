# Ollama Streamlit LangChain Chat App Demo

## Commands

```sh
python3 -m venv ollama_ui
source ollama_ui/bin/activate

python3 -m pip install --upgrade pip

python3 -m pip install -r requirements.txt --upgrade

# optional to monitor gpu performance
python3 -m pip install asitop

python3 --version # Python 3.12.2
```

```sh
# optional on Mac with watchdog
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
Improve the grammar of the following statement. Explain what was changed and why. If no changes are necessary, state, "No changes are necessary.":

There’s not a liberal America and a conservative America; there’s the United States of America. There’s not a Black America and white America and Latino America and Asian America; there’s the United States of America. We are one people, all of us pledging allegiance to the stars and stripes, all of us defending the United States of America. In the end, that’s what this election is about. Do we participate in a politics of cynicism, or do we participate in a politics of hope?
```
