from auth_decorators import require_authorized_role
from model import model_manager, LLM_PROFILES
import pynvml
import os

def setup(bot):
    @bot.command()
    @require_authorized_role
    async def optimize(ctx, action: str = None, profile: str = None):
        """
        Commande d'optimisation du contexte LLM
        Usage: !optimize [analyze|apply|profiles]
        """
        
        if action is None:
            help_msg = (
                "```\n"
                "🔧 OPTIMISATION GPU AVANCÉE\n"
                "────────────────────────────────\n"
                "!optimize analyze      - Analyser l'utilisation GPU/VRAM\n"
                "!optimize apply        - Appliquer l'optimisation recommandée\n"
                "!optimize profiles     - Afficher les profils disponibles\n"
                "!optimize current      - Afficher le profil actuel\n"
                "!optimize set <profil> - Changer de profil\n"
                "!optimize report       - Rapport d'optimisation détaillé\n"
                "!optimize metrics      - Métriques de performance temps réel\n"
                "!optimize auto on/off  - Optimisation automatique\n"
                "!optimize task <type>  - Optimiser pour un type de tâche\n"
                "                        (chat, batch, long_context)\n"
                "```"
            )
            await ctx.send(help_msg)
            return
        
        try:
            action_lower = action.lower()
            if action_lower == "analyze":
                await analyze_vram(ctx)
            elif action_lower == "apply":
                await apply_optimization(ctx)
            elif action_lower == "profiles":
                await show_profiles(ctx)
            elif action_lower == "current":
                await show_current_profile(ctx)
            elif action_lower == "set":
                # Supporte !optimize set <profil> via second argument
                if profile:
                    await set_profile(ctx, profile)
                else:
                    await ctx.send("❌ Spécifiez le profil: `!optimize set <profil>`")
            elif action_lower.startswith("set"):
                # Compat: supporte aussi !optimize "set turbo_max" en un seul argument
                parts = action.split()
                if len(parts) > 1:
                    profile_name = parts[1]
                    await set_profile(ctx, profile_name)
                else:
                    await ctx.send("❌ Spécifiez le profil: `!optimize set <profil>`")
            elif action_lower == "report":
                await show_optimization_report(ctx)
            elif action_lower == "metrics":
                await show_performance_metrics(ctx)
            elif action_lower == "auto":
                auto_state = profile.lower() if profile else None
                await toggle_auto_optimization(ctx, auto_state)
            elif action_lower == "task":
                task_type = profile if profile else "chat"
                await optimize_for_task(ctx, task_type)
            else:
                available_actions = "analyze, apply, profiles, current, set, report, metrics, auto, task"
                await ctx.send(f"❌ Action inconnue: `{action}`\nActions disponibles: {available_actions}")
                
        except Exception as e:
            await ctx.send(f"❌ Erreur lors de l'optimisation: {e}")

async def analyze_vram(ctx):
    """Analyse l'utilisation VRAM actuelle"""
    try:
        # Récupérer les informations du modèle
        current_profile = model_manager.get_current_profile()
        recommended_profile_key = model_manager.get_recommended_profile()
        
        if not current_profile or not current_profile['gpu_info']:
            await ctx.send("❌ Informations GPU non disponibles")
            return
        
        gpu_info = current_profile['gpu_info']
        gpu_name = gpu_info['name']
        vram_used = gpu_info['vram_used_mb']
        vram_total = gpu_info['vram_total_mb']
        vram_free = gpu_info['vram_free_mb']
        vram_percent = gpu_info['vram_usage_percent']
        
        # Analyse du statut
        if vram_percent > 90:
            status = "🔴 CRITIQUE"
            recommendation = "Réduction immédiate nécessaire"
        elif vram_percent > 80:
            status = "🟠 ÉLEVÉE"
            recommendation = "Surveiller et considérer une réduction"
        elif vram_percent > 60:
            status = "🟡 MODÉRÉE"
            recommendation = "Utilisation normale"
        else:
            status = "🟢 OPTIMALE"
            recommendation = "Possibilité d'augmenter les performances"
        
        # Profil recommandé
        recommended_profile = LLM_PROFILES[recommended_profile_key]
        current_profile_name = current_profile['config']['name']
        
        msg = (
            "```\n"
            "📊 ANALYSE VRAM POUR OPTIMISATION\n"
            "──────────────────────────────────\n"
            f"🖥️ GPU: {gpu_name}\n"
            f"🧮 VRAM: {vram_used} MB / {vram_total} MB ({vram_percent:.1f}%)\n"
            f"💾 VRAM libre: {vram_free} MB\n"
            f"📈 Statut: {status}\n"
            f"💡 Recommandation: {recommendation}\n"
            "\n"
            "🎯 PROFILS\n"
            "──────────────────────────────────\n"
            f"📋 Profil actuel: {current_profile_name}\n"
            f"🎯 Profil recommandé: {recommended_profile['name']}\n"
            f"🧮 Contexte recommandé: {recommended_profile['n_ctx']:,} tokens\n"
            "\n"
            "Utilisez !optimize apply pour appliquer\n"
            "ou !optimize profiles pour voir tous les profils\n"
            "```"
        )
        
        await ctx.send(msg)
        
    except Exception as e:
        await ctx.send(f"❌ Erreur lors de l'analyse VRAM: {e}")

async def apply_optimization(ctx):
    """Applique l'optimisation recommandée"""
    try:
        # Obtenir le profil recommandé
        current_profile_key = model_manager.current_profile
        recommended_profile_key = model_manager.get_recommended_profile()
        
        if current_profile_key == recommended_profile_key:
            await ctx.send("✅ Configuration déjà optimale - aucun changement nécessaire")
            return
        
        current_profile_name = LLM_PROFILES[current_profile_key]['name']
        recommended_profile_name = LLM_PROFILES[recommended_profile_key]['name']
        
        # Appliquer le changement de profil
        success = model_manager.change_profile(recommended_profile_key)
        
        if success:
            msg = (
                f"✅ **Optimisation appliquée avec succès**\n"
                f"```\n"
                f"📋 Ancien profil: {current_profile_name}\n"
                f"🎯 Nouveau profil: {recommended_profile_name}\n"
                f"🧮 Nouveau contexte: {LLM_PROFILES[recommended_profile_key]['n_ctx']:,} tokens\n"
                f"🔧 Couches GPU: {LLM_PROFILES[recommended_profile_key]['n_gpu_layers']}\n"
                f"📦 Batch size: {LLM_PROFILES[recommended_profile_key]['n_batch']}\n"
                f"```\n"
                f"✅ **Changement appliqué immédiatement - pas de redémarrage nécessaire**"
            )
        else:
            msg = (
                f"❌ **Échec de l'optimisation**\n"
                f"Le profil {recommended_profile_name} n'a pas pu être appliqué.\n"
                f"Le profil {current_profile_name} a été restauré."
            )
        
        await ctx.send(msg)
        
    except Exception as e:
        await ctx.send(f"❌ Erreur lors de l'application: {e}")

async def show_profiles(ctx):
    """Affiche tous les profils de configuration disponibles"""
    profiles = model_manager.get_available_profiles()
    current_profile_key = model_manager.current_profile
    
    msg_parts = [
        "```\n🎯 PROFILS DE CONFIGURATION DISPONIBLES\n",
        "────────────────────────────────────────\n"
    ]
    
    profile_emojis = {
        'performance_max': '🚀',
        'balanced': '⚖️',
        'economical': '💾',
        'emergency': '🆘',
        'cpu_only': '🖥️'
    }
    
    for key, profile in profiles.items():
        emoji = profile_emojis.get(key, '📋')
        current_marker = " (ACTUEL)" if key == current_profile_key else ""
        
        msg_parts.extend([
            f"\n{emoji} {profile['name'].upper()}{current_marker}\n",
            f"   Contexte: {profile['n_ctx']:,} tokens\n",
            f"   Couches GPU: {profile['n_gpu_layers']}\n",
            f"   Batch: {profile['n_batch']}\n",
            f"   VRAM min libre: {profile['min_vram_free_mb']} MB\n",
            f"   Usage: {profile['description']}\n"
        ])
    
    msg_parts.extend([
        "\n💡 Commandes utiles:\n",
        "   !optimize analyze - Voir le profil recommandé\n",
        "   !optimize set <profil> - Changer de profil\n",
        "   !optimize current - Voir le profil actuel\n",
        "```"
    ])
    
    await ctx.send(''.join(msg_parts))

async def show_current_profile(ctx):
    """Affiche le profil actuellement utilisé"""
    try:
        current_profile = model_manager.get_current_profile()
        context_info = model_manager.get_context_info()
        
        if not current_profile:
            await ctx.send("❌ Impossible de récupérer le profil actuel")
            return
        
        profile = current_profile['config']
        gpu_info = current_profile['gpu_info']
        
        msg = (
            "```\n"
            "🎯 PROFIL ACTUEL\n"
            "────────────────────────────────\n"
            f"📋 Nom: {profile['name']}\n"
            f"📝 Description: {profile['description']}\n"
            f"🧮 Contexte: {profile['n_ctx']:,} tokens\n"
            f"🔧 Couches GPU: {profile['n_gpu_layers']}\n"
            f"📦 Batch size: {profile['n_batch']}\n"
            f"🧵 Threads: {profile['n_threads']}\n"
        )
        
        if context_info:
            msg += f"⚡ Efficacité: {context_info['efficiency_percent']:.1f}%\n"
        
        if gpu_info:
            msg += (
                f"\n🖥️ GPU: {gpu_info['name']}\n"
                f"🧮 VRAM: {gpu_info['vram_used_mb']} MB / {gpu_info['vram_total_mb']} MB\n"
                f"💾 VRAM libre: {gpu_info['vram_free_mb']} MB\n"
            )
        
        msg += "```"
        
        await ctx.send(msg)
        
    except Exception as e:
        await ctx.send(f"❌ Erreur lors de l'affichage du profil: {e}")

async def set_profile(ctx, profile_name):
    """Change le profil de configuration"""
    try:
        # Mapper les noms courts aux clés (mis à jour avec nouveaux profils)
        profile_mapping = {
            'turbo': 'turbo_max',
            'max': 'turbo_max',
            'performance': 'performance_optimized',
            'perf': 'performance_optimized',
            'stable': 'stable_high',
            'high': 'stable_high',
            'balanced': 'balanced_adaptive',
            'equilibre': 'balanced_adaptive',
            'adaptive': 'balanced_adaptive',
            'conservative': 'conservative_stable',
            'conservateur': 'conservative_stable',
            'economical': 'conservative_stable',
            'eco': 'conservative_stable',
            'emergency': 'emergency_safe',
            'secours': 'emergency_safe',
            'safe': 'emergency_safe',
            'cpu': 'cpu_fallback',
            'fallback': 'cpu_fallback',
            # Compatibilité anciens noms
            'performance_max': 'performance_max',
            'turbo_4050': 'turbo_max'
        }
        
        profile_key = profile_mapping.get(profile_name.lower(), profile_name.lower())
        
        if profile_key not in LLM_PROFILES:
            available = ', '.join(profile_mapping.keys())
            await ctx.send(f"❌ Profil inconnu: `{profile_name}`\nProfils disponibles: {available}")
            return
        
        current_profile_key = model_manager.current_profile
        if current_profile_key == profile_key:
            await ctx.send(f"✅ Le profil `{LLM_PROFILES[profile_key]['name']}` est déjà actif")
            return
        
        # Changer le profil
        success = model_manager.change_profile(profile_key)
        
        if success:
            new_profile = LLM_PROFILES[profile_key]
            msg = (
                f"✅ **Profil changé avec succès**\n"
                f"```\n"
                f"🎯 Nouveau profil: {new_profile['name']}\n"
                f"🧮 Contexte: {new_profile['n_ctx']:,} tokens\n"
                f"🔧 Couches GPU: {new_profile['n_gpu_layers']}\n"
                f"📦 Batch size: {new_profile['n_batch']}\n"
                f"```\n"
                f"✅ **Changement appliqué immédiatement**"
            )
        else:
            msg = f"❌ **Échec du changement de profil**\nImpossible d'appliquer le profil `{LLM_PROFILES[profile_key]['name']}`"
        
        await ctx.send(msg)
        
    except Exception as e:
        await ctx.send(f"❌ Erreur lors du changement de profil: {e}")

async def show_optimization_report(ctx):
    """Affiche un rapport d'optimisation détaillé"""
    try:
        report = model_manager.get_gpu_optimization_report()
        
        if "error" in report:
            await ctx.send(f"❌ {report['error']}")
            if "fallback_info" in report:
                info = report["fallback_info"]
                msg = (
                    f"```\n"
                    f"📋 INFORMATIONS BASIQUES\n"
                    f"──────────────────────────\n"
                    f"Profil actuel: {info['profile_name']}\n"
                    f"Clé profil: {info['current_profile']}\n"
                )
                if info.get("gpu_info"):
                    gpu = info["gpu_info"]
                    msg += (
                        f"GPU: {gpu['name']}\n"
                        f"VRAM: {gpu['vram_used_mb']} MB / {gpu['vram_total_mb']} MB\n"
                    )
                msg += "```"
                await ctx.send(msg)
            return
        
        # Formatage du rapport complet
        current = report["current_metrics"]
        averages = report["averages_last_5min"]
        optimal = report["optimal_profile"]
        recommendations = report["recommendations"]
        monitoring = report["monitoring_status"]
        
        msg = (
            f"```\n"
            f"🚀 RAPPORT D'OPTIMISATION GPU DÉTAILLÉ\n"
            f"═══════════════════════════════════════\n"
            f"\n"
            f"🖥️ GPU ACTUELLE\n"
            f"──────────────────────────\n"
            f"GPU: {current['gpu_name']}\n"
            f"VRAM: {current['vram_usage']}\n"
            f"Température: {current['temperature']}\n"
            f"Consommation: {current['power_usage']}\n"
            f"Utilisation GPU: {current['gpu_utilization']}\n"
            f"Utilisation Mémoire: {current['memory_utilization']}\n"
            f"\n"
            f"📊 MOYENNES (5 DERNIÈRES MINUTES)\n"
            f"──────────────────────────────────\n"
            f"Température moy.: {averages['temperature']}\n"
            f"VRAM moy.: {averages['vram_usage']}\n"
            f"Utilisation GPU moy.: {averages['gpu_utilization']}\n"
            f"\n"
            f"🎯 PROFIL OPTIMAL RECOMMANDÉ\n"
            f"────────────────────────────\n"
            f"Nom: {optimal['name']}\n"
            f"Description: {optimal['description']}\n"
            f"```"
        )
        
        await ctx.send(msg)
        
        # Configuration optimale
        config = optimal["config"]
        config_msg = (
            f"```\n"
            f"⚙️ CONFIGURATION OPTIMALE\n"
            f"─────────────────────────\n"
            f"Contexte: {config['n_ctx']:,} tokens\n"
            f"Couches GPU: {config['n_gpu_layers']}\n"
            f"Batch size: {config['n_batch']}\n"
            f"Threads: {config['n_threads']}\n"
            f"Flash attention: {'Oui' if config.get('flash_attn') else 'Non'}\n"
            f"Offload KQV: {'Oui' if config.get('offload_kqv') else 'Non'}\n"
            f"Use mmap: {'Oui' if config.get('use_mmap') else 'Non'}\n"
            f"Use mlock: {'Oui' if config.get('use_mlock') else 'Non'}\n"
            f"```"
        )
        
        await ctx.send(config_msg)
        
        # Recommandations
        recommendations_msg = (
            f"💡 **RECOMMANDATIONS:**\n" + 
            "\n".join(f"• {rec}" for rec in recommendations)
        )
        
        await ctx.send(recommendations_msg)
        
        # Statut monitoring
        status_msg = (
            f"```\n"
            f"📡 STATUT MONITORING\n"
            f"───────────────────\n"
            f"Monitoring actif: {'Oui' if monitoring['active'] else 'Non'}\n"
            f"Auto-optimisation: {'Oui' if monitoring['auto_optimization'] else 'Non'}\n"
            f"Métriques collectées: {monitoring['metrics_collected']:,}\n"
            f"```"
        )
        
        await ctx.send(status_msg)
        
    except Exception as e:
        await ctx.send(f"❌ Erreur génération rapport: {e}")

async def show_performance_metrics(ctx):
    """Affiche les métriques de performance temps réel"""
    try:
        metrics = model_manager.get_performance_metrics()
        
        if not metrics:
            await ctx.send("❌ Métriques de performance non disponibles")
            return
        
        vram = metrics["vram_usage"]
        msg = (
            f"```\n"
            f"⚡ MÉTRIQUES PERFORMANCE TEMPS RÉEL\n"
            f"═══════════════════════════════════\n"
            f"\n"
            f"🖥️ {metrics['gpu_name']}\n"
            f"\n"
            f"💾 VRAM\n"
            f"──────\n"
            f"Utilisée: {vram['used_mb']:,} MB\n"
            f"Totale: {vram['total_mb']:,} MB\n"
            f"Libre: {vram['free_mb']:,} MB\n"
            f"Usage: {vram['usage_percent']:.1f}%\n"
            f"\n"
            f"🌡️ TEMPÉRATURE & PERFORMANCE\n"
            f"─────────────────────────────\n"
            f"Température: {metrics['temperature_c']}°C\n"
            f"Consommation: {metrics['power_usage_w']}W\n"
            f"Utilisation GPU: {metrics['gpu_utilization']}%\n"
            f"Utilisation mémoire: {metrics['memory_utilization']}%\n"
            f"\n"
            f"🕐 Dernière mise à jour: {metrics['timestamp']}\n"
            f"```"
        )
        
        # Barre de progression visuelle pour la VRAM
        vram_percent = vram['usage_percent']
        bar_length = 20
        filled = int(bar_length * vram_percent / 100)
        bar = '█' * filled + '░' * (bar_length - filled)
        
        bar_msg = f"**VRAM Usage:** `[{bar}]` **{vram_percent:.1f}%**"
        
        await ctx.send(msg)
        await ctx.send(bar_msg)
        
    except Exception as e:
        await ctx.send(f"❌ Erreur affichage métriques: {e}")

async def toggle_auto_optimization(ctx, state):
    """Active/désactive l'optimisation automatique"""
    try:
        if state is None:
            await ctx.send("❌ Spécifiez l'état: `!optimize auto on` ou `!optimize auto off`")
            return
        
        if state in ['on', 'oui', 'yes', '1', 'true']:
            enable = True
            state_text = "activée"
        elif state in ['off', 'non', 'no', '0', 'false']:
            enable = False
            state_text = "désactivée"
        else:
            await ctx.send("❌ État invalide. Utilisez `on` ou `off`")
            return
        
        success = model_manager.enable_auto_optimization(enable)
        
        if success:
            await ctx.send(f"✅ Optimisation automatique {state_text} avec succès")
        else:
            await ctx.send(f"❌ Impossible de {state_text.replace('ée', 'er')} l'optimisation automatique")
            
    except Exception as e:
        await ctx.send(f"❌ Erreur configuration auto-optimisation: {e}")

async def optimize_for_task(ctx, task_type):
    """Optimise pour un type de tâche spécifique"""
    try:
        valid_tasks = ['chat', 'batch', 'long_context']
        
        if task_type not in valid_tasks:
            await ctx.send(f"❌ Type de tâche invalide: `{task_type}`\n"
                          f"Types valides: {', '.join(valid_tasks)}")
            return
        
        task_descriptions = {
            'chat': 'conversation interactive (latence faible)',
            'batch': 'traitement en lot (throughput élevé)', 
            'long_context': 'contexte étendu (mémoire maximale)'
        }
        
        await ctx.send(f"🔧 Optimisation pour tâche: **{task_descriptions[task_type]}**")
        
        success = model_manager.optimize_for_task(task_type)
        
        if success:
            current_profile = model_manager.get_current_profile()
            profile_name = current_profile['config']['name']
            
            msg = (
                f"✅ **Optimisation appliquée avec succès**\n"
                f"🎯 Profil sélectionné: **{profile_name}**\n"
                f"📋 Optimisé pour: **{task_descriptions[task_type]}**\n"
                f"\n"
                f"💡 Utilisez `!optimize current` pour voir les détails"
            )
            await ctx.send(msg)
        else:
            await ctx.send(f"❌ Échec de l'optimisation pour la tâche `{task_type}`")
            
    except Exception as e:
        await ctx.send(f"❌ Erreur optimisation tâche: {e}")