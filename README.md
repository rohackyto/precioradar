# PrecioRadar (versión web en Streamlit)

Busca un producto **en este momento** en 10 tiendas del Perú (Plaza Vea, Oechsle, Promart, Wong, Metro, Estilos, Carsa, Makro, Shopstar y Electrolux), junta el mismo producto por código de barras o modelo y muestra qué tienda lo vende más barato, con enlace a cada una.

Es la versión publicable de `Pocs/precioradar` (Node, local). Esta no tiene recolector ni historial de precios: Streamlit Cloud no guarda archivos entre reinicios. Las búsquedas se guardan en caché 3 horas.

```bash
pip install -r requirements.txt
streamlit run app.py
```

Enlace directo a una búsqueda: `?q=freidora+de+aire`.

- `comparador.py`: lectura del catálogo público VTEX y cruce de productos (port de `vtex.mjs` + `lib.mjs`).
- `estilo_pills.py` y `.streamlit/config.toml`: estilo Píldora Studio, copiados desde `Pocs/_tema` con `sincronizar.py`.

Solo se consultan tiendas cuyo `robots.txt` no prohíbe `/api/` (revisado el 7 de noviembre de 2026). Antes de monetizar, pedir permiso a las tiendas o usar sus programas de afiliados.
