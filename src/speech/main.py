from DiscursosDeputadosCollector import DiscursosDeputadosCollector

# Exemplo de uso
collector = DiscursosDeputadosCollector()

# Coleta discursos de um período específico
df = collector.collect_discursos(
    data_inicio='2025-01-01',
    data_fim='2025-02-22',
    output_file='Discursos_2025.csv'
)

# Análise dos dados
print(f"Total de discursos coletados: {len(df)}")
print("\nAmostra de transcricões:")
print(df.sample(5)['transcricao'])