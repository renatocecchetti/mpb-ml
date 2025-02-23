# mpb-ml - Media Political Bias Machine Learning
Este repositório contém o Modelo de Aprendizado de Máquina, Conjunto de Dados e Código de Treinamento para Análise de Viés Político em Veículos de Comunicação Brasileiros

Pode ser utilizado de forma completa através da execução do pipeline ou de forma modularizada realizando a chamada à cada uma das funções. 
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

# Pipeline Completo
O pipeline irá realizar os seguintes passos:
1. Coleta dos discursos dos deputados
2. Enriquecimento com dados do espectro político dos partidos
3. Coleta de textos das colunas dos portais
4. Treinamento do modelo de classificação de viés
5. Realização de inferência nos dados dos portais

## 💻 Como Usar
```bash
python src/main.py
```
## Visualização dos Resultados
Um exemplo de visualização do resultado do Pipeline Completo encontra-se disponível no Jupyter Notebook [MediaBiasReport.ipynb](https://github.com/renatocecchetti/mpb-ml/blob/main/notebooks/MediaBiasReport.ipynb)

# Modularizado
## Scrapper de portais de notícias
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

# Exemplo de uso do coletor de discursos
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

# Exemplo de uso do enriquecedor
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
# 🎯 Treinamento e Inferência do Modelo de Viés Político em Mídia
## 📊 MediaBiasAnalyzer

### Descrição
Classe principal responsável por coordenar o processo de treinamento e análise de viés político em textos jornalísticos.

### Uso
```python
from MediaBiasAnalyzer import MediaBiasAnalyzer

path = '../../data/speech'
discursos = f'{path}/Discursos_Enriquecidos.csv'

# Inicializa o analisador
analyzer = MediaBiasAnalyzer()

# Treina o modelo
analyzer.train_model(training_data=discursos)

# Analisa todos os portais configurados
analyzer.analyze_media()
```
### ⚠️ Notas Importantes
- O modelo BERT requer GPU para treinamento eficiente
- Textos muito longos são truncados em 512 tokens
- Recomenda-se pelo menos 1000 exemplos para treinamento
- Os resultados podem variar dependendo dos dados de treinamento

## 📊 MediaBiasVisualizer

### Descrição
Classe responsável pela visualização e análise gráfica dos resultados de classificação de viés político em textos jornalísticos.

### Uso Básico
```python
from MediaBiasVisualizer import MediaBiasVisualizer

# Inicializa o visualizador
visualizer = MediaBiasVisualizer()

# Plota gráfico para um portal específico
visualizer.plot_portal_bias('G1')
```
<br>

# 🏗️ Estrutura do Projeto
```tree
.
├── LICENSE
├── README.md
├── data
│   ├── portals
│   │   ├── cnn_political_news.txt
│   │   ├── folha_political_news.txt
│   │   ├── g1_political_news.txt
│   │   ├── gazeta_political_news.txt
│   │   ├── istoe_political_news.txt
│   │   └── metropoles_political_news.txt
│   └── speech
│       └── Partidos.csv
├── models
│   └── political_bias_model.joblib
├── notebooks
│   └── MediaBiasReport.ipynb
├── output
│   ├── CNN_analysis.txt
│   ├── CNN_predictions.csv
│   ├── Folha_analysis.txt
│   ├── Folha_predictions.csv
│   ├── G1_analysis.txt
│   ├── G1_predictions.csv
│   ├── Gazeta_analysis.txt
│   ├── Gazeta_predictions.csv
│   ├── Istoe_analysis.txt
│   ├── Istoe_predictions.csv
│   ├── Metropoles_analysis.txt
│   ├── Metropoles_predictions.csv
│   ├── metrics_20250222_174248.txt
│   └── metrics_20250223_103248.txt
├── requirements.txt
└── src
    ├── main.py
    ├── model
    │   ├── MediaBiasAnalyzer.py
    │   ├── PoliticalBiasInferencer.py
    │   ├── PoliticalBiasModelTrainer.py
    │   └── main.py
    ├── scrapper
    │   ├── NewsPortalScraper.py
    │   ├── NewsScraper.py
    │   └── main.py
    ├── speech
    │   ├── DiscursosDeputadosCollector.py
    │   ├── PoliticalSpectrumEnricher.py
    │   └── main.py
    └── visual
        └── MediaBiasVisualizer.py
```
<br>

# 📝 Licença
Este projeto está licenciado sob a licença Apache-2.0 license - veja o arquivo [LICENSE](http://www.apache.org/licenses/LICENSE-2.0) para detalhes.

<br>

# 🤝 Contribuindo
Contribuições são bem-vindas!