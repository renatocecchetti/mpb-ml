# src/main.py
import logging
from pathlib import Path
from datetime import datetime
import matplotlib.pyplot as plt
from matplotlib.backends.backend_pdf import PdfPages

from .speech import DiscursosDeputadosCollector, PoliticalSpectrumEnricher
from .scrapper import NewsPortalScraper
from .model import MediaBiasAnalyzer
from .visual import MediaBiasVisualizer

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class MediaBiasAnalysisPipeline:
    """Pipeline completo de análise de viés político em mídia"""
    
    def __init__(self):
        """Inicializa o pipeline"""
        self.data_dir = Path('data')
        self.models_dir = Path('models')
        self.output_dir = Path('output')
        
        # Cria diretórios se não existirem
        self.data_dir.mkdir(exist_ok=True)
        self.models_dir.mkdir(exist_ok=True)
        self.output_dir.mkdir(exist_ok=True)
        
        # Define caminhos dos arquivos
        self.enriched_speech = self.data_dir / 'speech' / 'Discursos_Enriquecidos.csv'
        self.speech_file = self.data_dir / 'speech' / 'Discursos.csv'
        self.party_file = self.data_dir / 'speech' / 'Partidos.csv'
        self.model_file = self.models_dir / 'political_bias_model.joblib'
        
        # Define portais para análise
        self.portals_dir = self.data_dir / 'portals'
        self.portals = ['G1', 'CNN', 'Folha', 'Gazeta', 'Istoe', 'Metropoles']

    def run_pipeline(self):
        """Executa o pipeline completo"""
        try:
            logger.info("Iniciando Pipeline:")

            # 1. Coleta discursos
            logger.info("Iniciando coleta de discursos...")
            self._collect_speeches()

            # 2. Enriquece discursos
            logger.info("Iniciando enriquecimento dos discursos...")
            self._enrich_speeches

            # 3. Coleta notícias dos portais
            logger.info("Iniciando coleta de notícias...")
            self._collect_news()

            # 4. Treina modelo
            logger.info("Iniciando treinamento do modelo...")
            self._train_model()

            # 5. Realiza inferências
            logger.info("Realizando inferências...")
            self._run_inference()

            logger.info("Pipeline concluído com sucesso!")
            
        except Exception as e:
            logger.exception("Erro durante execução do pipeline")
            raise

    def _collect_speeches(self):
        """Coleta discursos dos deputados"""
        collector = DiscursosDeputadosCollector()
        
        df = collector.collect_discursos(
            data_inicio='2023-01-01',
            data_fim='2024-02-22',
            output_file=str(self.speech_file)
        )
        
        logger.info(f"Coletados {len(df)} discursos")

    def _enrich_speeches(self):
        """Enriquece os discursos com informações adicionais"""
        enricher = PoliticalSpectrumEnricher()

        # Carrega os dados
        enricher.load_data(
            partidos_path=self.party_file,
            discursos_path=self.speech_file
        )

        # Enriquece os dados
        enricher.enrich_data()

        # Salva os dados enriquecidos
        enricher.save_enriched_data(self.enriched_speech)

    def _collect_news(self):
        """Coleta notícias dos portais"""
        # Inicializa o scraper
        scraper = NewsPortalScraper()

        # coleta de todos os portais
        all_texts = scraper.scrape_all(limit_per_columnist=100)
        for portal, texts in all_texts.items():
            scraper.save_portal_texts(portal, texts, self.portals_dir / '{portal}_political_news.txt')

    def _train_model(self):
        """Treina o modelo de classificação"""
        # Inicializa o analyzer
        analyzer = MediaBiasAnalyzer()
    
        # Realiza o treinamento do modelo
        analyzer.train_model(training_data=self.enriched_speech)

    def _run_inference(self):
        """Realiza inferências nos textos coletados"""
        # Inicializa o analyzer
        analyzer = MediaBiasAnalyzer()
    
        # Realiza análise das mídias
        analyzer.analyze_media()

def main():
    """Função principal"""
    pipeline = MediaBiasAnalysisPipeline()
    pipeline.run_pipeline()

if __name__ == "__main__":
    main()
