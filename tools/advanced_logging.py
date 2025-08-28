"""
Module de logging avancé pour Neuro-Bot
Fournit un système de logs structuré avec interface graphique
"""

import os
import json
import logging
import sqlite3
from datetime import datetime, timedelta
from typing import List, Dict, Optional, Callable
from dataclasses import dataclass
from enum import Enum
import threading
from queue import Queue, Empty

class LogLevel(Enum):
    """Niveaux de log avec couleurs associées"""
    DEBUG = ("DEBUG", "#6c757d")
    INFO = ("INFO", "#17a2b8") 
    WARNING = ("WARNING", "#ffc107")
    ERROR = ("ERROR", "#dc3545")
    CRITICAL = ("CRITICAL", "#6f42c1")

@dataclass
class LogEntry:
    """Structure d'une entrée de log"""
    timestamp: datetime
    level: LogLevel
    logger_name: str
    message: str
    module: str = ""
    function: str = ""
    line_number: int = 0
    thread_id: int = 0
    user_id: Optional[str] = None
    session_id: Optional[str] = None

class LogDatabase:
    """Gestionnaire de base de données pour les logs"""
    
    def __init__(self, db_path: str):
        self.db_path = db_path
        self.init_database()
    
    def init_database(self):
        """Initialise la base de données des logs"""
        try:
            with sqlite3.connect(self.db_path) as conn:
                conn.execute("""
                    CREATE TABLE IF NOT EXISTS logs (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        timestamp TEXT NOT NULL,
                        level TEXT NOT NULL,
                        logger_name TEXT NOT NULL,
                        message TEXT NOT NULL,
                        module TEXT,
                        function TEXT,
                        line_number INTEGER,
                        thread_id INTEGER,
                        user_id TEXT,
                        session_id TEXT,
                        created_at DATETIME DEFAULT CURRENT_TIMESTAMP
                    )
                """)
                
                # Index pour améliorer les performances
                conn.execute("CREATE INDEX IF NOT EXISTS idx_logs_timestamp ON logs(timestamp)")
                conn.execute("CREATE INDEX IF NOT EXISTS idx_logs_level ON logs(level)")
                conn.execute("CREATE INDEX IF NOT EXISTS idx_logs_logger ON logs(logger_name)")
                conn.execute("CREATE INDEX IF NOT EXISTS idx_logs_user ON logs(user_id)")
                
                conn.commit()
        except Exception as e:
            print(f"Erreur initialisation base logs: {e}")
    
    def add_log(self, entry: LogEntry):
        """Ajoute une entrée de log à la base"""
        try:
            with sqlite3.connect(self.db_path) as conn:
                conn.execute("""
                    INSERT INTO logs (timestamp, level, logger_name, message, module, 
                                    function, line_number, thread_id, user_id, session_id)
                    VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                """, (
                    entry.timestamp.isoformat(),
                    entry.level.value[0],
                    entry.logger_name,
                    entry.message,
                    entry.module,
                    entry.function,
                    entry.line_number,
                    entry.thread_id,
                    entry.user_id,
                    entry.session_id
                ))
                conn.commit()
        except Exception as e:
            print(f"Erreur ajout log: {e}")
    
    def get_logs(self, 
                 limit: int = 1000,
                 level_filter: Optional[List[str]] = None,
                 search_term: Optional[str] = None,
                 start_date: Optional[datetime] = None,
                 end_date: Optional[datetime] = None,
                 logger_filter: Optional[str] = None) -> List[LogEntry]:
        """Récupère les logs avec filtres"""
        try:
            query = "SELECT * FROM logs WHERE 1=1"
            params = []
            
            if level_filter:
                placeholders = ','.join(['?' for _ in level_filter])
                query += f" AND level IN ({placeholders})"
                params.extend(level_filter)
            
            if search_term:
                query += " AND message LIKE ?"
                params.append(f"%{search_term}%")
            
            if start_date:
                query += " AND timestamp >= ?"
                params.append(start_date.isoformat())
            
            if end_date:
                query += " AND timestamp <= ?"
                params.append(end_date.isoformat())
            
            if logger_filter:
                query += " AND logger_name = ?"
                params.append(logger_filter)
            
            query += " ORDER BY timestamp DESC LIMIT ?"
            params.append(limit)
            
            with sqlite3.connect(self.db_path) as conn:
                cursor = conn.execute(query, params)
                rows = cursor.fetchall()
                
                logs = []
                for row in rows:
                    # Trouve le niveau correspondant
                    level = LogLevel.INFO  # défaut
                    for log_level in LogLevel:
                        if log_level.value[0] == row[2]:
                            level = log_level
                            break
                    
                    logs.append(LogEntry(
                        timestamp=datetime.fromisoformat(row[1]),
                        level=level,
                        logger_name=row[3],
                        message=row[4],
                        module=row[5] or "",
                        function=row[6] or "",
                        line_number=row[7] or 0,
                        thread_id=row[8] or 0,
                        user_id=row[9],
                        session_id=row[10]
                    ))
                
                return logs
                
        except Exception as e:
            print(f"Erreur récupération logs: {e}")
            return []
    
    def get_log_stats(self, days: int = 7) -> Dict:
        """Récupère les statistiques des logs"""
        try:
            start_date = datetime.now() - timedelta(days=days)
            
            with sqlite3.connect(self.db_path) as conn:
                # Statistiques par niveau
                cursor = conn.execute("""
                    SELECT level, COUNT(*) 
                    FROM logs 
                    WHERE timestamp >= ? 
                    GROUP BY level
                """, (start_date.isoformat(),))
                
                level_stats = dict(cursor.fetchall())
                
                # Statistiques par jour
                cursor = conn.execute("""
                    SELECT DATE(timestamp) as date, COUNT(*) 
                    FROM logs 
                    WHERE timestamp >= ? 
                    GROUP BY DATE(timestamp)
                    ORDER BY date
                """, (start_date.isoformat(),))
                
                daily_stats = dict(cursor.fetchall())
                
                # Top loggers
                cursor = conn.execute("""
                    SELECT logger_name, COUNT(*) 
                    FROM logs 
                    WHERE timestamp >= ? 
                    GROUP BY logger_name
                    ORDER BY COUNT(*) DESC
                    LIMIT 10
                """, (start_date.isoformat(),))
                
                logger_stats = dict(cursor.fetchall())
                
                return {
                    'level_stats': level_stats,
                    'daily_stats': daily_stats,
                    'logger_stats': logger_stats,
                    'total_logs': sum(level_stats.values()),
                    'period_days': days
                }
                
        except Exception as e:
            print(f"Erreur statistiques logs: {e}")
            return {}
    
    def cleanup_old_logs(self, days_to_keep: int = 30):
        """Nettoie les anciens logs"""
        try:
            cutoff_date = datetime.now() - timedelta(days=days_to_keep)
            
            with sqlite3.connect(self.db_path) as conn:
                cursor = conn.execute(
                    """
                    DELETE FROM logs 
                    WHERE timestamp < ?
                    """,
                    (cutoff_date.isoformat(),)
                )
                deleted_count = cursor.rowcount if cursor.rowcount != -1 else conn.total_changes
                conn.commit()
                return deleted_count
        except Exception as e:
            print(f"Erreur nettoyage logs: {e}")
            return 0

    def count_logs_older_than(self, cutoff_iso: str) -> int:
        """Compte le nombre de logs plus vieux qu'une date ISO"""
        try:
            with sqlite3.connect(self.db_path) as conn:
                cur = conn.execute(
                    "SELECT COUNT(*) FROM logs WHERE timestamp < ?",
                    (cutoff_iso,)
                )
                return int(cur.fetchone()[0] or 0)
        except Exception as e:
            print(f"Erreur comptage logs anciens: {e}")
            return 0

    def delete_all_logs(self) -> int:
        """Supprime toutes les entrées de la table des logs et renvoie le nombre supprimé"""
        try:
            with sqlite3.connect(self.db_path) as conn:
                # Compte avant suppression pour un retour fiable
                cur = conn.execute("SELECT COUNT(*) FROM logs")
                total = cur.fetchone()[0] or 0
                conn.execute("DELETE FROM logs")
                conn.commit()
                return total
        except Exception as e:
            print(f"Erreur suppression totale des logs: {e}")
            return 0

class AdvancedLogHandler(logging.Handler):
    """Handler personnalisé pour capturer les logs dans la base"""
    
    def __init__(self, log_db: LogDatabase, gui_callback: Optional[Callable] = None):
        super().__init__()
        self.log_db = log_db
        self.gui_callback = gui_callback
        self.session_id = datetime.now().strftime("%Y%m%d_%H%M%S")
    
    def emit(self, record):
        """Traite un enregistrement de log"""
        try:
            # Détermine le niveau
            level = LogLevel.INFO
            if record.levelno >= logging.CRITICAL:
                level = LogLevel.CRITICAL
            elif record.levelno >= logging.ERROR:
                level = LogLevel.ERROR
            elif record.levelno >= logging.WARNING:
                level = LogLevel.WARNING
            elif record.levelno >= logging.INFO:
                level = LogLevel.INFO
            else:
                level = LogLevel.DEBUG
            
            # Crée l'entrée de log
            entry = LogEntry(
                timestamp=datetime.fromtimestamp(record.created),
                level=level,
                logger_name=record.name,
                message=record.getMessage(),
                module=record.module if hasattr(record, 'module') else "",
                function=record.funcName if hasattr(record, 'funcName') else "",
                line_number=record.lineno if hasattr(record, 'lineno') else 0,
                thread_id=record.thread if hasattr(record, 'thread') else 0,
                user_id=getattr(record, 'user_id', None),
                session_id=self.session_id
            )
            
            # Sauvegarde en base
            self.log_db.add_log(entry)
            
            # Notifie l'interface graphique
            if self.gui_callback:
                self.gui_callback(entry)
                
        except Exception as e:
            print(f"Erreur dans AdvancedLogHandler: {e}")

class LogManager:
    """Gestionnaire principal du système de logs avancé"""
    
    def __init__(self, db_path: str, config_path: str = None):
        self.db_path = db_path
        self.config_path = config_path or os.path.join(os.path.dirname(db_path), "log_config.json")
        
        # Base de données des logs
        self.log_db = LogDatabase(db_path)
        
        # Configuration
        self.config = self.load_config()
        
        # Callbacks pour l'interface graphique
        self.gui_callbacks = []
        
        # Queue pour les notifications
        self.notification_queue = Queue()
        
        # Setup du logging
        self.setup_logging()
    
    def load_config(self) -> Dict:
        """Charge la configuration des logs"""
        default_config = {
            "log_level": "INFO",
            "max_file_size_mb": 10,
            "backup_count": 5,
            "cleanup_days": 30,
            "notifications_enabled": True,
            "notification_levels": ["ERROR", "CRITICAL"],
            "gui_max_entries": 1000,
            "auto_scroll": True,
            "dark_theme": True
        }
        
        try:
            if os.path.exists(self.config_path):
                with open(self.config_path, 'r', encoding='utf-8') as f:
                    config = json.load(f)
                    # Merge avec la config par défaut
                    default_config.update(config)
            else:
                self.save_config(default_config)
        except Exception as e:
            print(f"Erreur chargement config logs: {e}")
        
        return default_config
    
    def save_config(self, config: Dict = None):
        """Sauvegarde la configuration"""
        try:
            config_to_save = config or self.config
            with open(self.config_path, 'w', encoding='utf-8') as f:
                json.dump(config_to_save, f, indent=2, ensure_ascii=False)
        except Exception as e:
            print(f"Erreur sauvegarde config logs: {e}")
    
    def setup_logging(self):
        """Configure le système de logging"""
        # Handler pour la base de données
        db_handler = AdvancedLogHandler(self.log_db, self.notify_gui)
        db_handler.setLevel(getattr(logging, self.config.get("log_level", "INFO")))
        
        # Format des logs
        formatter = logging.Formatter(
            '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
        )
        db_handler.setFormatter(formatter)
        
        # Ajoute le handler au logger racine
        root_logger = logging.getLogger()
        root_logger.addHandler(db_handler)
        
        # Handler pour fichier (rotation)
        from logging.handlers import RotatingFileHandler
        
        log_dir = os.path.dirname(self.db_path)
        log_file = os.path.join(log_dir, "neuro_bot_advanced.log")
        
        file_handler = RotatingFileHandler(
            log_file,
            maxBytes=self.config.get("max_file_size_mb", 10) * 1024 * 1024,
            backupCount=self.config.get("backup_count", 5),
            encoding='utf-8'
        )
        file_handler.setFormatter(formatter)
        file_handler.setLevel(getattr(logging, self.config.get("log_level", "INFO")))
        
        root_logger.addHandler(file_handler)
    
    def notify_gui(self, entry: LogEntry):
        """Notifie l'interface graphique d'une nouvelle entrée"""
        for callback in self.gui_callbacks:
            try:
                callback(entry)
            except Exception as e:
                print(f"Erreur callback GUI: {e}")
        
        # Ajoute à la queue de notifications si nécessaire
        if (self.config.get("notifications_enabled", True) and 
            entry.level.value[0] in self.config.get("notification_levels", ["ERROR", "CRITICAL"])):
            self.notification_queue.put(entry)
    
    def add_gui_callback(self, callback: Callable):
        """Ajoute un callback pour l'interface graphique"""
        self.gui_callbacks.append(callback)
    
    def remove_gui_callback(self, callback: Callable):
        """Supprime un callback"""
        if callback in self.gui_callbacks:
            self.gui_callbacks.remove(callback)
    
    def get_logs(self, **kwargs) -> List[LogEntry]:
        """Récupère les logs avec filtres"""
        return self.log_db.get_logs(**kwargs)
    
    def get_stats(self, days: int = 7) -> Dict:
        """Récupère les statistiques"""
        return self.log_db.get_log_stats(days)
    
    def cleanup_logs(self, days_to_keep: int = None, cutoff_iso: str = None) -> int:
        """Nettoie les anciens logs. Si cutoff_iso est fourni, utilise la date exacte."""
        if cutoff_iso:
            return self.log_db.cleanup_before(cutoff_iso)
        days = days_to_keep or self.config.get("cleanup_days", 30)
        return self.log_db.cleanup_old_logs(days)

    def delete_all_logs(self) -> int:
        """Supprime toutes les entrées des logs"""
        return self.log_db.delete_all_logs()

    def count_logs_older_than(self, cutoff_dt: datetime) -> int:
        """Compte les logs plus vieux que cutoff_dt"""
        return self.log_db.count_logs_older_than(cutoff_dt.isoformat())
    
    def export_logs(self, 
                   filepath: str, 
                   format_type: str = "json",
                   **filter_kwargs) -> bool:
        """Exporte les logs vers un fichier"""
        try:
            logs = self.get_logs(**filter_kwargs)
            
            if format_type.lower() == "json":
                data = []
                for log in logs:
                    data.append({
                        "timestamp": log.timestamp.isoformat(),
                        "level": log.level.value[0],
                        "logger": log.logger_name,
                        "message": log.message,
                        "module": log.module,
                        "function": log.function,
                        "line": log.line_number,
                        "thread": log.thread_id,
                        "user_id": log.user_id,
                        "session_id": log.session_id
                    })
                
                with open(filepath, 'w', encoding='utf-8') as f:
                    json.dump(data, f, indent=2, ensure_ascii=False)
            
            elif format_type.lower() == "csv":
                import csv
                with open(filepath, 'w', newline='', encoding='utf-8') as f:
                    writer = csv.writer(f)
                    writer.writerow([
                        "Timestamp", "Level", "Logger", "Message", 
                        "Module", "Function", "Line", "Thread", "User ID", "Session ID"
                    ])
                    
                    for log in logs:
                        writer.writerow([
                            log.timestamp.isoformat(),
                            log.level.value[0],
                            log.logger_name,
                            log.message,
                            log.module,
                            log.function,
                            log.line_number,
                            log.thread_id,
                            log.user_id or "",
                            log.session_id or ""
                        ])
            
            elif format_type.lower() == "txt":
                with open(filepath, 'w', encoding='utf-8') as f:
                    for log in logs:
                        f.write(f"[{log.timestamp.strftime('%Y-%m-%d %H:%M:%S')}] "
                               f"{log.level.value[0]} - {log.logger_name} - {log.message}\n")
            
            return True
            
        except Exception as e:
            print(f"Erreur export logs: {e}")
            return False

# Instance globale (sera initialisée par config.py)
log_manager: Optional[LogManager] = None

def init_advanced_logging(db_path: str, config_path: str = None) -> LogManager:
    """Initialise le système de logs avancé"""
    global log_manager
    log_manager = LogManager(db_path, config_path)
    return log_manager

def get_log_manager() -> Optional[LogManager]:
    """Récupère l'instance du gestionnaire de logs"""
    return log_manager