from pathlib import Path
import requests
import logging
import time
from typing import List, Dict
from tqdm import tqdm
from .NewsScraper import NewsScraper
from src.config import ConfigManager

logger = logging.getLogger(__name__)

class NewsPortalScraper:
    """
    Classe para realizar scraping de diferentes portais de notícias brasileiros
    """
    
    def __init__(self):
        self.config = ConfigManager()
        self.scraper = NewsScraper()
        self.logger = logging.getLogger(__name__)

    def scrape_portal(self, portal_name: str) -> List[str]:
        """
        Método para realizar scraping de portais
        
        Args:
            portal_name: Nome do portal conforme definido no config.yaml
            
        Returns:
            Lista de textos coletados
        """
        if portal_name.lower() == 'cnn':
            return self.scrape_cnn()
            
        try:
            # Obtém configurações específicas do portal
            portal_config = self.config.get(f'news_portals.{portal_name.lower()}')
            if not portal_config:
                raise ValueError(f"Configurações não encontradas para o portal {portal_name}")
            
            columnists = portal_config.get('columnists', {})
            content_class = portal_config.get('content_class')
            post_class = portal_config.get('post_class')
            limit_per_columnist = self.config.get('scraping.limit_per_columnist')
            
            news = []
            texts = []

            # Coleta artigos de cada colunista
            for columnist_name, url in tqdm(columnists.items(), 
                                         desc=f"Coletando colunistas do {portal_name}"):
                self.logger.info(f'Coletando artigos de {columnist_name}')
                
                try:
                    column_news = self.scraper.get_news(
                        limit=limit_per_columnist,
                        url=url,
                        post_class=post_class,
                    )
                    news.extend(column_news)
                    time.sleep(self.config.get('scraping.sleep_time'))
                    
                except Exception as e:
                    self.logger.warning(f"Erro ao coletar artigos de {columnist_name}: {str(e)}")
                    continue

            # Coleta texto completo de cada artigo
            for article in tqdm(news, desc=f"Coletando textos do {portal_name}"):
                try:
                    # Trata URLs relativas se necessário
                    if portal_name.lower() == 'gazeta' and not article['link'].startswith('http'):
                        full_url = 'https://www.gazetadopovo.com.br' + article['link']
                    else:
                        full_url = article['link']
                        
                    text = self.scraper.get_full_text(
                        url=full_url,
                        content_class=content_class
                    )
                    if text:
                        texts.append(text)
                    time.sleep(self.config.get('scraping.sleep_time'))
                    
                except Exception as e:
                    self.logger.warning(f"Erro ao coletar texto do artigo {article['link']}: {str(e)}")
                    continue

            self.logger.info(f'Total de textos coletados do {portal_name}: {len(texts)}')
            return texts

        except Exception as e:
            self.logger.exception(f'Erro ao coletar notícias do {portal_name}: {str(e)}')
            return []

    def scrape_cnn(self) -> List[str]:
        """
        Método específico para CNN devido ao seu formato diferenciado (API)
        """
        portal_config = self.config.get('news_portals.cnn')
        columnists = portal_config.get('columnists', {}).get('id_mapping', {})
        base_url = portal_config.get('base_url')
        content_class = portal_config.get('content_class')
        limit_pages = self.config.get('scraping.limit_pages', 10)
        
        texts = []
        
        try:
            for columnist_name, columnist_id in tqdm(columnists.items(), 
                                                   desc="Coletando colunistas da CNN"):
                self.logger.info(f'Coletando artigos de {columnist_name}')
                
                for page in range(1, limit_pages + 1):
                    try:
                        url = f"{base_url}?page={page}&term_id={columnist_id}"
                        
                        response = requests.get(
                            url, 
                            timeout=self.config.get('scraping.timeout'), 
                            headers=self.scraper.headers
                        )
                        
                        if response.status_code != 200:
                            continue
                            
                        articles = response.json()
                        if not articles:
                            break
                            
                        for article in articles:
                            try:
                                text = self.scraper.get_full_text(
                                    article['link'],
                                    content_class=content_class
                                )
                                if text:
                                    texts.append(text)
                            except Exception as e:
                                self.logger.warning(
                                    f"Erro ao coletar texto do artigo {article['link']}: {str(e)}"
                                )
                                continue
                                
                        time.sleep(self.config.get('scraping.sleep_time'))
                        
                    except Exception as e:
                        self.logger.warning(
                            f"Erro na página {page} do colunista {columnist_name}: {str(e)}"
                        )
                        continue

            self.logger.info(f'Total de textos coletados da CNN: {len(texts)}')
            return texts

        except Exception as e:
            self.logger.exception(f'Erro ao coletar notícias da CNN: {str(e)}')
            return []

    def scrape_all_portals(self) -> Dict[str, List[str]]:
        """
        Realiza scraping de todos os portais configurados
        
        Returns:
            Dicionário com os textos de cada portal
        """
        results = {}
        supported_portals = self.config.get('news_portals.supported_portals', [])
        
        for portal in supported_portals:
            self.logger.info(f"Iniciando coleta do portal {portal}")
            texts = self.scrape_portal(portal)
            results[portal] = texts
            
        return results

    def save_portal_texts(self, portal: str, texts: List[str]) -> None:
        """
        Salva os textos de um portal em arquivo
        
        Args:
            portal: Nome do portal
            texts: Lista de textos para salvar
        """
        if not texts:
            self.logger.warning(f'Nenhum texto para salvar do portal {portal}')
            return

        output_dir = Path(self.config.get_full_path('general.data_dir_portals'))
        output_dir.mkdir(exist_ok=True)
        
        filename = output_dir / f'{portal}_political_news.txt'
        self.scraper.save_texts_to_file(texts, str(filename))