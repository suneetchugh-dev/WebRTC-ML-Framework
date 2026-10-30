#!/usr/bin/env python3
"""Run end-to-end experiment pipeline"""

import argparse

def main():
    parser = argparse.ArgumentParser(description="WebRTC degradation classification experiment")
    parser.add_argument('--label', default='normal', help='Condition label')
    parser.add_argument('--duration', type=int, default=60, help='Collection duration in seconds')
    args = parser.parse_args()
    print(f"Running experiment: label={args.label}, duration={args.duration}s")
    print("1. Apply netem (if needed)")
    print("2. Collect telemetry")
    print("3. Preprocess and extract features")
    print("4. Train/evaluate")

if __name__ == "__main__":
    main()
