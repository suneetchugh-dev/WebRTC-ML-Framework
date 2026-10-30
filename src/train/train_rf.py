#!/usr/bin/env python3
"""Train Random Forest classifier"""

import joblib
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import classification_report
from pathlib import Path

def train_model(X, y, **kwargs):
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42, stratify=y)
    clf = RandomForestClassifier(n_estimators=100, random_state=42, n_jobs=-1)
    clf.fit(X_train, y_train)
    return clf, X_test, y_test

def save_model(clf, path="results/models/rf_model.joblib"):
    Path(path).parent.mkdir(parents=True, exist_ok=True)
    joblib.dump(clf, path)
    print(f"Model saved to {path}")

if __name__ == "__main__":
    print("Training pipeline template")
