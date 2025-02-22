# main.py
import argparse
import logging
from pathlib import Path
import pandas as pd
from datetime import datetime
from PoliticalBiasModelTrainer import PoliticalBiasModelTrainer
from PoliticalBiasInferencer import PoliticalBiasInferencer

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

class MediaBiasAnalyzer:
    """
    Classe principal para executar análise de viés político em textos de mídia
    """
    
    def __init__(self, 
                 data_dir: str = '../../data/portals',
                 models_dir: str = '../../models',
                 output_dir: str = '../../output'):
        """
        Inicializa o analisador
        
        Args:
            data_dir: Diretório com dados de entrada
            models_dir: Diretório para salvar/carregar modelos
            output_dir: Diretório para salvar resultados
        """
        self.data_dir = Path(data_dir)
        self.models_dir = Path(models_dir)
        self.output_dir = Path(output_dir)
        
        # Cria diretórios se não existirem
        self.data_dir.mkdir(exist_ok=True)
        self.models_dir.mkdir(exist_ok=True)
        self.output_dir.mkdir(exist_ok=True)
        
        self.model_path = self.models_dir / 'political_bias_model.joblib'
        
        # Lista de portais de notícias suportados
        self.news_portals = [
            'G1', 'Folha', 'Gazeta', 'CNN', 'Istoe', 'Metropoles'
        ]

    def train_model(self, training_data: str):
        """
        Treina o modelo de classificação
        
        Args:
            training_data: Caminho para arquivo de dados de treinamento
        """
        try:
            logger.info("Iniciando treinamento do modelo...")
            
            # Carrega dados de treinamento
            df = pd.read_csv(training_data)
            
            # Inicializa e treina o modelo
            trainer = PoliticalBiasModelTrainer()
            X, y = trainer.prepare_data(df)
            model, metrics = trainer.train(X, y)
            
            # Salva o modelo
            trainer.save_model(self.model_path)
            
            # Salva métricas
            metrics_file = self.output_dir / f'metrics_{datetime.now().strftime("%Y%m%d_%H%M%S")}.txt'
            with open(metrics_file, 'w') as f:
                f.write(f"Accuracy: {metrics['accuracy']}\n\n")
                f.write("Classification Report:\n")
                f.write(metrics['classification_report'])
            
            logger.info(f"Modelo treinado e salvo em {self.model_path}")
            logger.info(f"Métricas salvas em {metrics_file}")
            
        except Exception as e:
            logger.exception("Erro durante o treinamento do modelo")
            raise

    def analyze_media(self, portal_name: str = None):
        """
        Realiza análise de viés político para um ou todos os portais
        
        Args:
            portal_name: Nome do portal específico (opcional)
        """
        try:
            # Verifica se o modelo existe
            if not self.model_path.exists():
                raise FileNotFoundError("Modelo não encontrado. Execute o treinamento primeiro.")
            
            # Inicializa o inferenciador
            inferencer = PoliticalBiasInferencer(str(self.model_path))
            
            # Define quais portais analisar
            portals_to_analyze = [portal_name] if portal_name else self.news_portals
            
            # Analisa cada portal
            for portal in portals_to_analyze:
                logger.info(f"Analisando portal: {portal}")
                
                # Carrega textos do portal
                input_file = self.data_dir / f'{portal}_political_news.txt'
                if not input_file.exists():
                    logger.warning(f"Arquivo não encontrado para {portal}")
                    continue
                    
                with open(input_file, 'r', encoding='utf-8') as f:
                    texts = [line.strip() for line in f.readlines()]
                
                # Realiza análise
                analysis = inferencer.analyze_media_bias(texts)
                
                # Salva predições
                output_file = self.output_dir / f'{portal}_predictions.csv'
                inferencer.save_predictions(texts, str(output_file))
                
                # Salva análise
                analysis_file = self.output_dir / f'{portal}_analysis.txt'
                with open(analysis_file, 'w') as f:
                    f.write(f"Análise de Viés Político - {portal}\n")
                    f.write(f"Total de textos analisados: {analysis['total_texts']}\n\n")
                    f.write("Distribuição por orientação política:\n")
                    for orientation, percentage in analysis['predictions'].items():
                        f.write(f"{orientation}: {percentage:.1f}%\n")
                
                logger.info(f"Análise do portal {portal} concluída")
                
        except Exception as e:
            logger.exception("Erro durante a análise dos portais")
            raise