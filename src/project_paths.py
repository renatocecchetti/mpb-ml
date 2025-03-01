import sys
from pathlib import Path

# Adiciona diretório raiz ao path do Python
root_dir = str(Path(__file__).parent)
sys.path.append(root_dir)