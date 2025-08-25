from llama_cpp import Llama
from config import config, logger
from utils import count_tokens, truncate_text_to_tokens, shorten_response
from memory import save_interaction, get_history, get_facts
import time


class ModelManager:
    """Gestionnaire du modèle LLM avec gestion d'erreurs améliorée"""
    
    def __init__(self):
        self.llm = None
        self._initialize_model()
    
    def _initialize_model(self):
        """Initialise le modèle LLaMA avec la configuration"""
        try:
            logger.info(f"Initialisation du modèle: {config.MODEL_PATH}")
            self.llm = Llama(
                model_path=config.MODEL_PATH,
                **config.LLM_CONFIG
            )
            logger.info("Modèle LLM initialisé avec succès")
        except Exception as e:
            logger.error(f"Erreur lors de l'initialisation du modèle: {e}")
            raise
    
    def is_ready(self) -> bool:
        """Vérifie si le modèle est prêt"""
        return self.llm is not None

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
        # Récupération sécurisée de n_ctx (peut être un attribut ou une méthode)
        n_ctx_attr = getattr(llm, "n_ctx", None)
        if callable(n_ctx_attr):
            # Si c'est une méthode, l'appeler
            max_total = n_ctx_attr()
        elif n_ctx_attr is not None:
            # Si c'est un attribut, l'utiliser directement
            max_total = n_ctx_attr
        else:
            # Fallback vers la configuration
            max_total = config.LLM_CONFIG.get('n_ctx', 4096)
        
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
                "Tu es Neuro, une IA française drôle, vive, légèrement sarcastique mais toujours attachante et gentille. "
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
        
        # Génération avec le modèle
        output = llm(
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