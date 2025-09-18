"""
Module central de gestion GPU/NVML
Centralise toutes les fonctionnalités liées au GPU pour éviter la duplication de code
"""

import os
import sys
from typing import Optional, Dict, Any, NamedTuple
from dataclasses import dataclass
from datetime import datetime

# Configuration du logging
from config import logger

# Configuration du PATH NVML pour Windows
def _setup_nvml_path():
    """Configure le PATH pour permettre l'importation de pynvml sur Windows"""
    nvml_paths = [
        r"C:\Program Files\NVIDIA Corporation\NVSMI",
        r"C:\Windows\System32",
    ]
    
    for path in nvml_paths:
        if os.path.isdir(path) and path not in os.environ.get("PATH", ""):
            os.environ["PATH"] += os.pathsep + path

# Initialisation du PATH avant l'import
_setup_nvml_path()

# Import conditionnel de pynvml
try:
    import pynvml
    NVIDIA_AVAILABLE = True
    logger.info("Module pynvml importé avec succès")
except ImportError as e:
    NVIDIA_AVAILABLE = False
    logger.warning(f"pynvml non disponible: {e}")
    # Module factice pour éviter les erreurs de typage
    class MockPynvml:
        def __getattr__(self, name):
            def mock_function(*args, **kwargs):
                raise RuntimeError("pynvml non disponible")
            return mock_function
    pynvml = MockPynvml()

@dataclass
class GPUInfo:
    """Informations sur le GPU"""
    name: str
    vram_total_mb: int
    vram_used_mb: int
    vram_free_mb: int
    vram_usage_percent: float
    temperature_c: int
    utilization_gpu: int
    utilization_memory: int
    power_usage_w: int = 0
    clock_graphics_mhz: int = 0
    clock_memory_mhz: int = 0

class GPUManager:
    """Gestionnaire centralisé pour toutes les opérations GPU"""
    
    def __init__(self):
        self.initialized = False
        self.gpu_handle = None
        self._init_gpu()
    
    def _init_gpu(self):
        """Initialise la connexion GPU"""
        if not NVIDIA_AVAILABLE:
            logger.warning("GPU NVIDIA non disponible - fonctionnalités limitées")
            return
        
        try:
            pynvml.nvmlInit()
            self.gpu_handle = pynvml.nvmlDeviceGetHandleByIndex(0)
            self.initialized = True
            logger.info("GPU monitoring initialisé avec succès")
        except Exception as e:
            logger.error(f"Erreur initialisation GPU: {e}")
            self.initialized = False
    
    def is_available(self) -> bool:
        """Vérifie si le GPU est disponible"""
        return NVIDIA_AVAILABLE and self.initialized
    
    def get_gpu_info(self) -> Optional[GPUInfo]:
        """Récupère les informations détaillées du GPU"""
        if not self.is_available():
            return None
        
        try:
            # Informations de base
            gpu_name = pynvml.nvmlDeviceGetName(self.gpu_handle)
            if isinstance(gpu_name, bytes):
                gpu_name = gpu_name.decode()
            
            # Mémoire
            mem_info = pynvml.nvmlDeviceGetMemoryInfo(self.gpu_handle)
            vram_total_mb = int(mem_info.total) // (1024**2)
            vram_used_mb = int(mem_info.used) // (1024**2)
            vram_free_mb = int(mem_info.free) // (1024**2)
            vram_usage_percent = (vram_used_mb / vram_total_mb) * 100
            
            # Utilisation
            try:
                utilization = pynvml.nvmlDeviceGetUtilizationRates(self.gpu_handle)
                gpu_util = utilization.gpu
                mem_util = utilization.memory
            except:
                gpu_util = 0
                mem_util = 0
            
            # Température
            try:
                temperature = pynvml.nvmlDeviceGetTemperature(self.gpu_handle, pynvml.NVML_TEMPERATURE_GPU)
            except:
                temperature = 0
            
            # Consommation électrique (optionnel)
            try:
                power_usage = pynvml.nvmlDeviceGetPowerUsage(self.gpu_handle) // 1000  # mW -> W
            except:
                power_usage = 0
            
            # Fréquences (optionnel)
            try:
                clock_graphics = pynvml.nvmlDeviceGetClockInfo(self.gpu_handle, pynvml.NVML_CLOCK_GRAPHICS)
                clock_memory = pynvml.nvmlDeviceGetClockInfo(self.gpu_handle, pynvml.NVML_CLOCK_MEM)
            except:
                clock_graphics = 0
                clock_memory = 0
            
            return GPUInfo(
                name=gpu_name,
                vram_total_mb=vram_total_mb,
                vram_used_mb=vram_used_mb,
                vram_free_mb=vram_free_mb,
                vram_usage_percent=vram_usage_percent,
                temperature_c=temperature,
                utilization_gpu=int(gpu_util),
                utilization_memory=int(mem_util),
                power_usage_w=power_usage,
                clock_graphics_mhz=clock_graphics,
                clock_memory_mhz=clock_memory
            )
            
        except Exception as e:
            logger.error(f"Erreur récupération info GPU: {e}")
            return None
    
    def get_vram_info(self) -> Optional[Dict[str, int]]:
        """Récupère uniquement les informations VRAM (optimisé pour les appels fréquents)"""
        if not self.is_available():
            return None
        
        try:
            mem_info = pynvml.nvmlDeviceGetMemoryInfo(self.gpu_handle)
            return {
                'total_mb': int(mem_info.total) // (1024**2),
                'used_mb': int(mem_info.used) // (1024**2),
                'free_mb': int(mem_info.free) // (1024**2),
                'usage_percent': int((int(mem_info.used) / int(mem_info.total)) * 100)
            }
        except Exception as e:
            logger.error(f"Erreur récupération VRAM: {e}")
            return None
    
    def get_temperature(self) -> Optional[int]:
        """Récupère la température GPU"""
        if not self.is_available():
            return None
        
        try:
            return pynvml.nvmlDeviceGetTemperature(self.gpu_handle, pynvml.NVML_TEMPERATURE_GPU)
        except Exception as e:
            logger.error(f"Erreur récupération température: {e}")
            return None
    
    def get_utilization(self) -> Optional[Dict[str, int]]:
        """Récupère l'utilisation GPU et mémoire"""
        if not self.is_available():
            return None
        
        try:
            utilization = pynvml.nvmlDeviceGetUtilizationRates(self.gpu_handle)
            return {
                'gpu': int(utilization.gpu),
                'memory': int(utilization.memory)
            }
        except Exception as e:
            logger.error(f"Erreur récupération utilisation: {e}")
            return None
    
    def shutdown(self):
        """Ferme proprement la connexion GPU"""
        if self.initialized and NVIDIA_AVAILABLE:
            try:
                pynvml.nvmlShutdown()
                logger.info("GPU monitoring fermé proprement")
            except:
                pass
            finally:
                self.initialized = False

# Instance globale du gestionnaire GPU
gpu_manager = GPUManager()

# Fonctions de convenance pour compatibilité avec l'ancien code
def is_gpu_available() -> bool:
    """Vérifie si le GPU est disponible"""
    return gpu_manager.is_available()

def get_gpu_info() -> Optional[GPUInfo]:
    """Récupère les informations GPU"""
    return gpu_manager.get_gpu_info()

def get_vram_info() -> Optional[Dict[str, int]]:
    """Récupère les informations VRAM"""
    return gpu_manager.get_vram_info()

def get_gpu_temperature() -> Optional[int]:
    """Récupère la température GPU"""
    return gpu_manager.get_temperature()

def get_gpu_utilization() -> Optional[Dict[str, int]]:
    """Récupère l'utilisation GPU"""
    return gpu_manager.get_utilization()

# Fonctions d'initialisation/nettoyage pour compatibilité
def init_nvml():
    """Initialise NVML (pour compatibilité)"""
    return gpu_manager.is_available()

def shutdown_nvml():
    """Ferme NVML (pour compatibilité)"""
    gpu_manager.shutdown()

# Export des classes et fonctions principales
__all__ = [
    'GPUInfo',
    'GPUManager', 
    'gpu_manager',
    'is_gpu_available',
    'get_gpu_info',
    'get_vram_info', 
    'get_gpu_temperature',
    'get_gpu_utilization',
    'init_nvml',
    'shutdown_nvml',
    'NVIDIA_AVAILABLE'
]