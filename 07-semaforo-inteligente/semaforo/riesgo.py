"""Sistema difuso de la práctica 6: riesgo de accidente en la intersección
según la cantidad de vehículos y la visibilidad (ver ../06-logica-difusa)."""

from .difuso import Regla, SistemaMamdani, Variable

TRAFICO = Variable("trafico", (0, 20), {"baja": (0, 0, 5), "media": (3, 8, 10), "alta": (8, 20, 20)})
VISIBILIDAD = Variable("visibilidad", (0, 10), {"mala": (0, 0, 3), "media": (2, 5, 7), "buena": (6, 10, 10)})
RIESGO = Variable("riesgo", (0, 10), {"bajo": (0, 0, 4), "medio": (3, 5, 7), "alto": (6, 10, 10)})

# Las cinco reglas de la práctica (marcadas con *) dejaban combinaciones sin
# regla, como tráfico medio con visibilidad media. Se completó la tabla
# manteniendo la idea: más tráfico y menos visibilidad, más riesgo.
#
#                 mala     media    buena
#   baja         medio*    bajo     bajo*
#   media        medio*   medio     bajo
#   alta         alto*     alto    medio*
TABLA = {
    "baja": {"mala": "medio", "media": "bajo", "buena": "bajo"},
    "media": {"mala": "medio", "media": "medio", "buena": "bajo"},
    "alta": {"mala": "alto", "media": "alto", "buena": "medio"},
}

SISTEMA = SistemaMamdani(
    [TRAFICO, VISIBILIDAD],
    RIESGO,
    [Regla({"trafico": t, "visibilidad": v}, r) for t, fila in TABLA.items() for v, r in fila.items()],
)


def riesgo_accidente(vehiculos, visibilidad):
    """Riesgo de 0 a 10. Más de 20 vehículos cuentan como 20 (tope del rango)."""
    return SISTEMA.evaluar(trafico=min(vehiculos, 20), visibilidad=visibilidad)


def nivel(riesgo):
    """Etiqueta con mayor pertenencia: "bajo", "medio" o "alto"."""
    grados = RIESGO.pertenencia(riesgo)
    return max(grados, key=grados.get)
