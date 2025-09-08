function [Theta,TrFunLength,Nreal,EpistError]=SpecifParam(Theta,TrFunLength,Nreal,EpistError)
% Create and then hide the GUI as it is being constructed.
clc
f = figure('Visible','off','Position',[520,610,401,250],'Name','Edit parameters');
% Construct the components.
set(f,'MenuBar','none');
htext = uicontrol('Style','text','String','Slope of the linear variogram, theta',...
'Position',[9,225,190,14],'HorizontalAlignment','left');
htext2 = uicontrol('Style','text','String','Length of transfer function',...
'Position',[9,175,190,14],'HorizontalAlignment','left');
htext3 = uicontrol('Style','text','String','Number of realisations',...
'Position',[9,125,190,14],'HorizontalAlignment','left');
htext4 = uicontrol('Style','text','String','Standard deviation of epistemic error',...
'Position',[9,75,190,14],'HorizontalAlignment','left');
heditTheta = uicontrol('Style','edit',...
'String',Theta,...
'Position',[7,197,372,25]);
heditTrFunLength = uicontrol('Style','edit',...
'String',TrFunLength,...
'Position',[7,147,372,25]);
heditNreal = uicontrol('Style','edit',...
'String',Nreal,...
'Position',[7,97,372,25]);
heditEpistErr = uicontrol('Style','edit',...
'String',EpistError,...
'Position',[7,47,372,25]);
hok = uicontrol('Style','pushbutton','String','OK',...
'Position',[9,7,118,24],...
'Callback',{@okbutton_Callback});
hpreviouschoice = uicontrol('Style','pushbutton','String','Previous choice',...
'Position',[140,7,118,24],...
'Callback',{@previouschoicebutton_Callback});
hcancel = uicontrol('Style','pushbutton',...
'String','Cancel',...
'Position',[277,7,118,24],...
'Callback',{@cancelbutton_Callback});
% Change units to normalized so components resize
% automatically.
set([f,hok,hcancel,hpreviouschoice,htext,htext2,htext3,htext4,heditTheta,heditTrFunLength,heditNreal,heditEpistErr],...
'Units','normalized');
defaultBackground = get(0,'defaultUicontrolBackgroundColor');
%set([f,hok,hcancel,hpreviouschoice,htext,htext2,htext3,htimeselect,hinputselect,houtputselect],...
%     'BackgroundColor',defaultBackground)
set(f,'Color',defaultBackground )
set([heditTheta,heditTrFunLength,heditNreal,heditEpistErr],'BackgroundColor','white')
% Move the GUI to the center of the screen.
movegui(f,'center')
% Make the GUI visible.
set(f,'NumberTitle','off','Name','Input data')
set(f,'Visible','on');
function previouschoicebutton_Callback(source,eventdata)
set(heditTheta,'string',Theta);
set(heditTrFunLength,'string',TrFunLength);
set(heditNreal,'string',Nreal);
set(heditEpistErr,'string',EpistError);
end
function cancelbutton_Callback(source,eventdata)
     if ischar(Theta)& ischar(TrFunLength) & ischar(Nreal)& ischar(EpistError)
Theta=str2num(Theta);
TrFunLength=str2num(TrFunLength);
Nreal=str2num(Nreal);
EpistError=str2num(EpistError);
     end
close(gcbf)
end
function okbutton_Callback(source,eventdata)
Theta=get(heditTheta,'string');
TrFunLength=get(heditTrFunLength,'string');
Nreal=get(heditNreal,'string');
EpistError=get(heditEpistErr,'string');
Theta=str2num(Theta);
TrFunLength=str2num(TrFunLength);
Nreal=str2num(Nreal);
EpistError=str2num(EpistError);
close(gcbf)
end
if ishghandle(f)
  % Go into uiwait if the figure handle is still valid.
  % This is mostly the case during regular use.
  uiwait(f);
end
end
