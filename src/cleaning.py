from __future__ import annotations

from typing import Iterable, Optional

import numpy as np
import pandas as pd


def fill_missing(
    df: pd.DataFrame,
    numeric_cols: Optional[Iterable[str]] = None,
    categorical_cols: Optional[Iterable[str]] = None,
    numeric_strategy: str = "median",
    categorical_strategy: str = "mode",
) -> pd.DataFrame:
    """
    Fill missing values in a DataFrame.

    Parameters
    ----------
    df : pd.DataFrame
        Input data.
    numeric_cols : optional iterable of str
        Numeric columns to fill. If None, infer numeric columns.
    categorical_cols : optional iterable of str
        Categorical columns to fill. If None, infer object/category columns.
    numeric_strategy : {"median", "mean", "zero"}
        Strategy for numeric columns.
    categorical_strategy : {"mode", "empty"}
        Strategy for categorical columns.

    Returns
    -------
    pd.DataFrame
        A new DataFrame with missing values filled.
    """
    out = df.copy()

    if numeric_cols is None:
        numeric_cols = out.select_dtypes(include=[np.number]).columns.tolist()
    if categorical_cols is None:
        categorical_cols = out.select_dtypes(include=["object", "category"]).columns.tolist()

    # Fill numeric columns
    for col in numeric_cols:
        if col not in out.columns:
            continue
        s = pd.to_numeric(out[col], errors="coerce")
        if numeric_strategy == "median":
            fill_value = s.median()
        elif numeric_strategy == "mean":
            fill_value = s.mean()
        elif numeric_strategy == "zero":
            fill_value = 0
        else:
            raise ValueError(f"Unsupported numeric_strategy: {numeric_strategy}")
        out[col] = s.fillna(fill_value)

    # Fill categorical columns
    for col in categorical_cols:
        if col not in out.columns:
            continue
        s = out[col].astype("object")
        if categorical_strategy == "mode":
            # mode can be empty if all values are NaN
            modes = s.mode(dropna=True)
            fill_value = modes.iloc[0] if len(modes) > 0 else "UNKNOWN"
        elif categorical_strategy == "empty":
            fill_value = ""
        else:
            raise ValueError(f"Unsupported categorical_strategy: {categorical_strategy}")
        out[col] = s.fillna(fill_value)

    return out


def remove_duplicates(
    df: pd.DataFrame,
    subset: Optional[Iterable[str]] = None,
    keep: str = "first",
) -> pd.DataFrame:
    """
    Remove duplicate rows.

    Parameters
    ----------
    df : pd.DataFrame
        Input data.
    subset : optional iterable of str
        Columns to consider for identifying duplicates. If None, use all columns.
    keep : {"first", "last", False}
        Which duplicates to keep.

    Returns
    -------
    pd.DataFrame
        A new DataFrame with duplicates removed.
    """
    out = df.copy()
    out = out.drop_duplicates(subset=list(subset) if subset is not None else None, keep=keep)
    out = out.reset_index(drop=True)
    return out
