from src.scrapper import NewsPortalScraper
from src.config import ConfigManager

config = ConfigManager()
scraper = NewsPortalScraper()

all_texts = scraper.scrape_all_portals()

# Salva os textos de cada portal
for portal, texts in all_texts.items():
    scraper.save_portal_texts(portal, texts)