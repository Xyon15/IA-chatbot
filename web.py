import asyncio
import aiohttp
from selectolax.parser import HTMLParser
from utils import shorten_response
import json
from config import config, logger

def load_web_state() -> bool:
    """Charge l'état de la recherche web"""
    try:
        with open(config.WEB_STATE_FILE, "r", encoding="utf-8") as f:
            data = json.load(f)
            state = data.get("enabled", False)
            logger.debug(f"État web chargé: {state}")
            return state
    except FileNotFoundError:
        logger.warning("Fichier web.json non trouvé, utilisation de la valeur par défaut")
        return False
    except Exception as e:
        logger.error(f"Erreur lors du chargement de web.json: {e}")
        return False

def save_web_state(enabled: bool):
    """Sauvegarde l'état de la recherche web"""
    try:
        with open(config.WEB_STATE_FILE, "w", encoding="utf-8") as f:
            json.dump({"enabled": enabled}, f, indent=2)
        logger.info(f"État web sauvegardé: {enabled}")
    except Exception as e:
        logger.error(f"Erreur lors de la sauvegarde de web.json: {e}")
        raise

async def duckduckgo_search(query: str) -> str:
    """Effectue une recherche DuckDuckGo avec l'API JSON"""
    url = f"https://api.duckduckgo.com/?q={query}&format=json&no_redirect=1&no_html=1"
    headers = {
        "Accept": "application/json",
        "User-Agent": "Mozilla/5.0"
    }

    logger.info(f"Recherche DuckDuckGo: {query}")
    
    try:
        async with aiohttp.ClientSession() as session:
            async with session.get(url, headers=headers, timeout=10) as resp:
                if resp.status == 200:
                    try:
                        data = await resp.json()
                        logger.debug("Réponse JSON reçue de DuckDuckGo")
                    except aiohttp.ContentTypeError:
                        logger.warning("Erreur de type de contenu, fallback vers HTML")
                        return await duckduckgo_html_fallback(query)

                    if data.get("Abstract"):
                        logger.info("Résultat trouvé dans Abstract")
                        return data["Abstract"]
                    elif data.get("Answer"):
                        logger.info("Résultat trouvé dans Answer")
                        return data["Answer"]
                    elif data.get("Definition"):
                        logger.info("Résultat trouvé dans Definition")
                        return data["Definition"]
                    else:
                        logger.info("Aucun résultat dans l'API JSON, fallback vers HTML")
                        return await duckduckgo_html_fallback(query)
                else:
                    error_msg = f"❌ Erreur HTTP {resp.status} (API JSON)."
                    logger.error(error_msg)
                    return error_msg
    except asyncio.TimeoutError:
        error_msg = "❌ Temps de réponse trop long (API JSON)."
        logger.error(error_msg)
        return error_msg
    except Exception as e:
        error_msg = f"❌ Erreur réseau (API JSON) : {e}"
        logger.error(error_msg)
        return error_msg

async def duckduckgo_html_fallback(query: str) -> str:
    """Fallback HTML pour la recherche DuckDuckGo"""
    url = f"https://html.duckduckgo.com/html/?q={query.replace(' ', '+')}"
    headers = {"User-Agent": "Mozilla/5.0"}

    logger.info(f"Fallback HTML pour: {query}")
    
    try:
        async with aiohttp.ClientSession() as session:
            async with session.get(url, headers=headers, timeout=10) as resp:
                if resp.status != 200:
                    error_msg = f"❌ Erreur HTTP {resp.status} (fallback HTML)."
                    logger.error(error_msg)
                    return error_msg

                html = await resp.text()
                tree = HTMLParser(html)
                results = tree.css(".result")

                if not results:
                    logger.warning("Aucun résultat trouvé dans le HTML")
                    return "😶 Aucun résultat trouvé (fallback HTML)."

                # Extraire snippets de 3 résultats max et les concaténer
                snippets = []
                for result in results[:3]:
                    snippet = result.css_first(".result__snippet")
                    if snippet:
                        text = snippet.text(strip=True)
                        if text:
                            snippets.append(text)

                logger.info(f"Trouvé {len(snippets)} snippets dans le HTML")
                merged = " ".join(snippets)
                # On renvoie un texte court (tronqué selon limites)
                return shorten_response(merged)
    except asyncio.TimeoutError:
        error_msg = "❌ Timeout lors de la recherche HTML."
        logger.error(error_msg)
        return error_msg
    except Exception as e:
        error_msg = f"❌ Erreur parsing HTML : {e}"
        logger.error(error_msg, exc_info=True)
        return error_msg