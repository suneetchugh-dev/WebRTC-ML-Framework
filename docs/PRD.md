# Product Requirements Document (PRD)

**Project**: WebRTC Multi-Cause Degradation Classification  
**Type**: Academic Research (ML + Networking)  
**Version**: 1.0.0  

## 1) Problem Statement
Current WebRTC QoE monitoring gives binary state ("good/bad") or a monolithic MOS that does not isolate root causes. To enable intelligent remediation, systems need to know *why* quality degrades (high latency, packet loss/frames dropped, jitter/instability).

## 2) Objective
Design and evaluate a lightweight ML framework that classifies multi-cause degradation in real-time using W3C `getStats()` telemetry under controlled, isolated network impairments.

## 3) Target Users
- **Researchers**: studying WebRTC QoE/root-cause analysis
- **Developers/Engineers**: integrating adaptive logic into WebRTC apps
- **Evaluators**: grading reproducible networking/ML experiments

## 4) Requirements

### Functional
- **FR-1**: Collect WebRTC `getStats()` telemetry (RTT, jitter, packet loss, frames sent/received/dropped, codec stats) during calls
- **FR-2**: Induce isolated impairments via `tc/netem` (delay, loss, jitter) with reproducible scripts
- **FR-3**: Label samples by dominant cause (normal, latency_high, packet_loss/frames_dropped, jitter_instability)
- **FR-4**: Extract features (per-interval aggregates, deltas, ratios)
- **FR-5**: Train lightweight classifier (Random Forest; configurable)
- **FR-6**: Evaluate with accuracy/precision/recall/F1/confusion matrix
- **FR-7**: Export trained model + preprocessing pipeline for inference

### Non-Functional
- **NFR-1**: Lightweight (tree-based) for low-latency inference
- **NFR-2**: Reproducible (scripts, fixed seeds, versioned deps)
- **NFR-3**: Isolated ground truth (single impairment per class)
- **NFR-4**: Minimal overhead suitable for client-side use
- **NFR-5**: Clear documentation for lab execution

## 5) Success Metrics
| Metric | Target | Notes |
|---|---|---|
| Overall Accuracy | >= 85% | On held-out test set from controlled experiments |
| Per-class F1 | >= 0.8 | For all defined degradation classes |
| Inference Time | < 5ms | Per prediction window (lightweight model) |
| Reproducibility | 100% | Via provided scripts/configs |

## 6) Scope & Non-Goals
**In scope**: controlled lab setup, multi-class classification, getStats-based features.  
**Out of scope**: subjective MOS collection at scale, deep learning on raw video, production-scale A/B testing.
