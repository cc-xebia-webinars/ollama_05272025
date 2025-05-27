# Setup Guide

The setup guide provides detailed instructions on how to install and configure various tools and services required for using Ollama effectively.

## Use Ollama like a Chatbot

1. Install [Ollama](https://ollama.com/download).

1. Explore the available models:
   ```bash
   ollama list
   ```

1. Install Llama 3.2
   ```bash
   ollama pull llama3:3.2
   ```

1. Run the Llama 3.2 model:
   ```bash
   ollama run llama3:3.2
   ```

1. Interact with the model like you would with a chatbot.

## Use Ollama as an Alternative to GitHub Copilot

1. Install [VS Code](https://code.visualstudio.com/).

1. Open VS Code and go to the Extensions view (Ctrl+Shift+X).

1. Install [Continue (id: Continue.continue)](https://marketplace.visualstudio.com/items?itemName=Continue.continue) extension for VS Code.

1. From the Continue extension chat interface, configure the model `Provider` to use `Ollama`. Click the `Connect` button.

1. A `config.yaml` file will be displayed. Ensure you have the necessary models installed.

1. Try using the chat and inline code suggestions powered by Continue and Ollama.


## Python-Ollama Development Environment

1. Install [Python](https://www.python.org/downloads/).

1. Install the [Python extension for VS Code](https://marketplace.visualstudio.com/items?itemName=ms-python.python).

1. Create a new Python virtual environment:
   ```bash
   python -m venv venv
   ```

1. Activate the virtual environment:
    - On Windows:
      ```bash
      venv\Scripts\activate
      ```
    - On macOS/Linux:
      ```bash
      source venv/bin/activate
      ```

1. Update Pip:
   ```bash
   python -m pip install --upgrade pip
   ```

1. Install the required Python packages:
    ```bash
    python -m pip install -r ./requirements.txt
    ```

1. Create a new file named `app.py`. Add the following code to it:
    ```python
    from ollama import chat
    from ollama import ChatResponse

    response: ChatResponse = chat(model='llama3.2', messages=[
    {
        'role': 'user',
        'content': 'Why is the sky blue?',
    },
    ])
    print(response['message']['content'])
    # or access fields directly from the response object
    print(response.message.content)
    ```
