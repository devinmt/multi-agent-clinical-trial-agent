from pathlib import Path

# Project configuration
PROJECT_ROOT = Path(__file__).parent
DATA_DIR = PROJECT_ROOT / "data"
MODELS_DIR = PROJECT_ROOT / "models"

# LLM configuration
LLM_CONFIG = {
    "model": "gpt-40-mini",
    "temperature": 0
}

# System configuration
MAX_DOCUMENTS = 100
MAX_RETRIES = 3
TIMEOUT = 300  # seconds