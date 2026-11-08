"""Estilo Power Platform Pills (el de Píldora Studio / Power Academy) para las apps Streamlit.

Fuente única: Pocs/_tema/estilo_pills.py. Se copia igual en cada app con `python _tema/sincronizar.py`
(cada app debe funcionar sola, p. ej. al publicarla en Streamlit Cloud). No edites las copias.

Uso, justo después de st.set_page_config(...):
    import estilo_pills
    estilo_pills.aplicar()
    estilo_pills.cabecera("ParqueoCerca", "Playas de estacionamiento cerca de ti", "Lima y Callao")
"""
from __future__ import annotations

from html import escape

import streamlit as st

FUENTES = ("https://fonts.googleapis.com/css2?family=Saira+Condensed:wght@600;700;800"
           "&family=Outfit:wght@400;500;600;700&family=JetBrains+Mono:wght@400;600&display=swap")

CSS = """
@import url('%(fuentes)s');
:root {
  --pp-ink: #0b0f2a; --pp-ink-2: #1e0b3d; --pp-panel: #121738; --pp-panel-2: #181e47;
  --pp-line: #2a3170; --pp-line-2: #3a4290; --pp-fg: #ffffff; --pp-muted: #a9b0da; --pp-dim: #7880b3;
  --pp-cyan: #22d3ee; --pp-magenta: #e040fb; --pp-violet: #8b5cf6; --pp-amber: #ffb900;
  --pp-ok: #34d399; --pp-bad: #f87171; --pp-on-accent: #081028;
  --pp-display: 'Saira Condensed', 'Arial Narrow', Impact, sans-serif;
  --pp-body: 'Outfit', 'Segoe UI', system-ui, sans-serif;
  --pp-mono: 'JetBrains Mono', Consolas, ui-monospace, monospace;
}

/* ---------- Fondo y marco (se ve como app en el celular) ---------- */
html, body { background: var(--pp-ink); }
.stApp {
  background:
    radial-gradient(1200px 600px at 85%% -10%%, rgb(139 92 246 / .22), transparent 60%%),
    radial-gradient(900px 500px at -10%% 10%%, rgb(34 211 238 / .10), transparent 60%%),
    linear-gradient(180deg, var(--pp-ink) 0%%, var(--pp-ink-2) 140%%) fixed !important;
}
.stApp, .stApp p, .stApp li, .stApp input, .stApp textarea, .stApp button, .stApp label { font-family: var(--pp-body); }
[data-testid="stHeader"] { background: transparent !important; height: 0 !important; }
[data-testid="stDecoration"] { display: none !important; }
[data-testid="stMainBlockContainer"] {
  padding-top: 1.4rem !important; padding-bottom: 3rem !important;
  padding-left: max(16px, env(safe-area-inset-left, 0px)) !important;
  padding-right: max(16px, env(safe-area-inset-right, 0px)) !important;
}
@media (min-width: 900px) { [data-testid="stMainBlockContainer"] { padding-left: 2.5rem !important; padding-right: 2.5rem !important; } }
.stElementContainer:has(iframe[title*="streamlit_js_eval"]) { display: none !important; }

/* ---------- Títulos ---------- */
h1, h2, h3, h4 { font-family: var(--pp-display) !important; letter-spacing: .01em; line-height: 1.05 !important; text-wrap: balance; }
h1 { font-weight: 800 !important; }
h2, h3 { font-weight: 700 !important; }
a { color: var(--pp-cyan); }
[data-testid="stCaptionContainer"], .stCaption { color: var(--pp-muted) !important; }
code { font-family: var(--pp-mono) !important; }

/* Cabecera de marca */
.pp-cab { margin: 0 0 .4rem; }
.pp-eyebrow, .pp-label {
  font: 600 11.5px/1.2 var(--pp-mono); letter-spacing: .14em; text-transform: uppercase; color: var(--pp-cyan);
}
.pp-titulo {
  font: 800 clamp(2.3rem, 9vw, 3.4rem)/1 var(--pp-display); margin: .25rem 0 .2rem; color: var(--pp-fg);
  display: flex; align-items: center; gap: .5rem; flex-wrap: wrap;
}
.pp-titulo .pp-glow { color: var(--pp-cyan); text-shadow: 0 0 18px rgb(34 211 238 / .55); }
.pp-titulo .pp-ico { font-size: .72em; filter: drop-shadow(0 0 10px rgb(224 64 251 / .45)); }
.pp-lema { color: var(--pp-muted); margin: 0; font-size: 1rem; max-width: 60ch; }
.pp-barra { height: 3px; border-radius: 99px; margin-top: .8rem;
  background: linear-gradient(90deg, var(--pp-cyan), var(--pp-violet), var(--pp-magenta)); opacity: .9; }
.pp-top { display: flex; justify-content: space-between; align-items: center; gap: .6rem; flex-wrap: wrap; }
.pp-apagar { margin-left: auto; font: 600 12px var(--pp-mono); letter-spacing: .08em; }
.pp-apagar a { color: var(--pp-muted) !important; text-decoration: none; border: 1px solid var(--pp-line-2);
  border-radius: 999px; padding: .25rem .7rem; white-space: nowrap; }
.pp-apagar a:hover { color: var(--pp-bad) !important; border-color: var(--pp-bad); }

/* ---------- Botones ---------- */
.stButton button, .stDownloadButton button, .stLinkButton a, [data-testid="stFormSubmitButton"] button {
  border-radius: 10px !important; font-weight: 600 !important; min-height: 2.75rem;
  background: var(--pp-panel-2) !important; border: 1px solid var(--pp-line-2) !important; color: var(--pp-fg) !important;
  transition: border-color .15s, box-shadow .15s, transform .05s;
}
.stButton button:hover, .stDownloadButton button:hover, .stLinkButton a:hover, [data-testid="stFormSubmitButton"] button:hover {
  border-color: var(--pp-cyan) !important; box-shadow: 0 0 0 3px rgb(34 211 238 / .15);
}
.stButton button:active, .stLinkButton a:active { transform: translateY(1px); }
.stButton button[kind="primary"], .stDownloadButton button[kind="primary"], .stLinkButton a[kind="primary"],
[data-testid="stFormSubmitButton"] button, .stButton button[data-testid="stBaseButton-primary"] {
  background: linear-gradient(90deg, var(--pp-cyan), var(--pp-violet)) !important; border: 0 !important;
  color: var(--pp-on-accent) !important;
}
.stButton button[kind="primary"] p, [data-testid="stFormSubmitButton"] button p, .stLinkButton a[kind="primary"] p { color: var(--pp-on-accent) !important; font-weight: 700; }

/* Controles segmentados y pastillas */
[data-testid="stButtonGroup"] button { border-radius: 10px !important; min-height: 2.5rem; background: var(--pp-panel) !important;
  border: 1px solid var(--pp-line) !important; }
[data-testid="stButtonGroup"] button[aria-checked="true"] {
  background: linear-gradient(90deg, rgb(34 211 238 / .22), rgb(139 92 246 / .28)) !important;
  border-color: var(--pp-cyan) !important; box-shadow: 0 0 14px rgb(34 211 238 / .25);
}
[data-testid="stButtonGroup"] button[aria-checked="true"] p { color: var(--pp-fg) !important; font-weight: 700; }

/* ---------- Campos ---------- */
[data-baseweb="input"], [data-baseweb="select"] > div, [data-baseweb="textarea"], .stNumberInput [data-baseweb="input"] {
  background: var(--pp-ink) !important; border-radius: 10px !important; border-color: var(--pp-line-2) !important;
}
[data-baseweb="input"]:focus-within, [data-baseweb="select"] > div:focus-within, [data-baseweb="textarea"]:focus-within {
  border-color: var(--pp-cyan) !important; box-shadow: 0 0 0 3px rgb(34 211 238 / .18);
}
[data-baseweb="input"] input, [data-baseweb="textarea"] textarea { background: transparent !important; }
[data-testid="stWidgetLabel"] p { color: var(--pp-muted); font-weight: 500; }

/* ---------- Tarjetas, métricas, pestañas ---------- */
[data-testid="stVerticalBlockBorderWrapper"], .stVerticalBlock[data-testid="stVerticalBlock"][style*="border"],
div[data-testid="stLayoutWrapper"] > div[data-testid="stVerticalBlock"]:has(> div) {
  border-radius: 16px;
}
[data-testid="stMetric"] {
  background: rgb(18 23 56 / .75); border: 1px solid var(--pp-line); border-radius: 14px; padding: .7rem .9rem;
}
[data-testid="stMetricLabel"] p { font: 600 11px/1.2 var(--pp-mono) !important; letter-spacing: .12em; text-transform: uppercase; color: var(--pp-muted) !important; }
[data-testid="stMetricValue"] { font-family: var(--pp-display) !important; font-weight: 700; color: var(--pp-fg); }
[data-testid="stMetricValue"] > div { font-family: var(--pp-display) !important; }
[data-testid="stMetricDelta"] { font-family: var(--pp-mono); font-size: .8rem; }
.stTabs [data-baseweb="tab-list"] { gap: .25rem; border-bottom: 1px solid var(--pp-line); overflow-x: auto; scrollbar-width: none; }
.stTabs [data-baseweb="tab"] { font-family: var(--pp-display); font-weight: 700; font-size: 1.05rem; letter-spacing: .02em;
  padding: .5rem .8rem; border-radius: 10px 10px 0 0; white-space: nowrap; }
.stTabs [data-baseweb="tab"] p { font-family: var(--pp-display); font-size: 1.05rem; font-weight: 700; }
.stTabs [aria-selected="true"] { background: rgb(34 211 238 / .08); }
.stTabs [aria-selected="true"] p { color: var(--pp-cyan); }
.stTabs [data-baseweb="tab-highlight"] { background: linear-gradient(90deg, var(--pp-cyan), var(--pp-magenta)) !important; height: 3px; }
[data-testid="stExpander"] details { border-radius: 14px !important; border-color: var(--pp-line) !important; background: rgb(18 23 56 / .6); }
[data-testid="stExpander"] summary p { font-weight: 600; }
[data-testid="stAlert"] > div { border-radius: 12px; }
[data-testid="stDataFrame"], [data-testid="stTable"] { border-radius: 12px; overflow: hidden; }
[data-testid="stForm"] { border-radius: 16px; border-color: var(--pp-line) !important; background: rgb(18 23 56 / .45); }
hr { border-color: var(--pp-line) !important; }
[data-testid="stSidebar"] { background: rgb(6 12 47 / .92) !important; border-right: 1px solid var(--pp-line); }
.stProgress > div > div > div > div { background: linear-gradient(90deg, var(--pp-cyan), var(--pp-magenta)) !important; }

/* ---------- Piezas de resultado (tarjeta principal, lista, ubicación) ---------- */
.pp-ubic { display: flex; align-items: center; gap: .55rem; font-weight: 600; line-height: 1.25; min-height: 2.75rem; }
.pp-ubic .pp-pin { width: 2rem; height: 2rem; flex: none; display: grid; place-items: center; border-radius: 10px;
  background: rgb(34 211 238 / .12); border: 1px solid rgb(34 211 238 / .45); color: var(--pp-cyan); font-size: 1rem; }
.pp-ubic small { display: block; font: 600 10.5px/1.3 var(--pp-mono); letter-spacing: .12em; color: var(--pp-muted); text-transform: uppercase; }
.pp-card { position: relative; border-radius: 18px; padding: 1rem 1.05rem 1.05rem; overflow: hidden;
  background: linear-gradient(160deg, rgb(24 30 71 / .95), rgb(18 23 56 / .95));
  border: 1px solid var(--pp-line-2); box-shadow: 0 18px 40px -18px rgb(139 92 246 / .55); }
.pp-card::before { content: ""; position: absolute; inset: 0 0 auto 0; height: 3px;
  background: linear-gradient(90deg, var(--pp-cyan), var(--pp-violet), var(--pp-magenta)); }
.pp-card-nombre { font: 800 1.65rem/1.05 var(--pp-display); margin: .35rem 0 .15rem; color: var(--pp-fg); }
.pp-card-sub { color: var(--pp-muted); font-size: .88rem; }
.pp-cifra { display: flex; align-items: baseline; gap: .35rem; margin: .7rem 0 .15rem; color: var(--pp-cyan);
  font: 800 clamp(3.2rem, 15vw, 4.6rem)/.95 var(--pp-display); text-shadow: 0 0 26px rgb(34 211 238 / .45); }
.pp-cifra { flex-wrap: wrap; row-gap: .3rem; }
.pp-num { white-space: nowrap; }
.pp-cifra small { font: 700 .95rem/1 var(--pp-mono); letter-spacing: .08em; color: var(--pp-muted); text-shadow: none; }
.pp-cifra.pp-sin { font-size: 2rem; color: var(--pp-muted); text-shadow: none; }
.pp-metricas { display: grid; grid-template-columns: repeat(3, 1fr); gap: .45rem; margin-top: .75rem; }
.pp-metricas > div { background: rgb(11 15 42 / .7); border: 1px solid var(--pp-line); border-radius: 12px; padding: .5rem .6rem; min-width: 0; }
.pp-metricas small { display: block; font: 600 10px/1.2 var(--pp-mono); letter-spacing: .12em; color: var(--pp-muted); text-transform: uppercase; }
.pp-metricas b { display: block; font: 700 1.25rem/1.15 var(--pp-display); margin-top: .2rem; color: var(--pp-fg);
  white-space: nowrap; overflow: hidden; text-overflow: ellipsis; }
.pp-ok { color: var(--pp-ok) !important; } .pp-bad { color: var(--pp-bad) !important; } .pp-warn { color: var(--pp-amber) !important; }
.pp-nota { color: var(--pp-muted); font-size: .8rem; margin-top: .6rem; line-height: 1.45; }
.pp-nota b { color: var(--pp-fg); font-weight: 600; }
.pp-enlaces { display: grid; grid-template-columns: 1fr 1fr; gap: .45rem; margin-top: .8rem; }
.pp-btn { display: flex; align-items: center; justify-content: center; gap: .4rem; min-height: 2.9rem; border-radius: 12px;
  font-weight: 700; font-size: .92rem; text-decoration: none !important; color: var(--pp-fg) !important;
  background: var(--pp-panel-2); border: 1px solid var(--pp-line-2); }
.pp-btn:hover { border-color: var(--pp-cyan); box-shadow: 0 0 0 3px rgb(34 211 238 / .15); }
.pp-btn-primario { background: linear-gradient(90deg, var(--pp-cyan), var(--pp-violet)); border: 0; color: var(--pp-on-accent) !important; }
.pp-lista-cab { display: flex; justify-content: space-between; align-items: baseline; margin: .3rem 0 .45rem; }
.pp-lista { display: grid; grid-template-columns: minmax(0, 1fr); gap: .4rem; }
.pp-fila { background: rgb(18 23 56 / .78); border: 1px solid var(--pp-line); border-radius: 14px; }
.pp-fila[open] { border-color: var(--pp-cyan); background: rgb(24 30 71 / .95); }
.pp-fila summary { list-style: none; display: flex; align-items: center; gap: .65rem; padding: .65rem .75rem; cursor: pointer; }
.pp-fila summary::-webkit-details-marker { display: none; }
.pp-pos { flex: none; width: 1.8rem; height: 1.8rem; display: grid; place-items: center; border-radius: 9px;
  font: 700 .95rem/1 var(--pp-display); background: var(--pp-ink); border: 1px solid var(--pp-line-2); color: var(--pp-muted); }
.pp-info { flex: 1; min-width: 0; }
.pp-info b { display: block; font-size: .93rem; white-space: nowrap; overflow: hidden; text-overflow: ellipsis; }
.pp-info small { display: block; color: var(--pp-muted); font-size: .76rem; margin-top: .1rem; white-space: nowrap; overflow: hidden; text-overflow: ellipsis; }
.pp-precio { flex: none; text-align: right; font: 700 1.3rem/1 var(--pp-display); color: var(--pp-cyan); }
.pp-precio small { display: block; font: 600 .62rem/1.3 var(--pp-mono); color: var(--pp-muted); letter-spacing: .06em; }
.pp-precio.pp-sin { color: var(--pp-dim); font-size: 1rem; }
.pp-flecha { flex: none; color: var(--pp-dim); transition: transform .15s; font-size: .8rem; }
.pp-fila[open] .pp-flecha { transform: rotate(180deg); color: var(--pp-cyan); }
.pp-detalle { padding: 0 .75rem .75rem 3.2rem; font-size: .82rem; color: var(--pp-muted); line-height: 1.5; }
.pp-detalle .pp-enlaces { margin-top: .55rem; }
.pp-mas > summary { list-style: none; text-align: center; padding: .7rem; cursor: pointer; border-radius: 14px;
  border: 1px dashed var(--pp-line-2); font: 600 12px var(--pp-mono); letter-spacing: .14em; color: var(--pp-cyan); }
.pp-mas > summary::-webkit-details-marker { display: none; }
.pp-mas[open] > summary { display: none; }
.pp-mas[open] { display: grid; grid-template-columns: minmax(0, 1fr); gap: .4rem; }
.pp-pie { border-top: 1px solid var(--pp-line); margin-top: .6rem; padding-top: .7rem; color: var(--pp-dim); font-size: .74rem; line-height: 1.5; }

.st-key-pp_ubic [data-testid="stHorizontalBlock"] { flex-wrap: nowrap !important; gap: .5rem !important; }
.st-key-pp_ubic [data-testid="stColumn"] { min-width: 0 !important; }
.st-key-pp_ubic [data-testid="stColumn"]:last-child { flex: 0 0 3.4rem !important; width: 3.4rem !important; }

/* ---------- Celular ---------- */
@media (max-width: 640px) {
  [data-testid="stMainBlockContainer"] { padding-top: .9rem !important; }
  .stApp:has([data-testid="stSidebar"]) [data-testid="stMainBlockContainer"] { padding-top: 3.2rem !important; }
  [data-testid="stMetric"] { padding: .55rem .7rem; }
  [data-testid="stMetricValue"] { font-size: 1.6rem !important; }
  .stButton button, .stLinkButton a { min-height: 3rem; }   /* dedo, no mouse */
}
""" % {"fuentes": FUENTES}


def aplicar() -> None:
    """Inyecta el estilo. Va después de st.set_page_config."""
    st.html(f"<style>{CSS}</style>")
    # PWA ligera: en el celular, "Agregar a pantalla de inicio" la abre a pantalla completa y con color de marca
    st.html("""<script>
    (function(){ try { const d = window.parent && window.parent.document ? window.parent.document : document;
      const meta = (n, c) => { if (!d.querySelector(`meta[name="${n}"]`)) { const m = d.createElement('meta');
        m.name = n; m.content = c; d.head.appendChild(m); } };
      meta('theme-color', '#0b0f2a'); meta('mobile-web-app-capable', 'yes');
      meta('apple-mobile-web-app-capable', 'yes'); meta('apple-mobile-web-app-status-bar-style', 'black-translucent');
    } catch (e) {} })();
    </script>""", unsafe_allow_javascript=True)


def cabecera(nombre: str, lema: str = "", eyebrow: str = "", icono: str = "", apagar_id: str = "") -> None:
    """Cabecera de marca. El nombre se parte en dos tonos (p. ej. 'Parqueo' blanco + 'Cerca' cian)."""
    import os
    partes = _partir(nombre)
    titulo = escape(partes[0]) + (f'<span class="pp-glow">{escape(partes[1])}</span>' if partes[1] else "")
    ico = f'<span class="pp-ico">{icono}</span>' if icono else ""
    apagar = ""
    if apagar_id and os.environ.get("POCS_LANZADOR"):  # solo si la encendió el lanzador local de POCs
        apagar = (f'<div class="pp-apagar"><a href="{os.environ["POCS_LANZADOR"]}/apagar/{apagar_id}" '
                  'target="_self">⏻ APAGAR ESTA APP</a></div>')
    st.html('<header class="pp-cab"><div class="pp-top">'
            + f'<div class="pp-eyebrow">{escape(eyebrow)}</div>{apagar}</div>'
            + f'<h1 class="pp-titulo">{ico}<span>{titulo}</span></h1>'
            + (f'<p class="pp-lema">{escape(lema)}</p><div class="pp-barra"></div>' if lema else "")
            + '</header>')


def ubicacion(nombre: str, rotulo: str = "Buscando cerca de") -> None:
    st.html(f'<div class="pp-ubic"><span class="pp-pin">◎</span><div><small>{escape(rotulo)}</small>{escape(nombre)}</div></div>')


def _enlaces(enlaces: list[tuple[str, str]]) -> str:
    """[(texto, url), ...]; el primero va con el degradado de marca."""
    return '<div class="pp-enlaces">' + "".join(
        f'<a class="pp-btn{" pp-btn-primario" if i == 0 else ""}" href="{escape(url)}" target="_blank" rel="noopener">'
        f'{escape(texto)}</a>' for i, (texto, url) in enumerate(enlaces)) + "</div>"


def tarjeta(etiqueta: str, nombre: str, sub: str, cifra: str | None, unidad: str,
            metricas: list[tuple[str, str, str]], enlaces: list[tuple[str, str]], nota: str = "") -> None:
    """Resultado principal. metricas: [(rótulo, valor, clase css: ''|'pp-ok'|'pp-bad'|'pp-warn')]. nota admite <b>."""
    cifra_html = (f'<div class="pp-cifra"><span class="pp-num">{escape(cifra)}</span><small>{escape(unidad)}</small></div>' if cifra
                  else f'<div class="pp-cifra pp-sin">{escape(unidad)}</div>')
    mets = "".join(f'<div><small>{escape(r)}</small><b class="{c}">{escape(v)}</b></div>' for r, v, c in metricas)
    st.html(f'<div class="pp-card"><div class="pp-label">{escape(etiqueta)}</div>'
            f'<div class="pp-card-nombre">{escape(nombre)}</div><div class="pp-card-sub">{escape(sub)}</div>'
            f'{cifra_html}<div class="pp-metricas">{mets}</div>'
            + (f'<div class="pp-nota">{nota}</div>' if nota else "") + _enlaces(enlaces) + '</div>')


def lista(titulo: str, rotulo_precio: str, filas: list[dict], visibles: int = 5, inicio: int = 2) -> None:
    """filas: dict(nombre, sub, precio (str|None), precio_sub, detalle, enlaces=[(texto, url)]). Texto plano, se escapa."""
    def fila(i: int, f: dict) -> str:
        precio = (f'<div class="pp-precio">{escape(f["precio"])}<small>{escape(f.get("precio_sub", ""))}</small></div>'
                  if f.get("precio") else '<div class="pp-precio pp-sin">—</div>')
        return (f'<details class="pp-fila"><summary><span class="pp-pos">{i}</span>'
                f'<div class="pp-info"><b>{escape(f["nombre"])}</b><small>{escape(f["sub"])}</small></div>'
                f'{precio}<span class="pp-flecha">▼</span></summary>'
                f'<div class="pp-detalle">{escape(f.get("detalle", ""))}{_enlaces(f["enlaces"])}</div></details>')
    html = [fila(i, f) for i, f in enumerate(filas, start=inicio)]
    cuerpo = "".join(html[:visibles])
    if len(html) > visibles:
        cuerpo += f'<details class="pp-mas"><summary>VER {len(html) - visibles} MÁS ▾</summary>{"".join(html[visibles:])}</details>'
    st.html(f'<div class="pp-lista-cab"><span class="pp-label">{escape(titulo)}</span>'
            f'<span class="pp-label" style="color:var(--pp-muted)">{escape(rotulo_precio)}</span></div>'
            f'<div class="pp-lista">{cuerpo}</div>')


def pie(texto: str) -> None:
    st.html(f'<div class="pp-pie">{escape(texto)}</div>')


def _partir(nombre: str) -> tuple[str, str]:
    """'ParqueoCerca' -> ('Parqueo', 'Cerca'); 'MiAuto al Día' -> ('MiAuto ', 'al Día'); 'Devolución4ta' -> ('Devolución', '4ta')."""
    if " " in nombre:
        a, b = nombre.split(" ", 1)
        return a + " ", b
    for i in range(len(nombre) - 1, 0, -1):
        if nombre[i].isupper() or (nombre[i].isdigit() and not nombre[i - 1].isdigit()):
            return nombre[:i], nombre[i:]
    return nombre, ""
