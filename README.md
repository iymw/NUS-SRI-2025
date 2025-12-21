# NUS-SRI Synthetic Instruction Dataset Toolkit

A small Python utility to generate synthetic instruction datasets (read / update / delete) for student records (NISN), inject realistic typos, and produce corresponding input and result CSVs for model evaluation.

---

## Why this project is useful

- Quickly create reproducible synthetic datasets of student records and instruction sequences to evaluate parsing and data-manipulation performance of models and parsers.
- Generate both clean and typo-containing instruction files to test robustness against misspellings and variations.
- Includes sample model outputs (GPT-4.1, Gemini) and an `Accuracy.ipynb` notebook for basic evaluation/analysis.

---

## Features

- Generates `raw` CSV with randomized NISN student identifiers and empty subject columns
- Generates instruction text files (`ins_{rows}.txt`) containing `Read`, `Update`, and `Delete` commands
- Applies common typos and variants to create `*_with_typos` files to stress-test systems
- Executes instructions and writes resulting CSV (`res_{rows}_with_typos.csv`) showing final state

---

## Quickstart

Requirements:

- Python 3.10+ (the script uses `match` / structural pattern matching)
- Install dependencies:

```bash
pip install -r requirements.txt
```

Run the generator and processor:

```bash
python True.py
```

This will write files to `Data/Test/` such as:

- `raw_{rows}_with_typos.csv` — initial raw student records (renamed after run)
- `ins_{rows}_with_typos.txt` — generated instruction sequence with typos
- `res_{rows}_with_typos.csv` — final dataset after executing instructions

Note: By default the script sets `rows = 250` at the top of `True.py`; change that number to generate different sizes (10, 50, 100, 150, 200, 250 are provided in `Data/Test/`).

---

## Usage examples & developer notes

- To create smaller or larger datasets, edit the `rows` variable in `True.py` or fork and adapt the script to accept a CLI argument.
- The script writes two instruction files (`ins_*.txt` and `ins_*_with_typos.txt`) — the `_with_typos` version is useful for evaluating model resilience.
- `Data/` already contains outputs from model runs (e.g., `GPT-4.1 2025-04-14/` and `Gemini 2.5 Flash/`) and `Accuracy.ipynb` to compare results.

---

## Project structure

- `True.py` — main generator and executor script
- `requirements.txt` — Python dependencies (pandas)
- `Data/` — test datasets, model outputs, and `Accuracy.ipynb`

---

## Acknowledgements & context

This repository is tailored for evaluating model parsing and data update robustness using synthetic student record instructions and for facilitating quick experimentation with different model outputs and evaluation scripts.

> Tip: Inspect `Data/Accuracy.ipynb` to see example evaluation steps and reproduce accuracy tables from model outputs.

---