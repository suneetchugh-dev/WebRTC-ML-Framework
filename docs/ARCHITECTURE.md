# Architecture

## System Overview
The pipeline is: **Collect (getStats) → Preprocess → Feature Extraction → Train/Evaluate → Inference**. Network conditions are controlled via `tc/netem` to ensure isolated ground truth labels.

```mermaid
graph TD
  A[WebRTC Peer Connection] -->|getStats() API| B[Telemetry Collector]
  C[tc/netem Impairments] --> D[Network Link]
  A <--> D
  B --> E[Raw CSV/JSON]
  E --> F[Preprocessing]
  F --> G[Feature Engineering]
  G --> H[Train/Test Split]
  H --> I[Random Forest Classifier]
  I --> J[Evaluation & Metrics]
  I --> K[Trained Model + Pipeline]
```

## Components

| Component | Purpose | Location |
|---|---|---|
| **Collector** | Capture `getStats()` snapshots at fixed intervals during calls | `src/collector/` |
| **Preprocessing** | Clean missing values, normalize timestamps, align intervals | `src/preprocessing/` |
| **Features** | Compute deltas/ratios (RTT/jitter/loss), frame stats | `src/features/` |
| **Train** | Train classifier with cross-validation | `src/train/` |
| **Evaluate** | Metrics, confusion matrix, classification report | `src/evaluate/` |
| **Utils** | Config, logging, helpers | `src/utils/` |
| **Scripts** | Experiment automation, netem setup | `scripts/` |

## Data Flow
1. **Setup**: Start WebRTC test call between peers on controlled network
2. **Impair**: Apply `tc netem` rule (delay/loss/jitter) for labeled class
3. **Collect**: Sample `getStats()` every 1s, log with timestamp + label
4. **Aggregate**: Create windows, compute features
5. **Train**: Fit model, save artifacts to `results/models/`
6. **Evaluate**: Generate reports/figures in `results/`

## Feature Set (Initial)
Key candidates from getStats(): `roundTripTime`, `jitter`, `packetsLost`, `packetsReceived`, `framesDropped`, `framesReceived`, `bytesReceived/Sent`, `availableOutgoingBitrate`. Derived: loss rate = packetsLost/(packetsLost+packetsReceived), RTT delta, jitter variance.

## Tech Stack
- **Language**: Python 3.10+
- **ML**: scikit-learn, pandas, numpy
- **Viz**: matplotlib, seaborn
- **WebRTC Test**: Browser (Chrome/Firefox) + custom test page or existing demo
- **Impairment**: Linux `tc`/`netem` (lab environment)
