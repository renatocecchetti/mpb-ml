import logging
#from .models import BiasClassifier
#from .data import DataLoader
from .utils import BRMediaWebScrapper

# Configuração do logger
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Informações do pacote
__version__ = '0.1.0'
__author__ = 'Renato Cecchetti'
__description__ = 'Brazilian Media Political Bias Classifier'

# Exports
__all__ = [
    'BRMediaWebScrapper',
]