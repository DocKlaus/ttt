from pathlib import Path

ROOT_DIR = Path(__file__).resolve().parents[1]
DATA_DIR = ROOT_DIR
# DATA_DIR = ROOT_DIR / "data"
FILE_NAME = "tree.pkl"
FILE_PATH = DATA_DIR / FILE_NAME