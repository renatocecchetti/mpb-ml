import requests
from bs4 import BeautifulSoup
import logging
from typing import List, Dict
import time
from src.config import ConfigManager

logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO)

class NewsScraper:

    def __init__(self):
        self.config = ConfigManager()
        self.headers = {
            'User-Agent': self.config.get('scraping.user_agent')
        }
        self.timeout = self.config.get('scraping.timeout', 10)
        self.sleep_time = self.config.get('scraping.sleep_time', 0.5)
        self.logger = logging.getLogger(__name__)

    def get_news(self, url: str, post_class: str, type: str = 'div', limit: int = None) -> List[Dict]:
        """
        Obtém notícias de uma URL específica
        
        Args:
            url: URL da página
            post_class: Classe CSS dos posts
            type: Tipo do elemento HTML (div, article, etc.)
            limit: Número máximo de notícias a serem obtidas
        
        Returns:
            Lista de dicionários contendo links das notícias
        """
        self.logger.info(f'Obtendo notícias de {url}')
        news_list = []
        max_retries = self.config.get('scraping.max_retries', 3)

        try:
            for attempt in range(max_retries * (limit or 1)):
                response = requests.get(
                    url, 
                    timeout=self.timeout, 
                    headers=self.headers
                )

                if response.status_code != 200:
                    self.logger.error(f'Erro ao obter notícias. Status Code: {response.status_code}')
                    break

                soup = BeautifulSoup(response.content, 'html.parser')
                post_sections = soup.find_all(type, {'class': post_class})

                if not post_sections:
                    self.logger.warning(f'Nenhum post encontrado com a classe {post_class}')
                    break

                for section in post_sections:
                    link_element = section.find('a')
                    if link_element and 'href' in link_element.attrs:
                        news_list.append({'link': link_element['href']})

                    if limit and len(news_list) >= limit:
                        self.logger.info(f'Limite de {limit} notícias atingido')
                        return news_list

                time.sleep(self.sleep_time)
                logger.info(f'{len(news_list)} notícias obtidas até agora.')

                # Se não encontrou mais posts, para o loop
                if len(post_sections) == 0:
                    break

                # Pausa para não sobrecarregar o servidor
                time.sleep(0.5)

            logger.info(f'Total final de {len(news_list)} notícias obtidas.')
            return news_list

        except Exception as e:
            self.logger.exception(f'Erro ao obter notícias: {str(e)}')
            return news_list

    def get_full_text(self, url: str, content_class: str) -> str:
        """
        Obtém o texto completo de uma notícia
        """
        try:
            response = requests.get(
                url, 
                timeout=self.timeout, 
                headers=self.headers
            )
            soup = BeautifulSoup(response.content, 'html.parser')
            post_sections = soup.find_all('div', {'class': content_class})
            return ' '.join([section.text.strip() for section in post_sections])
        except Exception as e:
            self.logger.exception(f'Erro ao obter texto completo: {str(e)}')
            return ''

    @staticmethod
    def save_texts_to_file(texts: List[str], filename: str) -> None:
        """
        Salva textos em um arquivo
        """
        try:
            with open(filename, 'w', encoding='utf-8') as file:
                for text in texts:
                    file.write(text.replace('\n', ' ').replace('\r', '') + '\n')
            logger.info(f'Textos salvos em {filename}')
        except Exception as e:
            logger.exception(f'Erro ao salvar arquivo: {str(e)}')
