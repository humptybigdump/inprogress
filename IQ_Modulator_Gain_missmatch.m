clear
clc
model = 'IQ_Modulator_with_imperfections.slx';
open_system(model);
% load_system(model);
spectrum_block = 'IQ_Modulator_with_imperfections/Complex Output Spectrum Analyzer';
% spectrum_block = 'IQ_Modulator_with_imperfections/Complex Output Power Density';
cfg = get_param(spectrum_block,'ScopeConfiguration');

iqblock = 'IQ_Modulator_with_imperfections/IQ Modulator';
set_param(iqblock, 'GainMismatch', '0');
set_param(iqblock, 'PhaseMismatch', '0');
sim(model);
% data = getMeasurementsData(cfg);
specTable = getSpectrumData(cfg);

for gain = ["0.1","0.2","1","5"]
    set_param(iqblock, 'GainMismatch', gain);
    sim(model);
    specTable = [specTable;getSpectrumData(cfg)];
end    
% get_param(iqblock,'DialogParameters')

%%
subplot(2,1,1);
hold on;
plot(specTable.FrequencyVector{1}/1e6, specTable.Spectrum{1}(:,2),'LineWidth',3);
plot(specTable.FrequencyVector{1}/1e6, specTable.Spectrum{1}(:,1),'LineWidth',3);
legend('Ideal','0 dB');
title('IQ Modulator Spectrum');
xlabel 'f in MHz';
ylabel 'dBm';
grid on;
subplot(2,1,2);
hold on;
plot(specTable.FrequencyVector{1}/1e6, specTable.Spectrum{1}(:,1)-specTable.Spectrum{1}(:,2),'LineWidth',3);
legend('0 dB');
title('IQ Modulator Error');
xlabel 'f in MHz';
ylabel 'dBm';
grid on;
%%
subplot(2,1,1);
plot(specTable.FrequencyVector{1}/1e6, specTable.Spectrum{2}(:,1),'LineWidth',3);
plot(specTable.FrequencyVector{1}/1e6, specTable.Spectrum{3}(:,1),'LineWidth',3);
plot(specTable.FrequencyVector{1}/1e6, specTable.Spectrum{4}(:,1),'LineWidth',3);
plot(specTable.FrequencyVector{1}/1e6, specTable.Spectrum{5}(:,1),'LineWidth',3);
legend('Ideal','0 dB','0.1 dB','0.2 dB','1 dB','5 dB');

subplot(2,1,2);
plot(specTable.FrequencyVector{1}/1e6, specTable.Spectrum{2}(:,1)-specTable.Spectrum{2}(:,2),'LineWidth',3);
plot(specTable.FrequencyVector{1}/1e6, specTable.Spectrum{3}(:,1)-specTable.Spectrum{3}(:,2),'LineWidth',3);
plot(specTable.FrequencyVector{1}/1e6, specTable.Spectrum{4}(:,1)-specTable.Spectrum{4}(:,2),'LineWidth',3);
plot(specTable.FrequencyVector{1}/1e6, specTable.Spectrum{5}(:,1)-specTable.Spectrum{5}(:,2),'LineWidth',3);
legend('0 dB','0.1 dB','0.2 dB','1 dB','5 dB');

