"""Video de reseña o unboxing de un producto con la API oficial de YouTube (YouTube Data API v3).

Sin clave de API solo se arma el enlace a la búsqueda en YouTube (no se consulta nada).
Costo por búsqueda: search.list (100 unidades) + videos.list (1). La cuota gratis es de 10 000 unidades al día,
unas 99 búsquedas; por eso la app guarda el resultado 24 horas.
"""
from __future__ import annotations

import re
from datetime import datetime, timedelta, timezone
from urllib.parse import quote_plus

import requests

API = "https://www.googleapis.com/youtube/v3"
MESES_ATRAS = 24          # "actual": publicado en los últimos 2 años
PALABRAS_VIDEO = "review | unboxing | reseña"
# Palabras que estorban en la búsqueda: colores, medidas sueltas y relleno de las tiendas
RUIDO = re.compile(r"\b(negro|negra|blanco|blanca|gris|plata|plateado|rojo|azul|dorado|color|nuevo|original|"
                   r"oferta|pack|combo|con|de|del|la|el|y|en|para)\b", re.I)


def consulta(nombre: str, marca: str = "") -> str:
    """'Freidora de Aire THOMAS 6L TH-AF60DNV Negro' -> 'Freidora Aire THOMAS 6L TH-AF60DNV'."""
    texto = re.sub(r"\(.*?\)|[|,\"“”]", " ", nombre)
    texto = RUIDO.sub(" ", texto)
    palabras = texto.split()[:7]
    if marca and marca.lower() not in " ".join(palabras).lower():
        palabras.insert(0, marca)
    return " ".join(palabras)


def enlace_busqueda(q: str) -> str:
    return f"https://www.youtube.com/results?search_query={quote_plus(q + ' review unboxing')}"


def buscar_video(q: str, clave: str, timeout: float = 8) -> dict | None:
    """Entre los videos relevantes de los últimos 2 años, el de más vistas. None si no hay ninguno."""
    desde = (datetime.now(timezone.utc) - timedelta(days=30 * MESES_ATRAS)).strftime("%Y-%m-%dT%H:%M:%SZ")
    r = requests.get(f"{API}/search", timeout=timeout, params={
        "key": clave, "part": "snippet", "type": "video", "maxResults": 15, "order": "relevance",
        "q": f"{q} {PALABRAS_VIDEO}", "publishedAfter": desde, "relevanceLanguage": "es",
        "regionCode": "PE", "safeSearch": "moderate", "videoEmbeddable": "true"})
    r.raise_for_status()
    ids = [it["id"]["videoId"] for it in r.json().get("items", []) if it.get("id", {}).get("videoId")]
    if not ids:
        return None
    r = requests.get(f"{API}/videos", timeout=timeout, params={
        "key": clave, "part": "snippet,statistics", "id": ",".join(ids)})
    r.raise_for_status()
    videos = [{
        "id": v["id"],
        "titulo": v["snippet"]["title"],
        "canal": v["snippet"]["channelTitle"],
        "fecha": v["snippet"]["publishedAt"][:10],
        "vistas": int(v.get("statistics", {}).get("viewCount", 0)),
    } for v in r.json().get("items", [])]
    if not videos:
        return None
    mejor = max(videos, key=lambda v: (v["vistas"], v["fecha"]))
    mejor["url"] = f"https://www.youtube.com/watch?v={mejor['id']}"
    return mejor


def vistas_legibles(n: int) -> str:
    if n >= 1_000_000:
        return f"{n / 1_000_000:.1f} M".replace(".0 ", " ")
    if n >= 1_000:
        return f"{n / 1_000:.0f} mil"
    return str(n)
