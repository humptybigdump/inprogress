clear; 
close all; 
clc;

% Nina Kunze, Janne Grofmeyer
% Temperatur, Niederschlag und Wolkenbedeckung

%% Daten einlesen
data = readtable('Temperatur.csv', 'Delimiter', ';', 'HeaderLines', 1, 'VariableNamingRule', 'preserve', 'Format', '%*s%s');
temp_str = data{:, 1};

% Dezimalkommas durch Punkte ersetzen und in einen numerischen Vektor konvertieren
temp_numeric = str2double(strrep(temp_str, ',', '.'));

% Zeitvektor ab dem 4.8. 00:00 Uhr
num_data_points = height(data);
start_time = datetime(2025, 8, 4, 0, 0, 0);
time_stamps = start_time + hours(0:num_data_points-1);

% Plot
figure;
plot(time_stamps, temp_numeric, 'LineWidth', 1.5, 'Color', [0.8500 0.3250 0.0980]);
title('Stündlicher Temperaturverlauf 04.08.-15.08.25', 'FontSize', 13);
xlabel('Datum und Uhrzeit', 'FontSize', 11);
ylabel('Temperatur (°C)', 'FontSize', 11);
grid on;

%Legende
legend('Temperatur', 'Location', 'best');

% Achsenlimits
xlim([min(time_stamps) max(time_stamps)]);
ylim([floor(min(temp_numeric)) - 1, ceil(max(temp_numeric)) + 1]);

%% Niederschlagsdaten einlesen

opts_prcp = detectImportOptions('Niederschlag.csv', 'Delimiter', ';');
opts_prcp = setvartype(opts_prcp, [1, 5], 'string');
niederschlagData = readtable('Niederschlag.csv', opts_prcp);

% Konvertieren des Datums-Strings in ein Datumsformat
prcpData = struct();
prcpData.date = datetime(niederschlagData{:, 1}, 'InputFormat', 'yyyy-MM-dd HH:mm:ss');
% Konvertieren der Dezimalwerte in Zahlen
prcpData.prcp = str2double(strrep(niederschlagData{:, 5}, ',', '.'));
% Filtern des Datumsbereichs
prcpFiltered = prcpData.date >= datetime('2025-08-04') & prcpData.date <= datetime('2025-08-15');
prcpData.date = prcpData.date(prcpFiltered);
prcpData.prcp = prcpData.prcp(prcpFiltered);

%% Wolkenbedeckungsdaten einlesen

opts_cloud = detectImportOptions('Wolkenbedeckung.csv', 'Delimiter', ';');
opts_cloud = setvartype(opts_cloud, 1, 'string'); % Erste Spalte als String einlesen
wolkenData = readtable('Wolkenbedeckung.csv', opts_cloud);
cloudData = struct();
% Entfernen des Endpunkts und Konvertieren
cleanDates = strrep(wolkenData{:, 1}, '.', '');
cloudData.Datum = datetime(strcat(cleanDates, '2025'), 'InputFormat', 'ddMMyyyy');
% Extrahieren des numerischen Werts aus dem String 'x/8'
cloudData.cloudCoverage = str2double(strrep(wolkenData{:, 2}, '/8', ''));
% Filtern des Datumsbereichs
cloudFiltered = cloudData.Datum >= datetime('2025-08-04') & cloudData.Datum <= datetime('2025-08-15');
cloudData.Datum = cloudData.Datum(cloudFiltered);
cloudData.cloudCoverage = cloudData.cloudCoverage(cloudFiltered);

% Plot
figure('Color', [1 1 1]);

% Linke y-Achse
yyaxis left;
plot(prcpData.date, prcpData.prcp, 'Color', 'b', 'LineWidth', 2);
ylabel('Niederschlag (mm)');
ax = gca;
ax.YColor = 'b';
ax.YLim = [0, 20];

% Rechte y-Achse
yyaxis right;
plot(cloudData.Datum, cloudData.cloudCoverage, 'Color', 'k', 'LineWidth', 2);
ylabel('Wolkenbedeckung (in Achteln)');
ax = gca;
ax.YColor = 'k';
ax.YLim = [0, 8];

% Titel und Legende
title('Niederschlag und Wolkenbedeckung', 'FontSize', 14);
xlabel('Datum', 'FontSize', 12);
legend('Niederschlag', 'Wolkenbedeckung', 'Location', 'northeast');

% Achsen formatieren und Gitter hinzufügen
grid on;
ax.XTick = prcpData.date; % jeder Tag ein Tick hat
xtickformat('dd.MM.'); % nicht Jahr anzeigen
xtickangle(45);
