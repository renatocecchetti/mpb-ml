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
    data_inicio='2020-01-01',
    data_fim='2024-12-31',
    output_file=speech_file
)

# Análise dos dados
print(f"Total de discursos coletados: {len(df)}")
print("\nAmostra de transcrições:")
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