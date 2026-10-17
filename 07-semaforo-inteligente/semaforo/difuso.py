"""Motor de inferencia difusa Mamdani, el mismo esquema que el Fuzzy Logic
Toolbox de MATLAB con sus opciones por defecto: AND = mínimo, implicación =
mínimo, agregación = máximo y desdifusión por centroide."""

from dataclasses import dataclass, field

import numpy as np


def trimf(x, a, b, c):
    """Función de pertenencia triangular con vértices a <= b <= c (como trimf)."""
    x = np.asarray(x, dtype=float)
    subida = np.where(b > a, (x - a) / (b - a if b > a else 1), (x >= b).astype(float))
    bajada = np.where(c > b, (c - x) / (c - b if c > b else 1), (x <= b).astype(float))
    return np.clip(np.minimum(subida, bajada), 0.0, 1.0)


@dataclass
class Variable:
    nombre: str
    rango: tuple
    conjuntos: dict = field(default_factory=dict)  # etiqueta -> (a, b, c)

    def pertenencia(self, valor):
        """Grado de pertenencia de `valor` a cada conjunto."""
        return {etiqueta: float(trimf(valor, *abc)) for etiqueta, abc in self.conjuntos.items()}

    def universo(self, puntos=1001):
        return np.linspace(*self.rango, puntos)


@dataclass
class Regla:
    antecedentes: dict  # variable de entrada -> etiqueta
    consecuente: str  # etiqueta de la salida


class SistemaMamdani:
    def __init__(self, entradas, salida, reglas):
        self.entradas = {v.nombre: v for v in entradas}
        self.salida = salida
        self.reglas = reglas
        for regla in reglas:
            for nombre, etiqueta in regla.antecedentes.items():
                if etiqueta not in self.entradas[nombre].conjuntos:
                    raise ValueError(f"{nombre} no tiene el conjunto {etiqueta!r}")
            if regla.consecuente not in salida.conjuntos:
                raise ValueError(f"{salida.nombre} no tiene el conjunto {regla.consecuente!r}")

    def activaciones(self, valores):
        """Grado con que se dispara cada regla para las entradas dadas."""
        for nombre, valor in valores.items():
            minimo, maximo = self.entradas[nombre].rango
            if not minimo <= valor <= maximo:
                raise ValueError(f"{nombre} = {valor} está fuera de [{minimo}, {maximo}]")
        grados = {n: v.pertenencia(valores[n]) for n, v in self.entradas.items()}
        return [min(grados[n][e] for n, e in r.antecedentes.items()) for r in self.reglas]

    def evaluar(self, **valores):
        x = self.salida.universo()
        agregado = np.zeros_like(x)
        for regla, fuerza in zip(self.reglas, self.activaciones(valores)):
            recorte = np.minimum(fuerza, trimf(x, *self.salida.conjuntos[regla.consecuente]))
            agregado = np.maximum(agregado, recorte)
        if agregado.sum() == 0:
            # Ninguna regla se dispara: MATLAB devuelve el centro del rango.
            return float(np.mean(self.salida.rango))
        return float((x * agregado).sum() / agregado.sum())
