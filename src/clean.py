from __future__ import annotations
import argparse
from pathlib import Path
import numpy as np
import pandas as pd
from utils import snake_case, coerce_stata_numeric

def main() -> None:
    p = argparse.ArgumentParser()
    p.add_argument("--input", required=True)
    p.add_argument("--outdir", required=True)
    p.add_argument("--reportdir", required=True)
    p.add_argument("--sample_n", type=int, default=200)
    args = p.parse_args()

    in_path = Path(args.input)
    outdir = Path(args.outdir)
    reportdir = Path(args.reportdir)
    outdir.mkdir(parents=True, exist_ok=True)
    reportdir.mkdir(parents=True, exist_ok=True)

    df_raw = pd.read_csv(in_path)
    df = df_raw.copy()
    df.columns = [snake_case(c) for c in df.columns]

    for col in df.select_dtypes(include=["object"]).columns:
        df[col] = df[col].astype(str).str.strip()
        df[col] = df[col].replace({"nan": np.nan, "NaN": np.nan, "None": np.nan})

    for col in ["hh_head_age", "hh_head_educ_years", "hh_has_electricity"]:
        if col in df.columns:
            df[col] = coerce_stata_numeric(df[col])

    for col in ["does_hh_own", "does_hh_has_access", "hh_any_od", "any_treatment"]:
        if col in df.columns:
            df[col] = pd.to_numeric(df[col], errors="coerce").astype("Int64")

    if "treat_cat" in df.columns:
        df["treat_cat"] = df["treat_cat"].astype("category")

    if "hh_head_age" in df.columns:
        df["hh_head_age_flag_outlier"] = ((df["hh_head_age"] < 15) | (df["hh_head_age"] > 100)).astype("Int64")
    if "hh_head_educ_years" in df.columns:
        df["hh_head_educ_years_flag_outlier"] = ((df["hh_head_educ_years"] < 0) | (df["hh_head_educ_years"] > 25)).astype("Int64")

    df.to_csv(outdir / "ta9_data_clean.csv", index=False)

    df_raw.sample(n=min(args.sample_n, len(df_raw)), random_state=42).to_csv(outdir / "sample_raw.csv", index=False)
    df.sample(n=min(args.sample_n, len(df)), random_state=42).to_csv(outdir / "sample_processed.csv", index=False)

    missing = (df.isna().mean() * 100).round(2).sort_values(ascending=False)
    miss_tbl = pd.DataFrame({"missing_pct": missing, "missing_n": df.isna().sum().reindex(missing.index).values})
    miss_tbl.to_csv(reportdir / "missingness_summary.csv")

    dict_rows = []
    for c in df.columns:
        s = df[c]
        ex = s.dropna().iloc[0] if s.dropna().shape[0] else ""
        dict_rows.append({"variable": c, "dtype": str(s.dtype), "missing_pct": float(s.isna().mean()*100), "example_value": ex})
    pd.DataFrame(dict_rows).to_csv(reportdir / "data_dictionary.csv", index=False)

    lines = ["# QA summary", f"- Rows: {df.shape[0]:,}", f"- Columns: {df.shape[1]}", "", "## Missingness (top 10)", miss_tbl.head(10).to_markdown(), "", "## Binary checks"]
    for col in ["does_hh_own", "does_hh_has_access", "hh_any_od", "any_treatment"]:
        if col in df.columns:
            vals = sorted([v for v in df[col].dropna().unique().tolist()])
            bad_n = int((~df[col].isin([0,1]) & df[col].notna()).sum())
            lines.append(f"- `{col}`: values={vals}; invalid_n={bad_n}")
    (reportdir / "qa_report.md").write_text("\n".join(lines), encoding="utf-8")

if __name__ == "__main__":
    main()
