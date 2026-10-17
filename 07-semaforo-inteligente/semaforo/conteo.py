"""Conteo de vehículos en una imagen con YOLOv8 preentrenado en COCO.

ultralytics se importa recién al contar, así el resto del proyecto (y las
pruebas) funciona sin instalarlo.
"""

# Clases de COCO que cuentan como vehículo.
CLASES_VEHICULO = {2: "auto", 3: "moto", 5: "bus", 7: "camión"}


def contar_vehiculos(imagen, modelo="yolov8n.pt", confianza=0.35):
    """Devuelve (total, detalle por tipo) de los vehículos en la imagen."""
    from ultralytics import YOLO

    resultado = YOLO(modelo)(imagen, conf=confianza, classes=list(CLASES_VEHICULO), verbose=False)[0]
    detalle = {}
    for clase in resultado.boxes.cls.tolist():
        tipo = CLASES_VEHICULO[int(clase)]
        detalle[tipo] = detalle.get(tipo, 0) + 1
    return sum(detalle.values()), detalle
