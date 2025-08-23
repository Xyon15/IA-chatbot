from llama_cpp import Llama
from config import MODEL_PATH
from utils import count_tokens, truncate_text_to_tokens, shorten_response
from memory import save_interaction, get_history, get_facts
import time


# --- Initialisation du modèle LLaMA avec GPU ---
llm = Llama(
    model_path=MODEL_PATH,
    n_gpu_layers=32,         # 32 couches sur le GPU (6 Go VRAM RTX 4050)
    n_threads=6,             # Pour éviter de saturer ton CPU
    n_ctx=4096,              # Contexte du modèle (doit correspondre à la capacité du modèle)
    n_batch=256,             # Taille des batchs
    verbose=True
)

async def generate_reply(user_id: str, prompt: str, context_limit: int = 10) -> str:
    max_total = getattr(llm, "n_ctx", 1024)  # ou llm.context_length selon ta version
    max_tokens = 400
    min_context = 1

    # Utilise la limite dynamique passée en argument (par défaut 10)
    limit = context_limit

    while limit >= min_context:
        history = get_history(user_id, limit=limit)
        full_prompt = (
            "Tu es Neuro, une IA française drôle, vive, légèrement sarcastique mais toujours attachante et gentille. "
            "Tu parles de façon expressive, naturelle, parfois spontanée.\n"
            "Tu ne cites jamais de sources ni de liens externes. Tu réponds toujours en français, même si la question est en anglais.\n"
            "Tu évites les réponses plates ou génériques.\n"
            "Si une information t'est donnée, utilise-la naturellement dans ta réponse sans dire que tu l’as trouvée ou recherchée.\n"
            "Neuro adore plaisanter, poser des questions en retour ou rebondir de manière surprenante.\n\n"
        )

        # Injecte les faits connus sur l'utilisateur
        facts = get_facts(user_id)
        if facts:
            full_prompt += "Voici ce que je sais à propos de cet utilisateur :\n"
            for f in facts:
                full_prompt += f"- {f}\n"
            full_prompt += "\n"

        # Ajouter l’historique
        for user_msg, bot_msg in history:
            full_prompt += f"Utilisateur: {user_msg}\nNeuro: {bot_msg}\n"

        full_prompt += f"Utilisateur: {prompt}\nNeuro:"

        prompt_tokens = count_tokens(full_prompt)
        if prompt_tokens + max_tokens <= max_total:
            break  # OK, on peut générer
        limit -= 1  # On réduit l'historique

    # Si c'est encore trop long, tronque le prompt
    if prompt_tokens + max_tokens > max_total:
        # Tronque le prompt pour ne pas dépasser la limite
        full_prompt = truncate_text_to_tokens(full_prompt, max_total - max_tokens)
        prompt_tokens = count_tokens(full_prompt)
        if prompt_tokens + max_tokens > max_total:
            err = f"❌ Erreur modèle : prompt ({prompt_tokens}) + réponse ({max_tokens}) > {max_total} tokens"
            print(err)
            return err

    start = time.time()
    try:
        output = llm(full_prompt, max_tokens=max_tokens, temperature=0.8, top_p=0.95, stop=["Utilisateur:", "\n"])
        # selon la version de llama_cpp, le retour peut varier ; on garde ton style
        reply = output["choices"][0]["text"].strip() if "choices" in output and output["choices"] else str(output).strip()
    except Exception as e:
        print(f"❌ Erreur modèle : {e}")
        reply = f"❌ Erreur modèle : {e}"

    end = time.time()
    print(f"⏱️ Réponse générée en {end - start:.2f} secondes")

    # Sauvegarde de l'interaction (mémoire conversationnelle)
    save_interaction(user_id, prompt, reply)

    return shorten_response(reply)