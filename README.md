# mpb-ml
Este repositório contém o Modelo de Aprendizado de Máquina, Conjunto de Dados e Código de Treinamento para Análise de Viés Político em Veículos de Comunicação Brasileiros
<br><br>
# 🚀 Instalação
## Clone o repositório
```bash
git clone https://github.com/renatocecchetti/mpb-ml.git
cd mpb-ml
```

## Instale as dependências
```bash
pip install -r requirements.txt
```
<br><br>
# Principais Recrusos

## News Portal Scraper
Sistema de coleta automatizada de notícias dos principais portais jornalísticos do Brasil.

### 📰 Sobre
Sistema que realiza scraping de colunas políticas dos seguintes portais:

- G1
- CNN Brasil
- Folha de São Paulo
- Gazeta do Povo
- IstoÉ
- Metrópoles

### 💻 Como Usar
#### Uso Básico
```python
from NewsPortalScraper import NewsPortalScraper

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
#### Métodos Disponíveis
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

#### Exemplo de Coleta Específica
```python
# Coleta apenas da CNN Brasil
cnn_texts = scraper.scrape_cnn(limit_pages=10)
scraper.save_portal_texts('cnn', cnn_texts, 'cnn_political_news.txt')

# Coleta apenas da Folha com limite personalizado
folha_texts = scraper.scrape_folha(limit_per_columnist=50)
scraper.save_portal_texts('folha', folha_texts, 'folha_political_news.txt')
```
#### 📋 Requisitos
```bash
Python 3.7+
requests>=2.31.0
beautifulsoup4>=4.12.2
tqdm>=4.66.1
lxml>=4.9.3
```
### ⚠️ Limitações e Considerações
- O scraper respeita delays entre requisições para evitar sobrecarga dos servidores
- Alguns portais podem requerer autenticação para acesso completo ao conteúdo
- As classes CSS dos portais podem mudar, necessitando atualização do código
- O número real de textos coletados pode ser menor que o limite definido

## 🏛️ Coletor de Discursos de Deputados

### Sobre
Classe Python para coletar discursos de deputados através da API da Câmara dos Deputados e processo de enriquecimento com dados de espectro político dos partidos brasileiros

### 🚀 Como Usar

#### Uso Básico
```python
from DiscursosDeputadosCollector import DiscursosDeputadosCollector
from PoliticalSpectrumEnricher import PoliticalSpectrumEnricher

# Exemplo de uso
collector = DiscursosDeputadosCollector()

path = '../../data/speech'
speech_file = f'{path}/Discursos.csv'
party_file = f'{path}/Partidos.csv'
merged_file = f'{path}/Discursos_Enriquecidos.csv'

# Coleta discursos de um período específico
df = collector.collect_discursos(
    data_inicio='2025-02-01',
    data_fim='2025-02-05',
    output_file=speech_file
)

# Análise dos dados
print(f"Total de discursos coletados: {len(df)}")
print("\nAmostra de transcricões:")
print(df.sample(5)['transcricao'])

# Exemplo de uso
enricher = PoliticalSpectrumEnricher()

# Carrega os dados
enricher.load_data(
    partidos_path=party_file,
    discursos_path=speech_file
)

# Enriquece os dados
df_enriched = enricher.enrich_data()

# Salva os dados enriquecidos
enricher.save_enriched_data(merged_file)

# Obtém estatísticas
stats = enricher.get_spectrum_statistics()
print("\nEstatísticas por Espectro Político:")
print(stats)
```
### 📊 Estrutura dos Dados Coletados e Enriquecidos

| Coluna | Descrição |
|:-------|:----------|
| `email` | Email institucional do deputado |
| `id` | ID único do deputado na Câmara |
| `idLegislatura` | ID da legislatura atual |
| `nome` | Nome completo do parlamentar |
| `siglaPartido` | Sigla do partido político |
| `siglaUf` | Unidade federativa que representa |
| `uri` | URI do deputado na API |
| `uriPartido` | URI do partido na API |
| `urlFoto` | URL da foto oficial |
| `dataHoraFim` | Timestamp do fim do discurso |
| `dataHoraInicio` | Timestamp do início do discurso |
| `keywords` | Palavras-chave do discurso |
| `sumario` | Resumo do conteúdo |
| `tipoDiscurso` | Classificação do discurso |
| `transcricao` | Texto completo |
| `urlAudio` | Link para o áudio |
| `urlVideo` | Link para o vídeo |
| `Espectro Político` | Espectro Político do Partido |

### 📋 Requisitos
```bash
Python 3.7+
requests>=2.31.0
pandas>=2.0.0
python-dateutil>=2.8.2
```
### ⚠️ Limitações e Considerações
- A API pode ter limites de requisições
- Alguns discursos podem não ter transcrição disponível
- O tempo de coleta pode variar dependendo do período solicitado
- Necessita conexão estável com a internet
<br><br>
# 🏗️ Estrutura do Projeto
```tree
news-portal-scraper/
├── src/
│   ├── __init__.py
│   ├── news_scraper.py
│   └── news_portal_scraper.py
├── requirements.txt
└── README.md
```
<br><br>
# 📝 Licença
Este projeto está licenciado sob a licença Apache-2.0 license - veja o arquivo [LICENSE](http://www.apache.org/licenses/LICENSE-2.0) para detalhes.
<br><br>

# 🤝 Contribuindo
Contribuições são bem-vindas!