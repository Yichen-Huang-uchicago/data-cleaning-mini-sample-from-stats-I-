from __future__ import annotations
import re
import numpy as np
import pandas as pd

STATA_MISSING_CODES = {
    ".": np.nan,
    ".a": np.nan, ".b": np.nan, ".c": np.nan, ".d": np.nan, ".e": np.nan,
    ".f": np.nan, ".g": np.nan, ".h": np.nan, ".i": np.nan, ".j": np.nan,
    ".k": np.nan, ".l": np.nan, ".m": np.nan, ".n": np.nan, ".o": np.nan,
    ".p": np.nan, ".q": np.nan, ".r": np.nan, ".s": np.nan, ".t": np.nan,
    ".u": np.nan, ".v": np.nan, ".w": np.nan, ".x": np.nan, ".y": np.nan, ".z": np.nan,
}

def snake_case(name: str) -> str:
    name = name.strip()
    name = re.sub(r"[^\w]+", "_", name)
    name = re.sub(r"__+", "_", name)
    return name.lower().strip("_")

def coerce_stata_numeric(series: pd.Series) -> pd.Series:
    if series.dtype == "object":
        series = series.replace(STATA_MISSING_CODES)
        return pd.to_numeric(series, errors="coerce")
    return series
