# Semáforo inteligente

Proyecto final del curso: un semáforo de dos sentidos que reparte el tiempo de
verde según cuántos vehículos esperan en cada uno.

1. **Conteo** (`semaforo/conteo.py`): YOLOv8 preentrenado en COCO cuenta autos,
   motos, buses y camiones en una foto de cada sentido.
2. **Riesgo** (`semaforo/riesgo.py`): el sistema difuso Mamdani de la práctica 6
   estima el riesgo de accidente (0 a 10) a partir del total de vehículos y la
   visibilidad.
3. **Ciclo** (`semaforo/ciclo.py`): en un ciclo de 60 s, el verde se reparte en
   proporción a la cola de cada sentido, con un mínimo de 12 s, y el riesgo
   alarga el "todo rojo" de despeje entre fases de 1 a 4 s.

La parte en Unity del proyecto, una intersección simulada que reparte el verde
con la misma regla, está en
[unity-simulacion-semaforo](https://github.com/Whiteherobot/unity-simulacion-semaforo).

El motor difuso (`semaforo/difuso.py`) está escrito con numpy y reproduce lo que
hace `evalfis` de MATLAB con las opciones por defecto (mínimo, máximo y
centroide).

## Uso

```bash
pip install -r requirements.txt
python -m semaforo --conteo 14 3 --visibilidad 2
```

```
Riesgo de accidente: 8.31 (alto)
Fase         Segundos
Verde A          35.0
Amarillo A        3.0
Todo rojo         3.5
Verde B          12.0
Amarillo B        3.0
Todo rojo         3.5
Ciclo            60.0
```

Con fotos en lugar de conteos (descarga `yolov8n.pt` la primera vez):

```bash
pip install -r requirements-deteccion.txt
python -m semaforo --imagenes sentido_a.jpg sentido_b.jpg --visibilidad 6
```

Para probar se pueden usar imágenes del dataset
[Vehicles de Roboflow 100](https://universe.roboflow.com/roboflow-100/vehicles-q0x2v)
(CC BY 4.0), el mismo que se usó en la práctica de lógica difusa.

## Pruebas

```bash
pip install pytest
pytest
```

Comprueban el motor difuso contra el caso de la práctica (tráfico 15 y
visibilidad 2 dan 8.31), que la tabla de reglas cubra todas las combinaciones,
que más tráfico o menos visibilidad nunca bajen el nivel de riesgo y que el
plan siempre sume el ciclo y respete el verde mínimo.
