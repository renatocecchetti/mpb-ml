import requests
import logging
import time
from typing import List, Dict
from tqdm import tqdm
from NewsScraper import NewsScraper

logger = logging.getLogger(__name__)

class NewsPortalScraper:
    """
    Classe para realizar scraping de diferentes portais de notícias brasileiros
    """
    
    def __init__(self):
        """Inicializa o scraper com a classe base NewsScraper"""
        self.scraper = NewsScraper()

    def scrape_g1(self, limit_per_columnist: int = 100) -> List[str]:
        """
        Realiza scraping das colunas políticas do G1
        
        Args:
            limit_per_columnist: Número máximo de notícias por colunista
        """
        g1_columnists = {
            'andreia_sadi': 'https://g1.globo.com/politica/blog/andreia-sadi/',
            'camila_bomfim': 'https://g1.globo.com/politica/blog/camila-bomfim/',
            'daniela_lima': 'https://g1.globo.com/politica/blog/daniela-lima/',
            'gerson_camarotti': 'https://g1.globo.com/politica/blog/gerson-camarotti/',
            'julia_duailibi': 'https://g1.globo.com/politica/blog/julia-duailibi/',
            'natuza_nery': 'https://g1.globo.com/politica/blog/natuza-nery/',
            'octavio_guedes': 'https://g1.globo.com/politica/blog/octavio-guedes/',
            'valdo_cruz': 'https://g1.globo.com/politica/blog/valdo-cruz/',
        }

        news = []
        texts = []

        try:
            for columnist_name, url in tqdm(g1_columnists.items(), desc="Coletando colunistas do G1"):
                logger.info(f'Coletando artigos de {columnist_name}')
                column_news = self.scraper.get_news(
                    limit=limit_per_columnist,
                    url=url,
                    post_class='bastian-feed-item',
                )
                news.extend(column_news)
                time.sleep(0.5)

            for article in tqdm(news, desc="Coletando textos do G1"):
                text = self.scraper.get_full_text(
                    url=article['link'],
                    content_class='mc-column content-text active-extra-styles'
                )
                if text:
                    texts.append(text)
                time.sleep(0.5)

            logger.info(f'Total de textos coletados do G1: {len(texts)}')
            return texts

        except Exception as e:
            logger.exception(f'Erro ao coletar notícias do G1: {str(e)}')
            return []

    def scrape_folha(self, limit_per_columnist: int = 100) -> List[str]:
        """
        Realiza scraping das colunas políticas da Folha
        """
        folha_columnists = {
            'adriana_fernandes': 'https://www1.folha.uol.com.br/colunas/adriana-fernandes/#40',
            'bruno_boghossian': 'https://www1.folha.uol.com.br/colunas/bruno-boghossian/',
            'camila_rocha': 'https://www1.folha.uol.com.br/colunas/camila-rocha/',
            'claudio_hebdo': 'https://www1.folha.uol.com.br/blogs/claudio-hebdo/',
            'conrado_hubner': 'https://www1.folha.uol.com.br/colunas/conrado-hubner-mendes/',
            'deborah_bizarria': 'https://www1.folha.uol.com.br/colunas/deborah-bizarria/',
            'desigualdades': 'https://www1.folha.uol.com.br/colunas/desigualdades/',
            'djamila_ribeiro': 'https://www1.folha.uol.com.br/colunas/djamila-ribeiro/',
            'dora_kramer': 'https://www1.folha.uol.com.br/colunas/dora-kramer/',
            'frederico_vasconcelos': 'https://www1.folha.uol.com.br/blogs/frederico-vasconcelos/',
            'ian_bremmer': 'https://www1.folha.uol.com.br/colunas/ian-bremmer/',
            'joao_pereira_coutinho': 'https://www1.folha.uol.com.br/colunas/joaopereiracoutinho/',
            'marcos_lisboa': 'https://www1.folha.uol.com.br/colunas/marcos-lisboa/',
            'marcos_mendes': 'https://www1.folha.uol.com.br/colunas/marcos-mendes/',
            'oscar_vilhena': 'https://www1.folha.uol.com.br/colunas/oscarvilhenavieira/',
            'painel': 'https://www1.folha.uol.com.br/colunas/painel/',
        }

        news = []
        texts = []

        try:
            for columnist_name, url in tqdm(folha_columnists.items(), desc="Coletando colunistas da Folha"):
                logger.info(f'Coletando artigos de {columnist_name}')
                column_news = self.scraper.get_news(
                    limit=limit_per_columnist,
                    url=url,
                    post_class='c-headline__content',
                )
                news.extend(column_news)
                time.sleep(0.5)

            for article in tqdm(news, desc="Coletando textos da Folha"):
                text = self.scraper.get_full_text(
                    url=article['link'],
                    content_class='c-news__content'
                )
                if text:
                    texts.append(text)
                time.sleep(0.5)

            logger.info(f'Total de textos coletados da Folha: {len(texts)}')
            return texts

        except Exception as e:
            logger.exception(f'Erro ao coletar notícias da Folha: {str(e)}')
            return []

    def scrape_cnn(self, limit_pages: int = 10) -> List[str]:
        """
        Realiza scraping das colunas políticas da CNN Brasil
        """
        cnn_columnists = {
            'jussara_soares': '48603',
            'luisa_martins': '59360',
            'taina_falcao': '16643',
            'gustavo_uribe': '684',
            'americo_martins': '37836',
            'larissa_rodrigues': '15966',
            'debora_bergamasco': '56760',
            'teo_cury': '16274',
            'julliana_lopes': '16259',
            'clarissa_oliveira': '47066',
            'iuri_pitta': '488',
        }

        texts = []
        
        try:
            for columnist_name, columnist_id in tqdm(cnn_columnists.items(), desc="Coletando colunistas da CNN"):
                logger.info(f'Coletando artigos de {columnist_name}')
                
                for page in range(1, limit_pages + 1):
                    url = f"https://www.cnnbrasil.com.br/wp-json/cnnbr/blogs/v1/articles?page={page}&term_id={columnist_id}"
                    
                    try:
                        response = requests.get(
                            url, 
                            timeout=10, 
                            headers=self.scraper.headers
                        )
                        
                        if response.status_code != 200:
                            continue
                            
                        articles = response.json()
                        if not articles:
                            break
                            
                        for article in articles:
                            text = self.scraper.get_full_text(
                                article['link'],
                                content_class='single-content'
                            )
                            if text:
                                texts.append(text)
                                
                        time.sleep(0.5)
                        
                    except Exception as e:
                        logger.warning(f"Erro na página {page} do colunista {columnist_name}: {str(e)}")
                        continue

            logger.info(f'Total de textos coletados da CNN: {len(texts)}')
            return texts

        except Exception as e:
            logger.exception(f'Erro ao coletar notícias da CNN: {str(e)}')
            return []

    def scrape_gazeta(self, limit_per_columnist: int = 20) -> List[str]:
        """
        Realiza scraping das colunas políticas da Gazeta do Povo
        """
        gazeta_columnists = {
            'adriano_gianturco': 'https://www.gazetadopovo.com.br/vozes/adriano-gianturco/',
            'alan_ghani': 'https://www.gazetadopovo.com.br/vozes/alan-ghani/',
            'alexandre_garcia': 'https://www.gazetadopovo.com.br/vozes/alexandre-garcia/',
            'carlos_di_franco': 'https://www.gazetadopovo.com.br/vozes/carlos-alberto-di-franco/',
            'deltan_dallagnol': 'https://www.gazetadopovo.com.br/vozes/deltan-dallagnol/',
            'rodrigo_constantino': 'https://www.gazetadopovo.com.br/rodrigo-constantino/',
            'sergio_moro': 'https://www.gazetadopovo.com.br/vozes/sergio-moro/',
        }

        news = []
        texts = []

        try:
            for columnist_name, url in tqdm(gazeta_columnists.items(), desc="Coletando colunistas da Gazeta"):
                logger.info(f'Coletando artigos de {columnist_name}')
                
                column_news = self.scraper.get_news(
                    limit=limit_per_columnist,
                    url=url,
                    post_class='cardDefault_card-content__q5Ykc cardDefault_has-image__NZ4EN cardDefault_visual-image-type-right__glBPB',
                )
                
                news.extend(column_news)
                time.sleep(0.5)

            for article in tqdm(news, desc="Coletando textos da Gazeta"):
                full_url = 'https://www.gazetadopovo.com.br' + article['link']
                text = self.scraper.get_full_text(
                    url=full_url,
                    content_class='postBody_post-body-container__1KhtH'
                )
                if text:
                    texts.append(text)
                time.sleep(0.5)

            logger.info(f'Total de textos coletados da Gazeta: {len(texts)}')
            return texts

        except Exception as e:
            logger.exception(f'Erro ao coletar notícias da Gazeta: {str(e)}')
            return []

    def scrape_istoe(self, limit_per_columnist: int = 100) -> List[str]:
        """
        Realiza scraping das colunas políticas da IstoÉ
        """
        istoe_columnists = {
            'mazzini': 'https://istoe.com.br/coluna/coluna-do-mazzini/',
            'kertzman': 'https://istoe.com.br/coluna/ricardo-kertzman/',
        }

        news = []
        texts = []

        try:
            for columnist_name, url in tqdm(istoe_columnists.items(), desc="Coletando colunistas da IstoÉ"):
                logger.info(f'Coletando artigos de {columnist_name}')
                
                column_news = self.scraper.get_news(
                    limit=limit_per_columnist,
                    url=url,
                    post_class='box-article-horizontal-cat d-flex f-column md-column sm-column col-lg-100',
                    type='article'
                )
                
                news.extend(column_news)
                time.sleep(0.5)

            for article in tqdm(news, desc="Coletando textos da IstoÉ"):
                text = self.scraper.get_full_text(
                    url=article['link'],
                    content_class='post-content-wrap col-lg-100 col-md-100'
                )
                if text:
                    texts.append(text)
                time.sleep(0.5)

            logger.info(f'Total de textos coletados da IstoÉ: {len(texts)}')
            return texts

        except Exception as e:
            logger.exception(f'Erro ao coletar notícias da IstoÉ: {str(e)}')
            return []

    def scrape_metropoles(self, limit_per_columnist: int = 20) -> List[str]:
        """
        Realiza scraping das colunas políticas do Metrópoles
        """
        metropoles_columnists = {
            'grande_angular': 'https://www.metropoles.com/colunas/grande-angular',
            'igor_gadelha': 'https://www.metropoles.com/colunas/igor-gadelha',
            'leandro_mazzini': 'https://www.metropoles.com/colunas/podcast-do-leandro-mazzini',
            'tacio_lorran': 'https://www.metropoles.com/colunas/tacio-lorran',
            'mario_sabino': 'https://www.metropoles.com/colunas/mario-sabino',
            'paulo_cappelli': 'https://www.metropoles.com/colunas/paulo-cappelli',
        }

        news = []
        texts = []

        try:
            for columnist_name, url in tqdm(metropoles_columnists.items(), desc="Coletando colunistas do Metrópoles"):
                logger.info(f'Coletando artigos de {columnist_name}')
                
                column_news = self.scraper.get_news(
                    limit=limit_per_columnist,
                    url=url,
                    post_class='Grid__Col-sc-owmjhw-2 iyeymd'
                )
                
                news.extend(column_news)
                time.sleep(0.5)

            for article in tqdm(news, desc="Coletando textos do Metrópoles"):
                text = self.scraper.get_full_text(
                    url=article['link'],
                    content_class='ConteudoNoticiaWrapper__Artigo-sc-19fsm27-1 iZYHrO'
                )
                if text:
                    texts.append(text)
                time.sleep(0.5)

            logger.info(f'Total de textos coletados do Metrópoles: {len(texts)}')
            return texts

        except Exception as e:
            logger.exception(f'Erro ao coletar notícias do Metrópoles: {str(e)}')
            return []

    def save_portal_texts(self, portal: str, texts: List[str], filename: str = None) -> None:
        """
        Salva os textos de um portal em arquivo
        
        Args:
            portal: Nome do portal
            texts: Lista de textos para salvar
            filename: Nome do arquivo (opcional)
        """
        if not texts:
            logger.warning(f'Nenhum texto para salvar do portal {portal}')
            return

        filename = filename or f'{portal}_texts.txt'
        self.scraper.save_texts_to_file(texts, filename)

    def scrape_all(self, limit_per_columnist: int = 100) -> Dict[str, List[str]]:
        """
        Realiza scraping de todos os portais configurados
        
        Args:
            limit_per_columnist: Número máximo de notícias por colunista
            
        Returns:
            Dicionário com os textos de cada portal
        """
        return {
            'g1': self.scrape_g1(limit_per_columnist),
            'folha': self.scrape_folha(limit_per_columnist),
            'cnn': self.scrape_cnn(limit_per_columnist),
            'gazeta': self.scrape_gazeta(limit_per_columnist),
            'istoe': self.scrape_istoe(limit_per_columnist),
            'metropoles': self.scrape_metropoles(limit_per_columnist)
        }
