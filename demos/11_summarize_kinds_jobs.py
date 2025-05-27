import csv
from itertools import islice

from ollama import ChatResponse, GenerateResponse, chat, generate

job_kind: list[str] = []

with open("demos/data/job_postings.csv", "r") as file:
    # read csv file and get column names
    reader = csv.DictReader(file)
    if not reader.fieldnames:
        raise ValueError("The CSV file does not have any columns.")

    for row in islice(reader, 100):
        response: ChatResponse = chat(
            model="llama3.2",
            messages=[
                {
                    "role": "system",
                    "content": (
                        "You will analyze a job posting and summarize "
                        "the kind of jobs being offered as a 1-3 word phrase. "
                        "Do NOT provide any detailed analysis or descriptions "
                        "of the job posting."
                    ),
                },
                {
                    "role": "user",
                    "content": (
                        "Here is the job posting description:\n\n"
                        f"{row['description']}\n\n"
                    ),
                },
            ],
        )

        job_kind.append(str(response.message.content))

    summary_response: GenerateResponse = generate(
        model="llama3.2",
        prompt=(
            "Please group related entries together and update their "
            f"counts:\n\n{','.join(job_kind)}"
        ),
    )

    print(summary_response.response)
