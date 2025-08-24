from config import logger

try:
    from transformers import GPT2TokenizerFast
    tokenizer = GPT2TokenizerFast.from_pretrained("gpt2")
    logger.info("Tokenizer GPT-2 initialisé avec succès")
except Exception as e:
    tokenizer = None
    logger.warning(f"Tokenizer non disponible : {e}")

def count_tokens(text: str) -> int:
    if tokenizer:
        return len(tokenizer.encode(text))
    else:
        # fallback approximatif
        return max(1, len(text) // 3)

def truncate_text_to_tokens(text: str, max_tokens: int) -> str:
    """
    Tronque text à max_tokens tokens en utilisant tokenizer si disponible,
    sinon tronque en caractères (approx).
    """
    if tokenizer:
        tokens = tokenizer.encode(text)
        if len(tokens) <= max_tokens:
            return text
        truncated = tokenizer.decode(tokens[:max_tokens], clean_up_tokenization_spaces=True, skip_special_tokens=True)
        return truncated
    else:
        # fallback approximatif : coupe aux max_tokens*3 caractères
        approx_chars = max_tokens * 3
        if len(text) <= approx_chars:
            return text
        return text[:approx_chars].rsplit(" ", 1)[0]

def shorten_response(text: str, max_length: int | None = None) -> str:
    """
    Raccourci la réponse proprement.
    Si max_length est None on lit le fichier character_limits.json.
    """
    from config import config
    import json
    
    if max_length is None:
        try:
            with open(config.LIMITS_FILE, "r", encoding="utf-8") as f:
                limits_config = json.load(f)
                max_length = limits_config.get("max_reply_length", 1900)
        except Exception as e:
            logger.warning(f"Erreur lecture limits file: {e}, utilisation valeur par défaut")
            max_length = 1900

    if len(text) <= max_length:
        return text

    # Couper proprement au dernier saut de ligne ou point avant max_length
    cut_point = max(text.rfind("\n", 0, max_length), text.rfind(".", 0, max_length))
    if cut_point == -1:
        cut_point = max_length

    truncated = text[:cut_point].rstrip()
    logger.debug(f"Réponse tronquée de {len(text)} à {len(truncated)} caractères")
    return truncated