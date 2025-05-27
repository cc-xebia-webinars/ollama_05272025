from ollama import ChatResponse, chat

messages: list = [
    {
        "role": "system",
        "content": (
            "You are a Python and computer programming expert. Also, you "
            "provide tutoring to new Python programmers. They will ask "
            "you questions, you will answer, but you will do so in a "
            "condescending and annoying way. However, do not use any bad "
            "or offensive language"
        ),
    },
]


while True:
    question = input("> ")

    messages.append(
        {
            "role": "user",
            "content": question,
        }
    )

    response: ChatResponse = chat(
        model="llama3.2",
        messages=messages,
    )

    messages.append(response["message"])

    content = response["message"]["content"]

    print(f"{content}\n\n")
