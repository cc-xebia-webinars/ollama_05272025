from ollama import ChatResponse, chat

# read first 8096 characters of demos/data/job_postings.csv
with open("demos/data/job_postings.csv", "r") as file:
    data = file.read(8096)

response: ChatResponse = chat(
    model="llama3.2",
    messages=[
        {
            "role": "system",
            "content": (
                "You will analyze some file content and describe what "
                "the file contains. Please provide a detailed description "
                "of the content."
            ),
        },
        {
            "role": "user",
            "content": (
                f"Here is the first {len(data)} characters of the "
                f"file content: {data}."
            ),
        },
        {
            "role": "user",
            "content": (
                "Summarize your analysis of the file content into "
                "2-3 sentences. Do not provide details"
            ),
        },
    ],
)

print(response.message.content)
