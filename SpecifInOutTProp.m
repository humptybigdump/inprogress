function [time_format,time_units,ini_conc,mean_subs]=SpecifInOutTProp(time_format1,time_units1,ini_conc1,mean_subs1)
% Create and then hide the GUI as it is being constructed.
f = figure('Visible','off','units','pix','Position',[520,560,468,240],'Name','Specify options');
% Construct the components.
set(f,'MenuBar','none');
htimepropertiespanel = uipanel('units','pix','Title','Time properties',...
     'Position',[10,51,251,178]);
hinoutpropertiespanel = uipanel('units','pix','Title','Input/output properties',...
     'Position',[269,51,186,178]);
htimeformatbuttongroup = uibuttongroup(htimepropertiespanel,...
     'Title','Time format','units','pix','Position',[11,13,109,145]);
htimeunitsbuttongroup = uibuttongroup(htimepropertiespanel,...
     'Title','Time units','units','pix','Position',[128,13,109,145]);
hiniconcentrbuttongroup = uibuttongroup(hinoutpropertiespanel,...
     'Title','Initial concentration','units','pix','Position',[11,88,162,71]);
hmeansubstrbuttongroup = uibuttongroup(hinoutpropertiespanel,...
     'Title','Mean substraction','units','pix','Position',[11,11,162,71]);
hradionotspecif = uicontrol(htimeformatbuttongroup,...
     'units','pix','Style','radiobutton',...
     'String','Not specified',...
     'Position',[9,96,87,23]);
hradiomatlab = uicontrol(htimeformatbuttongroup,'Style','radiobutton',...
     'String','Matlab time',...
     'Position',[9,72,87,23]);
hradiounix = uicontrol(htimeformatbuttongroup,'Style','radiobutton',...
     'String','Unix time',...
     'Position',[9,48,87,23]);
hradioexcel= uicontrol(htimeformatbuttongroup,'Style','radiobutton',...
     'String','Excel time',...
     'Position',[9,23,87,23]);
hradiodays = uicontrol('Style','radiobutton',...
     'String','Days','parent',htimeunitsbuttongroup,...
     'Position',[9,96,87,23]);
hradiohours = uicontrol('Style','radiobutton',...
     'String','Hours','parent',htimeunitsbuttongroup,...
     'Position',[9,72,87,23]);
hradiominutes = uicontrol('Style','radiobutton',...
     'String','Minutes','parent',htimeunitsbuttongroup,...
     'Position',[9,48,87,23]);
hradioseconds= uicontrol('Style','radiobutton',...
     'String','Seconds','parent',htimeunitsbuttongroup,...
     'Position',[9,23,87,23]);
hradionattracer = uicontrol('Style','radiobutton',...
     'String','Natural tracer, c0<>0','parent',hiniconcentrbuttongroup,...
     'Position',[9,32,139,23]);
hradioarttracer = uicontrol('Style','radiobutton',...
     'String','Artificial tracer, c0=0','parent',hiniconcentrbuttongroup,...
     'Position',[9,11,139,23]);
hradiosubstr = uicontrol('Style','radiobutton',...
     'String','Substract','parent',hmeansubstrbuttongroup,...
     'Position',[9,32,139,23]);
hradionotsubstr = uicontrol('Style','radiobutton',...
     'String','Do not substract','parent',hmeansubstrbuttongroup,...
     'Position',[9,11,139,23]);
hok = uicontrol('Style','pushbutton','String','OK',...
     'Position',[14,17,118,24],...
     'Callback',{@okbutton_Callback});
hpreviouschoice = uicontrol('Style','pushbutton','String','Previous choice',...
     'Position',[145,17,118,24],...
     'Callback',{@previouschoicebutton_Callback});
hcancel = uicontrol('Style','pushbutton',...
     'String','Cancel',...
     'Position',[282,17,118,24],...
     'Callback',{@cancelbutton_Callback});
set([f,hok,hcancel,hpreviouschoice,...
     htimepropertiespanel,hinoutpropertiespanel,htimeformatbuttongroup,...
     htimeunitsbuttongroup, hiniconcentrbuttongroup, hmeansubstrbuttongroup,...
     hradionotspecif, hradiomatlab, hradiounix, hradioexcel,hradiodays, ...
     hradiohours, hradiominutes, hradioseconds, hradionattracer, hradioarttracer, hradiosubstr ...
     hradionotsubstr],'Units','normalized');
defaultBackground = get(0,'defaultUicontrolBackgroundColor');
set(f,'Color',defaultBackground )
% Move the GUI to the center of the screen.
movegui(f,'center')
% Make the GUI visible.
switch time_format1
    case 'n'
         set(htimeformatbuttongroup,'selectedobject',hradionotspecif)
    case 'm'
         set(htimeformatbuttongroup,'selectedobject',hradiomatlab)
    case 'u'
         set(htimeformatbuttongroup,'selectedobject',hradiounix)
    case 'e'
         set(htimeformatbuttongroup,'selectedobject',hradioexcel)
end
switch time_units1
    case 'd'; 
         set(htimeunitsbuttongroup,'selectedobject',hradiodays)
    case 'h'; 
         set(htimeunitsbuttongroup,'selectedobject',hradiohours)
    case 'm'; 
         set(htimeunitsbuttongroup,'selectedobject',hradiominutes)
    case 's';  
         set(htimeunitsbuttongroup,'selectedobject',hradioseconds)
end
switch ini_conc1
    case 1; 
         set(hiniconcentrbuttongroup,'selectedobject',hradionattracer)
    case 0; 
         set(hiniconcentrbuttongroup,'selectedobject',hradioarttracer)
end
switch mean_subs1
    case 'S'; 
         set(hmeansubstrbuttongroup,'selectedobject',hradiosubstr)
    case 'NS'; 
         set(hmeansubstrbuttongroup,'selectedobject',hradionotsubstr)
end
set(f,'NumberTitle','off','Name','Input data')
set(f,'Visible','on');
function previouschoicebutton_Callback(source,eventdata)
switch time_format1
    case 'n'
         set(htimeformatbuttongroup,'selectedobject',hradionotspecif)
    case 'm'
         set(htimeformatbuttongroup,'selectedobject',hradiomatlab)
    case 'u'
         set(htimeformatbuttongroup,'selectedobject',hradiounix)
    case 'e'
         set(htimeformatbuttongroup,'selectedobject',hradioexcel)
end
switch time_units1
    case 'd'; 
         set(htimeunitsbuttongroup,'selectedobject',hradiodays)
    case 'h'; 
         set(htimeunitsbuttongroup,'selectedobject',hradiohours)
    case 'm'; 
         set(htimeunitsbuttongroup,'selectedobject',hradiominutes)
    case 's';  
         set(htimeunitsbuttongroup,'selectedobject',hradioseconds)
end
switch ini_conc1
    case 1; 
         set(hiniconcentrbuttongroup,'selectedobject',hradionattracer)
    case 0; 
         set(hiniconcentrbuttongroup,'selectedobject',hradioarttracer)
end
switch mean_subs1
    case 'S'; 
         set(hmeansubstrbuttongroup,'selectedobject',hradiosubstr)
    case 'NS'; 
         set(hmeansubstrbuttongroup,'selectedobject',hradionotsubstr)
end
end
function cancelbutton_Callback(source,eventdata)
time_format=time_format1;
time_units=time_units1;
ini_conc=ini_conc1;
mean_subs=mean_subs1;
close(gcbf)
end
function okbutton_Callback(source,eventdata)
switch findobj(get(htimeformatbuttongroup,'selectedobject'))
    case hradionotspecif
         time_format='n'; %not specified format of time
    case  hradiomatlab
         time_format='m'; %matlab time
    case hradiounix
         time_format='u'; 
    case hradioexcel
        time_format='e';   %excel time number of days since 1900-Jan-0, 
                               %plus a fractional portion of a 24 hour day:   
                               %ddddd.tttttt
end
switch findobj(get(htimeunitsbuttongroup,'selectedobject'))
    case hradiodays
         time_units='d'; 
    case hradiohours
         time_units='h'; 
    case hradiominutes
         time_units='m'; 
    case hradioseconds
         time_units='s';   
end
switch findobj(get(hiniconcentrbuttongroup,'selectedobject'))
    case hradionattracer
         ini_conc=1; 
    case hradioarttracer
         ini_conc=0; 
end
switch findobj(get(hmeansubstrbuttongroup,'selectedobject'))
    case hradiosubstr
         mean_subs='S'; 
    case hradionotsubstr
         mean_subs='NS'; 
end
close(gcbf)
end
if ishghandle(f)
  % Go into uiwait if the figure handle is still valid.
  % This is mostly the case during regular use.
  uiwait(f);
end
end
