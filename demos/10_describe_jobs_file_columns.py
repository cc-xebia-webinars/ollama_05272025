import csv
import textwrap
from itertools import islice

from ollama import ChatResponse, chat
from prettytable import PrettyTable

job_postings_file_description = """
The file appears to be a job posting database containing various job
listings across different industries, including insurance, marketing,
finance, and non-profit sectors. The postings include detailed job
descriptions, salary ranges, benefits, and requirements for each position.
The data is structured in a tabular format with specific columns and rows
detailing each job listing.
"""

column_names_examples: dict[str, list[str]] = {}
column_descriptions: list[list[str]] = []


def wrap_text(text: str, width: int) -> str:
    return "\n".join(textwrap.wrap(str(text), width=width))


with open("demos/data/job_postings.csv", "r") as file:
    # read csv file and get column names
    reader = csv.DictReader(file)
    if not reader.fieldnames:
        raise ValueError("The CSV file does not have any columns.")
    for row in islice(reader, 10):
        for column_name in reader.fieldnames:
            column_name_examples = column_names_examples.get(column_name, [])
            column_name_examples.append(row[column_name])
            column_names_examples[column_name] = column_name_examples

    for column_name, column_values in column_names_examples.items():
        response: ChatResponse = chat(
            model="llama3.2",
            messages=[
                {
                    "role": "system",
                    "content": (
                        "You will analyze a column name and its associated "
                        "data to write a description for the column. The "
                        "columns and data come from a file described below:"
                        f"\n\n{job_postings_file_description}"
                    ),
                },
                {
                    "role": "user",
                    "content": (
                        f"Here is the comma separated list of example values "
                        f"for the column named {column_name}:\n\n"
                        f"{','.join(column_values)}"
                    ),
                },
                {
                    "role": "user",
                    "content": (
                        "Summarize your description of the column in one "
                        "sentence. Do not repeat the name of the column "
                        "in the description. Do not start the description "
                        "with phrase such as 'This column', just describe "
                        "the column without referring to in the subject "
                        "of the description."
                    ),
                },
            ],
        )

        column_descriptions.append(
            [column_name, wrap_text(str(response.message.content), 50)]
        )


table = PrettyTable()
table.field_names = ["Column Name", "Description"]
table.align = "l"
table.add_rows(column_descriptions)
print(table)
