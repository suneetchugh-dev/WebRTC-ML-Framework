#!/usr/bin/env python3
"""Load and process collected CSV files from web UI"""
import pandas as pd
import json
from pathlib import Path
from datetime import datetime

def load_csv_files(raw_dir="data/raw"):
    files = list(Path(raw_dir).glob("*.csv"))
    dfs = []
    for f in files:
        try:
            df = pd.read_csv(f)
            dfs.append(df)
            print(f"Loaded {f.name}: {len(df)} rows")
        except Exception as e:
            print(f"Error loading {f}: {e}")
    return pd.concat(dfs, ignore_index=True) if dfs else pd.DataFrame()

if __name__ == "__main__":
    df = load_csv_files()
    print(f"\nTotal samples: {len(df)}")
    if not df.empty:
        print(f"Labels: {df['label'].value_counts().to_dict()}")
