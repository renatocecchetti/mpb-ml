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

# Arquivo de Configuração (config.yaml)
## Visão Geral
O arquivo config.yaml centraliza todas as configurações do sistema de análise de viés político em texto. Este guia detalha cada seção e suas opções.

Estrutura do Arquivo
1. Configurações Gerais (general)
```bash
general:
  data_dir: 'data'              # Diretório base para dados
  data_dir_portals: 'data/portals'  # Subdiretório para dados dos portais
  data_dir_speech: 'data/speech'    # Subdiretório para discursos
  models_dir: 'models'          # Diretório para modelos treinados
  output_dir: 'output'          # Diretório para resultados
  log_level: 'INFO'             # Nível de logging
  log_format: '%(asctime)s...'  # Formato das mensagens de log

```
2. Configurações do Modelo (model)
```bash
model:
  name: 'political_bias_model.joblib'  # Nome do arquivo do modelo
  bert_model: 'neuralmind/bert-base-portuguese-cased'  # Modelo BERT pré-treinado
  hidden_layer_sizes: [100]     # Arquitetura da rede neural
  max_iter: 5000                # Máximo de iterações
  random_state: 1               # Semente aleatória
  embeddings_file_name: 'embeddings.npy'  # Arquivo de embeddings
  reuse_embedding: False        # Reutilizar embeddings existentes
```
3. Portais de Notícias (news_portals)
- supported_portals: Lista de portais suportados
- Para cada portal:
    - columnists: Dicionário de colunistas e suas URLs
    - content_class: Classe CSS para extrair conteúdo
    - post_class: Classe CSS para identificar posts

Exemplo de configuração de portal:
```bash
g1:
  columnists:
    andreia_sadi: 'https://g1.globo.com/politica/blog/andreia-sadi/'
    # ...
  content_class: 'mc-column content-text active-extra-styles'
  post_class: 'bastian-feed-item'
```
4. Configurações de Scraping (scraping)
```bash
scraping:
  user_agent: 'Mozilla/5.0...'  # User agent para requisições
  timeout: 10                   # Timeout em segundos
  sleep_time: 0.5              # Intervalo entre requisições
  max_retries: 3               # Máximo de tentativas
  items_per_page: 100          # Itens por página
  limit_per_columnist: 100     # Limite de artigos por colunista
```
5. Visualização (visualization)
```bash
visualization:
  figure_size: [10, 6]         # Tamanho dos gráficos
  colors:                      # Cores por orientação política
    left: 'red'
    center: 'gray'
    right: 'blue'
  spectrum_order: ['Esquerda', 'Centro', 'Direita']  # Ordem no gráfico
```
6. API da Câmara (camara_api)
```bash
camara_api:
  base_url: 'https://dadosabertos.camara.leg.br/api/v2'
  endpoints:                    # Endpoints da API
    deputados: '/deputados'
    discursos: '/deputados/{id}/discursos'
  params:                      # Parâmetros padrão
    ordem: 'ASC'
    ordenarPor: 'nome'
    itens_por_pagina: 100
```
7. Configurações de Discursos (discursos)
```bash
discursos:
  paths:                       # Caminhos dos arquivos
    base_dir: 'data/speech'
    discursos_file: 'Discursos.csv'
    # ...
  data_collection:            # Parâmetros de coleta
    data_inicio: '2021-03-02'
    data_fim: '2025-03-01'
    sample_size: 5
  required_columns:           # Colunas obrigatórias
    discursos: ['transcricao', 'siglaPartido', ...]
    partidos: ['Sigla', 'Nome', ...]
  spectrum_mapping:          # Mapeamento do espectro político
    'Centro': 'Centro'
    'Centro-direita': 'Direita'
    # ...
```
### Uso e Manutenção
#### Adicionando Novos Portais
1. Adicione o nome do portal em supported_portals
2. Crie uma nova seção com:
    - Lista de colunistas
    - Classes CSS necessárias
    - Configurações específicas

#### Atualizando Configurações
- Scraping: Ajuste sleep_time e timeout conforme necessário
- Modelo: Modifique parâmetros do modelo em model
- Visualização: Personalize cores e tamanhos em visualization

#### Manutenção
- Verifique URLs periodicamente
- Atualize classes CSS quando os sites mudarem
- Ajuste parâmetros de scraping conforme necessidade

#### Boas Práticas
- Mantenha backup do arquivo
- Documente alterações
- Teste novas configurações em ambiente de desenvolvimento
- Monitore logs para ajustes de parâmetros

#### Observações
- Classes CSS podem mudar com atualizações dos portais
- Respeite limites de requisições dos sites
- Mantenha sleep_time adequado para evitar bloqueios
- Faça backup regular dos dados coletados

<br>
Este arquivo de configuração centraliza todas as configurações do sistema, facilitando manutenção e ajustes sem necessidade de alterar o código-fonte.

<br>

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