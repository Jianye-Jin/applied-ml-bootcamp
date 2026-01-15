import pandas as pd

from cleaning import fill_missing, remove_duplicates


def make_dirty_data() -> pd.DataFrame:
    # Toy dataset with missing values + duplicates
    return pd.DataFrame(
        {
            "user_id": [1, 2, 2, 3, 4, 4, 4],
            "country": ["UK", "UK", "UK", None, "DE", "DE", "DE"],
            "age": [23, None, None, 31, 28, 28, 28],
            "salary": [70000, 82000, 82000, None, 60000, 60000, 60000],
        }
    )


def main() -> None:
    df = make_dirty_data()

    rows_before = len(df)
    missing_before = int(df.isna().sum().sum())

    print("=== Before cleaning ===")
    print(df)
    print(f"Rows: {rows_before}")
    print(f"Missing values (total): {missing_before}")
    print()

    # 1) Fill missing values
    df_filled = fill_missing(df, numeric_strategy="median", categorical_strategy="mode")

    # 2) Remove duplicates (here we define duplicates by user_id+country+age+salary)
    df_clean = remove_duplicates(df_filled, subset=["user_id", "country", "age", "salary"], keep="first")

    rows_after = len(df_clean)
    missing_after = int(df_clean.isna().sum().sum())

    print("=== After cleaning ===")
    print(df_clean)
    print(f"Rows: {rows_after} (delta {rows_after - rows_before})")
    print(f"Missing values (total): {missing_after} (delta {missing_after - missing_before})")


if __name__ == "__main__":
    main()
