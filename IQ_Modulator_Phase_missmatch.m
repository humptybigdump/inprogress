clear
clc
model = 'IQ_Modulator_with_imperfections.slx';
open_system(model);
% load_system(model);
spectrum_block = 'IQ_Modulator_with_imperfections/Complex Output Spectrum Analyzer';
% spectrum_block = 'IQ_Modulator_with_imperfections/Complex Output Power Density';
cfg = get_param(spectrum_block,'ScopeConfiguration');

iqblock = 'IQ_Modulator_with_imperfections/IQ Modulator';
set_param(iqblock, 'PhaseMismatch', '0');
set_param(iqblock, 'GainMismatch', '0');
sim(model);
data = getMeasurementsData(cfg);
specTable = getSpectrumData(cfg);

for phase = ['2','4','8','90']
    set_param(iqblock, 'PhaseMismatch', phase);
    sim(model);
    data = [data;getMeasurementsData(cfg)];
    specTable = [specTable;getSpectrumData(cfg)];
end    
% get_param(iqblock,'DialogParameters')

%%
subplot(2,1,1);
hold on;
plot(specTable.FrequencyVector{1}/1e6, specTable.Spectrum{1}(:,2),'LineWidth',3,"Color","#A2142F");
plot(specTable.FrequencyVector{1}/1e6, specTable.Spectrum{1}(:,1),'LineWidth',3,"Color","#0072BD");
legend('Ideal','0°');
title('IQ Modulator Spectrum');
xlabel 'f in MHz';
ylabel 'dBm';
grid on;

subplot(2,1,2);
hold on;
plot(specTable.FrequencyVector{1}/1e6, specTable.Spectrum{1}(:,1)-specTable.Spectrum{1}(:,2),'LineWidth',3,"Color","#0072BD");
legend('0°');
title('IQ Modulator Error');
xlabel 'f in MHz';
ylabel 'dBm';
grid on;
%%
subplot(2,1,1);
plot(specTable.FrequencyVector{1}/1e6, specTable.Spectrum{2}(:,1),'LineWidth',3,"Color","#EDB120");
plot(specTable.FrequencyVector{1}/1e6, specTable.Spectrum{3}(:,1),'LineWidth',3,"Color","#7E2F8E");
plot(specTable.FrequencyVector{1}/1e6, specTable.Spectrum{4}(:,1),'LineWidth',3,"Color","#77AC30");
plot(specTable.FrequencyVector{1}/1e6, specTable.Spectrum{5}(:,1),'LineWidth',3,"Color","#D95319");
legend('Ideal','0°','2°','4°','8°','90°');

subplot(2,1,2);
plot(specTable.FrequencyVector{1}/1e6, specTable.Spectrum{2}(:,1)-specTable.Spectrum{2}(:,2),'LineWidth',3,"Color","#EDB120");
plot(specTable.FrequencyVector{1}/1e6, specTable.Spectrum{3}(:,1)-specTable.Spectrum{3}(:,2),'LineWidth',3,"Color","#7E2F8E");
plot(specTable.FrequencyVector{1}/1e6, specTable.Spectrum{4}(:,1)-specTable.Spectrum{4}(:,2),'LineWidth',3,"Color","#77AC30");
plot(specTable.FrequencyVector{1}/1e6, specTable.Spectrum{5}(:,1)-specTable.Spectrum{5}(:,2),'LineWidth',3,"Color","#D95319");
legend('0°','2°','4°','8°','90°');
