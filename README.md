# mpb-ml
Este repositório contém o Modelo de Aprendizado de Máquina, Conjunto de Dados e Código de Treinamento para Análise de Viés Político em Veículos de Comunicação Brasileiros

# News Portal Scraper
Sistema de coleta automatizada de notícias dos principais portais jornalísticos do Brasil.

## 📰 Sobre
Sistema que realiza scraping de colunas políticas dos seguintes portais:

- G1
- CNN Brasil
- Folha de São Paulo
- Gazeta do Povo
- IstoÉ
- Metrópoles

## 🚀 Instalação
### Clone o repositório
```bash
git clone https://github.com/renatocecchetti/mpb-ml.git
cd mpb-ml
```

### Instale as dependências
```bash
pip install -r requirements.txt
```

## 💻 Como Usar
### Uso Básico
```python
from news_portal_scraper import NewsPortalScraper

# Inicializa o scraper
scraper = NewsPortalScraper()

# Coleta de um portal específico
g1_texts = scraper.scrape_g1(limit_per_columnist=100)
scraper.save_portal_texts('g1', g1_texts, 'g1_political_news.txt')

# Ou coleta de todos os portais
all_texts = scraper.scrape_all(limit_per_columnist=100)
for portal, texts in all_texts.items():
    scraper.save_portal_texts(portal, texts, f'{portal}_political_news.txt')
```
### Métodos Disponíveis
| Método | Descrição |
|--------|-----------|
| `scrape_g1(limit_per_columnist=100)` | Coleta textos dos colunistas políticos do G1 |
| `scrape_cnn(limit_pages=10)` | Coleta textos dos colunistas da CNN Brasil |
| `scrape_folha(limit_per_columnist=100)` | Coleta textos dos colunistas da Folha |
| `scrape_gazeta(limit_per_columnist=20)` | Coleta textos dos colunistas da Gazeta |
| `scrape_istoe(limit_per_columnist=100)` | Coleta textos dos colunistas da IstoÉ |
| `scrape_metropoles(limit_per_columnist=20)` | Coleta textos dos colunistas do Metrópoles |
| `scrape_all(limit_per_columnist=100)` | Coleta textos de todos os portais |
| `save_portal_texts(portal, texts, filename)` | Salva os textos coletados em arquivo |

### Exemplo de Coleta Específica
```python
# Coleta apenas da CNN Brasil
cnn_texts = scraper.scrape_cnn(limit_pages=10)
scraper.save_portal_texts('cnn', cnn_texts, 'cnn_political_news.txt')

# Coleta apenas da Folha com limite personalizado
folha_texts = scraper.scrape_folha(limit_per_columnist=50)
scraper.save_portal_texts('folha', folha_texts, 'folha_political_news.txt')
```
## 📋 Requisitos
```bash
Python 3.7+
requests>=2.31.0
beautifulsoup4>=4.12.2
tqdm>=4.66.1
lxml>=4.9.3
```
## ⚠️ Limitações e Considerações
- O scraper respeita delays entre requisições para evitar sobrecarga dos servidores
- Alguns portais podem requerer autenticação para acesso completo ao conteúdo
- As classes CSS dos portais podem mudar, necessitando atualização do código
- O número real de textos coletados pode ser menor que o limite definido

## 🏗️ Estrutura do Projeto
```tree
news-portal-scraper/
├── src/
│   ├── __init__.py
│   ├── news_scraper.py
│   └── news_portal_scraper.py
├── requirements.txt
└── README.md
```

## 📝 Licença
Este projeto está licenciado sob a licença Apache-2.0 license - veja o arquivo [LICENSE](http://www.apache.org/licenses/LICENSE-2.0) para detalhes.

## 🤝 Contribuindo
Contribuições são bem-vindas!
