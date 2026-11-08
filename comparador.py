"""Búsqueda en vivo en el catálogo público VTEX de 10 tiendas y cruce del mismo producto entre ellas.

Port en Python de precioradar/vtex.mjs y lib.mjs (la versión Node local). Las reglas de cruce son las mismas:
1) mismo EAN; 2) misma marca + código de modelo (unido al EAN si otra tienda lo tiene); los combos y packs
no se cruzan por modelo; una tienda con precio a más de 2.2 veces de la mediana se separa.
"""
from __future__ import annotations

import hashlib
import re
import unicodedata
from collections import Counter
from concurrent.futures import ThreadPoolExecutor
from urllib.parse import quote

import requests

# Tiendas sin "Disallow: /api/" en su robots.txt (revisado el 2026-11-07). Excluidas porque lo prohíben:
# Coolbox, Tienda Claro, Real Plaza y Vivanda.
TIENDAS = [
    {"id": "plazavea", "nombre": "Plaza Vea", "host": "https://www.plazavea.com.pe"},
    {"id": "oechsle", "nombre": "Oechsle", "host": "https://www.oechsle.pe"},
    {"id": "promart", "nombre": "Promart", "host": "https://www.promart.pe"},
    {"id": "wong", "nombre": "Wong", "host": "https://www.wong.pe"},
    {"id": "metro", "nombre": "Metro", "host": "https://www.metro.pe"},
    {"id": "estilos", "nombre": "Estilos", "host": "https://www.estilos.com.pe"},
    {"id": "carsa", "nombre": "Carsa", "host": "https://www.carsa.pe"},
    {"id": "makro", "nombre": "Makro", "host": "https://www.makro.plazavea.com.pe"},
    {"id": "shopstar", "nombre": "Shopstar", "host": "https://www.shopstar.pe"},
    {"id": "electrolux", "nombre": "Electrolux", "host": "https://www.electrolux.com.pe"},
]
NOMBRE = {t["id"]: t["nombre"] for t in TIENDAS}
ORDEN = [t["id"] for t in TIENDAS]
POR_PAGINA = 50
AGENTE = "Mozilla/5.0 (compatible; PrecioRadar/0.2; comparador de precios)"
DESVIO_MAX = 2.2


def normalizar(s) -> str:
    s = unicodedata.normalize("NFD", str(s or ""))
    return "".join(c for c in s if not unicodedata.combining(c)).lower()


UNIDAD = re.compile(r"^\d+(?:[.,]\d+)?(GB|TB|MB|MP|HZ|KHZ|W|KW|L|LT|LTS|KG|G|GR|CM|MM|M|MAH|PULG|ML|V|BTU|RPM|LBS|OZ|PIES)$")
SUFIJO_REGION = re.compile(r"(GXPE|XPE|GXPR)$")


def codigo_modelo(texto) -> str | None:
    """Código de modelo dentro de un nombre: el token más largo que mezcla letras y números."""
    mejor = None
    for t in re.split(r"[^A-Z0-9\-/]+", str(texto or "").upper()):
        c = re.sub(r"[-/]", "", t)
        if len(c) < 6 or len(c) > 20 or not re.search(r"[A-Z]", c) or not re.search(r"\d", c):
            continue
        if UNIDAD.match(c) or re.match(r"^\d+X\d+", c):
            continue
        sin_region = SUFIJO_REGION.sub("", c)
        if len(sin_region) >= 6:
            c = sin_region
        if not mejor or len(c) > len(mejor):
            mejor = c
    return mejor


def ean_valido(e) -> bool:
    """EAN/UPC global. Los que empiezan con 2 son códigos internos de la tienda."""
    e = str(e or "")
    return bool(re.fullmatch(r"\d{8,14}", e)) and not e.startswith("2") and not re.fullmatch(r"0+", e)


def _imagen_chica(url):
    if not url:
        return None
    url = re.sub(r"^http:", "https:", url)
    return re.sub(r"/arquivos/ids/(\d+)(?:-\d+-\d+)?/", r"/arquivos/ids/\1-300-300/", url)


def registros(tienda: dict, p: dict) -> list[dict]:
    """Un registro por SKU disponible: el precio más bajo entre los vendedores de esa tienda."""
    items = p.get("items") or []
    salida = []
    for it in items:
        ofertas = [s.get("commertialOffer") for s in it.get("sellers") or []]
        ofertas = [o for o in ofertas if o and (o.get("Price") or 0) > 0
                   and ((o.get("AvailableQuantity") or 0) > 0 or o.get("IsAvailable"))]
        if not ofertas:
            continue
        o = min(ofertas, key=lambda x: x["Price"])
        nombre = re.sub(r"\s+", " ", it.get("nameComplete") or p.get("productName") or "").strip()
        combo = re.search(r"\b(combo|pack|kit|set)\b|\+", nombre, re.I)
        salida.append({
            "tienda": tienda["id"], "sku": str(it.get("itemId")), "nombre": nombre,
            "marca": (p.get("brand") or "").strip(),
            "ean": str(it["ean"]) if ean_valido(it.get("ean")) else None,
            "modelo": None if combo else (codigo_modelo(nombre) or codigo_modelo(p.get("productReference"))),
            "precio": float(o["Price"]),
            "precioLista": float(o["ListPrice"]) if (o.get("ListPrice") or 0) > o["Price"] else None,
            "imagen": _imagen_chica(((it.get("images") or [{}])[0]).get("imageUrl")),
            "enlace": (p.get("link") or "") + (f"?skuId={it.get('itemId')}" if len(items) > 1 else ""),
        })
    return salida


def buscar_en_tienda(tienda: dict, termino: str, timeout: float = 8) -> list[dict]:
    url = (f"{tienda['host']}/api/catalog_system/pub/products/search?ft={quote(termino)}"
           f"&_from=0&_to={POR_PAGINA - 1}")
    r = requests.get(url, headers={"User-Agent": AGENTE, "Accept": "application/json"}, timeout=timeout)
    if r.status_code == 404:
        return []
    r.raise_for_status()
    datos = r.json()
    return [reg for p in (datos if isinstance(datos, list) else []) for reg in registros(tienda, p)]


def buscar(termino: str) -> tuple[list[dict], list[str]]:
    """Consulta las 10 tiendas a la vez. Devuelve (productos agrupados, nombres de tiendas que fallaron)."""
    regs, fallas = [], []
    with ThreadPoolExecutor(max_workers=len(TIENDAS)) as ex:
        futuros = {ex.submit(buscar_en_tienda, t, termino): t for t in TIENDAS}
        for f, t in futuros.items():
            try:
                regs.extend(f.result())
            except Exception:  # noqa: BLE001 - una tienda caída no detiene la búsqueda
                fallas.append(t["nombre"])
    return agrupar(regs), fallas


# ---------- Cruce ----------
def _marca_norm(r) -> str:
    return re.sub(r"\s+", "", normalizar(r["marca"]))


def _mas_comun(valores):
    c = Counter(v for v in valores if v)
    return c.most_common(1)[0][0] if c else None


def muy_lejos(precio: float, precios: list[float]) -> bool:
    if len(precios) < 2:
        return False
    orden = sorted(precios)
    if len(orden) == 2:
        ref = orden[1] if precio == orden[0] else orden[0]
    else:
        ref = orden[len(orden) // 2]
    return precio / ref > DESVIO_MAX or ref / precio > DESVIO_MAX


def recalcular(p: dict) -> dict:
    p["ofertas"].sort(key=lambda o: (o["precio"], ORDEN.index(o["tienda"]) if o["tienda"] in ORDEN else 99))
    p["nombre"] = p["ofertas"][0]["nombre"] or p["nombre"]
    p["precioMin"] = p["ofertas"][0]["precio"]
    p["precioMax"] = p["ofertas"][-1]["precio"]
    p["descuento"] = max([0] + [round((1 - o["precio"] / o["precioLista"]) * 100)
                                for o in p["ofertas"] if o.get("precioLista")])
    return p


def _armar(clave: str, rs: list[dict]) -> dict:
    return recalcular({
        "id": hashlib.sha1(clave.encode()).hexdigest()[:10], "nombre": "",
        "marca": _mas_comun(r["marca"] for r in rs) or "",
        "imagen": next((r["imagen"] for r in rs if r.get("imagen")), None),
        "ofertas": [{k: r.get(k) for k in ("tienda", "precio", "precioLista", "enlace", "nombre")} for r in rs],
    })


def agrupar(regs: list[dict]) -> list[dict]:
    unicos = {}
    for r in regs:
        unicos.setdefault(f"{r['tienda']}:{r['sku']}", r)
    ean_por_modelo = {f"{_marca_norm(r)}:{r['modelo']}": r["ean"] for r in unicos.values() if r["ean"] and r["modelo"]}

    grupos: dict[str, list[dict]] = {}
    for r in unicos.values():
        clave = f"e:{r['ean']}" if r["ean"] else None
        if not clave and r["modelo"]:
            mk = f"{_marca_norm(r)}:{r['modelo']}"
            clave = f"e:{ean_por_modelo[mk]}" if mk in ean_por_modelo else f"m:{mk}"
        clave = clave or f"s:{r['tienda']}:{r['sku']}"
        grupos.setdefault(clave, []).append(r)

    productos = []
    for clave, rs in grupos.items():
        por_tienda = {}
        for r in rs:
            if r["tienda"] not in por_tienda or r["precio"] < por_tienda[r["tienda"]]["precio"]:
                por_tienda[r["tienda"]] = r
        ofertas = list(por_tienda.values())
        precios = [o["precio"] for o in ofertas]
        solos = [o for o in ofertas if muy_lejos(o["precio"], precios)]
        if len(ofertas) == 2 and solos:
            # Con dos tiendas y precios muy distintos no se sabe cuál es el producto correcto: van separados
            productos.extend(_armar(f"s:{o['tienda']}:{o['sku']}", [o]) for o in ofertas)
            continue
        productos.extend(_armar(f"s:{o['tienda']}:{o['sku']}", [o]) for o in solos)
        ofertas = [o for o in ofertas if o not in solos]
        if ofertas:
            productos.append(_armar(clave, ofertas))
    return productos


def relevantes(productos: list[dict], termino: str) -> list[dict]:
    """Deja los productos cuyo nombre o marca contiene todas las palabras buscadas (sin tildes)."""
    palabras = [w for w in normalizar(termino).split() if len(w) > 1]
    return [p for p in productos
            if all(w in normalizar(f"{p['marca']} {p['nombre']}") for w in palabras)] or productos
