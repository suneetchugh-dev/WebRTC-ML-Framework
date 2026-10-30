from pathlib import Path

# Project paths
ROOT = Path(__file__).resolve().parents[2]
DATA_RAW = ROOT / "data" / "raw"
DATA_PROCESSED = ROOT / "data" / "processed"
RESULTS = ROOT / "results"
MODELS = RESULTS / "models"
FIGURES = RESULTS / "figures"
TABLES = RESULTS / "tables"

# Ensure directories exist
for p in [DATA_RAW, DATA_PROCESSED, MODELS, FIGURES, TABLES]:
    p.mkdir(parents=True, exist_ok=True)

# Experiment config
SAMPLING_INTERVAL_SEC = 1.0
RANDOM_SEED = 42
TEST_SIZE = 0.2
CV_FOLDS = 5
CLASSES = ["normal", "latency_high", "packet_loss_frames_dropped", "jitter_instability"]
DEFAULT_MODEL = "random_forest"
