function [timepath,inputpath,outputpath,initialtime,timestep]=SpecifPath(timepath1,inputpath1,outputpath1,initialtime1,timestep1)
% Create and then hide the GUI as it is being constructed.
f = figure('Visible','off','Position',[520,599,409,201],'Name','Specify path');
% Construct the components.
set(f,'MenuBar','none');
htimevalueandstep = uicontrol('Style','checkbox','String','Set time initial value and step',...
'Position',[229,178,171,23],...
'Callback',{@timevalueandstep_Callback});
htimeselect = uicontrol('Style','pushbutton','String','...',...
'Position',[377,149,23,25],...
'Callback',{@timeselectbutton_Callback});
hinputselect = uicontrol('Style','pushbutton','String','...',...
'Position',[377,99,23,25],...
'Callback',{@inputselectbutton_Callback});
houtputselect = uicontrol('Style','pushbutton',...
'String','...',...
'Position',[377,49,23,25],...
'Callback',{@outputselectbutton_Callback});
htext = uicontrol('Style','text','String','Time',...
'Position',[8,176,82,14],'HorizontalAlignment','left');
htext2 = uicontrol('Style','text','String','Input signal',...
'Position',[8,127,82,14],'HorizontalAlignment','left');
htext3 = uicontrol('Style','text','String','Output signal',...
'Position',[8,77,82,14],'HorizontalAlignment','left');
htext4 = uicontrol('Style','text','String','Initial time',...
'Visible','off','Position',[5,178,52,15],'HorizontalAlignment','left');
htext5 = uicontrol('Style','text','String','Time step',...
'Visible','off','Position',[105,177,52,14],'HorizontalAlignment','left');
heditinitialtime = uicontrol('Style','edit',...
'String',initialtime1,...
'Visible','off','Position',[7,149,86,25],'HorizontalAlignment','center');
hedittimestep = uicontrol('Style','edit',...
'String',timestep1,...
'Visible','off','Position',[105,149,86,25],'HorizontalAlignment','center');
hedittime = uicontrol('Style','edit',...
'String',timepath1,...
'Position',[6,149,372,25],...
'Callback',{@edittime_Callback},'HorizontalAlignment','center');
heditinput = uicontrol('Style','edit',...
'String',inputpath1,...
'Position',[6,99,372,25],...
'Callback',{@editinput_Callback},'HorizontalAlignment','center');
heditoutput = uicontrol('Style','edit',...
'String',outputpath1,...
'Position',[6,49,372,25],...
'Callback',{@editinput_Callback},'HorizontalAlignment','right');
hok = uicontrol('Style','pushbutton','String','OK',...
'Position',[8,9,118,24],...
'Callback',{@okbutton_Callback});
hpreviouschoice = uicontrol('Style','pushbutton','String','Previous choice',...
'Position',[139,9,118,24],...
'Callback',{@previouschoicebutton_Callback});
hcancel = uicontrol('Style','pushbutton',...
'String','Cancel',...
'Position',[276,9,118,24],...
'Callback',{@cancelbutton_Callback});
% Change units to normalized so components resize
% automatically.
set([f,hok,hcancel,hpreviouschoice,htext,htext2,htext3,hedittime,heditinput,heditoutput,htimeselect,hinputselect,houtputselect],...
'Units','normalized');

defaultBackground = get(0,'defaultUicontrolBackgroundColor');
%set([f,hok,hcancel,hpreviouschoice,htext,htext2,htext3,htimeselect,hinputselect,houtputselect],...
%     'BackgroundColor',defaultBackground)
set(f,'Color',defaultBackground )
set(hedittime,'BackgroundColor','white')
set(heditinput,'BackgroundColor','white')
set(heditoutput,'BackgroundColor','white')
set(heditinitialtime,'BackgroundColor','white')
set(hedittimestep,'BackgroundColor','white')
set([hedittime,heditinput,heditoutput],'HorizontalAlignment','left')
% Move the GUI to the center of the screen.
movegui(f,'center')
% Make the GUI visible.
set(f,'NumberTitle','off','Name','Input data')
if strmatch('not specified',timepath1)
     set(htimeselect,'Visible','off');
     set(hedittime,'Visible','off');
     set(htext,'Visible','off');
     set(htext4,'Visible','on');
     set(htext5,'Visible','on');
     set(heditinitialtime,'Visible','on');
     set(hedittimestep,'Visible','on');
     set(hedittime,'string','not specified');
     set(heditinitialtime,'string',initialtime1);
     set(hedittimestep,'string',timestep1);
     set(htimevalueandstep,'Value',1);
else
     set(htimeselect,'Visible','on');
     set(hedittime,'Visible','on');
     set(htext,'Visible','on');
     set(htext4,'Visible','off');
     set(htext5,'Visible','off');
     set(heditinitialtime,'Visible','off');
     set(hedittimestep,'Visible','off');
     set(hedittime,'string',timepath1);
     set(heditinitialtime,'string','not specified');
     set(hedittimestep,'string','not specified');
end
set(f,'Visible','on');
% Callbacks 
currentFolder=pwd;
function timevalueandstep_Callback(source,eventdata)
k=get(htimevalueandstep,'Value');
if k==1
     set(htimeselect,'Visible','off');
     set(hedittime,'Visible','off');
     set(htext,'Visible','off');
     set(htext4,'Visible','on');
     set(htext5,'Visible','on');
     set(heditinitialtime,'Visible','on');
     set(hedittimestep,'Visible','on');
     set(hedittime,'string','not specified');
     set(heditinitialtime,'string',initialtime1);
     set(hedittimestep,'string',timestep1);
else
     set(htimeselect,'Visible','on');
     set(hedittime,'Visible','on');
     set(htext,'Visible','on');
     set(htext4,'Visible','off');
     set(htext5,'Visible','off');
     set(heditinitialtime,'Visible','off');
     set(hedittimestep,'Visible','off');
     set(hedittime,'string',timepath1);
     set(heditinitialtime,'string','not specified');
     set(hedittimestep,'string','not specified');
end
     
end

function timeselectbutton_Callback(source,eventdata)
[file,pathname] = uigetfile('*.txt');
if ~isempty(pathname) 
     pathname;
cd(pathname);
end
time=[file,pathname];
set(hedittime,'string',[pathname file])
end
function inputselectbutton_Callback(source,eventdata)
[file,pathname] = uigetfile('*.txt');
if ~isempty(pathname) 
     pathname;
cd(pathname);
input=[file,pathname];
set(heditinput,'string',[pathname file])
end
end
function outputselectbutton_Callback(source,eventdata)
[file,pathname] = uigetfile('*.txt');
if ~isempty(pathname) 
     pathname;
output=[file,pathname];
set(heditoutput,'string',[pathname  file])
end
end
function previouschoicebutton_Callback(source,eventdata)
set(hedittime,'string',timepath1);
set(heditinput,'string',inputpath1);
set(heditoutput,'string',outputpath1);
set(heditinitialtime,'string',initialtime1);
set(hedittimestep,'string',timestep1);
end
function cancelbutton_Callback(source,eventdata)
timepath=timepath1;
inputpath=inputpath1;
outputpath=outputpath1;
initialtime=initialtime1;
timestep=timestep1;
cd(currentFolder);
close(gcbf)
end
function okbutton_Callback(source,eventdata)
timepath=get(hedittime,'string');
inputpath=get(heditinput,'string');
outputpath=get(heditoutput,'string');
initialtime=get(heditinitialtime,'string');
timestep=get(hedittimestep,'string');
cd(currentFolder);
close(gcbf)
end
if ishghandle(f)
  % Go into uiwait if the figure handle is still valid.
  % This is mostly the case during regular use.
  uiwait(f);
end
end
