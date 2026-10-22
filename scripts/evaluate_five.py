import csv
import re
import tempfile
from pathlib import Path

import nbformat
from nbclient import NotebookClient

NOTEBOOK = Path("experiments/RDHEMI_multi_image_eval.ipynb")
OUTPUT = Path("results/multi_image_eval.csv")
SAMPLE_COUNT = 5


def output_text(notebook):
    parts = []
    for cell in notebook.cells:
        for output in cell.get("outputs", []):
            if output.get("text"):
                parts.append(output["text"])
            data = output.get("data", {})
            if "text/plain" in data:
                parts.append(data["text/plain"])
    return "\n".join(parts)


def extract(pattern, text, cast=str):
    match = re.search(pattern, text, re.IGNORECASE)
    return cast(match.group(1)) if match else None


def main():
    if not NOTEBOOK.exists():
        raise FileNotFoundError(
            f"Notebook not found: {NOTEBOOK}\n"
            "Run this script from your project root."
        )

    original = nbformat.read(NOTEBOOK, as_version=4)

    # Find the image-loading cell.
    image_cells = [
        cell for cell in original.cells
        if cell.cell_type == "code"
        and "PneumoniaMNIST" in cell.source
        and "sample_index" in cell.source
    ]

    if len(image_cells) != 1:
        raise RuntimeError(
            "Expected exactly one image-loading cell containing "
            "'PneumoniaMNIST' and 'sample_index'."
        )

    kernel_name = original.metadata.get(
        "kernelspec", {}
    ).get("name", "python3")

    OUTPUT.parent.mkdir(parents=True, exist_ok=True)
    rows = []

    for index in range(SAMPLE_COUNT):
        print(f"\nRunning image {index + 1}/{SAMPLE_COUNT}...")

        notebook = nbformat.from_dict(original)
        target = next(
            cell for cell in notebook.cells
            if cell.cell_type == "code"
            and "PneumoniaMNIST" in cell.source
            and "sample_index" in cell.source
        )

        target.source = re.sub(
            r"(?m)^(\s*sample_index\s*=\s*)\d+.*$",
            rf"\g<1>{index}",
            target.source,
            count=1,
        )

        try:
            with tempfile.TemporaryDirectory() as temp_dir:
                client = NotebookClient(
                    notebook,
                    timeout=1200,
                    kernel_name=kernel_name,
                    resources={"metadata": {"path": str(Path.cwd())}},
                )
                client.execute()

            text = output_text(notebook)

            row = {
                "image_index": index,
                "capacity_bits": extract(
                    r"Reserved Room Length\s*\(l_tau\)\s*:\s*(\d+)",
                    text, int,
                ),
                "payload_bits": extract(
                    r"Payload length:\s*(\d+)\s*bits",
                    text, int,
                ),
                "embedding_rate_bpp": extract(
                    r"Embedding rate:\s*([0-9.eE+-]+)",
                    text, float,
                ),
                "metadata_recovered": extract(
                    r"Metadata recovered exactly:\s*(True|False)",
                    text,
                ),
                "pixel_perfect": extract(
                    r"Pixel-perfect recovery:\s*(True|False)",
                    text,
                ),
                "restoration_mse": extract(
                    r"Restoration MSE:\s*([0-9.eE+-]+)",
                    text, float,
                ),
                "status": "completed",
            }

            # Detect an experiment that ran but did not print expected results.
            required = [
                "capacity_bits", "payload_bits",
                "metadata_recovered", "pixel_perfect",
                "restoration_mse",
            ]
            missing = [key for key in required if row[key] is None]
            if missing:
                row["status"] = "missing outputs: " + ", ".join(missing)

            print(row)
            rows.append(row)

        except Exception as error:
            print(f"FAILED for image {index}: {error}")
            rows.append({
                "image_index": index,
                "capacity_bits": None,
                "payload_bits": None,
                "embedding_rate_bpp": None,
                "metadata_recovered": None,
                "pixel_perfect": None,
                "restoration_mse": None,
                "status": f"failed: {type(error).__name__}: {error}",
            })

    with OUTPUT.open("w", newline="", encoding="utf-8") as file:
        writer = csv.DictWriter(file, fieldnames=rows[0].keys())
        writer.writeheader()
        writer.writerows(rows)

    print(f"\nResults saved to: {OUTPUT}")
    print("Check the status column and confirm all expected values were captured.")


if __name__ == "__main__":
    main()
