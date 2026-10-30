#!/usr/bin/env python3
"""Feature extraction from WebRTC stats"""

import pandas as pd

FEATURES = [
    'rtt_ms',
    'jitter_ms', 
    'packets_lost',
    'packets_received',
    'loss_rate',
    'frames_dropped',
    'frames_received',
    'frames_dropped_rate'
]

def extract_features(df):
    """Extract derived features"""
    df = df.copy()
    # Compute loss rate if possible
    if 'packets_lost' in df.columns and 'packets_received' in df.columns:
        total = df['packets_lost'] + df['packets_received']
        df['loss_rate'] = df['packets_lost'] / total.replace(0, 1)
    # Compute frame drop rate
    if 'frames_dropped' in df.columns and 'frames_received' in df.columns:
        total_f = df['frames_dropped'] + df['frames_received']
        df['frames_dropped_rate'] = df['frames_dropped'] / total_f.replace(0, 1)
    return df

if __name__ == "__main__":
    print("Feature extraction template")
