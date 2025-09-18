from llama_cpp import Llama
from config import config, logger
from utils import count_tokens, truncate_text_to_tokens, shorten_response
from memory import save_interaction, get_history, get_facts
import time
import os
import sys
import asyncio

# S'assurer que nvml.dll est trouvable (Windows) AVANT d'importer pynvml
try:
    nvml_paths = [
        r"C:\\Program Files\\NVIDIA Corporation\\NVSMI",
        r"C:\\Windows\\System32",
    ]
    for _p in nvml_paths:
        if os.path.isdir(_p) and _p not in os.environ.get("PATH", ""):
            os.environ["PATH"] += os.pathsep + _p
except Exception:
    # Ne bloque pas si on ne peut pas modifier le PATH
    pass

# Import optionnel pour la détection GPU
try:
    import pynvml
    NVIDIA_AVAILABLE = True
except ImportError:
    NVIDIA_AVAILABLE = False


# Import de l'optimiseur GPU avancé
try:
    from tools.gpu_optimizer import gpu_optimizer
    GPU_OPTIMIZER_AVAILABLE = True
except ImportError:
    GPU_OPTIMIZER_AVAILABLE = False
    logger.warning("Optimiseur GPU avancé non disponible - utilisation des profils standards")

# Profils de configuration LLM optimisés - compatibilité avec l'ancien système
LLM_PROFILES = {
    'turbo_max': {
        'name': 'Turbo Maximum',
        'description': 'Performance maximale avec toutes les optimisations RTX 4050 6GB',
        'n_gpu_layers': -1,
        'n_threads': 6,
        'n_ctx': 16384,
        'n_batch': 1024,
        'flash_attn': True,
        'offload_kqv': True,
        'use_mmap': True,
        'use_mlock': True,
        'verbose': False,
        'min_vram_free_mb': 3000
    },
    'performance_optimized': {
        'name': 'Performance Optimisée',
        'description': 'Équilibre optimal performance/stabilité pour RTX 4050',
        'n_gpu_layers': 35,
        'n_threads': 6,
        'n_ctx': 12288,
        'n_batch': 512,
        'flash_attn': True,
        'offload_kqv': True,
        'use_mmap': True,
        'use_mlock': True,
        'verbose': False,
        'min_vram_free_mb': 2000
    },
    'stable_high': {
        'name': 'Stable Haute Performance',
        'description': 'Performance élevée avec priorité à la stabilité',
        'n_gpu_layers': 30,
        'n_threads': 6,
        'n_ctx': 10240,
        'n_batch': 256,
        'flash_attn': True,
        'offload_kqv': True,
        'use_mmap': True,
        'use_mlock': False,
        'verbose': False,
        'min_vram_free_mb': 1500
    },
    'balanced_adaptive': {
        'name': 'Équilibré Adaptatif',
        'description': 'Configuration équilibrée avec adaptation automatique',
        'n_gpu_layers': 25,
        'n_threads': 6,
        'n_ctx': 8192,
        'n_batch': 128,
        'flash_attn': False,
        'offload_kqv': True,
        'use_mmap': True,
        'use_mlock': False,
        'verbose': False,
        'min_vram_free_mb': 1000
    },
    'conservative_stable': {
        'name': 'Conservateur Stable',
        'description': 'Configuration conservatrice pour utilisation prolongée',
        'n_gpu_layers': 20,
        'n_threads': 8,
        'n_ctx': 6144,
        'n_batch': 64,
        'flash_attn': False,
        'offload_kqv': False,
        'use_mmap': True,
        'use_mlock': False,
        'verbose': False,
        'min_vram_free_mb': 500
    },
    'emergency_safe': {
        'name': 'Sécurité d\'Urgence',
        'description': 'Configuration minimale de sécurité',
        'n_gpu_layers': 10,
        'n_threads': 8,
        'n_ctx': 4096,
        'n_batch': 32,
        'flash_attn': False,
        'offload_kqv': False,
        'use_mmap': False,
        'use_mlock': False,
        'verbose': False,
        'min_vram_free_mb': 0
    },
    'cpu_fallback': {
        'name': 'Fallback CPU',
        'description': 'Utilisation CPU uniquement en cas de problème GPU',
        'n_gpu_layers': 0,
        'n_threads': 12,
        'n_ctx': 4096,
        'n_batch': 16,
        'flash_attn': False,
        'offload_kqv': False,
        'use_mmap': True,
        'use_mlock': False,
        'verbose': False,
        'min_vram_free_mb': 0
    },
    # Profils de compatibilité avec l'ancien système
    'performance_max': {
        'name': 'Performance Maximale (Compat)',
        'description': 'Alias vers turbo_max pour compatibilité',
        'n_gpu_layers': -1,
        'n_threads': 6,
        'n_ctx': 16384,
        'n_batch': 1024,
        'verbose': False,
        'min_vram_free_mb': 3000
    },
    'balanced': {
        'name': 'Équilibrée (Compat)',
        'description': 'Alias vers balanced_adaptive pour compatibilité',
        'n_gpu_layers': 25,
        'n_threads': 6,
        'n_ctx': 8192,
        'n_batch': 128,
        'verbose': False,
        'min_vram_free_mb': 1000
    },
    'economical': {
        'name': 'Économique (Compat)',
        'description': 'Alias vers conservative_stable pour compatibilité',
        'n_gpu_layers': 20,
        'n_threads': 8,
        'n_ctx': 6144,
        'n_batch': 64,
        'verbose': False,
        'min_vram_free_mb': 500
    },
    'emergency': {
        'name': 'Secours (Compat)',
        'description': 'Alias vers emergency_safe pour compatibilité',
        'n_gpu_layers': 10,
        'n_threads': 8,
        'n_ctx': 4096,
        'n_batch': 32,
        'verbose': False,
        'min_vram_free_mb': 0
    },
    'cpu_only': {
        'name': 'CPU Uniquement (Compat)',
        'description': 'Alias vers cpu_fallback pour compatibilité',
        'n_gpu_layers': 0,
        'n_threads': 12,
        'n_ctx': 4096,
        'n_batch': 16,
        'verbose': False,
        'min_vram_free_mb': 0
    }
}

class ModelManager:
    """Gestionnaire du modèle LLM avec configuration automatique optimisée"""
    
    def __init__(self):
        self.llm = None
        self.current_profile = None
        self.gpu_info = None
        self._detect_gpu_capabilities()
        self._initialize_model()
    
    def _detect_gpu_capabilities(self):
        """Détecte les capacités GPU et détermine la configuration optimale"""
        if not NVIDIA_AVAILABLE:
            logger.info("GPU NVIDIA non disponible - utilisation CPU uniquement")
            self.current_profile = 'cpu_only'
            return
        
        try:
            pynvml.nvmlInit()
            handle = pynvml.nvmlDeviceGetHandleByIndex(0)
            
            # Informations GPU
            gpu_name = pynvml.nvmlDeviceGetName(handle)
            if isinstance(gpu_name, bytes):
                gpu_name = gpu_name.decode()
            
            mem_info = pynvml.nvmlDeviceGetMemoryInfo(handle)
            vram_total_mb = mem_info.total // (1024**2)
            vram_free_mb = mem_info.free // (1024**2)
            vram_used_mb = mem_info.used // (1024**2)
            
            self.gpu_info = {
                'name': gpu_name,
                'vram_total_mb': vram_total_mb,
                'vram_free_mb': vram_free_mb,
                'vram_used_mb': vram_used_mb,
                'vram_usage_percent': (vram_used_mb / vram_total_mb) * 100
            }
            
            pynvml.nvmlShutdown()
            
            # Sélection automatique du profil optimal
            self.current_profile = self._select_optimal_profile()
            
            logger.info(f"GPU détectée: {gpu_name}")
            logger.info(f"VRAM: {vram_used_mb} MB utilisée / {vram_total_mb} MB total ({vram_free_mb} MB libre)")
            logger.info(f"Profil sélectionné: {LLM_PROFILES[self.current_profile]['name']}")
            
        except Exception as e:
            logger.warning(f"Erreur détection GPU: {e} - utilisation CPU uniquement")
            self.current_profile = 'cpu_only'
    
    def _select_optimal_profile(self):
        """Sélectionne le profil optimal selon la VRAM disponible et l'optimiseur avancé"""
        if not self.gpu_info:
            return 'cpu_fallback'
        
        # Utiliser l'optimiseur GPU avancé si disponible
        if GPU_OPTIMIZER_AVAILABLE:
            try:
                optimal_profile = gpu_optimizer.select_optimal_profile()
                if optimal_profile in LLM_PROFILES:
                    logger.info(f"Profil sélectionné par l'optimiseur avancé: {optimal_profile}")
                    return optimal_profile
                else:
                    logger.warning(f"Profil optimiseur inconnu: {optimal_profile}, fallback vers sélection classique")
            except Exception as e:
                logger.error(f"Erreur optimiseur GPU avancé: {e}, fallback vers sélection classique")
        
        # Sélection classique basée sur VRAM disponible
        vram_free = self.gpu_info['vram_free_mb']
        
        # Ordre de préférence des nouveaux profils (du plus performant au moins performant)
        profile_order = ['turbo_max', 'performance_optimized', 'stable_high', 'balanced_adaptive', 
                        'conservative_stable', 'emergency_safe']
        
        for profile_key in profile_order:
            profile = LLM_PROFILES[profile_key]
            if vram_free >= profile['min_vram_free_mb']:
                return profile_key
        
        # Si aucun profil ne convient, utiliser le profil d'urgence
        return 'emergency_safe'
    
    def _get_llm_config(self):
        """Récupère la configuration LLM pour le profil actuel"""
        profile = LLM_PROFILES[self.current_profile].copy()
        
        # Supprimer les métadonnées pour ne garder que la config LLM
        config_keys = ['name', 'description', 'min_vram_free_mb']
        for key in config_keys:
            profile.pop(key, None)
        
        return profile
    
    def _initialize_model(self):
        """Initialise le modèle LLaMA avec la configuration optimisée"""
        try:
            llm_config = self._get_llm_config()
            profile_name = LLM_PROFILES[self.current_profile]['name']
            
            logger.info(f"Initialisation du modèle: {config.MODEL_PATH}")
            logger.info(f"Configuration: {profile_name}")
            logger.info(f"Paramètres LLM: {llm_config}")
            
            # Utiliser la configuration de l'optimiseur GPU si disponible
            if GPU_OPTIMIZER_AVAILABLE:
                try:
                    optimized_config = gpu_optimizer.get_profile_config(self.current_profile)
                    # Fusionner avec la config existante, optimiseur priorisé
                    llm_config.update(optimized_config)
                    logger.info(f"Configuration optimiseur GPU appliquée: {optimized_config}")
                except Exception as e:
                    logger.warning(f"Impossible d'utiliser config optimiseur: {e}")
            
            self.llm = Llama(
                model_path=config.MODEL_PATH,
                **llm_config
            )

            # Infos système du backend (permet de confirmer CUDA) + chemin du package
            try:
                import llama_cpp as _py_pkg
                from llama_cpp import llama_cpp as _llama_cpp
                sys_info = _llama_cpp.llama_print_system_info().decode("utf-8")
                logger.info("llama.cpp system info:\n" + sys_info)
                logger.info(f"llama_cpp package path: {_py_pkg.__file__}")
                self.runtime_info = {
                    'system_info': sys_info,
                    'cuda': ("CUDA" in sys_info) or ("cuBLAS" in sys_info) or ("ggml-cuda" in sys_info),
                    'llm_config_used': llm_config,
                    'module_path': _py_pkg.__file__,
                }
            except Exception as _e:
                logger.warning(f"Impossible de récupérer les infos système llama.cpp: {_e}")
                self.runtime_info = {
                    'system_info': None,
                    'cuda': None,
                    'llm_config_used': llm_config,
                    'module_path': None,
                }

            logger.info("Modèle LLM initialisé avec succès")
        except Exception as e:
            logger.error(f"Erreur lors de l'initialisation du modèle: {e}")
            # Tentative avec profil d'urgence si ce n'était pas déjà le cas
            if self.current_profile != 'emergency':
                logger.info("Tentative avec profil d'urgence...")
                self.current_profile = 'emergency'
                try:
                    llm_config = self._get_llm_config()
                    self.llm = Llama(
                        model_path=config.MODEL_PATH,
                        **llm_config
                    )
                    logger.info("Modèle initialisé avec profil d'urgence")
                except Exception as e2:
                    logger.error(f"Échec même avec profil d'urgence: {e2}")
                    raise e2
            else:
                raise e
    
    def is_ready(self) -> bool:
        """Vérifie si le modèle est prêt"""
        return self.llm is not None
    
    def get_current_profile(self):
        """Retourne le profil actuellement utilisé"""
        info = {
            'key': self.current_profile,
            'config': LLM_PROFILES[self.current_profile],
            'gpu_info': self.gpu_info
        }
        # expose info runtime (CUDA détecté, config utilisée) pour !stats/!optimize
        if hasattr(self, 'runtime_info'):
            info['runtime'] = self.runtime_info
        return info
    
    def get_available_profiles(self):
        """Retourne tous les profils disponibles"""
        return LLM_PROFILES
    
    def get_recommended_profile(self):
        """Retourne le profil recommandé selon la VRAM actuelle et l'optimiseur"""
        if not NVIDIA_AVAILABLE:
            return 'cpu_fallback'
        
        # Utiliser l'optimiseur GPU avancé si disponible
        if GPU_OPTIMIZER_AVAILABLE:
            try:
                return gpu_optimizer.select_optimal_profile()
            except Exception as e:
                logger.warning(f"Erreur optimiseur pour recommandation: {e}")
        
        # Méthode classique de fallback
        try:
            pynvml.nvmlInit()
            handle = pynvml.nvmlDeviceGetHandleByIndex(0)
            mem_info = pynvml.nvmlDeviceGetMemoryInfo(handle)
            vram_free_mb = mem_info.free // (1024**2)
            pynvml.nvmlShutdown()
            
            # Sélection du profil optimal avec nouveaux profils
            profile_order = ['turbo_max', 'performance_optimized', 'stable_high', 
                           'balanced_adaptive', 'conservative_stable', 'emergency_safe']
            for profile_key in profile_order:
                profile = LLM_PROFILES[profile_key]
                if vram_free_mb >= profile['min_vram_free_mb']:
                    return profile_key
            return 'emergency_safe'
            
        except Exception as e:
            logger.warning(f"Erreur détection VRAM: {e}")
            return self.current_profile
    
    def change_profile(self, profile_key):
        """Change le profil de configuration (nécessite un redémarrage du modèle)"""
        if profile_key not in LLM_PROFILES:
            raise ValueError(f"Profil inconnu: {profile_key}")
        
        old_profile = self.current_profile
        self.current_profile = profile_key
        
        try:
            # Libérer l'ancien modèle
            if self.llm:
                del self.llm
                self.llm = None
            
            # Réinitialiser avec le nouveau profil
            self._initialize_model()
            logger.info(f"Profil changé: {old_profile} → {profile_key}")
            return True
            
        except Exception as e:
            logger.error(f"Erreur changement de profil: {e}")
            # Restaurer l'ancien profil en cas d'échec
            self.current_profile = old_profile
            try:
                self._initialize_model()
                logger.info(f"Profil restauré: {old_profile}")
            except Exception as e2:
                logger.error(f"Impossible de restaurer le profil: {e2}")
            return False
    
    def get_context_info(self):
        """Retourne les informations sur le contexte actuel"""
        if not self.is_ready():
            return None
        
        try:
            # Récupération sécurisée de n_ctx
            n_ctx_attr = getattr(self.llm, "n_ctx", None)
            if callable(n_ctx_attr):
                actual_ctx = n_ctx_attr()
            elif n_ctx_attr is not None:
                actual_ctx = n_ctx_attr
            else:
                actual_ctx = LLM_PROFILES[self.current_profile]['n_ctx']
            
            configured_ctx = LLM_PROFILES[self.current_profile]['n_ctx']
            training_ctx = 32768  # Contexte d'entraînement typique pour les modèles 7B
            
            return {
                'configured_ctx': configured_ctx,
                'actual_ctx': actual_ctx,
                'training_ctx': training_ctx,
                'efficiency_percent': (actual_ctx / training_ctx) * 100,
                'profile': self.current_profile
            }
            
        except Exception as e:
            logger.error(f"Erreur récupération info contexte: {e}")
            return None
    
    def get_gpu_optimization_report(self):
        """Retourne un rapport d'optimisation GPU détaillé"""
        if not GPU_OPTIMIZER_AVAILABLE:
            return {
                "error": "Optimiseur GPU avancé non disponible",
                "fallback_info": {
                    "current_profile": self.current_profile,
                    "profile_name": LLM_PROFILES[self.current_profile]['name'],
                    "gpu_info": self.gpu_info
                }
            }
        
        try:
            return gpu_optimizer.get_optimization_report()
        except Exception as e:
            logger.error(f"Erreur rapport optimisation GPU: {e}")
            return {"error": f"Erreur génération rapport: {e}"}
    
    def get_gpu_metrics(self):
        """Obtient les métriques GPU actuelles"""
        if GPU_OPTIMIZER_AVAILABLE:
            try:
                metrics = gpu_optimizer.get_gpu_metrics()
                if metrics:
                    return {
                        "name": metrics.name,
                        "vram_usage": f"{metrics.vram_used_mb} MB / {metrics.vram_total_mb} MB ({metrics.usage_percent:.1f}%)",
                        "temperature": f"{metrics.temperature_c}°C",
                        "power_usage": f"{metrics.power_usage_w}W",
                        "gpu_utilization": f"{metrics.utilization_gpu}%"
                    }
            except Exception as e:
                logger.error(f"Erreur récupération métriques GPU: {e}")
        return None
    
    @property
    def auto_optimization_enabled(self):
        """Vérifie si l'auto-optimisation est activée"""
        if GPU_OPTIMIZER_AVAILABLE:
            return gpu_optimizer.auto_optimization_enabled
        return False
    
    def enable_auto_optimization(self, enable: bool = True):
        """Active/désactive l'optimisation automatique"""
        if GPU_OPTIMIZER_AVAILABLE:
            try:
                gpu_optimizer.auto_optimization_enabled = enable
                status = "activée" if enable else "désactivée"
                logger.info(f"Optimisation automatique {status}")
                return True
            except Exception as e:
                logger.error(f"Erreur configuration auto-optimisation: {e}")
                return False
        else:
            logger.warning("Optimisation automatique non disponible - optimiseur GPU manquant")
            return False
    
    def get_performance_metrics(self):
        """Retourne les métriques de performance actuelles"""
        if not GPU_OPTIMIZER_AVAILABLE:
            return None
        
        try:
            metrics = gpu_optimizer.current_metrics
            if metrics:
                return {
                    "gpu_name": metrics.name,
                    "vram_usage": {
                        "used_mb": metrics.vram_used_mb,
                        "total_mb": metrics.vram_total_mb,
                        "free_mb": metrics.vram_free_mb,
                        "usage_percent": metrics.usage_percent
                    },
                    "temperature_c": metrics.temperature_c,
                    "power_usage_w": metrics.power_usage_w,
                    "gpu_utilization": metrics.utilization_gpu,
                    "memory_utilization": metrics.utilization_memory,
                    "timestamp": metrics.timestamp.isoformat()
                }
            else:
                return None
        except Exception as e:
            logger.error(f"Erreur récupération métriques performance: {e}")
            return None
    
    def optimize_for_task(self, task_type: str = "chat"):
        """Optimise la configuration pour un type de tâche spécifique"""
        if not GPU_OPTIMIZER_AVAILABLE:
            logger.warning("Optimisation par tâche non disponible - optimiseur GPU manquant")
            return False
        
        try:
            current_metrics = gpu_optimizer.get_gpu_metrics()
            if not current_metrics:
                logger.warning("Impossible d'optimiser - métriques GPU non disponibles")
                return False
            
            # Logique d'optimisation basée sur le type de tâche
            if task_type == "chat":
                # Pour le chat, privilégier la latence faible
                if current_metrics.vram_free_mb >= 3000 and current_metrics.temperature_c < 75:
                    optimal_profile = "turbo_max"
                elif current_metrics.vram_free_mb >= 2000:
                    optimal_profile = "performance_optimized"
                else:
                    optimal_profile = "stable_high"
            
            elif task_type == "batch":
                # Pour le traitement batch, privilégier le throughput
                if current_metrics.vram_free_mb >= 2500:
                    optimal_profile = "performance_optimized"
                else:
                    optimal_profile = "balanced_adaptive"
            
            elif task_type == "long_context":
                # Pour les longs contextes, privilégier la taille de contexte
                if current_metrics.vram_free_mb >= 3500:
                    optimal_profile = "turbo_max"
                elif current_metrics.vram_free_mb >= 2000:
                    optimal_profile = "stable_high"
                else:
                    optimal_profile = "conservative_stable"
            
            else:
                optimal_profile = gpu_optimizer.select_optimal_profile()
            
            # Appliquer le profil si différent
            if optimal_profile != self.current_profile:
                success = self.change_profile(optimal_profile)
                if success:
                    logger.info(f"Optimisation pour tâche '{task_type}' appliquée: {optimal_profile}")
                return success
            else:
                logger.info(f"Profil déjà optimal pour tâche '{task_type}': {optimal_profile}")
                return True
                
        except Exception as e:
            logger.error(f"Erreur optimisation pour tâche '{task_type}': {e}")
            return False

# Instance globale du gestionnaire de modèle
model_manager = ModelManager()
llm = model_manager.llm

async def generate_reply(user_id: str, prompt: str, context_limit: int = 10) -> str:
    """Génère une réponse en utilisant le modèle LLM avec gestion d'erreurs améliorée"""
    
    if not model_manager.is_ready():
        error_msg = "❌ Modèle non initialisé"
        logger.error(error_msg)
        return error_msg
    
    try:
        # Récupération sécurisée de n_ctx depuis le profil actuel
        context_info = model_manager.get_context_info()
        if context_info:
            max_total = context_info['actual_ctx']
        else:
            # Fallback vers la configuration du profil
            max_total = LLM_PROFILES[model_manager.current_profile]['n_ctx']
        
        # S'assurer que max_total est un entier
        max_total = int(max_total)
        max_tokens = 400
        min_context = 1

        # Utilise la limite dynamique passée en argument
        limit = context_limit
        logger.debug(f"Génération de réponse pour {user_id} avec contexte limite: {limit}")

        while limit >= min_context:
            history = get_history(user_id, limit=limit)
            full_prompt = (
                "Tu es Kira , une IA française drôle, vive, légèrement sarcastique mais toujours attachante et gentille. "
                "Tu parles de façon expressive, naturelle, parfois spontanée.\n"
                "Tu ne cites jamais de sources ni de liens externes. Tu réponds toujours en français, même si la question est en anglais.\n"
                "Tu évites les réponses plates ou génériques.\n"
                "Si une information t'est donnée, utilise-la naturellement dans ta réponse sans dire que tu l'as trouvée ou recherchée.\n"
                "Neuro adore plaisanter, poser des questions en retour ou rebondir de manière surprenante.\n\n"
            )

            # Injecte les faits connus sur l'utilisateur
            facts = get_facts(user_id)
            if facts:
                full_prompt += "Voici ce que je sais à propos de cet utilisateur :\n"
                for f in facts:
                    full_prompt += f"- {f}\n"
                full_prompt += "\n"

            # Ajouter l'historique
            for user_msg, bot_msg in history:
                full_prompt += f"Utilisateur: {user_msg}\nNeuro: {bot_msg}\n"

            full_prompt += f"Utilisateur: {prompt}\nNeuro:"

            prompt_tokens = count_tokens(full_prompt)
            if prompt_tokens + max_tokens <= max_total:
                break  # OK, on peut générer
            limit -= 1  # On réduit l'historique
            logger.debug(f"Réduction du contexte à {limit} pour respecter les limites de tokens")

        # Si c'est encore trop long, tronque le prompt
        if prompt_tokens + max_tokens > max_total:
            logger.warning(f"Troncature nécessaire: {prompt_tokens} + {max_tokens} > {max_total}")
            full_prompt = truncate_text_to_tokens(full_prompt, max_total - max_tokens)
            prompt_tokens = count_tokens(full_prompt)
            if prompt_tokens + max_tokens > max_total:
                err = f"❌ Erreur modèle : prompt ({prompt_tokens}) + réponse ({max_tokens}) > {max_total} tokens"
                logger.error(err)
                return err

        start = time.time()
        
        # Génération avec le modèle (exécuté dans un thread pour ne pas bloquer l'event loop)
        output = await asyncio.to_thread(
            llm,
            full_prompt,
            max_tokens=max_tokens,
            temperature=0.8,
            top_p=0.95,
            stop=["Utilisateur:", "\n"]
        )
        
        # Extraction de la réponse selon le format de sortie
        if isinstance(output, dict) and "choices" in output and output["choices"]:
            reply = output["choices"][0]["text"].strip()
        else:
            reply = str(output).strip()
        
        end = time.time()
        generation_time = end - start
        logger.info(f"Réponse générée en {generation_time:.2f}s pour {user_id}")

        # Sauvegarde de l'interaction (mémoire conversationnelle)
        save_interaction(user_id, prompt, reply)

        return shorten_response(reply)
        
    except Exception as e:
        error_msg = f"❌ Erreur lors de la génération: {str(e)}"
        logger.error(f"Erreur génération pour {user_id}: {e}", exc_info=True)
        return error_msg