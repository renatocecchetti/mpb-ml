import yaml
from pathlib import Path
from typing import Any, Dict

class ConfigManager:
    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance
    
    def __init__(self):
        self.project_root = Path(__file__).parent.parent.parent
        if not hasattr(self, 'config'):
            self.load_config()
        
    def load_config(self, config_path: str = None):
        """
        Carrega configurações do arquivo YAML da raiz do projeto
        """
        try:
            config_file = self.project_root / 'config.yaml'
            
            if not config_file.is_file():
                raise FileNotFoundError(
                    f"Arquivo config.yaml não encontrado em: {config_file}"
                )
                
            with open(config_file, 'r', encoding='utf-8') as f:
                self.config = yaml.safe_load(f)
                
        except Exception as e:
            raise Exception(f"Erro ao carregar configurações: {str(e)}")
    
    def get(self, path: str, default: Any = None) -> Any:
        """
        Obtém valor do caminho especificado na configuração
        
        Args:
            path: Caminho na configuração (ex: 'model.bert_model')
            default: Valor padrão caso caminho não exista
        """
        keys = path.split('.')
        value = self.config
        
        for key in keys:
            try:
                value = value[key]
            except (KeyError, TypeError):
                return default
                
        return value
        
    def get_full_path(self, path_config: str) -> Path:
        """
        Retorna o caminho completo para um path configurado
        
        Args:
            path_config: Chave de configuração do path (ex: 'general.data_dir')
            
        Returns:
            Path completo absoluto
        """
        relative_path = self.get(path_config)
        return self.project_root / relative_path
