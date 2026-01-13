import argparse
from pathlib import Path

import pandas as pd


def make_sample_csv(path: Path, n: int = 20) -> None:
    """
    Create a tiny CSV for demo purpose.
    It intentionally includes missing values.
    """
    df = pd.DataFrame(
        {
            "id": range(1, n + 1),
            "department": [
                "ml", "ml", "data", "data", "platform",
                "ml", "data", "platform", "platform", "ml",
                "data", "ml", "platform", "data", "ml",
                "platform", "data", "ml", "platform", "data",
            ][:n],
            "salary": [
                70000, 82000, 65000, None, 90000,
                78000, 62000, 88000, None, 76000,
                64000, 83000, 91000, 61000, None,
                87000, 63000, 80000, 92000, 60000,
            ][:n],
            "years_exp": [
                1, 3, 2, 1, 4,
                2, 1, 3, 2, None,
                1, 4, 5, 1, 2,
                3, 2, 3, 5, 1,
            ][:n],
        }
    )

    path.parent.mkdir(parents=True, exist_ok=True)
    df.to_csv(path, index=False)


def main() -> int:
    parser = argparse.ArgumentParser(description="Day1 stats: read a CSV and print basic stats.")
    parser.add_argument("--csv", type=str, default="data/sample.csv", help="Path to CSV file")
    parser.add_argument("--num", type=str, default="salary", help="Numeric column for mean/min/max")
    parser.add_argument("--cat", type=str, default="department", help="Category column for groupby count")
    args = parser.parse_args()

    csv_path = Path(args.csv)

    # If CSV doesn't exist, generate a tiny one (still read-from-CSV workflow).
    if not csv_path.exists():
        make_sample_csv(csv_path, n=20)
        print(f"[info] CSV not found. Generated sample CSV at: {csv_path}")

    # Read CSV
    df = pd.read_csv(csv_path)

    # 1) Row count
    n_rows = len(df)

    # 2) Missing values count (overall + per column)
    missing_total = int(df.isna().sum().sum())
    missing_by_col = df.isna().sum()

    # 3) Numeric stats (mean/min/max) for a chosen column (if exists and numeric)
    num_col = args.num
    if num_col in df.columns:
        num_series = pd.to_numeric(df[num_col], errors="coerce")
        num_mean = float(num_series.mean())
        num_min = float(num_series.min())
        num_max = float(num_series.max())
    else:
        num_mean = num_min = num_max = float("nan")

    # 4) Groupby count for a category column
    cat_col = args.cat
    if cat_col in df.columns:
        group_counts = df.groupby(cat_col).size().sort_values(ascending=False)
    else:
        group_counts = pd.Series(dtype=int)

    # Print results
    print("=== Day1 Stats ===")
    print(f"CSV: {csv_path}")
    print(f"Rows: {n_rows}")
    print(f"Missing values (total): {missing_total}")
    print("Missing values (by column):")
    print(missing_by_col.to_string())

    if num_col in df.columns:
        print(f"{num_col} stats: mean={num_mean:.2f}, min={num_min:.2f}, max={num_max:.2f}")
    else:
        print(f"[warn] numeric column '{num_col}' not found, skipped mean/min/max")

    if cat_col in df.columns:
        print(f"Groupby counts by '{cat_col}':")
        print(group_counts.to_string())
    else:
        print(f"[warn] category column '{cat_col}' not found, skipped groupby")

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
