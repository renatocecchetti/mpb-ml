from pathlib import Path

ROOT_DIR = Path(__file__).parent.parent
CONFIG_PATH = ROOT_DIR / "config.yaml"

def get_project_root():
    return ROOT_DIR

def get_config_path():
    return CONFIG_PATH