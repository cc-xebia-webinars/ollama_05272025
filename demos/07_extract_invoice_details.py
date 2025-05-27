import re
import shutil
from os import PathLike
from pathlib import Path

from ollama import chat

accounting_form_bytes = Path(
    "demos/data/assets/accounting-form.png"
).read_bytes()


def extract_invoice_details_to_text(invoice_file_path: PathLike) -> str:
    invoice_bytes = Path(invoice_file_path).read_bytes()

    response = chat(
        model="llama4",
        # model="llama3.2-vision",
        messages=[
            {
                "role": "system",
                "content": (
                    "You are a bookkeeper helping to post invoices "
                    "to an online accounting system. Here is the accounting "
                    "form to be filled out with information from the invoice."
                ),
                "images": [accounting_form_bytes],
            },
            {
                "role": "user",
                "content": (
                    "Please fill out the accounting form with the "
                    "data from the following file."
                ),
                "images": [invoice_bytes],
            },
            {
                "role": "user",
                "content": (
                    "The output format is JSON. Do not output any content "
                    "other than JSON. The JSON structure should match the "
                    "structure of the accounting form. The JSON structure "
                    "will be populated with details from the invoice."
                ),
            },
        ],
    )

    if not response.message.content:
        return ""

    return response.message.content


def process_invoice_details_text(invoice_details_text: str) -> str:
    json_content_re = re.compile(r"```json(.*?)```", re.DOTALL)

    json_content_match = json_content_re.search(invoice_details_text)
    if not json_content_match:
        return r'{"message": "Failed to generate JSON document of invoice"}'

    json_content_groups = json_content_match.groups()

    if len(json_content_groups) == 1:
        return str(json_content_groups[0]).strip()
    else:
        return r'{"message": "Failed to generate JSON document of invoice"}'


def main() -> None:
    shutil.rmtree("output", ignore_errors=True)
    output_path = Path("output")
    output_path.mkdir(exist_ok=True)
    invoices_path = Path("demos") / "data" / "invoices"

    for invoice_image_file in sorted(
        invoices_path.glob("sample_invoice_*.png")
    ):
        print(f"Processing {invoice_image_file}...")

        invoice_details_text = extract_invoice_details_to_text(
            invoice_image_file
        )
        print(f"Response from Ollama: {invoice_details_text}")

        invoice_json_file = output_path / (
            invoice_image_file.name.split(".")[0] + ".json"
        )
        invoice_json_file.write_text(
            process_invoice_details_text(invoice_details_text),
            encoding="UTF-8",
        )


if __name__ == "__main__":
    main()
