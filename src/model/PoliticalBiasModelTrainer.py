import os
import numpy as np
import pandas as pd
from transformers import AutoTokenizer, AutoModel
from sklearn.model_selection import train_test_split
from sklearn.neural_network import MLPClassifier
from sklearn.metrics import classification_report, confusion_matrix
from typing import Tuple, Dict, List
import logging
from tqdm import tqdm
from src.config import ConfigManager
import joblib

logger = logging.getLogger(__name__)

class PoliticalBiasModelTrainer:
    def __init__(self):
        self.config = ConfigManager()
        self.bert_model = self.config.get('model.bert_model')
        self.embedding_file = f'{self.config.get_full_path('general.models_dir')}/{self.config.get('model.embeddings_file_name')}'
        self.reuse_embedding = self.config.get('model.reuse_embedding', False)
        
        self.tokenizer = AutoTokenizer.from_pretrained(self.bert_model)
        self.bert_model = AutoModel.from_pretrained(self.bert_model)
        self.classifier = None
        
        # Mapeamento de classes
        self.mapping = self.config.get('model.class_mapping', {
            'Centro': 0,
            'Centro-direita': 1,
            'Direita': 1,
            'Extrema-direita': 1,
            'Centro-esquerda': 2,
            'Esquerda': 2,
            'Extrema-esquerda': 2
        })
        
        self.logger = logging.getLogger(__name__)

    def generate_embeddings(self, texts: List[str]) -> np.ndarray:
        batch_size = self.config.get('model.batch_size', 10)
        embeddings_list = []
        
        for i in tqdm(range(0, len(texts), batch_size)):
            batch_texts = texts[i:i+batch_size]
            inputs = self.tokenizer(batch_texts, return_tensors="pt", 
                                  truncation=True, padding=True, 
                                  max_length=self.config.get('model.max_length', 512))
            
            outputs = self.bert_model(**inputs)
            batch_embeddings = outputs.last_hidden_state.mean(dim=1).detach().numpy()
            embeddings_list.append(batch_embeddings)
            
        return np.concatenate(embeddings_list, axis=0)
    
    def prepare_data(self, df: pd.DataFrame) -> Tuple[np.ndarray, np.ndarray]:
        """Prepara os dados para treinamento"""
        texts = df['transcricao'].tolist()
        labels = df['Espectro Político'].map(self.mapping)

        print(self.reuse_embedding)
        print(os.path.exists(self.embedding_file))

        if self.reuse_embedding and os.path.exists(self.embedding_file):
            try:
                embeddings = np.load(self.embedding_file)
                return embeddings, labels.values
            except FileNotFoundError:
                logger.info("Arquivo de embeddings não encontrado. Gerando novos embeddings...")
        else:
            logger.info("Gerando embeddings...")
            embeddings = self.generate_embeddings(texts)
            np.save(self.embedding_file, embeddings)
        
        return embeddings, labels.values

    def train(self, X: np.ndarray, y: np.ndarray) -> Tuple[MLPClassifier, Dict]:
        X_train, X_test, y_train, y_test = train_test_split(
            X, y, 
            stratify=y, 
            random_state=self.config.get('model.random_state', 1)
        )
        
        self.classifier = MLPClassifier(
            hidden_layer_sizes=self.config.get('model.hidden_layer_sizes', (100)),
            random_state=self.config.get('model.random_state', 1),
            max_iter=self.config.get('model.max_iter', 5000),
            verbose=True
        )
        
        self.classifier.fit(X_train, y_train)
        
        y_pred = self.classifier.predict(X_test)
        metrics = {
            'accuracy': self.classifier.score(X_test, y_test),
            'classification_report': classification_report(y_test, y_pred),
            'confusion_matrix': confusion_matrix(y_test, y_pred, normalize='true')
        }
        
        return self.classifier, metrics
    
    def save_model(self, path: str = 'political_bias_model.joblib'):
        """Salva o modelo treinado"""
        if self.classifier is None:
            raise ValueError("Modelo ainda não foi treinado")
        joblib.dump(self.classifier, path)