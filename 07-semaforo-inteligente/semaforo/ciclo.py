"""Reparto del ciclo de un semáforo de dos sentidos (A y B)."""

from dataclasses import dataclass

from .riesgo import nivel, riesgo_accidente

CICLO = 60  # segundos
VERDE_MINIMO = 12
AMARILLO = 3


@dataclass(frozen=True)
class Plan:
    verde_a: float
    verde_b: float
    amarillo: float
    todo_rojo: float
    riesgo: float
    nivel: str

    @property
    def ciclo(self):
        return self.verde_a + self.verde_b + 2 * (self.amarillo + self.todo_rojo)


def _medio_segundo(valor):
    return round(valor * 2) / 2


def planificar(vehiculos_a, vehiculos_b, visibilidad, ciclo=CICLO, verde_minimo=VERDE_MINIMO, amarillo=AMARILLO):
    """Reparte el verde en proporción a los vehículos de cada sentido.

    El riesgo difuso alarga el "todo rojo" (los segundos en que los dos
    sentidos están en rojo para despejar la intersección) de 1 a 4 s. Cada
    sentido recibe al menos `verde_minimo`, aunque no tenga vehículos.
    """
    if vehiculos_a < 0 or vehiculos_b < 0:
        raise ValueError("La cantidad de vehículos no puede ser negativa.")

    riesgo = riesgo_accidente(vehiculos_a + vehiculos_b, visibilidad)
    todo_rojo = _medio_segundo(1 + 3 * riesgo / 10)
    verde_total = ciclo - 2 * (amarillo + todo_rojo)
    if verde_total < 2 * verde_minimo:
        raise ValueError(f"Un ciclo de {ciclo} s no alcanza para dos verdes de {verde_minimo} s.")

    total = vehiculos_a + vehiculos_b
    proporcion = 0.5 if total == 0 else vehiculos_a / total
    verde_a = _medio_segundo(proporcion * verde_total)
    verde_a = min(max(verde_a, verde_minimo), verde_total - verde_minimo)
    return Plan(verde_a, verde_total - verde_a, amarillo, todo_rojo, round(riesgo, 2), nivel(riesgo))
