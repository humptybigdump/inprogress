function SpecifViewSignal(Time,InpSig,OutSig);
% Create and then hide the GUI as it is being constructed.
f = figure('Visible','off','units','pix','Position',[520,354,595,280],'Name','Specify options');
% Construct the components.
set(f,'MenuBar','none');
ah1 = axes('Parent',f,'units','pixels',...
           'Position',[65 55 526 218]);
set([f,ah1],'Units','normalized');

       handle= plot(ah1,Time,InpSig,'-k',Time,OutSig,'-r');
       set(handle,'linewidth',1.5);
       t_tick=linspace(Time(1),Time(end),6);
       set(ah1,'XTick',t_tick);
       xlabel(ah1,'Time');
       ylabel(ah1,'Amplitude');
       leg1=legend(ah1,'Input signal','Output signal');
       set(leg1,'Location','NorthEastOutside');
 defaultBackground = get(0,'defaultUicontrolBackgroundColor');
set(f,'Color',defaultBackground )
% Move the GUI to the center of the screen.
movegui(f,'center')
% Make the GUI visible.
set(f,'NumberTitle','off','Name','Input/output signal')
set(f,'Visible','on');
      