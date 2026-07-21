from pathlib import Path

# 本文件路径是：project_root/src/bossmind/paths.py
PACKAGE_DIR = Path(__file__).resolve().parent
PROJECT_ROOT = PACKAGE_DIR.parent.parent

CONFIGS_DIR = PROJECT_ROOT / "configs"

GAME_VERSION_FILE = CONFIGS_DIR / "game_version.yaml"