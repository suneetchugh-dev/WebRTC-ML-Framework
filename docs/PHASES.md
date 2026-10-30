# Implementation Phases

## Phase 0: Planning & Setup (Week 1)
- [x] Review existing research paper and format
- [x] Create project structure in `Research-Project/`
- [x] Write PRD, Architecture, AGENTS
- [ ] Setup Python environment and `requirements.txt`
- [ ] Prepare lab environment checklist

## Phase 1: Testbed & Data Collection (Week 1-2)
- [ ] Setup WebRTC peer connection test (local/LAN)
- [ ] Implement `getStats()` collector (`src/collector/collect.py`)
- [ ] Create `tc/netem` scripts for isolated impairments
- [ ] Run baseline (normal) and impaired runs, collect raw data
- [ ] Validate labeling and data integrity

## Phase 2: Preprocessing & Features (Week 2)
- [ ] Clean data (`src/preprocessing/clean.py`)
- [ ] Extract features (`src/features/extract.py`)
- [ ] Handle missing values, outliers
- [ ] Create processed dataset in `data/processed/`

## Phase 3: Modeling & Training (Week 2-3)
- [ ] Train Random Forest classifier (`src/train/train_rf.py`)
- [ ] Hyperparameter tuning (GridSearchCV)
- [ ] Cross-validation
- [ ] Save model/pipeline to `results/models/`

## Phase 4: Evaluation & Analysis (Week 3)
- [ ] Compute metrics and confusion matrix
- [ ] Generate figures/tables
- [ ] Analyze misclassifications
- [ ] Document findings

## Phase 5: Documentation & Paper Integration (Week 3-4)
- [ ] Complete all docs in `docs/`
- [ ] Prepare lab manual/execution guide
- [ ] Update research paper with results
- [ ] Final review and cleanup
