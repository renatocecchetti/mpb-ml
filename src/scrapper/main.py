from NewsPortalScraper import NewsPortalScraper

# Inicializa o scraper
scraper = NewsPortalScraper()

# coleta de todos os portais
all_texts = scraper.scrape_all(limit_per_columnist=1)
for portal, texts in all_texts.items():
    scraper.save_portal_texts(portal, texts, f'../../data/portals/{portal}_political_news.txt')