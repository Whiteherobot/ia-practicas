import numpy as np
import pytest

from semaforo.difuso import Regla, SistemaMamdani, Variable, trimf
from semaforo.riesgo import TABLA, nivel, riesgo_accidente


def test_trimf_como_matlab():
    x = np.array([0, 2.5, 5, 7.5, 10])
    assert trimf(x, 0, 5, 10).tolist() == [0, 0.5, 1, 0.5, 0]
    # Hombros: a == b o b == c dejan el borde en 1.
    assert trimf(x, 0, 0, 5).tolist() == [1, 0.5, 0, 0, 0]
    assert trimf(x, 5, 10, 10).tolist() == [0, 0, 0, 0.5, 1]


def test_caso_de_la_practica():
    # fuzzy.m evaluaba tráfico 15 con visibilidad 2: solo se dispara
    # "alta y mala -> alto" con fuerza 1/3, y el centroide queda en 8.31.
    assert riesgo_accidente(15, 2) == pytest.approx(8.31, abs=0.01)
    assert nivel(riesgo_accidente(15, 2)) == "alto"


def test_la_tabla_cubre_todas_las_combinaciones():
    assert {t: set(f) for t, f in TABLA.items()} == {t: {"mala", "media", "buena"} for t in ("baja", "media", "alta")}
    # Antes, tráfico medio con visibilidad media no tenía regla.
    assert nivel(riesgo_accidente(8, 5)) == "medio"


ORDEN = {"bajo": 0, "medio": 1, "alto": 2}


# El centroide de Mamdani no es monótono punto a punto (cuando una sola regla
# se debilita, el centroide de su conjunto recortado se corre), pero el nivel
# de riesgo sí tiene que serlo.
@pytest.mark.parametrize("visibilidad", [0, 2.5, 5, 7.5, 10])
def test_mas_trafico_nunca_baja_el_nivel(visibilidad):
    niveles = [ORDEN[nivel(riesgo_accidente(v, visibilidad))] for v in range(0, 21)]
    assert niveles == sorted(niveles)


@pytest.mark.parametrize("vehiculos", [0, 5, 10, 15, 20])
def test_mas_visibilidad_nunca_sube_el_nivel(vehiculos):
    niveles = [ORDEN[nivel(riesgo_accidente(vehiculos, v / 2))] for v in range(0, 21)]
    assert niveles == sorted(niveles, reverse=True)


def test_mas_de_20_vehiculos_cuentan_como_20():
    assert riesgo_accidente(35, 4) == riesgo_accidente(20, 4)


def test_entradas_fuera_de_rango_y_reglas_mal_escritas():
    with pytest.raises(ValueError, match="fuera de"):
        riesgo_accidente(5, 11)
    x = Variable("x", (0, 1), {"poco": (0, 0, 1)})
    with pytest.raises(ValueError, match="no tiene el conjunto"):
        SistemaMamdani([x], x, [Regla({"x": "mucho"}, "poco")])


def test_sin_reglas_disparadas_devuelve_el_centro_del_rango():
    x = Variable("x", (0, 10), {"bajo": (0, 0, 2)})
    y = Variable("y", (0, 10), {"alto": (8, 10, 10)})
    assert SistemaMamdani([x], y, [Regla({"x": "bajo"}, "alto")]).evaluar(x=9) == 5
