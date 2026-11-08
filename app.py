"""PrecioRadar (versión web): busca un producto en 10 tiendas del Perú y compara el precio del mismo producto."""
from __future__ import annotations

import os

import streamlit as st

import youtube
from comparador import NOMBRE, TIENDAS, buscar, relevantes

st.set_page_config(page_title="PrecioRadar", page_icon="📡", layout="centered")
import estilo_pills  # noqa: E402
estilo_pills.aplicar()

SUGERENCIAS = ["Televisor 55", "Freidora de aire", "Refrigeradora", "Laptop", "Audífonos",
               "Colchón", "Perfume", "Arroz", "Aceite", "Comida para perro"]


@st.cache_data(ttl=3 * 3600, show_spinner=False, max_entries=300)
def buscar_cache(termino: str):
    return buscar(termino)


def clave_youtube() -> str:
    """Clave de la YouTube Data API: en Streamlit Cloud va en Settings → Secrets (YOUTUBE_API_KEY = "...")."""
    try:
        return st.secrets.get("YOUTUBE_API_KEY", "") or os.environ.get("YOUTUBE_API_KEY", "")
    except Exception:  # noqa: BLE001 - sin archivo de secretos
        return os.environ.get("YOUTUBE_API_KEY", "")


@st.cache_data(ttl=24 * 3600, show_spinner=False, max_entries=500)
def video_cache(q: str) -> dict | None:
    try:
        return youtube.buscar_video(q, clave_youtube())
    except Exception:  # noqa: BLE001 - sin cuota o sin red: se muestra solo el enlace de búsqueda
        return None


def soles(x: float) -> str:
    return f"S/ {x:,.2f}".replace(".00", "")


estilo_pills.cabecera("PrecioRadar", lema="El mismo producto en 10 tiendas del Perú, del más barato al más caro.",
                      eyebrow="Comparador de precios · Perú", icono="📡", apagar_id="precioradar")

with st.form("busqueda", border=False):
    c1, c2 = st.columns([5, 1.3], vertical_alignment="bottom")
    escrito = c1.text_input("¿Qué buscas?", placeholder="Ej.: televisor samsung 55, freidora de aire…",
                            value=st.session_state.get("termino", st.query_params.get("q", "")))
    enviado = c2.form_submit_button("Buscar", type="primary", use_container_width=True)
if enviado:
    st.session_state.termino = escrito.strip()
    st.session_state.pop("sugerencia", None)

elegida = st.pills("Búsquedas populares", SUGERENCIAS, key="sugerencia", label_visibility="collapsed")
termino = (elegida or st.session_state.get("termino") or st.query_params.get("q", "")).strip()
if termino:
    st.query_params["q"] = termino  # enlace compartible: ...streamlit.app/?q=freidora+de+aire

if len(termino) < 3:
    st.html('<div class="pp-card"><div class="pp-label">Cómo funciona</div>'
            '<div class="pp-card-sub">Escribe un producto y lo buscamos en este momento en '
            + ", ".join(t["nombre"] for t in TIENDAS) +
            '. Juntamos el mismo producto (por código de barras o modelo) y te mostramos qué tienda lo vende más barato.'
            '</div></div>')
    estilo_pills.pie("Los precios vienen del catálogo público de cada tienda y pueden cambiar. Verifica en la tienda antes de comprar.")
    st.stop()

with st.spinner(f"Buscando «{termino}» en 10 tiendas…"):
    productos, fallas = buscar_cache(termino.lower())
productos = relevantes(productos, termino)

c1, c2 = st.columns(2)
vista = c1.segmented_control("Mostrar", ["En 2+ tiendas", "Todos"], default="En 2+ tiendas",
                             label_visibility="collapsed")
orden = c2.segmented_control("Ordenar", ["Mayor ahorro", "Menor precio"], default="Mayor ahorro",
                             label_visibility="collapsed")
comparables = [p for p in productos if len(p["ofertas"]) >= 2]
lista = comparables if vista != "Todos" and comparables else productos
if orden == "Menor precio":
    lista = sorted(lista, key=lambda p: p["precioMin"])
else:
    lista = sorted(lista, key=lambda p: (-len(p["ofertas"]), -(p["precioMax"] - p["precioMin"]), p["precioMin"]))

if fallas:
    st.caption(f"No respondieron: {', '.join(fallas)}.")
if not lista:
    st.info("No encontramos ese producto en las tiendas. Prueba con otras palabras (marca o modelo).")
    st.stop()
if vista != "Todos" and not comparables:
    st.caption("Ninguno de estos productos aparece en más de una tienda; te mostramos todos.")


def enlaces(p: dict, maximo: int = 10) -> list[tuple[str, str]]:
    return [(f"{NOMBRE[o['tienda']]} · {soles(o['precio'])}", o["enlace"]) for o in p["ofertas"][:maximo]]


mejor = lista[0]
n = len(mejor["ofertas"])
ahorro = mejor["precioMax"] - mejor["precioMin"]
estilo_pills.tarjeta(
    "Mejor comparación" if n > 1 else "Mejor resultado",
    mejor["nombre"], mejor["marca"] or "Sin marca",
    soles(mejor["precioMin"]), f"en {NOMBRE[mejor['ofertas'][0]['tienda']]}",
    [("Tiendas", str(n), ""),
     ("Ahorras", soles(ahorro) if n > 1 else "—", "pp-ok" if ahorro > 0 else ""),
     ("Descuento", f"{mejor['descuento']}%" if mejor["descuento"] else "—", "pp-warn" if mejor["descuento"] else "")],
    enlaces(mejor),
    nota=(f"Comparado con la tienda más cara (<b>{soles(mejor['precioMax'])}</b>)." if n > 1 else ""),
)
q_video = youtube.consulta(mejor["nombre"], mejor["marca"])
video = video_cache(q_video) if clave_youtube() else None
st.html('<div class="pp-lista-cab"><span class="pp-label">Video del producto</span>'
        '<span class="pp-label" style="color:var(--pp-muted)">YouTube</span></div>')
if video:
    st.video(video["url"])
    st.caption(f"**{video['titulo']}** · {video['canal']} · {youtube.vistas_legibles(video['vistas'])} vistas · {video['fecha']}")
    c1, c2 = st.columns(2)
    c1.link_button("▶ Abrir en YouTube", video["url"], type="primary", use_container_width=True)
    c2.link_button("Más reseñas", youtube.enlace_busqueda(q_video), use_container_width=True)
else:
    if mejor.get("imagen"):
        st.image(mejor["imagen"], width=160)
    st.link_button("▶ Ver reseñas y unboxing en YouTube", youtube.enlace_busqueda(q_video),
                   type="primary", use_container_width=True)

filas = [{
    "nombre": p["nombre"],
    "sub": f"{p['marca'] or 'Sin marca'} · {len(p['ofertas'])} tienda{'s' if len(p['ofertas']) > 1 else ''}",
    "precio": soles(p["precioMin"]),
    "precio_sub": f" hasta {soles(p['precioMax'])}" if len(p["ofertas"]) > 1 else f" en {NOMBRE[p['ofertas'][0]['tienda']]}",
    "detalle": (f"Ahorras {soles(p['precioMax'] - p['precioMin'])} comprando en {NOMBRE[p['ofertas'][0]['tienda']]}."
                if len(p["ofertas"]) > 1 else ""),
    "enlaces": enlaces(p) + [("▶ Video en YouTube", youtube.enlace_busqueda(youtube.consulta(p["nombre"], p["marca"])))],
} for p in lista[1:40]]
if filas:
    estilo_pills.lista(f"Otros {len(filas)} resultados", "Desde", filas, visibles=8)

estilo_pills.pie(f"{len(productos)} productos encontrados en vivo. Los precios vienen del catálogo público de cada tienda "
                 "y pueden cambiar; verifica en la tienda antes de comprar. Solo tiendas cuyo robots.txt permite su API.")
