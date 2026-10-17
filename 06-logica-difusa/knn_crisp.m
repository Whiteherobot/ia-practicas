%% Clasificación Crisp con KNN

% === Datos de entrada ===
X = [
    3 9;
    15 2;
    6 3;
    10 7;
    1 10;
    18 1
];

% Etiquetas de clase
Y = [1; 3; 2; 2; 1; 3];

% === Entrenamiento del modelo KNN ===
mdlKNN = fitcknn(X, Y, 'NumNeighbors', 3);

% === Predicción con los mismos datos ===
Ypred = predict(mdlKNN, X);

% === Mostrar resultados ===
disp('Predicciones vs Reales:');
disp(table(Y, Ypred, 'VariableNames', {'Real','Predicho'}));

% === Calcular precisión ===
accuracy = sum(Y == Ypred) / length(Y);
fprintf('Precisión total del modelo (entrenamiento): %.2f%%\n', accuracy * 100);

% === Visualización del espacio de decisión ===

% Crear malla de puntos para graficar el espacio
x1range = linspace(min(X(:,1)) - 1, max(X(:,1)) + 1, 100);
x2range = linspace(min(X(:,2)) - 1, max(X(:,2)) + 1, 100);
[X1Grid, X2Grid] = meshgrid(x1range, x2range);
gridPoints = [X1Grid(:), X2Grid(:)];

% Predicción para cada punto de la malla
YGridPred = predict(mdlKNN, gridPoints);
YGridPred = reshape(YGridPred, size(X1Grid));

% Definir colores para cada clase
colors = lines(max(Y)); % paleta de colores

% Crear figura
figure;
hold on;

% Dibujar fondo de clasificación (espacio de decisión)
for classIdx = 1:max(Y)
    mask = (YGridPred == classIdx);
    scatter(X1Grid(mask), X2Grid(mask), 10, colors(classIdx,:), ...
        'filled', 'MarkerFaceAlpha', 0.1);
end

% Dibujar puntos reales con círculos
for classIdx = 1:max(Y)
    idxReal = (Y == classIdx);
    scatter(X(idxReal,1), X(idxReal,2), 100, colors(classIdx,:), ...
        'o', 'filled', 'DisplayName', sprintf('Clase %d Real', classIdx));
end

% Dibujar predicciones con cruces
for classIdx = 1:max(Y)
    idxPred = (Ypred == classIdx);
    scatter(X(idxPred,1), X(idxPred,2), 100, colors(classIdx,:), ...
        'x', 'LineWidth', 2, 'DisplayName', sprintf('Clase %d Predicho', classIdx));
end

% Etiquetas y detalles
xlabel('X1');
ylabel('X2');
title('Clasificación KNN (Crisp)');
legend('Location','bestoutside');
grid on;
hold off;
