from pathlib import Path

from ollama import generate

byte_data = Path("demos/data/invoices/sample_invoice_1.png").read_bytes()

for response in generate(
    #"llama4",
    "llama3.2-vision",
    "what is the total amount of the invoice?",
    images=[byte_data],
    stream=True,
):
    print(response["response"], end="", flush=True)

print()
