from comparador import agrupar, codigo_modelo, ean_valido, relevantes


def reg(tienda, sku, precio, **extra):
    r = {"tienda": tienda, "sku": str(sku), "precio": precio, "nombre": f"Producto {sku}", "marca": "Samsung",
         "ean": None, "modelo": None, "precioLista": None, "imagen": None, "enlace": f"https://{tienda}/p"}
    r.update(extra)
    return r


def test_codigo_modelo():
    assert codigo_modelo('Televisor Samsung 55" UN55M70HAGXPE Mini LED 4K') == "UN55M70HA"
    assert codigo_modelo("Celular Galaxy A56 5G 256GB") is None
    assert codigo_modelo("Refrigeradora INDURAMA 529L No Frost RI-795DI") == "RI795DI"


def test_ean_valido():
    assert ean_valido("8806099059231")
    assert not ean_valido("2022000000276")
    assert not ean_valido("undefined")
    assert not ean_valido("")


def test_agrupar_por_ean_y_modelo():
    ps = agrupar([
        reg("plazavea", 1, 100, ean="8806099059231", modelo="UN55M70HA"),
        reg("oechsle", 2, 90, modelo="UN55M70HA", marca="SAMSUNG"),
        reg("promart", 3, 120, ean="8806099059231"),
        reg("promart", 4, 50),
    ])
    assert len(ps) == 2
    tv = next(p for p in ps if len(p["ofertas"]) == 3)
    assert [o["tienda"] for o in tv["ofertas"]] == ["oechsle", "plazavea", "promart"]
    assert (tv["precioMin"], tv["precioMax"]) == (90, 120)


def test_agrupar_precio_mas_bajo_por_tienda():
    [p] = agrupar([reg("wong", 1, 100, ean="7750000000001"), reg("wong", 2, 80, ean="7750000000001")])
    assert len(p["ofertas"]) == 1 and p["precioMin"] == 80


def test_agrupar_separa_precio_lejano():
    e = {"ean": "7750000000002"}
    ps = agrupar([reg("plazavea", 1, 900, **e), reg("oechsle", 2, 950, **e), reg("promart", 3, 2999, **e)])
    assert len(ps) == 2
    assert len(agrupar([reg("plazavea", 1, 49, **e), reg("oechsle", 2, 139, **e)])) == 2


def test_relevantes():
    ps = [{"marca": "Oster", "nombre": "Freidora de Aire 5L", "ofertas": []},
          {"marca": "Oster", "nombre": "Licuadora", "ofertas": []}]
    assert len(relevantes(ps, "freidora aire")) == 1
    assert len(relevantes(ps, "zzz")) == 2  # sin coincidencias se devuelve todo
