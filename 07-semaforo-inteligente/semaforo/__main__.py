"""Uso:
    python -m semaforo --conteo 14 3 --visibilidad 2
    python -m semaforo --imagenes sentido_a.jpg sentido_b.jpg --visibilidad 7
"""

import argparse

from .ciclo import CICLO, planificar


def main(argv=None):
    parser = argparse.ArgumentParser(prog="semaforo", description="Reparte el ciclo de un semáforo de dos sentidos.")
    origen = parser.add_mutually_exclusive_group(required=True)
    origen.add_argument("--conteo", nargs=2, type=int, metavar=("A", "B"), help="vehículos en cada sentido")
    origen.add_argument("--imagenes", nargs=2, metavar=("A", "B"), help="una foto de cada sentido (usa YOLOv8)")
    parser.add_argument("--visibilidad", type=float, required=True, help="de 0 (nula) a 10 (perfecta)")
    parser.add_argument("--ciclo", type=float, default=CICLO, help=f"duración del ciclo en segundos (por defecto {CICLO})")
    args = parser.parse_args(argv)

    if args.conteo:
        a, b = args.conteo
    else:
        from .conteo import contar_vehiculos

        (a, detalle_a), (b, detalle_b) = (contar_vehiculos(img) for img in args.imagenes)
        print(f"Sentido A: {a} vehículos {detalle_a}")
        print(f"Sentido B: {b} vehículos {detalle_b}")

    plan = planificar(a, b, args.visibilidad, ciclo=args.ciclo)
    print(f"Riesgo de accidente: {plan.riesgo:.2f} ({plan.nivel})")
    print(f"{'Fase':<12}{'Segundos':>9}")
    for fase, segundos in (
        ("Verde A", plan.verde_a),
        ("Amarillo A", plan.amarillo),
        ("Todo rojo", plan.todo_rojo),
        ("Verde B", plan.verde_b),
        ("Amarillo B", plan.amarillo),
        ("Todo rojo", plan.todo_rojo),
    ):
        print(f"{fase:<12}{segundos:>9.1f}")
    print(f"{'Ciclo':<12}{plan.ciclo:>9.1f}")


if __name__ == "__main__":
    main()
