import pandas as pd
import logging
from typing import Optional
from pathlib import Path
from src.config import ConfigManager

logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO)

class PoliticalSpectrumEnricher:
    """
    Classe para enriquecer base de discursos com espectro político dos partidos
    """
    
    def __init__(self):
        """Inicializa o enricher"""
        self.config = ConfigManager()
        self.partidos_df = None
        self.discursos_df = None
        self.enriched_df = None
        self.logger = logging.getLogger(__name__)

    def load_data(self,
                  partidos_path: str,
                  discursos_path: str) -> None:
        """
        Carrega os dados dos arquivos CSV
        
        Args:
            partidos_path: Caminho para o arquivo de partidos
            discursos_path: Caminho para o arquivo de discursos
        """
        try:
            self.logger.info(f"Carregando dados de {partidos_path} e {discursos_path}")
            
            self.partidos_df = pd.read_csv(partidos_path)
            self._process_partidos()
            
            self.discursos_df = pd.read_csv(discursos_path)
            self._process_discursos()
            
            self.logger.info("Dados carregados com sucesso")
            
        except Exception as e:
            self.logger.exception(f"Erro ao carregar dados: {str(e)}")
            raise

    def _process_partidos(self) -> None:
        """Processa e limpa dados dos partidos"""
        try:
            # Corrige nomenclatura conforme configuração
            corrections = self.config.get('data_processing.spectrum_corrections', {})
            for old, new in corrections.items():
                self.partidos_df.loc[
                    self.partidos_df['Espectro Político'] == old,
                    'Espectro Político'
                ] = new
            
            # Remove linhas sem dados essenciais
            required_columns = self.config.get('data_processing.required_columns.partidos', 
                                            ['Sigla', 'Espectro Político'])
            self.partidos_df.dropna(
                subset=required_columns,
                how='all',
                inplace=True
            )
            
            self.logger.info(f"Processados dados de {len(self.partidos_df)} partidos")
            
        except Exception as e:
            self.logger.exception(f"Erro ao processar partidos: {str(e)}")
            raise

    def _process_discursos(self) -> None:
        """Processa e limpa dados dos discursos"""
        try:
            required_columns = self.config.get('data_processing.required_columns.discursos', 
                                            ['siglaPartido'])
            self.discursos_df.dropna(
                subset=required_columns,
                how='all',
                inplace=True
            )
            
            self.logger.info(f"Processados dados de {len(self.discursos_df)} discursos")
            
        except Exception as e:
            self.logger.exception(f"Erro ao processar discursos: {str(e)}")
            raise

    def enrich_data(self) -> pd.DataFrame:
        """
        Realiza o merge entre discursos e partidos
        
        Returns:
            DataFrame enriquecido com espectro político
        """
        try:
            if self.partidos_df is None or self.discursos_df is None:
                raise ValueError("Dados não foram carregados. Execute load_data primeiro.")
            
            self.logger.info("Iniciando enriquecimento dos dados")
            
            merge_config = self.config.get('data_processing.merge_config', {
                'left_on': 'siglaPartido',
                'right_on': 'Sigla',
                'how': 'inner'
            })
            
            self.enriched_df = self.discursos_df.merge(
                self.partidos_df[['Sigla', 'Espectro Político']],
                **merge_config
            )
            
            required_columns = self.config.get('data_processing.required_columns.enriched', 
                                            ['Espectro Político', 'transcricao'])
            self.enriched_df.dropna(
                subset=required_columns,
                how='all',
                inplace=True
            )
            
            self.logger.info(f"Dados enriquecidos: {len(self.enriched_df)} registros")
            
            return self.enriched_df
            
        except Exception as e:
            self.logger.exception(f"Erro ao enriquecer dados: {str(e)}")
            raise

    def save_enriched_data(self, enriched_path, stats_path: str) -> None:
        """
        Salva os dados enriquecidos em arquivo
        
        Args:
            output_path: Caminho para salvar o arquivo
        """
        try:
            if self.enriched_df is None:
                raise ValueError("Não há dados enriquecidos. Execute enrich_data primeiro.")
            
            self.enriched_df.to_csv(enriched_path, index=True)
                
            agg_config = self.config.get('data_processing.aggregation_config', {
                'id': 'count',
                'siglaPartido': 'nunique',
                'nome': 'nunique'
            })
            
            stats = self.enriched_df.groupby('Espectro Político').agg(agg_config)
            stats.columns = ['Total_Discursos', 'Total_Partidos', 'Total_Deputados']
            
            stats.to_csv(stats_path, index=True)
            
        except Exception as e:
            self.logger.exception(f"Erro ao gerar estatísticas: {str(e)}")
            raise


    def get_spectrum_statistics(self) -> pd.DataFrame:
        """
        Retorna estatísticas por espectro político
        
        Returns:
            DataFrame com estatísticas
        """
        try:
            if self.enriched_df is None:
                raise ValueError("Não há dados enriquecidos. Execute enrich_data primeiro.")
                
            stats = self.enriched_df.groupby('Espectro Político').agg({
                'id': 'count',
                'siglaPartido': 'nunique',
                'nome': 'nunique'
            }).rename(columns={
                'id': 'Total_Discursos',
                'siglaPartido': 'Total_Partidos',
                'nome': 'Total_Deputados'
            })
            
            return stats
            
        except Exception as e:
            logger.exception(f"Erro ao gerar estatísticas: {str(e)}")
            raise
