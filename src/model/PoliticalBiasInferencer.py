import numpy as np
import pandas as pd
from transformers import AutoTokenizer, AutoModel
import joblib
from typing import List, Dict
from collections import Counter
import logging
from src.config import ConfigManager
from pathlib import Path

logger = logging.getLogger(__name__)

class PoliticalBiasInferencer:
    def __init__(self):
        self.config = ConfigManager()
        
        model_dir = Path(self.config.get_full_path('general.models_dir'))
        self.model_path = model_dir / self.config.get('model.name')
        self.bert_model = self.config.get('model.bert_model')
        
        self.classifier = joblib.load(self.model_path)
        self.tokenizer = AutoTokenizer.from_pretrained(self.bert_model)
        self.bert_model = AutoModel.from_pretrained(self.bert_model)
        
        self.output_mapping = self.config.get('model.output_mapping', {
            0: 'Centro',
            1: 'Direita',
            2: 'Esquerda'
        })
        
        self.logger = logging.getLogger(__name__)
        
    def predict(self, text: str) -> str:
        inputs = self.tokenizer(
            text, 
            return_tensors="pt", 
            truncation=True, 
            padding=True, 
            max_length=self.config.get('model.max_length', 512)
        )
        outputs = self.bert_model(**inputs)
        embedding = outputs.last_hidden_state.mean(dim=1).detach().numpy()
        prediction = self.classifier.predict(embedding)[0]
        return self.output_mapping[prediction]
    
    def predict_batch(self, texts: List[str]) -> List[str]:
        """Realiza predições para uma lista de textos"""
        predictions = []
        for text in texts:
            try:
                pred = self.predict(text)
                predictions.append(pred)
            except Exception as e:
                logger.error(f"Erro ao processar texto: {str(e)}")
                predictions.append(None)
        return predictions
    
    def analyze_media_bias(self, texts: List[str]) -> Dict:
        """Analisa o viés político de um conjunto de textos"""
        predictions = self.predict_batch(texts)
        
        predictions = [p for p in predictions if p is not None]
        
        total = len(predictions)
        counts = Counter(predictions)
        
        analysis = {
            'total_texts': total,
            'predictions': {
                orientation: (count/total * 100)
                for orientation, count in counts.items()
            }
        }
        
        return analysis
    
    def save_predictions(self, 
                        texts: List[str],
                        output_path: str):
        """Salva as predições em arquivo"""
        predictions = self.predict_batch(texts)
        
        df = pd.DataFrame({
            'text': texts,
            'prediction': predictions
        })
        
        df.to_csv(output_path, index=False)
        logger.info(f"Predições salvas em {output_path}")
