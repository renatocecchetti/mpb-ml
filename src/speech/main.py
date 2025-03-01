import sys
from pathlib import Path
import logging
current_dir = Path(__file__).parent
project_root = current_dir.parent.parent
sys.path.append(str(project_root))

from src.speech import DiscursosDeputadosCollector
from src.speech import PoliticalSpectrumEnricher
from src.config import ConfigManager

config = ConfigManager()

# Configura logging
logging.basicConfig(
    level=config.get('general.log_level'),
    format=config.get('general.log_format')
)
logger = logging.getLogger(__name__)

# Inicializa coletores
collector = DiscursosDeputadosCollector()
enricher = PoliticalSpectrumEnricher()

try:
    # Coleta discursos
    df = collector.collect_discursos(
        data_inicio=config.get('discursos.data_collection.data_inicio'),
        data_fim=config.get('discursos.data_collection.data_fim'),
        output_file=str(Path(config.get_full_path('discursos.paths.base_dir')) / 
                         config.get('discursos.paths.discursos_file'))
    )
    
    # Enriquece dados
    enricher.load_data(
        partidos_path=str(Path(config.get_full_path('discursos.paths.base_dir')) /
                          config.get('discursos.paths.partidos_file')),
        discursos_path=str(Path(config.get_full_path('discursos.paths.base_dir')) /
                           config.get('discursos.paths.discursos_file'))
    )

    df_enriched = enricher.enrich_data()

    enricher.save_enriched_data(
        enriched_path=str(Path(config.get_full_path('discursos.paths.base_dir')) /
                         config.get('discursos.paths.merged_file')),
        stats_path=str(Path(config.get_full_path('discursos.paths.base_dir')) /
                          config.get('discursos.paths.stats_file'))
    )
    
    # Obtém e exibe estatísticas
    stats = enricher.get_spectrum_statistics()
    logger.info("\nEstatísticas por Espectro Político:")
    logger.info(stats)
    
except Exception as e:
    logger.exception("Erro durante o processamento")
    raise