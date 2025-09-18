import os
import logging
from dotenv import load_dotenv

# Configuration du logging structuré
def setup_logging():
    """Configure le système de logging pour l'application"""
    log_format = '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    
    # Créer le dossier logs s'il n'existe pas
    log_dir = os.path.join(os.path.dirname(__file__), "logs")
    os.makedirs(log_dir, exist_ok=True)
    
    logging.basicConfig(
        level=logging.INFO,
        format=log_format,
        handlers=[
            logging.FileHandler(os.path.join(log_dir, 'kira_bot.log'), encoding='utf-8'),
            logging.StreamHandler()
        ]
    )
    
    # Logger spécifique pour le bot
    logger = logging.getLogger('kira_bot')
    return logger

def setup_advanced_logging():
    """Configure le système de logging avancé"""
    try:
        from tools.advanced_logging import init_advanced_logging
        
        # Chemin de la base de données des logs
        log_db_path = os.path.join(os.path.dirname(__file__), "data", "logs.db")
        log_config_path = os.path.join(os.path.dirname(__file__), "JSON", "log_config.json")
        
        # Initialise le gestionnaire de logs avancé
        log_manager = init_advanced_logging(log_db_path, log_config_path)
        
        return log_manager
    except ImportError:
        print("Module advanced_logging non disponible, utilisation du logging standard")
        return None
    except Exception as e:
        print(f"Erreur initialisation logging avancé: {e}")
        return None

class Config:
    """Classe de configuration centralisée pour le bot Kira"""
    
    def __init__(self):
        # Forcer le rechargement du fichier .env pour éviter les problèmes de cache
        load_dotenv(override=True)
        
        # Variables d'environnement
        self.TOKEN = os.getenv("DISCORD_TOKEN")
        self.AUTH_SECRET = os.getenv("AUTH_SECRET")
        
        # Configuration Discord
        self.AUTHORIZED_ROLE = os.getenv("AUTHORIZED_ROLE", "NeuroMaster")
        
        # Chemins des fichiers de configuration
        self.base_dir = os.path.dirname(__file__)
        self.json_dir = os.path.join(self.base_dir, "JSON")
        self.models_dir = os.path.join(self.base_dir, "models")
        self.data_dir = os.getenv("DATA_DIR", os.path.join(self.base_dir, "data"))
        
        # Créer les dossiers nécessaires
        os.makedirs(self.json_dir, exist_ok=True)
        os.makedirs(self.models_dir, exist_ok=True)
        os.makedirs(self.data_dir, exist_ok=True)
        
        # Fichiers JSON
        self.LIMITS_FILE = os.path.join(self.json_dir, "character_limits.json")
        self.WEB_STATE_FILE = os.path.join(self.json_dir, "web.json")
        self.CONFIG_PATH = os.path.join(self.json_dir, "context.json")
        self.AUTO_REPLY_PATH = os.path.join(self.json_dir, "autoreply.json")
        
        # Base de données (portable)
        self.DB_PATH = os.getenv("DB_PATH", os.path.join(self.data_dir, "neuro.db"))
        
        # Modèle par défaut (configurable)
        default_model = "zephyr-7b-beta.Q5_K_M.gguf"
        self.MODEL_PATH = os.getenv("MODEL_PATH", 
                                   os.path.join(self.models_dir, default_model))
        
        # Configuration LLM déplacée vers model.py pour gestion automatique
        # Les profils sont maintenant gérés automatiquement selon la VRAM disponible
        
        # Validation des variables critiques
        self._validate_config()
    
    def _validate_config(self):
        """Valide la configuration et lève des erreurs si nécessaire"""
        if not self.TOKEN:
            raise ValueError("DISCORD_TOKEN manquant dans les variables d'environnement")
        
        if not self.AUTH_SECRET:
            raise ValueError("AUTH_SECRET manquant dans les variables d'environnement")
        
        if not os.path.exists(self.MODEL_PATH):
            raise FileNotFoundError(f"Modèle non trouvé : {self.MODEL_PATH}")

# Instance globale de configuration
config = Config()

# Variables pour compatibilité avec l'ancien code
TOKEN = config.TOKEN
AUTH_SECRET = config.AUTH_SECRET
AUTHORIZED_ROLE = config.AUTHORIZED_ROLE
LIMITS_FILE = config.LIMITS_FILE
WEB_STATE_FILE = config.WEB_STATE_FILE
CONFIG_PATH = config.CONFIG_PATH
AUTO_REPLY_PATH = config.AUTO_REPLY_PATH
DB_PATH = config.DB_PATH
MODEL_PATH = config.MODEL_PATH

# Logger global
logger = setup_logging()

# Gestionnaire de logs avancé (optionnel)
advanced_log_manager = setup_advanced_logging()