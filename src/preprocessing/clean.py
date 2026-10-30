#!/usr/bin/env python3
"""Preprocess raw telemetry data"""

import pandas as pd
from pathlib import Path

def load_raw_data(raw_dir="data/raw"):
    files = list(Path(raw_dir).glob("*.csv")) + list(Path(raw_dir).glob("*.json"))
    dfs = []
    for f in files:
        if f.suffix == '.csv':
            dfs.append(pd.read_csv(f))
        elif f.suffix == '.json':
            dfs.append(pd.read_json(f))
    return pd.concat(dfs, ignore_index=True) if dfs else pd.DataFrame()

def clean_data(df):
    df = df.dropna(how='all')
    df = df.drop_duplicates()
    return df

if __name__ == "__main__":
    print("Preprocessing pipeline template")
