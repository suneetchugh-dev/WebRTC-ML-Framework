#!/usr/bin/env python3
"""End-to-end pipeline: load data, preprocess, extract features, train, evaluate"""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent / "src"))

import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.ensemble import ExtraTreesClassifier
from sklearn.preprocessing import StandardScaler, LabelEncoder
from sklearn.pipeline import Pipeline
from sklearn.metrics import classification_report, confusion_matrix, accuracy_score
import matplotlib.pyplot as plt
import seaborn as sns
import joblib
import json

from utils import config

def main():
    print("="*60)
    print("WebRTC Multi-Cause Degradation Classification Pipeline")
    print("="*60)
    
    # Load data
    print("\n[1/5] Loading data from data/raw/...")
    raw_files = list(config.DATA_RAW.glob("*.csv"))
    if not raw_files:
        print("ERROR: No CSV files found in data/raw/")
        return
    
    dfs = []
    for f in raw_files:
        df = pd.read_csv(f)
        print(f"  - {f.name}: {len(df)} samples")
        dfs.append(df)
    df = pd.concat(dfs, ignore_index=True)
    print(f"Total samples: {len(df)}")
    print(f"Label distribution:\n{df['label'].value_counts()}")
    
    # Feature engineering
    print("\n[2/5] Extracting features...")
    df = df.copy()
    if 'run_id' not in df.columns:
        df['run_id'] = 'default'

    for col in ['packets_lost', 'packets_received', 'frames_dropped', 'frames_received']:
        if col not in df.columns:
            df[col] = 0

    total = df['packets_lost'] + df['packets_received']
    df['loss_rate'] = (df['packets_lost'] / total.replace(0, np.nan)).fillna(0)
    df['loss_accumulated'] = df.groupby('run_id')['packets_lost'].cumsum()

    total_f = df['frames_dropped'] + df['frames_received']
    df['frames_dropped_rate'] = (df['frames_dropped'] / total_f.replace(0, np.nan)).fillna(0)
    df['frames_dropped_accumulated'] = df.groupby('run_id')['frames_dropped'].cumsum()

    for col in ['rtt_ms', 'rtt', 'jitter_ms', 'jitter', 'packets_sent', 'frames_sent', 'bytes_sent']:
        if col in df.columns:
            df[f'{col}_diff'] = df.groupby('run_id')[col].diff().fillna(0)
            df[f'{col}_diff2'] = df.groupby('run_id')[col].diff(2).fillna(0)
            try:
                df[f'{col}_ma3'] = df.groupby('run_id')[col].rolling(3).mean().reset_index(0, drop=True).fillna(df[col])
                df[f'{col}_ma5'] = df.groupby('run_id')[col].rolling(5).mean().reset_index(0, drop=True).fillna(df[col])
                df[f'{col}_std3'] = df.groupby('run_id')[col].rolling(3).std().reset_index(0, drop=True).fillna(0)
                df[f'{col}_std5'] = df.groupby('run_id')[col].rolling(5).std().reset_index(0, drop=True).fillna(0)
                df[f'{col}_max3'] = df.groupby('run_id')[col].rolling(3).max().reset_index(0, drop=True).fillna(df[col])
                df[f'{col}_min3'] = df.groupby('run_id')[col].rolling(3).min().reset_index(0, drop=True).fillna(df[col])
            except:
                pass
            df[f'{col}_pct_change'] = df.groupby('run_id')[col].pct_change().replace([np.inf, -np.inf], 0).fillna(0)

    if 'rtt_ms' in df.columns and 'jitter_ms' in df.columns:
        df['rtt_jitter_interaction'] = df['rtt_ms'] * df['jitter_ms']
    if 'rtt_ms' in df.columns:
        df['rtt_zscore'] = (df['rtt_ms'] - df['rtt_ms'].mean()) / (df['rtt_ms'].std() + 1e-6)
    if 'jitter_ms' in df.columns:
        df['jitter_zscore'] = (df['jitter_ms'] - df['jitter_ms'].mean()) / (df['jitter_ms'].std() + 1e-6)
    
    feature_cols = []
    for c in df.columns:
        if c not in ['timestamp', 'run_id', 'label', 'raw'] and df[c].dtype in ['int64', 'float64', 'float32']:
            feature_cols.append(c)
    
    X = df[feature_cols].fillna(0)
    y = df['label']
    
    print(f"Features used ({len(feature_cols)}): {feature_cols[:10]}...")
    
    le = LabelEncoder()
    y_encoded = le.fit_transform(y)
    class_names = le.classes_.tolist()
    print(f"Classes: {class_names}")
    
    with open(config.RESULTS / "feature_list.json", 'w') as f:
        json.dump({'features': feature_cols, 'classes': class_names}, f, indent=2)
    
    print("\n[3/5] Training ExtraTrees classifier...")
    X_train, X_test, y_train, y_test = train_test_split(
        X, y_encoded, test_size=config.TEST_SIZE, random_state=config.RANDOM_SEED, stratify=y_encoded
    )
    
    pipe = Pipeline([
        ('scaler', StandardScaler()),
        ('clf', ExtraTreesClassifier(n_estimators=500, random_state=config.RANDOM_SEED, n_jobs=-1, max_depth=25, min_samples_split=3))
    ])
    pipe.fit(X_train, y_train)
    
    joblib.dump(pipe, config.MODELS / "rf_model.joblib")
    joblib.dump(le, config.MODELS / "label_encoder.joblib")
    joblib.dump(pipe.named_steps['scaler'], config.MODELS / "preprocessor_pipeline.joblib")
    print(f"Saved model to {config.MODELS / 'rf_model.joblib'}")
    
    print("\n[4/5] Evaluating...")
    y_pred = pipe.predict(X_test)
    acc = accuracy_score(y_test, y_pred)
    print(f"\nAccuracy: {acc:.4f}")
    print("\nClassification Report:")
    report = classification_report(y_test, y_pred, target_names=class_names)
    print(report)
    
    with open(config.TABLES / "classification_report.txt", 'w') as f:
        f.write(f"Accuracy: {acc:.4f}\n\n")
        f.write(report)
    
    cm = confusion_matrix(y_test, y_pred)
    plt.figure(figsize=(10, 8))
    sns.heatmap(cm, annot=True, fmt='d', cmap='Blues', xticklabels=class_names, yticklabels=class_names)
    plt.title('Confusion Matrix - WebRTC Degradation Classification')
    plt.ylabel('True Label')
    plt.xlabel('Predicted Label')
    plt.tight_layout()
    plt.savefig(config.FIGURES / "confusion_matrix.png", dpi=300)
    plt.close()
    print(f"Saved confusion matrix to {config.FIGURES / 'confusion_matrix.png'}")
    
    if hasattr(pipe.named_steps['clf'], 'feature_importances_'):
        importances = pipe.named_steps['clf'].feature_importances_
        indices = np.argsort(importances)[::-1][:15]
        plt.figure(figsize=(12, 6))
        plt.title('Feature Importances (Top 15)')
        plt.bar(range(len(indices)), importances[indices])
        plt.xticks(range(len(indices)), [feature_cols[i] for i in indices], rotation=45, ha='right')
        plt.tight_layout()
        plt.savefig(config.FIGURES / "feature_importance.png", dpi=300)
        plt.close()
        print(f"Saved feature importance to {config.FIGURES / 'feature_importance.png'}")
    
    print("\n[5/5] Complete!")
    print("="*60)
    print(f"Results saved to: {config.RESULTS}")
    print("="*60)

if __name__ == "__main__":
    main()
