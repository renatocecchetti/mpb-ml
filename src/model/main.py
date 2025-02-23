from MediaBiasAnalyzer import MediaBiasAnalyzer

def main():
    """Função principal"""    
    analyzer = MediaBiasAnalyzer()
    
    analyzer.train_model(training_data="../../data/speech/Discursos_Enriquecidos.csv")
    analyzer.analyze_media()

if __name__ == "__main__":
    main()