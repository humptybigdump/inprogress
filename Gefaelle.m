clear;
close all;
clc;

% Nina Kunze, Janne Grofmeyer
% Gefälle Ammer und Goldersbach

%% Daten einlesen
opts = detectImportOptions('GPSW.csv', 'DecimalSeparator', ',');
data = readtable('GPSW.csv', opts);

x_all = data{:,6};               % Distanz entlang der Strecke [m]
y_all = data{:,9};               % Höhe [m]
wassertiefe_all = data{:,12};    % Wassertiefe [cm]

% Umrechnen in m
wassertiefe_all = wassertiefe_all ./ 100;

%% Daten Ammer (Zeilen 1–36)

x = x_all(1:36);
y = y_all(1:36);
wassertiefe = wassertiefe_all(1:36);

% Zeile 15 rausnehmen
x(15) = [];            % geht 1m hoch an M2, macht kein Sinn
y(15) = [];
wassertiefe(15) = [];

% Wasseroberfläche berechnen
wasserOberflaeche = y + wassertiefe;

%% Daten Goldersbach (Zeile 40-55)

xG = x_all(40:55);
yG = y_all(40:55);
wassertiefeG = wassertiefe_all(40:55);

% Zeile 5
xG(5) = [];             
yG(5) = [];            % passt nicht, da hat das Messgerät auch gesponnen
wassertiefeG(5) = [];

% Wasseroberfläche berechnen
wasserOberflaecheG = yG + wassertiefeG;



%% Gesamt Längsprofil Ammer

figure('Position', [100, 100, 1000, 400]);  % [links, unten, Breite, Höhe]

subplot(1,2,1); 
hold on;

% Wasserfüllung schattieren
fill([x; flipud(x)], [y; flipud(wasserOberflaeche)], 'c','FaceAlpha', 0.3, 'EdgeColor','none');

% Flussbett
plot(x, y, 'k-', 'LineWidth', 1.5);

% Wasseroberfläche
plot(x, wasserOberflaeche, 'b-', 'LineWidth', 1.5);

% Gesamtgefälle-Linie
plot([x(1), x(end)], [y(1), y(end)], 'r', 'LineWidth', 1.5);

xlabel('Distanz [m]');
ylabel('Höhe über MSL [m]');
title('Längsprofil entlang der Messstrecke der Ammer');
legend('Wasser','Flussbett','Wasseroberfläche','Gesamtgefälle: -4.03 ‰','Location','southwest');
grid on;

% Messstellen markieren
x_messstellen = [438.409, 1763.555, 3477.429, 4472.345];
for i = 1:length(x_messstellen)
    xline(x_messstellen(i), '--k', ['M', num2str(i)], ...
        'LabelHorizontalAlignment','center', 'LabelOrientation','horizontal','HandleVisibility','off');
end


% Gesamtsteigung berechnen
total_dy = y(end) - y(1);        % Gesamter Höhenunterschied
total_dx = x(end) - x(1);        % Gesamtdistanz
total_slope = (total_dy / total_dx) * 1000;
disp(['Gesamtsteigung gesamt: ', num2str(total_slope), ' ‰']);



% Goldersbach Längsprofil
subplot(1,2,2); 
hold on;

fill([xG; flipud(xG)], [yG; flipud(wasserOberflaecheG)], 'c','FaceAlpha',0.3,'EdgeColor','none');

plot(xG, yG, 'k-', 'LineWidth', 1.5);
plot(xG, wasserOberflaecheG, 'b-', 'LineWidth', 1.5);
plot([xG(1), xG(end)], [yG(1), yG(end)], 'r', 'LineWidth', 1.5);

xlabel('Distanz [m]');
ylabel('Höhe über MSL [m]');
title('Längsprofil entlang der Messstrecke Goldersbach');
legend('Wasser','Flussbett','Wasseroberfläche','Gesamtgefälle: -6.37 ‰','Location','southwest');
grid on;

total_slope5 = (yG(end) - yG(1)) / (xG(end) - xG(1)) * 1000;
disp(['Gefälle Goldersbach: ', num2str(total_slope5), ' ‰']);




%% Längsprofile einzelne Abschnitte

figure('Position',[100 100 800 500]); % Figure vergrößern

% Abschnitte definieren
abschnitte = {
    struct('name','M0–M1','range',[0, 438.409])
    struct('name','M1–M2','range',[438.409, 1763.555])
    struct('name','M2–M3','range',[1763.555, 3477.429])
    struct('name','M3–M4','range',[3477.429, 4472.345])
};

% Plot-Handles für die Legende
leg_handles = [];

for i = 1:length(abschnitte)
    idx = x > abschnitte{i}.range(1) & x <= abschnitte{i}.range(2);
    xi = x(idx);
    yi = y(idx);
    wi = wassertiefe(idx);
    wasserOberflaeche = yi + wi;

    h = subplot(2,2,i); % 2x2 Subplots
    hold on;

    % oben Platz für Legende
    pos = h.Position;
    pos(4) = pos(4)*0.95;    % Höhe verkleinern
    pos(2) = pos(2) - 0.03; % Subplot etwas nach unten verschieben
    h.Position = pos;       % neue Position setzen


    % Wasser schattieren
    h_fill = fill([xi; flipud(xi)], [yi; flipud(wasserOberflaeche)], 'c', 'FaceAlpha',0.3,'EdgeColor','none');

    % Flussbett
    h_bett = plot(xi, yi, 'k-', 'LineWidth', 1.5);

    % Wasseroberfläche
    h_wasser = plot(xi, wasserOberflaeche, 'b-', 'LineWidth', 1.5);

    % Gesamtgefälle-Linie
    h_slope = plot([xi(1), xi(end)], [yi(1), yi(end)], 'r', 'LineWidth', 1.5);

    xlabel('Distanz [m]');
    ylabel('Höhe über MSL [m]');
    title(['Längsprofil ', abschnitte{i}.name]);
    grid on;

    total_slope = (yi(end) - yi(1)) / (xi(end) - xi(1)) * 1000;
    disp(['Gefälle ', abschnitte{i}.name, ': ', num2str(total_slope), ' ‰']);

    % nur einmal die Handles für die gemeinsame Legende speichern
    if i == 1
        leg_handles = [h_fill, h_bett, h_wasser, h_slope];
    end
end

% Gemeinsame Legende in der Figure

lgd = legend(leg_handles, ...
    {'Wasser','Flussbett','Wasseroberfläche','Gesamtgefälle'}, ...
    'Orientation','horizontal');

lgd.Position = [0.3 0.93 0.4 0.07]; % [x y width height] -> anpassen bis mittig
