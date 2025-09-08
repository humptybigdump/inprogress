function [type_estimate]=SpecifCalcOpt(type_estimate1)
% Create and then hide the GUI as it is being constructed.
f = figure('Visible','off','units','pix','Position',[520,656,413,144],'Name','Specify options');
% Construct the components.
set(f,'MenuBar','none');
htypeestbuttongroup = uibuttongroup( 'Title','Type of estimation','units','pix','Position',[15,41,387,102]);
hradiosmoothest = uicontrol(htypeestbuttongroup,...
     'units','pix','Style','radiobutton',...
     'String','Smooth estimate',...
     'Position',[14,57,135,23]);
hradiocondreal = uicontrol(htypeestbuttongroup,'Style','radiobutton',...
     'String','Conditional realisations',...
     'Position',[14,35,135,23]);
hradiocondrealsmoothest= uicontrol(htypeestbuttongroup,'Style','radiobutton',...
     'String','Conditional realisations with estimate of smoothness parameter',...
     'Position',[14,12,355,23]);
hok = uicontrol('Style','pushbutton','String','OK',...
     'Position',[15,12,118,24],...
     'Callback',{@okbutton_Callback});
hpreviouschoice = uicontrol('Style','pushbutton','String','Previous choice',...
     'Position',[146,12,118,24],...
     'Callback',{@previouschoicebutton_Callback});
hcancel = uicontrol('Style','pushbutton',...
     'String','Cancel',...
     'Position',[283,12,118,24],...
     'Callback',{@cancelbutton_Callback});
set([f,hok,hcancel,hpreviouschoice,htypeestbuttongroup,...
     hradiosmoothest, hradiocondreal, hradiocondrealsmoothest],'Units','normalized');
defaultBackground = get(0,'defaultUicontrolBackgroundColor');
set(f,'Color',defaultBackground )
% Move the GUI to the center of the screen.
movegui(f,'center')
% Make the GUI visible.
switch type_estimate1
    case 'sm'
         set(htypeestbuttongroup,'selectedobject',hradiosmoothest)
    case 'cr'
         set(htypeestbuttongroup,'selectedobject',hradiocondreal)
    case 'cr+'
         set(htypeestbuttongroup,'selectedobject',hradiocondrealsmoothest)
end
set(f,'NumberTitle','off','Name','Input data')
set(f,'Visible','on');
function previouschoicebutton_Callback(source,eventdata)
switch type_estimate1
    case 'sm'
         set(htypeestbuttongroup,'selectedobject',hradiosmoothest)
    case 'cr'
         set(htypeestbuttongroup,'selectedobject',hradiocondreal)
    case 'cr+'
         set(htypeestbuttongroup,'selectedobject',hradiocondrealsmoothest)
end
end
function cancelbutton_Callback(source,eventdata)
type_estimate=type_estimate1;
close(gcbf)
end
function okbutton_Callback(source,eventdata)
switch findobj(get(htypeestbuttongroup,'selectedobject'))
    case hradiosmoothest
         type_estimate='sm'; %not specified format of time
    case  hradiocondreal
         type_estimate='cr'; %matlab time
    case hradiocondrealsmoothest
         type_estimate='cr+'; 
end
close(gcbf)
end
if ishghandle(f)
  % Go into uiwait if the figure handle is still valid.
  % This is mostly the case during regular use.
  uiwait(f);
end
end