import asyncio
import aiohttp
from selectolax.parser import HTMLParser
from utils import shorten_response
import json
from config import WEB_STATE_FILE

def load_web_state() -> bool:
    try:
        with open(WEB_STATE_FILE, "r", encoding="utf-8") as f:
            data = json.load(f)
            return data.get("enabled", False)
    except FileNotFoundError:
        return False

def save_web_state(enabled: bool):
    with open(WEB_STATE_FILE, "w", encoding="utf-8") as f:
        json.dump({"enabled": enabled}, f, indent=2)

async def duckduckgo_search(query: str) -> str:
    url = f"https://api.duckduckgo.com/?q={query}&format=json&no_redirect=1&no_html=1"
    headers = {
        "Accept": "application/json",
        "User-Agent": "Mozilla/5.0"
    }

    try:
        async with aiohttp.ClientSession() as session:
            async with session.get(url, headers=headers, timeout=10) as resp:
                if resp.status == 200:
                    try:
                        data = await resp.json()
                    except aiohttp.ContentTypeError:
                        # Certains retours DDG renvoient application/x-javascript : fallback au HTML
                        return await duckduckgo_html_fallback(query)

                    if data.get("Abstract"):
                        return data["Abstract"]
                    elif data.get("Answer"):
                        return data["Answer"]
                    elif data.get("Definition"):
                        return data["Definition"]
                    else:
                        return await duckduckgo_html_fallback(query)
                else:
                    return f"❌ Erreur HTTP {resp.status} (API JSON)."
    except asyncio.TimeoutError:
        return "❌ Temps de réponse trop long (API JSON)."
    except Exception as e:
        return f"❌ Erreur réseau (API JSON) : {e}"

async def duckduckgo_html_fallback(query: str) -> str:
    url = f"https://html.duckduckgo.com/html/?q={query.replace(' ', '+')}"
    headers = {"User-Agent": "Mozilla/5.0"}

    try:
        async with aiohttp.ClientSession() as session:
            async with session.get(url, headers=headers, timeout=10) as resp:
                if resp.status != 200:
                    return f"❌ Erreur HTTP {resp.status} (fallback HTML)."

                html = await resp.text()
                tree = HTMLParser(html)
                results = tree.css(".result")

                if not results:
                    return "😶 Aucun résultat trouvé (fallback HTML)."

                # Extraire snippets de 3 résultats max et les concaténer
                snippets = []
                for result in results[:3]:
                    snippet = result.css_first(".result__snippet")
                    if snippet:
                        text = snippet.text(strip=True)
                        if text:
                            snippets.append(text)

                merged = " ".join(snippets)
                # On renvoie un texte court (tronqué selon limites)
                return shorten_response(merged)
    except asyncio.TimeoutError:
        return "❌ Timeout lors de la recherche HTML."
    except Exception as e:
        return f"❌ Erreur parsing HTML : {e}"