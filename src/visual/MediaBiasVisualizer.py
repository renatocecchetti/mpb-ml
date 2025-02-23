import pandas as pd
import matplotlib.pyplot as plt
from collections import Counter
from pathlib import Path

class MediaBiasVisualizer:
    
    def __init__(self, output_dir: str = 'output'):
        """
        Inicializa o visualizador
        
        Args:
            output_dir: Diretório com os arquivos de predições
        """
        self.output_dir = Path(output_dir)
        self.desired_order = ['Esquerda', 'Centro', 'Direita']
        self.colors = ['red', 'gray', 'blue']
        
    def load_predictions(self, portal: str) -> pd.DataFrame:
        """Carrega predições de um portal"""
        file_path = self.output_dir / f'{portal}_predictions.csv'
        return pd.read_csv(file_path)
    
    def plot_portal_bias(self, portal: str):
        """Plota gráfico de viés para um portal"""
        # Carrega dados
        df = self.load_predictions(portal)
        
        # Conta predições
        counts = Counter(df['prediction'])
        total = len(df)
        
        # Calcula percentagens
        percentages = {
            cls: (counts.get(cls, 0) / total * 100)
            for cls in self.desired_order
        }
        
        # Cria gráfico
        plt.figure(figsize=(10, 6))
        
        # Plota barras
        bars = plt.bar(
            list(percentages.keys()),
            list(percentages.values()),
            color=self.colors
        )
        
        # Configura gráfico
        plt.title(f'Distribuição do Viés Político - {portal}')
        plt.xlabel('Orientação Política')
        plt.ylabel('Porcentagem')
        
        # Adiciona rótulos
        for bar in bars:
            height = bar.get_height()
            plt.text(
                bar.get_x() + bar.get_width()/2.,
                height,
                f'{height:.1f}%',
                ha='center',
                va='bottom'
            )
        
        plt.ylim(0, 100)
        plt.show()