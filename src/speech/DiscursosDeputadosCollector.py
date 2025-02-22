import requests
import pandas as pd
from typing import List, Dict
import logging
from datetime import datetime

logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO)

class DiscursosDeputadosCollector:
    """
    Classe para coletar discursos de deputados da API da Câmara dos Deputados
    """
    
    def __init__(self):
        """Inicializa as URLs base e configura headers"""
        self.base_url = "https://dadosabertos.camara.leg.br/api/v2"
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
        }

    def get_deputados(self) -> List[Dict]:
        """Obtém lista de deputados"""
        try:
            response = requests.get(
                f"{self.base_url}/deputados?ordem=ASC&ordenarPor=nome",
                headers=self.headers
            )
            
            if response.status_code == 200:
                return response.json()["dados"]
            else:
                logger.error(f"Erro ao obter deputados: {response.status_code}")
                return []
                
        except Exception as e:
            logger.exception(f"Erro ao obter deputados: {str(e)}")
            return []

    def get_discursos_deputado(self, 
                              deputado_id: int, 
                              data_inicio: str, 
                              data_fim: str,
                              itens_por_pagina: int = 100) -> List[Dict]:
        """
        Obtém discursos de um deputado específico
        
        Args:
            deputado_id: ID do deputado
            data_inicio: Data inicial (YYYY-MM-DD)
            data_fim: Data final (YYYY-MM-DD)
            itens_por_pagina: Número de itens por página
        """
        discursos_totais = []
        pagina = 1
        
        try:
            while True:
                response = requests.get(
                    f"{self.base_url}/deputados/{deputado_id}/discursos",
                    params={
                        "dataInicio": data_inicio,
                        "dataFim": data_fim,
                        "ordenarPor": "dataHoraInicio",
                        "ordem": "DESC",
                        "pagina": pagina,
                        "itens": itens_por_pagina
                    },
                    headers=self.headers
                )
                
                if response.status_code == 200:
                    discursos = response.json()["dados"]
                    discursos_totais.extend(discursos)
                    
                    if len(discursos) < itens_por_pagina:
                        break
                        
                    pagina += 1
                else:
                    logger.error(f"Erro ao obter discursos do deputado {deputado_id}: {response.status_code}")
                    break
                    
            return discursos_totais
            
        except Exception as e:
            logger.exception(f"Erro ao obter discursos do deputado {deputado_id}: {str(e)}")
            return []

    def collect_discursos(self, 
                         data_inicio: str, 
                         data_fim: str,
                         output_file: str = 'Discursos.csv') -> pd.DataFrame:
        """
        Coleta todos os discursos no período especificado
        
        Args:
            data_inicio: Data inicial (YYYY-MM-DD)
            data_fim: Data final (YYYY-MM-DD)
            output_file: Nome do arquivo de saída
        """
        try:
            # Valida formato das datas
            datetime.strptime(data_inicio, '%Y-%m-%d')
            datetime.strptime(data_fim, '%Y-%m-%d')
            
            dados = []
            deputados = self.get_deputados()
            
            logger.info(f"Coletando discursos de {len(deputados)} deputados")
            
            for deputado in deputados:
                discursos = self.get_discursos_deputado(
                    deputado['id'],
                    data_inicio,
                    data_fim
                )
                
                logger.info(f"Coletados {len(discursos)} discursos do deputado {deputado['nome']}")
                
                dados.append({
                    'deputado': deputado,
                    'discursos': discursos
                })

            # Processa os dados para DataFrame
            rows = []
            for dado in dados:
                deputado_data = dado['deputado']
                for discurso in dado['discursos']:
                    row = {
                        "email": deputado_data["email"],
                        "id": deputado_data["id"],
                        "idLegislatura": deputado_data["idLegislatura"],
                        "nome": deputado_data["nome"],
                        "siglaPartido": deputado_data["siglaPartido"],
                        "siglaUf": deputado_data["siglaUf"],
                        "uri": deputado_data["uri"],
                        "uriPartido": deputado_data["uriPartido"],
                        "urlFoto": deputado_data["urlFoto"],
                        "dataHoraFim": discurso["dataHoraFim"],
                        "dataHoraInicio": discurso["dataHoraInicio"],
                        "faseEvento_dataHoraFim": discurso["faseEvento"]["dataHoraFim"],
                        "faseEvento_dataHoraInicio": discurso["faseEvento"]["dataHoraInicio"],
                        "faseEvento_titulo": discurso["faseEvento"]["titulo"],
                        "keywords": discurso["keywords"],
                        "sumario": discurso["sumario"],
                        "tipoDiscurso": discurso["tipoDiscurso"],
                        "transcricao": discurso["transcricao"],
                        "uriEvento": discurso["uriEvento"],
                        "urlAudio": discurso["urlAudio"],
                        "urlTexto": discurso["urlTexto"],
                        "urlVideo": discurso["urlVideo"]
                    }
                    rows.append(row)

            df = pd.DataFrame(rows)
            
            if output_file:
                df.to_csv(output_file, index=False)
                logger.info(f"Dados salvos em {output_file}")
                
            return df
            
        except ValueError as e:
            logger.error(f"Formato de data inválido: {str(e)}")
            raise
        except Exception as e:
            logger.exception(f"Erro ao coletar discursos: {str(e)}")
            raise

