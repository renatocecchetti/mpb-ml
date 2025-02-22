import requests
from bs4 import BeautifulSoup
import logging
from typing import List, Dict

logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO)

class NewsScraper:

    def __init__(self):
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 '
                         '(KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36'
        }

    def get_news(self, 
                limit: int, 
                url: str, 
                post_class: str,
                type: str = 'div'
                ) -> List[Dict]:
        """
        Obtém notícias de uma URL específica
        
        Args:
            limit: Número máximo de notícias a serem obtidas
            url: URL da página
            post_class: Classe CSS dos posts
            type: Tipo do elemento HTML (div, article, etc.)
        
        Returns:
            Lista de dicionários contendo links das notícias
        """
        logger.info(f'Obtendo notícias de {url}')
        news_list = []

        try:
            # Tenta no máximo limit * 2 vezes para dar margem a posts que não tenham links
            for attempt in range(limit * 2):
                response = requests.get(url, timeout=10, headers=self.headers)

                if response.status_code != 200:
                    logger.error(f'Erro ao obter notícias. Status Code: {response.status_code}')
                    break

                soup = BeautifulSoup(response.content, 'html.parser')
                post_sections = soup.find_all(type, {'class': post_class})

                if not post_sections:
                    logger.warning(f'Nenhum post encontrado com a classe {post_class}')
                    break

                for section in post_sections:
                    link_element = section.find('a')

                    if link_element and 'href' in link_element.attrs:
                        news_list.append({
                            'link': link_element['href'],
                        })

                        if len(news_list) >= limit:
                            logger.info(f'Limite de {limit} notícias atingido')
                            return news_list

                logger.info(f'{len(news_list)} notícias obtidas até agora.')

                # Se não encontrou mais posts, para o loop
                if len(post_sections) == 0:
                    break

                # Pausa para não sobrecarregar o servidor
                time.sleep(0.5)

            logger.info(f'Total final de {len(news_list)} notícias obtidas.')
            return news_list

        except Exception as e:
            logger.exception(f'Erro ao obter notícias: {str(e)}')
            return news_list

    def get_full_text(self, url: str, content_class: str = 'mc-column content-text active-extra-styles') -> str:
        """
        Obtém o texto completo de uma notícia
        """
        try:
            response = requests.get(url, timeout=10, headers=self.headers)
            soup = BeautifulSoup(response.content, 'html.parser')
            post_sections = soup.find_all('div', {'class': content_class})
            return ' '.join([section.text.strip() for section in post_sections])
        except Exception as e:
            logger.exception(f'Erro ao obter texto completo: {str(e)}')
            return ''

    @staticmethod
    def save_texts_to_file(texts: List[str], filename: str) -> None:
        """
        Salva textos em um arquivo
        """
        try:
            with open(filename, 'w', encoding='utf-8') as file:
                for text in texts:
                    file.write(text + '\n')
            logger.info(f'Textos salvos em {filename}')
        except Exception as e:
            logger.exception(f'Erro ao salvar arquivo: {str(e)}')
