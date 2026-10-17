# ia-practicas

[![CI](https://github.com/Whiteherobot/ia-practicas/actions/workflows/ci.yml/badge.svg)](https://github.com/Whiteherobot/ia-practicas/actions/workflows/ci.yml)

Prácticas de Inteligencia Artificial (abril-julio de 2025), hechas en pareja con
Michael Franco. Van del análisis exploratorio de datos a redes convolucionales y
lógica difusa, y terminan en un proyecto que junta visión por computador y
control difuso.

| Carpeta | Qué hay |
|---|---|
| [01-analisis-exploratorio](01-analisis-exploratorio) | Análisis exploratorio del dataset Heart Disease: tipos de variables, estadísticas, correlaciones y datos faltantes. |
| [02-knn-heart-disease](02-knn-heart-disease) | Pipeline de transformación de variables y clasificación con KNN, comparando métricas de distancia y valores de K. Incluye el informe y la presentación. |
| [03-neurona-y-xor](03-neurona-y-xor) | Una neurona con activación propia y su gradiente, una red desde cero para XOR de 4 entradas y el backpropagation hecho a mano en Excel. |
| [04-knn-vs-red-neuronal](04-knn-vs-red-neuronal) | El mismo problema de clasificación resuelto con KNN y con una red en Keras, con curvas de entrenamiento y comparación de métricas. |
| [05-cnn-food101](05-cnn-food101) | Clasificación de platos de Food-101 con una CNN desde cero y con transfer learning (MobileNetV2); matriz de confusión y comparación del entrenamiento. |
| [06-logica-difusa](06-logica-difusa) | Sistema Mamdani en MATLAB que estima el riesgo de accidente en una intersección según el tráfico y la visibilidad, y un KNN "crisp" para comparar. |
| [07-semaforo-inteligente](07-semaforo-inteligente) | Proyecto final: YOLOv8 cuenta los vehículos de cada sentido y el sistema difuso de la práctica 6, pasado a Python, ayuda a repartir el ciclo del semáforo. Con pruebas. |

Los notebooks se dejaron con sus salidas, tal como se entregaron, para que se
puedan leer en GitHub sin ejecutarlos.

## De dónde sale

El repo (antes `IA`) era la carpeta entera del curso: además de nuestro trabajo
tenía las diapositivas, guías y notebooks de ejemplo del docente, exportaciones
HTML de cada notebook y fotos de prueba bajadas de internet y de WhatsApp. En
2026 se quitó todo lo que no era nuestro o no tenía licencia clara, se ordenó una
carpeta por práctica y el proyecto final, que había quedado en un boceto (un
`detect.py` vacío y un submódulo de yolov5 roto), se terminó como un programa
que funciona y tiene pruebas. También se completó la tabla de reglas del sistema
difuso, que con 5 reglas dejaba combinaciones sin cubrir.

## Autores

- Michael Lata ([@Whiteherobot](https://github.com/Whiteherobot))
- Michael Franco ([@michfranko](https://github.com/michfranko))

Licencia MIT.
