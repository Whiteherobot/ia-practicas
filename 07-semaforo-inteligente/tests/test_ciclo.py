import pytest

from semaforo.__main__ import main
from semaforo.ciclo import planificar


@pytest.mark.parametrize("a,b,visibilidad", [(14, 3, 2), (0, 0, 9), (5, 5, 5), (1, 30, 0), (20, 0, 10)])
def test_el_plan_ocupa_el_ciclo_y_respeta_el_minimo(a, b, visibilidad):
    plan = planificar(a, b, visibilidad)
    assert plan.ciclo == 60
    assert plan.verde_a >= 12 and plan.verde_b >= 12


def test_el_verde_sigue_a_la_demanda():
    assert planificar(10, 5, 8).verde_a > planificar(5, 10, 8).verde_a
    parejo = planificar(6, 6, 8)
    assert parejo.verde_a == parejo.verde_b


def test_sin_vehiculos_reparte_por_igual():
    plan = planificar(0, 0, 10)
    assert plan.verde_a == plan.verde_b


def test_mas_riesgo_mas_todo_rojo():
    seguro = planificar(1, 1, 10)
    riesgoso = planificar(10, 8, 1)
    assert seguro.nivel == "bajo" and riesgoso.nivel == "alto"
    assert 1 <= seguro.todo_rojo < riesgoso.todo_rojo <= 4


def test_un_sentido_vacio_igual_recibe_el_minimo():
    plan = planificar(18, 0, 6)
    assert plan.verde_b == 12


def test_errores():
    with pytest.raises(ValueError, match="negativa"):
        planificar(-1, 3, 5)
    with pytest.raises(ValueError, match="no alcanza"):
        planificar(3, 3, 5, ciclo=30)


def test_linea_de_comandos(capsys):
    main(["--conteo", "14", "3", "--visibilidad", "2"])
    salida = capsys.readouterr().out
    assert "Riesgo de accidente: 8.31 (alto)" in salida
    assert "Verde A          35.0" in salida
    assert "Ciclo            60.0" in salida
