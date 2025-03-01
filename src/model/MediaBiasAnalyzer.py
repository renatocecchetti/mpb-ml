import argparse
import logging
from pathlib import Path
import pandas as pd
from datetime import datetime
from src.config import ConfigManager
from .PoliticalBiasModelTrainer import PoliticalBiasModelTrainer
from .PoliticalBiasInferencer import PoliticalBiasInferencer

class MediaBiasAnalyzer:
    def __init__(self):
        self.config = ConfigManager()
        
        # Configuração de logging
        logging.basicConfig(
            level=self.config.get('general.log_level'),
            format=self.config.get('general.log_format')
        )
        self.logger = logging.getLogger(__name__)
        
        # Configuração de diretórios
        self.data_dir = Path(self.config.get_full_path('general.data_dir_portals'))
        self.models_dir = Path(self.config.get_full_path('general.models_dir'))
        self.output_dir = Path(self.config.get_full_path('general.output_dir'))
        
        # Cria diretórios se não existirem
        self.data_dir.mkdir(exist_ok=True)
        self.models_dir.mkdir(exist_ok=True)
        self.output_dir.mkdir(exist_ok=True)
        
        self.model_path = self.models_dir / self.config.get('model.name')
        self.news_portals = self.config.get('news_portals.supported_portals')
        self.dataframe = str(Path(self.config.get_full_path('discursos.paths.base_dir')) /
                         self.config.get('discursos.paths.merged_file'))

    def train_model(self):
        try:
            self.logger.info("Iniciando treinamento do modelo...")
            
            df = pd.read_csv(self.dataframe)
            trainer = PoliticalBiasModelTrainer()
            X, y = trainer.prepare_data(df)
            model, metrics = trainer.train(X, y)
            
            trainer.save_model(self.model_path)
            
            metrics_file = self.output_dir / f'metrics_{datetime.now().strftime("%Y%m%d_%H%M%S")}.txt'
            with open(metrics_file, 'w') as f:
                f.write(f"Accuracy: {metrics['accuracy']}\n\n")
                f.write("Classification Report:\n")
                f.write(metrics['classification_report'])
            
            self.logger.info(f"Modelo treinado e salvo em {self.model_path}")
            self.logger.info(f"Métricas salvas em {metrics_file}")
            
        except Exception as e:
            self.logger.exception("Erro durante o treinamento do modelo")
            raise

    def analyze_media(self, portal_name: str = None):
        try:
            if not self.model_path.exists():
                raise FileNotFoundError("Modelo não encontrado. Execute o treinamento primeiro.")
            
            inferencer = PoliticalBiasInferencer()
            portals_to_analyze = [portal_name] if portal_name else self.news_portals
            
            for portal in portals_to_analyze:
                self.logger.info(f"Analisando portal: {portal}")
                
                input_file = self.data_dir / f'{portal.lower()}_political_news.txt'
                if not input_file.exists():
                    self.logger.warning(f"Arquivo não encontrado para {portal}")
                    continue
                    
                with open(input_file, 'r', encoding='utf-8') as f:
                    texts = [line.strip() for line in f.readlines()]
                
                analysis = inferencer.analyze_media_bias(texts)
                
                output_file = self.output_dir / f'{portal}_predictions.csv'
                inferencer.save_predictions(texts, str(output_file))
                
                analysis_file = self.output_dir / f'{portal}_analysis.txt'
                with open(analysis_file, 'w') as f:
                    f.write(f"Análise de Viés Político - {portal}\n")
                    f.write(f"Total de textos analisados: {analysis['total_texts']}\n\n")
                    f.write("Distribuição por orientação política:\n")
                    for orientation, percentage in analysis['predictions'].items():
                        f.write(f"{orientation}: {percentage:.1f}%\n")
                
                self.logger.info(f"Análise do portal {portal} concluída")
                
        except Exception as e:
            self.logger.exception("Erro durante a análise dos portais")
            raise