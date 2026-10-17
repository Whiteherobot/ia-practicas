%% SISTEMA DIFUSO: Riesgo de accidentes

% Crear nuevo sistema tipo Mamdani
fis = mamfis('Name','RiesgoAccidente');

%% === VARIABLES DE ENTRADA ===

% Entrada 1: Intensidad del tráfico (0 a 20)
fis = addInput(fis,[0 20],'Name','intensidad_trafico');
fis = addMF(fis,'intensidad_trafico','trimf',[0 0 5],'Name','baja');
fis = addMF(fis,'intensidad_trafico','trimf',[3 8 10],'Name','media');
fis = addMF(fis,'intensidad_trafico','trimf',[8 20 20],'Name','alta');

% Entrada 2: Visibilidad (0 a 10)
fis = addInput(fis,[0 10],'Name','visibilidad');
fis = addMF(fis,'visibilidad','trimf',[0 0 3],'Name','mala');
fis = addMF(fis,'visibilidad','trimf',[2 5 7],'Name','media');
fis = addMF(fis,'visibilidad','trimf',[6 10 10],'Name','buena');

%% === VARIABLE DE SALIDA ===

% Salida: Riesgo de accidente (0 a 10)
fis = addOutput(fis,[0 10],'Name','riesgo_accidente');
fis = addMF(fis,'riesgo_accidente','trimf',[0 0 4],'Name','bajo');
fis = addMF(fis,'riesgo_accidente','trimf',[3 5 7],'Name','medio');
fis = addMF(fis,'riesgo_accidente','trimf',[6 10 10],'Name','alto');

%% === REGLAS DIFUSAS ===

% Tabla completa: con las 5 reglas originales, combinaciones como tráfico
% medio y visibilidad media no disparaban ninguna regla y evalfis devolvía 5.
ruleList = [
    1 1 2 1 1;   % baja & mala → medio
    1 2 1 1 1;   % baja & media → bajo
    1 3 1 1 1;   % baja & buena → bajo
    2 1 2 1 1;   % media & mala → medio
    2 2 2 1 1;   % media & media → medio
    2 3 1 1 1;   % media & buena → bajo
    3 1 3 1 1;   % alta & mala → alto
    3 2 3 1 1;   % alta & media → alto
    3 3 2 1 1;   % alta & buena → medio
];

fis = addRule(fis, ruleList);

%% === MOSTRAR SISTEMA ===
disp(fis)
% Opcional: abrir el editor visual
% fuzzy(fis)

%% === EVALUAR CASOS DE PRUEBA ===
% Caso: tráfico = 15, visibilidad = 2
entrada = [15 2];
salida = evalfis(fis, entrada);
fprintf('Entrada: intensidad_trafico = %.2f, visibilidad = %.2f\n', entrada(1), entrada(2));
fprintf('Resultado estimado de riesgo: %.2f\n', salida);

%% === VISUALIZACIONES ===
figure;
subplot(3,1,1); plotmf(fis,'input',1); title('Intensidad del Tráfico');
subplot(3,1,2); plotmf(fis,'input',2); title('Visibilidad');
subplot(3,1,3); plotmf(fis,'output',1); title('Riesgo de Accidente');
