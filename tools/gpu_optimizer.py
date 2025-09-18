#!/usr/bin/env python3
"""
Optimiseur GPU Avancé pour Kira-Bot
Optimise automatiquement les performances GPU et gère les profils adaptatifs
"""

import os
import sys
import time
import json
import threading
from pathlib import Path
from dataclasses import dataclass
from typing import Dict, List, Optional, Tuple, Any
from datetime import datetime, timedelta
from config import logger

try:
    import pynvml
    NVIDIA_AVAILABLE = True
except ImportError:
    NVIDIA_AVAILABLE = False
    logger.warning("pynvml non disponible - fonctionnalités GPU limitées")

try:
    import psutil
    PSUTIL_AVAILABLE = True
except ImportError:
    PSUTIL_AVAILABLE = False
    logger.warning("psutil non disponible - monitoring système limité")

@dataclass
class GPUMetrics:
    """Métriques GPU pour l'optimisation"""
    name: str
    vram_total_mb: int
    vram_used_mb: int
    vram_free_mb: int
    usage_percent: float
    temperature_c: int
    power_usage_w: int
    clock_graphics_mhz: int
    clock_memory_mhz: int
    utilization_gpu: int
    utilization_memory: int
    timestamp: datetime

@dataclass
class SystemMetrics:
    """Métriques système pour l'optimisation globale"""
    cpu_percent: float
    ram_percent: float
    ram_available_gb: float
    cpu_temp_c: Optional[float]
    timestamp: datetime

@dataclass
class PerformanceProfile:
    """Profil de performance avancé avec métriques d'optimisation"""
    name: str
    description: str
    n_gpu_layers: int
    n_threads: int
    n_ctx: int
    n_batch: int
    flash_attn: bool
    offload_kqv: bool
    use_mmap: bool
    use_mlock: bool
    numa: bool
    verbose: bool
    # Conditions d'activation
    min_vram_free_mb: int
    min_vram_total_mb: int
    max_temperature_c: int
    max_power_usage_w: int
    # Optimisations spéciales
    tensor_split: Optional[List[float]]
    rope_scaling_factor: float
    rope_freq_base: float
    # Métriques cibles
    target_tokens_per_sec: float
    target_vram_usage_percent: float

class GPUOptimizer:
    """Optimiseur GPU avancé avec profils adaptatifs et monitoring en temps réel"""
    
    def __init__(self):
        self.gpu_handle = None
        self.monitoring_active = False
        self.metrics_history: List[GPUMetrics] = []
        self.system_metrics_history: List[SystemMetrics] = []
        self.current_metrics: Optional[GPUMetrics] = None
        self.current_system_metrics: Optional[SystemMetrics] = None
        self.performance_data = {}
        self.auto_optimization_enabled = True
        self.monitoring_thread = None
        
        # Profils de performance optimisés pour RTX 4050 6GB
        self.performance_profiles = self._create_optimized_profiles()
        
        # Initialiser le monitoring GPU
        self._init_gpu_monitoring()
        
        # Démarrer le monitoring automatique
        self.start_monitoring()
    
    def _create_optimized_profiles(self) -> Dict[str, PerformanceProfile]:
        """Crée les profils de performance optimisés"""
        return {
            'turbo_max': PerformanceProfile(
                name='Turbo Maximum',
                description='Performance maximale avec toutes les optimisations RTX 4050 6GB',
                n_gpu_layers=-1,  # Tous les layers sur GPU
                n_threads=6,
                n_ctx=16384,  # Contexte étendu
                n_batch=1024,  # Batch size maximale pour RTX 4050
                flash_attn=True,
                offload_kqv=True,
                use_mmap=True,
                use_mlock=True,
                numa=False,  # Pas de NUMA sur desktop
                verbose=False,
                min_vram_free_mb=3000,
                min_vram_total_mb=5500,
                max_temperature_c=83,
                max_power_usage_w=115,
                tensor_split=None,
                rope_scaling_factor=1.0,
                rope_freq_base=10000.0,
                target_tokens_per_sec=25.0,
                target_vram_usage_percent=75.0
            ),
            'performance_optimized': PerformanceProfile(
                name='Performance Optimisée',
                description='Équilibre optimal performance/stabilité pour RTX 4050',
                n_gpu_layers=35,
                n_threads=6,
                n_ctx=12288,
                n_batch=512,
                flash_attn=True,
                offload_kqv=True,
                use_mmap=True,
                use_mlock=True,
                numa=False,
                verbose=False,
                min_vram_free_mb=2000,
                min_vram_total_mb=5000,
                max_temperature_c=80,
                max_power_usage_w=110,
                tensor_split=None,
                rope_scaling_factor=1.0,
                rope_freq_base=10000.0,
                target_tokens_per_sec=20.0,
                target_vram_usage_percent=70.0
            ),
            'stable_high': PerformanceProfile(
                name='Stable Haute Performance',
                description='Performance élevée avec priorité à la stabilité',
                n_gpu_layers=30,
                n_threads=6,
                n_ctx=10240,
                n_batch=256,
                flash_attn=True,
                offload_kqv=True,
                use_mmap=True,
                use_mlock=False,
                numa=False,
                verbose=False,
                min_vram_free_mb=1500,
                min_vram_total_mb=4500,
                max_temperature_c=78,
                max_power_usage_w=105,
                tensor_split=None,
                rope_scaling_factor=1.0,
                rope_freq_base=10000.0,
                target_tokens_per_sec=18.0,
                target_vram_usage_percent=65.0
            ),
            'balanced_adaptive': PerformanceProfile(
                name='Équilibré Adaptatif',
                description='Configuration équilibrée avec adaptation automatique',
                n_gpu_layers=25,
                n_threads=6,
                n_ctx=8192,
                n_batch=128,
                flash_attn=False,
                offload_kqv=True,
                use_mmap=True,
                use_mlock=False,
                numa=False,
                verbose=False,
                min_vram_free_mb=1000,
                min_vram_total_mb=4000,
                max_temperature_c=75,
                max_power_usage_w=100,
                tensor_split=None,
                rope_scaling_factor=1.0,
                rope_freq_base=10000.0,
                target_tokens_per_sec=15.0,
                target_vram_usage_percent=60.0
            ),
            'conservative_stable': PerformanceProfile(
                name='Conservateur Stable',
                description='Configuration conservatrice pour utilisation prolongée',
                n_gpu_layers=20,
                n_threads=8,  # Plus de threads CPU
                n_ctx=6144,
                n_batch=64,
                flash_attn=False,
                offload_kqv=False,
                use_mmap=True,
                use_mlock=False,
                numa=False,
                verbose=False,
                min_vram_free_mb=500,
                min_vram_total_mb=3000,
                max_temperature_c=70,
                max_power_usage_w=95,
                tensor_split=None,
                rope_scaling_factor=1.0,
                rope_freq_base=10000.0,
                target_tokens_per_sec=12.0,
                target_vram_usage_percent=50.0
            ),
            'emergency_safe': PerformanceProfile(
                name='Sécurité d\'Urgence',
                description='Configuration minimale de sécurité',
                n_gpu_layers=10,
                n_threads=8,
                n_ctx=4096,
                n_batch=32,
                flash_attn=False,
                offload_kqv=False,
                use_mmap=False,
                use_mlock=False,
                numa=False,
                verbose=False,
                min_vram_free_mb=0,
                min_vram_total_mb=2000,
                max_temperature_c=90,
                max_power_usage_w=120,
                tensor_split=None,
                rope_scaling_factor=1.0,
                rope_freq_base=10000.0,
                target_tokens_per_sec=8.0,
                target_vram_usage_percent=40.0
            ),
            'cpu_fallback': PerformanceProfile(
                name='Fallback CPU',
                description='Utilisation CPU uniquement en cas de problème GPU',
                n_gpu_layers=0,
                n_threads=12,  # Maximum threads CPU
                n_ctx=4096,
                n_batch=16,
                flash_attn=False,
                offload_kqv=False,
                use_mmap=True,
                use_mlock=False,
                numa=False,
                verbose=False,
                min_vram_free_mb=0,
                min_vram_total_mb=0,
                max_temperature_c=95,
                max_power_usage_w=150,
                tensor_split=None,
                rope_scaling_factor=1.0,
                rope_freq_base=10000.0,
                target_tokens_per_sec=3.0,
                target_vram_usage_percent=0.0
            )
        }
    
    def _init_gpu_monitoring(self):
        """Initialise le monitoring GPU"""
        if not NVIDIA_AVAILABLE:
            logger.warning("GPU monitoring indisponible - NVIDIA GPU non détectée")
            return
        
        try:
            pynvml.nvmlInit()
            self.gpu_handle = pynvml.nvmlDeviceGetHandleByIndex(0)
            logger.info("GPU monitoring initialisé avec succès")
        except Exception as e:
            logger.error(f"Erreur initialisation GPU monitoring: {e}")
            self.gpu_handle = None
    
    def get_gpu_metrics(self) -> Optional[GPUMetrics]:
        """Récupère les métriques GPU détaillées"""
        if not self.gpu_handle:
            return None
        
        try:
            # Informations mémoire
            mem_info = pynvml.nvmlDeviceGetMemoryInfo(self.gpu_handle)
            
            # Informations GPU
            gpu_name = pynvml.nvmlDeviceGetName(self.gpu_handle)
            if isinstance(gpu_name, bytes):
                gpu_name = gpu_name.decode()
            
            # Température
            try:
                temperature = pynvml.nvmlDeviceGetTemperature(self.gpu_handle, pynvml.NVML_TEMPERATURE_GPU)
            except:
                temperature = 0
            
            # Consommation électrique
            try:
                power_usage = pynvml.nvmlDeviceGetPowerUsage(self.gpu_handle) // 1000  # mW -> W
            except:
                power_usage = 0
            
            # Fréquences
            try:
                clock_info = pynvml.nvmlDeviceGetClockInfo(self.gpu_handle, pynvml.NVML_CLOCK_GRAPHICS)
                memory_clock = pynvml.nvmlDeviceGetClockInfo(self.gpu_handle, pynvml.NVML_CLOCK_MEM)
            except:
                clock_info = 0
                memory_clock = 0
            
            # Utilisation
            try:
                utilization = pynvml.nvmlDeviceGetUtilizationRates(self.gpu_handle)
                gpu_util = utilization.gpu
                mem_util = utilization.memory
            except:
                gpu_util = 0
                mem_util = 0
            
            return GPUMetrics(
                name=gpu_name,
                vram_total_mb=int(mem_info.total) // (1024**2),
                vram_used_mb=int(mem_info.used) // (1024**2),
                vram_free_mb=int(mem_info.free) // (1024**2),
                usage_percent=(int(mem_info.used) / int(mem_info.total)) * 100,
                temperature_c=temperature,
                power_usage_w=power_usage,
                clock_graphics_mhz=clock_info,
                clock_memory_mhz=memory_clock,
                utilization_gpu=int(gpu_util),
                utilization_memory=int(mem_util),
                timestamp=datetime.now()
            )
            
        except Exception as e:
            logger.error(f"Erreur récupération métriques GPU: {e}")
            return None
    
    def get_system_metrics(self) -> Optional[SystemMetrics]:
        """Récupère les métriques système"""
        if not PSUTIL_AVAILABLE:
            return None
        
        try:
            cpu_percent = psutil.cpu_percent(interval=0.1)
            memory = psutil.virtual_memory()
            
            # Température CPU si disponible
            cpu_temp = None
            try:
                sensors_temperatures = getattr(psutil, 'sensors_temperatures', None)
                if sensors_temperatures:
                    temps = sensors_temperatures()
                    if 'coretemp' in temps:
                        cpu_temp = max(temp.current for temp in temps['coretemp'])
            except:
                pass
            
            return SystemMetrics(
                cpu_percent=cpu_percent,
                ram_percent=memory.percent,
                ram_available_gb=memory.available / (1024**3),
                cpu_temp_c=cpu_temp,
                timestamp=datetime.now()
            )
            
        except Exception as e:
            logger.error(f"Erreur récupération métriques système: {e}")
            return None
    
    def start_monitoring(self, interval: float = 5.0):
        """Démarre le monitoring en arrière-plan"""
        if self.monitoring_active:
            return
        
        self.monitoring_active = True
        self.monitoring_thread = threading.Thread(
            target=self._monitoring_loop, 
            args=(interval,), 
            daemon=True
        )
        self.monitoring_thread.start()
        logger.info(f"Monitoring GPU démarré (intervalle: {interval}s)")
    
    def stop_monitoring(self):
        """Arrête le monitoring"""
        self.monitoring_active = False
        if self.monitoring_thread:
            self.monitoring_thread.join(timeout=10)
        logger.info("Monitoring GPU arrêté")
    
    def _monitoring_loop(self, interval: float):
        """Boucle principale de monitoring"""
        while self.monitoring_active:
            try:
                # Récupérer les métriques
                gpu_metrics = self.get_gpu_metrics()
                system_metrics = self.get_system_metrics()
                
                # Limiter l'historique (dernières 24h avec échantillon toutes les 5s)
                max_history = int(24 * 3600 / interval)
                
                if gpu_metrics:
                    self.current_metrics = gpu_metrics
                    self.metrics_history.append(gpu_metrics)
                    
                    if len(self.metrics_history) > max_history:
                        self.metrics_history = self.metrics_history[-max_history:]
                
                if system_metrics:
                    self.current_system_metrics = system_metrics
                    self.system_metrics_history.append(system_metrics)
                    
                    # Limiter l'historique système
                    if len(self.system_metrics_history) > max_history:
                        self.system_metrics_history = self.system_metrics_history[-max_history:]
                
                # Optimisation automatique si activée
                if self.auto_optimization_enabled and gpu_metrics:
                    self._check_auto_optimization(gpu_metrics, system_metrics)
                
                time.sleep(interval)
                
            except Exception as e:
                logger.error(f"Erreur dans la boucle de monitoring: {e}")
                time.sleep(interval)
    
    def _check_auto_optimization(self, gpu_metrics: GPUMetrics, system_metrics: Optional[SystemMetrics]):
        """Vérifie si une optimisation automatique est nécessaire"""
        try:
            # Vérification température critique
            if gpu_metrics.temperature_c > 85:
                logger.warning(f"Température GPU critique: {gpu_metrics.temperature_c}°C")
                self._apply_emergency_cooling()
                return
            
            # Vérification utilisation VRAM critique
            if gpu_metrics.usage_percent > 95:
                logger.warning(f"VRAM critique: {gpu_metrics.usage_percent:.1f}%")
                self._reduce_vram_usage()
                return
            
            # Optimisation proactive si conditions favorables
            if (gpu_metrics.temperature_c < 70 and 
                gpu_metrics.usage_percent < 60 and 
                system_metrics and system_metrics.cpu_percent < 50):
                self._consider_performance_boost()
                
        except Exception as e:
            logger.error(f"Erreur optimisation automatique: {e}")
    
    def _apply_emergency_cooling(self):
        """Applique des mesures d'urgence pour le refroidissement"""
        # Cette méthode sera appelée par le système de gestion des modèles
        logger.warning("Application des mesures de refroidissement d'urgence")
        # Signaler qu'il faut passer à un profil plus conservateur
        
    def _reduce_vram_usage(self):
        """Réduit l'utilisation de la VRAM"""
        logger.warning("Réduction de l'utilisation VRAM")
        # Signaler qu'il faut réduire les paramètres
    
    def _consider_performance_boost(self):
        """Considère une augmentation des performances"""
        logger.info("Conditions favorables détectées - considération boost performance")
        # Signaler qu'on peut augmenter les performances
    
    def select_optimal_profile(self) -> str:
        """Sélectionne automatiquement le profil optimal"""
        if not self.current_metrics:
            logger.warning("Pas de métriques GPU - sélection profil par défaut")
            return 'balanced_adaptive'
        
        metrics = self.current_metrics
        
        # Profil de sélection basé sur les métriques actuelles
        try:
            # Vérifications de sécurité en premier
            if (metrics.temperature_c > 80 or 
                metrics.usage_percent > 90 or 
                metrics.power_usage_w > 110):
                return 'conservative_stable'
            
            # Sélection performance basée sur VRAM disponible
            if metrics.vram_free_mb >= 3000:
                if metrics.temperature_c < 75:
                    return 'turbo_max'
                else:
                    return 'performance_optimized'
            
            elif metrics.vram_free_mb >= 2000:
                return 'stable_high'
            
            elif metrics.vram_free_mb >= 1000:
                return 'balanced_adaptive'
            
            else:
                return 'conservative_stable'
                
        except Exception as e:
            logger.error(f"Erreur sélection profil optimal: {e}")
            return 'balanced_adaptive'
    
    def get_profile_config(self, profile_name: str) -> Dict[str, Any]:
        """Convertit un profil de performance en configuration LLM"""
        if profile_name not in self.performance_profiles:
            raise ValueError(f"Profil inconnu: {profile_name}")
        
        profile = self.performance_profiles[profile_name]
        
        config = {
            'n_gpu_layers': profile.n_gpu_layers,
            'n_threads': profile.n_threads,
            'n_ctx': profile.n_ctx,
            'n_batch': profile.n_batch,
            'verbose': profile.verbose,
            'use_mmap': profile.use_mmap,
            'use_mlock': profile.use_mlock,
            'numa': profile.numa
        }
        
        # Ajouter les optimisations spéciales si disponibles
        if profile.flash_attn:
            config['flash_attn'] = True
        
        if profile.offload_kqv:
            config['offload_kqv'] = True
        
        if profile.tensor_split:
            config['tensor_split'] = profile.tensor_split
        
        if profile.rope_scaling_factor != 1.0:
            config['rope_scaling_factor'] = profile.rope_scaling_factor
            
        if profile.rope_freq_base != 10000.0:
            config['rope_freq_base'] = profile.rope_freq_base
        
        return config
    
    def get_optimization_report(self) -> Dict[str, Any]:
        """Génère un rapport d'optimisation détaillé"""
        if not self.current_metrics:
            return {"error": "Aucune métrique GPU disponible"}
        
        metrics = self.current_metrics
        optimal_profile = self.select_optimal_profile()
        
        # Analyse des performances récentes
        recent_metrics = self.metrics_history[-60:] if len(self.metrics_history) >= 60 else self.metrics_history
        
        avg_temp = sum(m.temperature_c for m in recent_metrics) / len(recent_metrics) if recent_metrics else 0
        avg_vram_usage = sum(m.usage_percent for m in recent_metrics) / len(recent_metrics) if recent_metrics else 0
        avg_gpu_util = sum(m.utilization_gpu for m in recent_metrics) / len(recent_metrics) if recent_metrics else 0
        
        return {
            "timestamp": datetime.now().isoformat(),
            "current_metrics": {
                "gpu_name": metrics.name,
                "vram_usage": f"{metrics.vram_used_mb} MB / {metrics.vram_total_mb} MB ({metrics.usage_percent:.1f}%)",
                "temperature": f"{metrics.temperature_c}°C",
                "power_usage": f"{metrics.power_usage_w}W",
                "gpu_utilization": f"{metrics.utilization_gpu}%",
                "memory_utilization": f"{metrics.utilization_memory}%"
            },
            "averages_last_5min": {
                "temperature": f"{avg_temp:.1f}°C",
                "vram_usage": f"{avg_vram_usage:.1f}%",
                "gpu_utilization": f"{avg_gpu_util:.1f}%"
            },
            "optimal_profile": {
                "name": optimal_profile,
                "description": self.performance_profiles[optimal_profile].description,
                "config": self.get_profile_config(optimal_profile)
            },
            "recommendations": self._generate_recommendations(metrics),
            "monitoring_status": {
                "active": self.monitoring_active,
                "auto_optimization": self.auto_optimization_enabled,
                "metrics_collected": len(self.metrics_history)
            }
        }
    
    def _generate_recommendations(self, metrics: GPUMetrics) -> List[str]:
        """Génère des recommandations d'optimisation"""
        recommendations = []
        
        if metrics.temperature_c > 80:
            recommendations.append("🌡️ Température élevée - réduire les paramètres ou améliorer refroidissement")
        
        if metrics.usage_percent > 90:
            recommendations.append("💾 VRAM proche saturation - réduire n_ctx ou n_batch")
        
        if metrics.utilization_gpu < 50:
            recommendations.append("⚡ GPU sous-utilisé - augmenter n_gpu_layers ou n_batch")
        
        if metrics.power_usage_w > 100:
            recommendations.append("🔋 Consommation élevée - surveiller la stabilité")
        
        if metrics.vram_free_mb > 2000 and metrics.temperature_c < 70:
            recommendations.append("🚀 Conditions optimales - possibilité d'augmenter les performances")
        
        return recommendations or ["✅ Configuration actuelle optimale"]

# Instance globale de l'optimiseur
gpu_optimizer = GPUOptimizer()