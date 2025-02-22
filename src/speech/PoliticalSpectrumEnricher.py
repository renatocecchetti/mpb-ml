import pandas as pd
import logging
from typing import Optional
from pathlib import Path

logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO)

class PoliticalSpectrumEnricher:
    """
    Classe para enriquecer base de discursos com espectro político dos partidos
    """
    
    def __init__(self):
        """Inicializa o enricher"""
        self.partidos_df = None
        self.discursos_df = None
        self.enriched_df = None

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
            logger.info(f"Carregando dados de {partidos_path} e {discursos_path}")
            
            # Carrega e processa partidos
            self.partidos_df = pd.read_csv(partidos_path)
            self._process_partidos()
            
            # Carrega e processa discursos
            self.discursos_df = pd.read_csv(discursos_path)
            self._process_discursos()
            
            logger.info("Dados carregados com sucesso")
            
        except Exception as e:
            logger.exception(f"Erro ao carregar dados: {str(e)}")
            raise

    def _process_partidos(self) -> None:
        """Processa e limpa dados dos partidos"""
        try:
            # Corrige nomenclatura do espectro político
            self.partidos_df.loc[
                self.partidos_df['Espectro Político'] == 'Extrema- direita',
                'Espectro Político'
            ] = 'Extrema-direita'
            
            # Remove linhas sem sigla ou espectro político
            self.partidos_df.dropna(
                subset=['Sigla', 'Espectro Político'],
                how='all',
                inplace=True
            )
            
            logger.info(f"Processados dados de {len(self.partidos_df)} partidos")
            
        except Exception as e:
            logger.exception(f"Erro ao processar partidos: {str(e)}")
            raise

    def _process_discursos(self) -> None:
        """Processa e limpa dados dos discursos"""
        try:
            # Remove discursos sem partido
            self.discursos_df.dropna(
                subset=['siglaPartido'],
                how='all',
                inplace=True
            )
            
            logger.info(f"Processados dados de {len(self.discursos_df)} discursos")
            
        except Exception as e:
            logger.exception(f"Erro ao processar discursos: {str(e)}")
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
            
            logger.info("Iniciando enriquecimento dos dados")
            
            # Realiza o merge
            self.enriched_df = self.discursos_df.merge(
                self.partidos_df[['Sigla', 'Espectro Político']],
                left_on='siglaPartido',
                right_on='Sigla',
                how='inner'
            )
            
            # Remove registros sem espectro político ou transcrição
            self.enriched_df.dropna(
                subset=['Espectro Político', 'transcricao'],
                how='all',
                inplace=True
            )
            
            logger.info(f"Dados enriquecidos: {len(self.enriched_df)} registros")
            
            return self.enriched_df
            
        except Exception as e:
            logger.exception(f"Erro ao enriquecer dados: {str(e)}")
            raise

    def save_enriched_data(self, output_path: str) -> None:
        """
        Salva os dados enriquecidos em arquivo
        
        Args:
            output_path: Caminho para salvar o arquivo
        """
        try:
            if self.enriched_df is None:
                raise ValueError("Não há dados enriquecidos. Execute enrich_data primeiro.")
                
            self.enriched_df.to_csv(output_path, index=False)
            logger.info(f"Dados salvos em {output_path}")
            
        except Exception as e:
            logger.exception(f"Erro ao salvar dados: {str(e)}")
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
