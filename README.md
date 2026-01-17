# applied-ml-bootcamp

A production-minded, minimal applied-ML scaffold used for daily ML engineering drills (data IO, cleaning, SQL, and small reproducible scripts).

## What’s inside
- `src/` — small runnable scripts and utilities
- `notes/` — markdown notes with query definitions and outputs
- `sql/` — toy schema and seed SQL (SQLite)
- `data/` — local data/db files (ignored by git)

## Prerequisites
- macOS / Linux
- Git + GitHub CLI (`gh`)
- SQLite (`sqlite3`)
- Conda (recommended: Miniforge/Miniconda)

## Clone repo
```bash
git clone https://github.com/Jianye-Jin/applied-ml-bootcamp.git
cd applied-ml-bootcamp
```

## Setup (Conda)
>First time only: create the env. Later: just activate it.

```bash
# 1) Create and activate an environment (skip if already exists)
conda create -n dsml -y python=3.11
conda activate dsml

# 2) Install dependencies
python -m pip install -r requirements.txt
> If you already have an env, just `conda activate dsml` and install requirements.
```

## Quickstart (Run)

### Day 1 — scaffold sanity check
```bash
python -m src.train
```

Expected output:
```text
applied-ml-bootcamp: scaffold is running
```

### Day 2 — CSV stats (toy dataset)
```bash
python src/day1_stats.py
```

Expected output (example):
```text
=== Day1 Stats ===
CSV: data/sample.csv
Rows: 20
Missing values (total): 4
Missing values (by column):
id           0
department   0
salary       3
years_exp    1
salary stats: mean=76000.00, min=60000.00, max=92000.00
Groupby counts by 'department':
data      7
ml        7
platform  6
```

### Day 3 — data cleaning demo
```bash
python src/day3_run.py
```

Expected output (example):
```text
=== Before cleaning ===
Rows: 7
Missing values (total): 4

=== After cleaning ===
Rows: 4 (delta -3)
Missing values (total): 0 (delta -4)
```

### Day 4 — SQL drills (SQLite)
This repo uses a toy SQLite database at `data/day2.db`.

Rebuild the toy DB (safe to re-run):
```bash
sqlite3 data/day2.db < sql/day2_setup.sql
```

Generate the Day 4 note with queries + outputs:
```bash
sed -n '1,220p' notes/day4_sql.md
```

## Notes
* Local datasets and databases live under `data/` and are ignored by git by design.
* For SQL, query definitions and results are stored in `notes/`.
