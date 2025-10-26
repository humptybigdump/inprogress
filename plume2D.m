function varargout = plume2D(varargin)
% PLUME2D M-file for plume2D.fig
%      PLUME2D, by itself, creates a new PLUME2D or raises the existing
%      singleton*.
%
%      H = PLUME2D returns the handle to a new PLUME2D or the handle to
%      the existing singleton*.
%
%      PLUME2D('CALLBACK',hObject,eventData,handles,...) calls the local
%      function named CALLBACK in PLUME2D.M with the given input arguments.
%
%      PLUME2D('Property','Value',...) creates a new PLUME2D or raises the
%      existing singleton*.  Starting from the left, property value pairs are
%      applied to the GUI before plume2D_OpeningFunction gets called.  An
%      unrecognized property name or invalid value makes property application
%      stop.  All inputs are passed to plume2D_OpeningFcn via varargin.
%
%      *See GUI Options on GUIDE's Tools menu.  Choose "GUI allows only one
%      instance to run (singleton)".
%
% See also: GUIDE, GUIDATA, GUIHANDLES

% Copyright 2002-2003 The MathWorks, Inc.

% Edit the above text to modify the response to help plume2D

% Last Modified by GUIDE v2.5 04-Oct-2016 15:17:10

% Begin initialization code - DO NOT EDIT
gui_Singleton = 1;
gui_State = struct('gui_Name',       mfilename, ...
                   'gui_Singleton',  gui_Singleton, ...
                   'gui_OpeningFcn', @plume2D_OpeningFcn, ...
                   'gui_OutputFcn',  @plume2D_OutputFcn, ...
                   'gui_LayoutFcn',  [] , ...
                   'gui_Callback',   []);
if nargin && ischar(varargin{1})
    gui_State.gui_Callback = str2func(varargin{1});
end

if nargout
    [varargout{1:nargout}] = gui_mainfcn(gui_State, varargin{:});
else
    gui_mainfcn(gui_State, varargin{:});
end
% End initialization code - DO NOT EDIT


% --- Executes just before plume2D is made visible.
function plume2D_OpeningFcn(hObject, eventdata, handles, varargin)
% This function has no output args, see OutputFcn.
% hObject    handle to figure
% eventdata  reserved - to be defined in a future version of MATLAB
% handles    structure with handles and user data (see GUIDATA)
% varargin   command line arguments to plume2D (see VARARGIN)

% Choose default command line output for untitled1
handles.output = hObject;

% Choose default command line output for plume2D
handles.output = hObject;
handles.metricdata.a     = 1;    % stoichiometric coefficient of compound A
handles.metricdata.b     = 1;    % stoichiometric coefficient of compound B
handles.metricdata.c     = 1;    % stoichiometric coefficient of compound C
handles.metricdata.v     = 1e-5; % velocity [m/s]
handles.metricdata.Dt    = 1e-8; % transverse dispersion coefficient [m2/s]
handles.metricdata.w     = 0.1;  % width of the plume [m]
handles.metricdata.Ain   = 1e-3; % concentration of A in the source
handles.metricdata.Bamb  = 1e-3; % ambient concentration of B
handles.metricdata.KA    = 1e-4; % Monod coefficient for compound A [mol/l]
handles.metricdata.KB    = 1e-4; % Monod coefficient for compound A [mol/l]
handles.metricdata.mumax = 1e-5; % maximum growth rate [1/s]
handles.metricdata.kdec  = 1e-6; % maximum growth rate [1/s]
handles.metricdata.Y     = 1;    % specific yield [g Bio/mol]
handles.metricdata.coord = 5;    % coordinate for plot of profile
handles.whatplot = 1;            % what to plot
handles.typeplot = 1;            % type of plot
updatecalc(handles);

% Update handles structure
guidata(hObject, handles);



% UIWAIT makes plume2D wait for user response (see UIRESUME)
% uiwait(handles.plume2D);


% --- Outputs from this function are returned to the command line.
function varargout = plume2D_OutputFcn(hObject, eventdata, handles) 
% varargout  cell array for returning output args (see VARARGOUT);
% hObject    handle to figure
% eventdata  reserved - to be defined in a future version of MATLAB
% handles    structure with handles and user data (see GUIDATA)

% Get default command line output from handles structure
varargout{1} = handles.output;



% ============= CALLBACKS ==============================================
function stoichA_Callback(hObject, eventdata, handles)
% hObject    handle to stoichA (see GCBO)
% eventdata  reserved - to be defined in a future version of MATLAB
% handles    structure with handles and user data (see GUIDATA)

% Hints: get(hObject,'String') returns contents of stoichA as text
%        str2double(get(hObject,'String')) returns contents of stoichA as a double
a = str2double(get(hObject, 'String'));
if isnan(a)
    set(hObject, 'String', 1);
    errordlg('Input must be a number','Error');
end

% Save the new stochiometric coefficient
handles.metricdata.a = a;
updatecalc(handles);
guidata(hObject, handles);

function StoichB_Callback(hObject, eventdata, handles)
% hObject    handle to StoichB (see GCBO)
% eventdata  reserved - to be defined in a future version of MATLAB
% handles    structure with handles and user data (see GUIDATA)

% Hints: get(hObject,'String') returns contents of StoichB as text
%        str2double(get(hObject,'String')) returns contents of StoichB as a double
b = str2double(get(hObject, 'String'));
if isnan(b)
    set(hObject, 'String', 1);
    errordlg('Input must be a number','Error');
end

% Save the new stochiometric coefficient
handles.metricdata.b = b;
updatecalc(handles);
guidata(hObject, handles);


function StoichC_Callback(hObject, eventdata, handles)
% hObject    handle to StoichC (see GCBO)
% eventdata  reserved - to be defined in a future version of MATLAB
% handles    structure with handles and user data (see GUIDATA)

% Hints: get(hObject,'String') returns contents of StoichC as text
%        str2double(get(hObject,'String')) returns contents of StoichC as a double
c = str2double(get(hObject, 'String'));
if isnan(c)
    set(hObject, 'String', 1);
    errordlg('Input must be a number','Error');
end

% Save the new stochiometric coefficient
handles.metricdata.c = c;
updatecalc(handles);
guidata(hObject, handles);


function velo_Callback(hObject, eventdata, handles)
% hObject    handle to velo (see GCBO)
% eventdata  reserved - to be defined in a future version of MATLAB
% handles    structure with handles and user data (see GUIDATA)

% Hints: get(hObject,'String') returns contents of velo as text
%        str2double(get(hObject,'String')) returns contents of velo as a double
v = str2double(get(hObject, 'String'));
if isnan(v)
    set(hObject, 'String', 1e-5);
    errordlg('Input must be a number','Error');
end

% Save the new velocity value
handles.metricdata.v = v;
updatecalc(handles);
guidata(hObject, handles);


function transdiss_Callback(hObject, eventdata, handles)
% hObject    handle to transdiss (see GCBO)
% eventdata  reserved - to be defined in a future version of MATLAB
% handles    structure with handles and user data (see GUIDATA)

% Hints: get(hObject,'String') returns contents of transdiss as text
%        str2double(get(hObject,'String')) returns contents of transdiss as a double
Dt = str2double(get(hObject, 'String'));
if isnan(Dt)
    set(hObject, 'String', 1e-8);
    errordlg('Input must be a number','Error');
end

% Save the new transverse dispersion coefficient
handles.metricdata.Dt = Dt;
updatecalc(handles);
guidata(hObject, handles);


function width_Callback(hObject, eventdata, handles)
% hObject    handle to width (see GCBO)
% eventdata  reserved - to be defined in a future version of MATLAB
% handles    structure with handles and user data (see GUIDATA)

% Hints: get(hObject,'String') returns contents of width as text
%        str2double(get(hObject,'String')) returns contents of width as a double
w = str2double(get(hObject, 'String'));
if isnan(w)
    set(hObject, 'String', 0.1);
    errordlg('Input must be a number','Error');
end

% Save the new width value
handles.metricdata.w = w;
updatecalc(handles);
guidata(hObject, handles);


function cAin_Callback(hObject, eventdata, handles)
% hObject    handle to cAin (see GCBO)
% eventdata  reserved - to be defined in a future version of MATLAB
% handles    structure with handles and user data (see GUIDATA)

% Hints: get(hObject,'String') returns contents of cAin as text
%        str2double(get(hObject,'String')) returns contents of cAin as a double
Ain = str2double(get(hObject, 'String'));
if isnan(Ain)
    set(hObject, 'String', 1e-3);
    errordlg('Input must be a number','Error');
end

% Save the input concentration value
handles.metricdata.Ain = Ain;
updatecalc(handles);
guidata(hObject, handles);


function cBamb_Callback(hObject, eventdata, handles)
% hObject    handle to cBamb (see GCBO)
% eventdata  reserved - to be defined in a future version of MATLAB
% handles    structure with handles and user data (see GUIDATA)

% Hints: get(hObject,'String') returns contents of cBamb as text
%        str2double(get(hObject,'String')) returns contents of cBamb as a double
Bamb = str2double(get(hObject, 'String'));
if isnan(Bamb)
    set(hObject, 'String', 1);
    errordlg('Input must be a number','Error');
end

% Save the new ambient concentration value
handles.metricdata.Bamb = Bamb;
updatecalc(handles);
guidata(hObject, handles);




function KA_Callback(hObject, eventdata, handles)
% hObject    handle to KA (see GCBO)
% eventdata  reserved - to be defined in a future version of MATLAB
% handles    structure with handles and user data (see GUIDATA)

% Hints: get(hObject,'String') returns contents of KA as text
%        str2double(get(hObject,'String')) returns contents of KA as a double
KA = str2double(get(hObject, 'String'));
if isnan(KA)
    set(hObject, 'String', 1);
    errordlg('Input must be a number','Error');
end

% Save the new ambient concentration value
handles.metricdata.KA = KA;
updatecalc(handles);
guidata(hObject, handles);

function KB_Callback(hObject, eventdata, handles)
% hObject    handle to KB (see GCBO)
% eventdata  reserved - to be defined in a future version of MATLAB
% handles    structure with handles and user data (see GUIDATA)

% Hints: get(hObject,'String') returns contents of KB as text
%        str2double(get(hObject,'String')) returns contents of KB as a double
KB = str2double(get(hObject, 'String'));
if isnan(KB)
    set(hObject, 'String', 1);
    errordlg('Input must be a number','Error');
end

% Save the new ambient concentration value
handles.metricdata.KB = KB;
updatecalc(handles);
guidata(hObject, handles);


function mumax_Callback(hObject, eventdata, handles)
% hObject    handle to mumax (see GCBO)
% eventdata  reserved - to be defined in a future version of MATLAB
% handles    structure with handles and user data (see GUIDATA)

% Hints: get(hObject,'String') returns contents of mumax as text
%        str2double(get(hObject,'String')) returns contents of mumax as a double
mumax = str2double(get(hObject, 'String'));
if isnan(mumax)
    set(hObject, 'String', 1);
    errordlg('Input must be a number','Error');
end

% Save the new ambient concentration value
handles.metricdata.mumax = mumax;
updatecalc(handles);
guidata(hObject, handles);


function kdec_Callback(hObject, eventdata, handles)
% hObject    handle to mumax (see GCBO)
% eventdata  reserved - to be defined in a future version of MATLAB
% handles    structure with handles and user data (see GUIDATA)

% Hints: get(hObject,'String') returns contents of mumax as text
%        str2double(get(hObject,'String')) returns contents of mumax as a double
kdec = str2double(get(hObject, 'String'));
if isnan(kdec)
    set(hObject, 'String', 1);
    errordlg('Input must be a number','Error');
end

% Save the new ambient concentration value
handles.metricdata.kdec = kdec;
updatecalc(handles);
guidata(hObject, handles);


function yield_Callback(hObject, eventdata, handles)
% hObject    handle to yield (see GCBO)
% eventdata  reserved - to be defined in a future version of MATLAB
% handles    structure with handles and user data (see GUIDATA)

% Hints: get(hObject,'String') returns contents of yield as text
%        str2double(get(hObject,'String')) returns contents of yield as a double
Y = str2double(get(hObject, 'String'));
if isnan(Y)
    set(hObject, 'String', 1);
    errordlg('Input must be a number','Error');
end

% Save the new ambient concentration value
handles.metricdata.Y = Y;
updatecalc(handles);
guidata(hObject, handles);


function coord_Callback(hObject, eventdata, handles)
% hObject    handle to coord (see GCBO)
% eventdata  reserved - to be defined in a future version of MATLAB
% handles    structure with handles and user data (see GUIDATA)

% Hints: get(hObject,'String') returns contents of coord as text
%        str2double(get(hObject,'String')) returns contents of coord as a double
coord = str2double(get(hObject, 'String'));
if isnan(coord)
    set(hObject, 'String', 1);
    errordlg('Input must be a number','Error');
end

% Save the new ambient concentration value
handles.metricdata.coord = coord;
updatecalc(handles);
guidata(hObject, handles);


% --- Executes on selection change in whatplot.
function whatplot_Callback(hObject, eventdata, handles)
% hObject    handle to whatplot (see GCBO)
% eventdata  reserved - to be defined in a future version of MATLAB
% handles    structure with handles and user data (see GUIDATA)

% Hints: contents = get(hObject,'String') returns whatplot contents as cell array
%        contents{get(hObject,'Value')} returns selected item from whatplot
handles.whatplot=get(hObject,'Value');
updatecalc(handles);
guidata(hObject, handles);


% --- Executes on selection change in typeplot.
function typeplot_Callback(hObject, eventdata, handles)
% hObject    handle to typeplot (see GCBO)
% eventdata  reserved - to be defined in a future version of MATLAB
% handles    structure with handles and user data (see GUIDATA)

% Hints: contents = get(hObject,'String') returns typeplot contents as cell array
%        contents{get(hObject,'Value')} returns selected item from typeplot
handles.typeplot=get(hObject,'Value');
updatecalc(handles);
guidata(hObject, handles);

% function length_Callback(hObject, eventdata, handles)
% function CritMix_Callback(hObject, eventdata, handles)
% function plumewidth_Callback(hObject, eventdata, handles)

% =========================================================================
function updatecalc(handles)

handles.metricdata.Xcrit = handles.metricdata.a*handles.metricdata.Bamb/...
                          (handles.metricdata.b*handles.metricdata.Ain + ...
                           handles.metricdata.a*handles.metricdata.Bamb); % critical mixing ratio
handles.metricdata.L     = handles.metricdata.v*handles.metricdata.w^2/16/...
                           handles.metricdata.Dt/...
                           erfinv(handles.metricdata.Xcrit)^2; % length of the plume

set(handles.length , 'String', handles.metricdata.L);
set(handles.CritMix, 'String', handles.metricdata.Xcrit);

axes(handles.axes1);
L=handles.metricdata.L;
w=handles.metricdata.w;
v=handles.metricdata.v;
Dt=handles.metricdata.Dt;
Ain=handles.metricdata.Ain;
Bamb=handles.metricdata.Bamb;
a=handles.metricdata.a;
b=handles.metricdata.b;
c=handles.metricdata.c;
Xcrit=handles.metricdata.Xcrit;
KA=handles.metricdata.KA;
KB=handles.metricdata.KB;
mumax=handles.metricdata.mumax;
kdec=handles.metricdata.kdec;
Y=handles.metricdata.Y;
coord=handles.metricdata.coord;

switch handles.typeplot
    case 1
        set(handles.coord,'enable','off');
        set(handles.coordtext,'enable','off');
        set(handles.coorunit,'enable','off');
        xvec=[1:150]/100*L;
        yvec=[-100:100]/100*w;
        [x,y]=meshgrid(xvec,yvec);
        X=0.5*(erf((0.5*y/w+0.25).*sqrt(v*w^2./x/Dt)) - erf((0.5*y/w-0.25).*sqrt(v*w^2./x/Dt)));
        while (max(X(end,:))>Xcrit)
            y=y*1.2;
            X=0.5*(erf((0.5*y/w+0.25).*sqrt(v*w^2./x/Dt)) - erf((0.5*y/w-0.25).*sqrt(v*w^2./x/Dt)));
        end
        [A,B,C]=concdist(x,y,1,w,Dt/v,a,b,c,KA,KB,Ain,Bamb,kdec,mumax,Y,v);
        [Ab,Bb,Cb,Bio]=concdist(x,y,2,w,Dt/v,a,b,c,KA,KB,Ain,Bamb,kdec,mumax,Y,v);
        switch handles.whatplot
            case 1
                pcolor(x,y,X);
                title(sprintf('Mixing Ratio, min=%0.3g, max=%0.3g',[0 1]));
                caxis([0 1]);
            case 2
                pcolor(x,y,A);
                title(sprintf('Plume-Borne Reactant A, min=%0.3g mol/l, max=%0.3g mol/l',caxis));
            case 3
                pcolor(x,y,B);
                title(sprintf('Ambient Reactant B, min=%0.3g mol/l, max=%0.3g mol/l',caxis));
            case 4
                pcolor(x,y,C);
                title(sprintf('Reaction Product C, min=%0.3g mol/l, max=%0.3g mol/l',caxis));
            case 5
                pcolor(x,y,Ab);
                title(sprintf('Plume-Borne Reactant A, min=%0.3g mol/l, max=%0.3g mol/l',caxis));
            case 6
                pcolor(x,y,Bb);
                title(sprintf('Ambient Reactant B, min=%0.3g mol/l, max=%0.3g mol/l',caxis));
            case 7
                pcolor(x,y,Cb);
                title(sprintf('Reaction Product C, min=%0.3g mol/l, max=%0.3g mol/l',caxis));
            case 8
                pcolor(x,y,Bio);
                Bios=sort(Bio(~isnan(Bio)));
                maxbio=Bios(floor(size(Bios,1)*0.995));clear Bios;
                caxis([0 maxbio]);
                title(sprintf('Biomass, min=%0.3g g/l, max=%0.3g g/l',[0 maxbio]));
        end
        %map=colormap('gray');colormap(flipud(map));
        clim=caxis;
        shading interp;
        xlabel('x [m]');ylabel('y [m]');
        hold on
        cmat=contour(x,y,X,handles.metricdata.Xcrit*[1 1],'w');caxis(clim);
        hold off
        %colorbar
        cmat=cmat(:,2:end);
        handles.metricdata.plumewidth=max(cmat(2,:))-min(cmat(2,:));
        set(handles.plumewidth, 'String', handles.metricdata.plumewidth);
    case 2
        set(handles.coord,'enable','on');
        set(handles.coordtext,'enable','on','string','x =');
        set(handles.coorunit,'enable','on');
        x=max([coord eps]);
        y=[-150:150]/100*w;
        X=0.5*(erf((0.5*y/w+0.25).*sqrt(v*w^2./x/Dt)) - erf((0.5*y/w-0.25).*sqrt(v*w^2./x/Dt)));
        while (X(end)>Xcrit)
            y=y*1.2;
            X=0.5*(erf((0.5*y/w+0.25).*sqrt(v*w^2./x/Dt)) - erf((0.5*y/w-0.25).*sqrt(v*w^2./x/Dt)));
        end
        [A,B,C]=concdist(x,y,1,w,Dt/v,a,b,c,KA,KB,Ain,Bamb,kdec,mumax,Y,v);
        [Ab,Bb,Cb,Bio]=concdist(x,y,2,w,Dt/v,a,b,c,KA,KB,Ain,Bamb,kdec,mumax,Y,v);
        if (x>L)
            handles.metricdata.plumewidth=0;
        else
            handles.metricdata.plumewidth=min(y(X<=Xcrit&y>0))-max(y(X<=Xcrit&y<0));
        end
        set(handles.plumewidth, 'String', handles.metricdata.plumewidth);
        switch handles.whatplot
            case 1
                plot(y,X);title('Mixing Ratio');ylabel('X [-]');
            case 2
                plot(y,[A;Ab]);title('Plume-Borne Reactant A');ylabel('c_A [mol/l]');
                legend('instantaneous','biokinetic',0);
            case 3
                plot(y,[B;Bb]);title('Ambient Reactant B');ylabel('c_B [mol/l]');
                legend('instantaneous','biokinetic',0);
            case 4
                plot(y,[C;Cb]);title('Reaction Product C');ylabel('c_C [mol/l]');
                legend('instantaneous','biokinetic',0);
            case 5
                plot(y,[A;Ab]);title('Plume-Borne Reactant A');ylabel('c_A [mol/l]');
                legend('instantaneous','biokinetic',0);
            case 6
                plot(y,[B;Bb]);title('Ambient Reactant B');ylabel('c_B [mol/l]');
                legend('instantaneous','biokinetic',0);
            case 7
                plot(y,[C;Cb]);title('Reaction Product C');ylabel('c_C [mol/l]');
                legend('instantaneous','biokinetic',0);
            case 8
                plot(y,Bio);title('Biomass');ylabel('c_{bio} [g/l]');
        end
        xlabel('y [m]');
        xlim([min(y) max(y)]);
    case 3
        set(handles.coord,'enable','on');
        set(handles.coordtext,'enable','on','string','y =');
        set(handles.coorunit,'enable','on');
        x=[1:150]/100*L;
        y=coord;
        X=0.5*(erf((0.5*y/w+0.25).*sqrt(v*w^2./x/Dt)) - erf((0.5*y/w-0.25).*sqrt(v*w^2./x/Dt)));
        [A,B,C]=concdist(x,y,1,w,Dt/v,a,b,c,KA,KB,Ain,Bamb,kdec,mumax,Y,v);
        [Ab,Bb,Cb,Bio]=concdist(x,y,2,w,Dt/v,a,b,c,KA,KB,Ain,Bamb,kdec,mumax,Y,v);
        set(handles.plumewidth, 'String','-');
        switch handles.whatplot
            case 1
                plot(x,X);title('Mixing Ratio');ylabel('X [-]');
            case 2
                plot(x,[A;Ab]);title('Plume-Borne Reactant A');ylabel('c_A [mol/l]');
                legend('instantaneous','biokinetic',0);
            case 3
                plot(x,[B;Bb]);title('Ambient Reactant B');ylabel('c_B [mol/l]');
                legend('instantaneous','biokinetic',0);
            case 4
                plot(x,[C;Cb]);title('Reaction Product C');ylabel('c_C [mol/l]');
                legend('instantaneous','biokinetic',0);
            case 5
                plot(x,[A;Ab]);title('Plume-Borne Reactant A');ylabel('c_A [mol/l]');
                legend('instantaneous','biokinetic',0);
            case 6
                plot(x,[B;Bb]);title('Ambient Reactant B');ylabel('c_B [mol/l]');
                legend('instantaneous','biokinetic',0);
            case 7
                plot(x,[C;Cb]);title('Reaction Product C');ylabel('c_C [mol/l]');
                legend('instantaneous','biokinetic',0);
            case 8
                plot(x,Bio);title('Biomass');ylabel('c_{bio} [g/l]');
        end
        xlabel('x [m]');
        xlim([0 L*1.5]);
end

% =========================================================================
% calculation of concentrations
function [A,B,C,Bio]=concdist(x,z,type,h,alpha,a,b,c,KA,KB,Ain,Bamb,kdec,mumax,Y,v)

% decay coefficients normalized by growth coefficient
kdecrel=kdec/mumax;

% Distribution of the mixing ratio
X=0.5*(erf((z+h/2)/2./sqrt(x*alpha))-erf((z-h/2)/2./sqrt(x*alpha)));
% Total concentrations
Atot=X*Ain;
Btot=(1-X)*Bamb;

% Critical mixing ratio
Xcrit= a*Bamb/(b*Ain+a*Bamb);

switch type
case 1
% =========================================================================
% Concentrations for instantaneous reaction
% =========================================================================
% concentrations
A=zeros(size(X));
B=zeros(size(X));
C=zeros(size(X));
A(X>=Xcrit)=X(X>=Xcrit)*Ain-a/b*Bamb*(1-X(X>=Xcrit));
C(X>=Xcrit)=c/b*Bamb*(1-X(X>=Xcrit));
B(X<Xcrit)=(1-X(X<Xcrit))*Bamb-b/a*Ain*X(X<Xcrit);
C(X<Xcrit)=c/a*Ain*X(X<Xcrit);

case 2
% =========================================================================
% Concentrations for double-Monod kinetics with linear decay
% =========================================================================
% dimensionless criterion for existence of biomass
omega_max=Xcrit*Ain/(KA+Xcrit*Ain)*(1-Xcrit)*...
          Bamb/(KB+(1-Xcrit)*Bamb)/kdecrel;

if omega_max<1
    C=zeros(size(X));
    A=Atot;
    B=Btot;
    Bio=zeros(size(X));
else
% polynomial coefficients
p2=(1-kdecrel)*a*b/c^2;
p1=kdecrel*((KA+Atot)*b/c+(KB+Btot)*a/c)-Atot*b/c-Btot*a/c;
p0=Atot.*Btot-kdecrel*(KA+Atot).*(KB+Btot);

Xmin=fzero(@(X) C_ex_X(X,a,b,c,KA,KB,Ain,Bamb,kdec,mumax)-...
                X*dCdX_ex_X(X,a,b,c,KA,KB,Ain,Bamb,kdec,mumax),Xcrit);
Xmax=fzero(@(X) C_ex_X(X,a,b,c,KA,KB,Ain,Bamb,kdec,mumax)+...
                (1-X)*dCdX_ex_X(X,a,b,c,KA,KB,Ain,Bamb,kdec,mumax),Xcrit);
slope1=dCdX_ex_X(Xmin,a,b,c,KA,KB,Ain,Bamb,kdec,mumax);
slope2=dCdX_ex_X(Xmax,a,b,c,KA,KB,Ain,Bamb,kdec,mumax);

C=C_ex_X(X,a,b,c,KA,KB,Ain,Bamb,kdec,mumax);
C(X<Xmin)=slope1*X(X<Xmin);
C(X>Xmax)=(X(X>Xmax)-1)*slope2;


A=Atot-a/c*C;
B=Btot-b/c*C;

% calculate derivatives
dXdx=0.25*(pi*x.^3*alpha).^-0.5.*((z-h/2).*exp(-(z-h/2).^2./(4*x*alpha)) ...
                                 -(z+h/2).*exp(-(z+h/2).^2./(4*x*alpha)));
dXdz=0.5*(pi*x*alpha).^-0.5.*(exp(-(z+h/2).^2./(4*x*alpha))- ...
                              exp(-(z-h/2).^2./(4*x*alpha)));
d2Xdz2=dXdx/alpha;
% partial derivatives of polynomial coefficients with respect to total
% concentrations
dp1dCA=(kdecrel-1)*b/c*ones(size(X));
dp1dCB=(kdecrel-1)*a/c*ones(size(X));
dp0dCA=Btot-kdecrel*(KB+Btot);
dp0dCB=Atot-kdecrel*(KA+Atot);
d2p0dCAdCB=(1-kdecrel)*ones(size(X));
% resulting derivatives of product concentration with respect to total
% concentration
dCCdCA=-0.5/p2*dp1dCA-(p1.^2-4*p0*p2).^-0.5.*(0.5*p1/p2.*dp1dCA-dp0dCA);
dCCdCB=-0.5/p2*dp1dCB-(p1.^2-4*p0*p2).^-0.5.*(0.5*p1/p2.*dp1dCB-dp0dCB);
d2CCdCA2=(p1.^2-4*p0*p2).^-1.5.*(0.25*p1/p2.*dp1dCA-0.5*dp0dCA).^2 ...
        -(p1.^2-4*p0*p2).^-0.5.*(0.5/p2*dp1dCA.^2);
d2CCdCB2=(p1.^2-4*p0*p2).^-1.5.*(0.25*p1/p2.*dp1dCB-0.5*dp0dCB).^2 ...
        -(p1.^2-4*p0*p2).^-0.5.*(0.5/p2*dp1dCB.^2);
d2CCdCAdCB=(p1.^2-4*p0*p2).^-1.5.*(0.25*p1/p2.*dp1dCA-0.5*dp0dCA).*(0.25*p1/p2.*dp1dCB-0.5*dp0dCB) ...
          -(p1.^2-4*p0*p2).^-0.5.*(0.5/p2*dp1dCA.*dp1dCB-d2p0dCAdCB);
clear dp1dCA dp1dCB dp0dCA d2p0dCAdCB
% resulting spatial derivatives of product concentration
dC2dx=dCCdCA.*dXdx*Ain-dCCdCB.*dXdx*Bamb;
d2C2dz2=d2CCdCA2.*dXdz.^2*Ain^2 + dCCdCA.*d2Xdz2*Ain - ...
      2*d2CCdCAdCB.*dXdz.^2*Ain*Bamb + ...
        d2CCdCB2.*dXdz.^2*Bamb^2 - dCCdCB.*d2Xdz2*Bamb;
clear dXdx dXdz d2Xdz2 dCCdCA dCCdCB d2CCdCA2 d2CCdCB2 d2CCdCAdCB

% compute biomass concentration
warning off
Bio=(dC2dx-alpha*d2C2dz2).*(KA+A).*(KB+B)./A./B/c/mumax*Y*v;
warning on
Bio(X<Xmin | X>Xmax)=0;
clear dC2dx d2C2dz2
end
end

function C=C_ex_X(X,a,b,c,KA,KB,Ain,Bamb,kdec,mumax)
% decay coefficients normalized by growth coefficient
kdecrel=kdec/mumax;
% Total concentrations
Atot=X*Ain;
Btot=(1-X)*Bamb;
% polynomial coefficients
p2=(1-kdecrel)*a*b/c^2;
p1=kdecrel*((KA+Atot)*b/c+(KB+Btot)*a/c)-Atot*b/c-Btot*a/c;
p0=Atot.*Btot-kdecrel*(KA+Atot).*(KB+Btot);
% solve for aqueous-phase concentrations
warning off
C=0.5*(-p1-sqrt(p1.^2-4*p2.*p0))./p2;
warning on

function dCdX=dCdX_ex_X(X,a,b,c,KA,KB,Ain,Bamb,kdec,mumax)
% decay coefficients normalized by growth coefficient
kdecrel=kdec/mumax;
% Total concentrations
Atot=X*Ain;
Btot=(1-X)*Bamb;
% polynomial coefficients
p2=(1-kdecrel)*a*b/c^2;
p1=kdecrel*((KA+Atot)*b/c+(KB+Btot)*a/c)-Atot*b/c-Btot*a/c;
p0=Atot.*Btot-kdecrel*(KA+Atot).*(KB+Btot);
% Derivatives of polynomial coefficients with respect to X
dp0dX=Ain*Bamb*(1-2*X)*(1-kdecrel)-kdecrel*(Ain*KB-Bamb*KA);
dp1dX=(kdecrel-1)*(Ain*b/c-Bamb*a/c);
% Derivatives of C with respect to polynomial coefficients
dCdp0=1./sqrt(p1.^2-4*p2.*p0);
dCdp1=-0.5./p2.*(p1./sqrt(p1.^2-4*p2.*p0)+1);
% put it all together
dCdX=dp0dX.*dCdp0 + dp1dX.*dCdp1;

% ============= CREATE FUNCTIONS =======================================
function stoichA_CreateFcn(hObject, eventdata, handles)
if ispc && isequal(get(hObject,'BackgroundColor'), get(0,'defaultUicontrolBackgroundColor'))
    set(hObject,'BackgroundColor','white');
end
function StoichB_CreateFcn(hObject, eventdata, handles)
if ispc && isequal(get(hObject,'BackgroundColor'), get(0,'defaultUicontrolBackgroundColor'))
    set(hObject,'BackgroundColor','white');
end
function length_CreateFcn(hObject, eventdata, handles)
function StoichC_CreateFcn(hObject, eventdata, handles)
if ispc && isequal(get(hObject,'BackgroundColor'), get(0,'defaultUicontrolBackgroundColor'))
    set(hObject,'BackgroundColor','white');
end
function velo_CreateFcn(hObject, eventdata, handles)
if ispc && isequal(get(hObject,'BackgroundColor'), get(0,'defaultUicontrolBackgroundColor'))
    set(hObject,'BackgroundColor','white');
end
function transdiss_CreateFcn(hObject, eventdata, handles)
if ispc && isequal(get(hObject,'BackgroundColor'), get(0,'defaultUicontrolBackgroundColor'))
    set(hObject,'BackgroundColor','white');
end
function width_CreateFcn(hObject, eventdata, handles)
if ispc && isequal(get(hObject,'BackgroundColor'), get(0,'defaultUicontrolBackgroundColor'))
    set(hObject,'BackgroundColor','white');
end
function cAin_CreateFcn(hObject, eventdata, handles)
if ispc && isequal(get(hObject,'BackgroundColor'), get(0,'defaultUicontrolBackgroundColor'))
    set(hObject,'BackgroundColor','white');
end
function cBamb_CreateFcn(hObject, eventdata, handles)
if ispc && isequal(get(hObject,'BackgroundColor'), get(0,'defaultUicontrolBackgroundColor'))
    set(hObject,'BackgroundColor','white');
end
function whatplot_CreateFcn(hObject, eventdata, handles)
if ispc && isequal(get(hObject,'BackgroundColor'), get(0,'defaultUicontrolBackgroundColor'))
    set(hObject,'BackgroundColor','white');
end
function CritMix_CreateFcn(hObject, eventdata, handles)
if ispc && isequal(get(hObject,'BackgroundColor'), get(0,'defaultUicontrolBackgroundColor'))
    set(hObject,'BackgroundColor','white');
end
function plumewidth_CreateFcn(hObject, eventdata, handles)
if ispc && isequal(get(hObject,'BackgroundColor'), get(0,'defaultUicontrolBackgroundColor'))
    set(hObject,'BackgroundColor','white');
end
function KA_CreateFcn(hObject, eventdata, handles)
if ispc && isequal(get(hObject,'BackgroundColor'), get(0,'defaultUicontrolBackgroundColor'))
    set(hObject,'BackgroundColor','white');
end
function KB_CreateFcn(hObject, eventdata, handles)
if ispc && isequal(get(hObject,'BackgroundColor'), get(0,'defaultUicontrolBackgroundColor'))
    set(hObject,'BackgroundColor','white');
end
function mumax_CreateFcn(hObject, eventdata, handles)
if ispc && isequal(get(hObject,'BackgroundColor'), get(0,'defaultUicontrolBackgroundColor'))
    set(hObject,'BackgroundColor','white');
end
function kdec_CreateFcn(hObject, eventdata, handles)
if ispc && isequal(get(hObject,'BackgroundColor'), get(0,'defaultUicontrolBackgroundColor'))
    set(hObject,'BackgroundColor','white');
end
function typeplot_CreateFcn(hObject, eventdata, handles)
if ispc && isequal(get(hObject,'BackgroundColor'), get(0,'defaultUicontrolBackgroundColor'))
    set(hObject,'BackgroundColor','white');
end
function coord_CreateFcn(hObject, eventdata, handles)
if ispc && isequal(get(hObject,'BackgroundColor'), get(0,'defaultUicontrolBackgroundColor'))
    set(hObject,'BackgroundColor','white');
end
function yield_CreateFcn(hObject, eventdata, handles)
if ispc && isequal(get(hObject,'BackgroundColor'), get(0,'defaultUicontrolBackgroundColor'))
    set(hObject,'BackgroundColor','white');
end




% --- Executes during object creation, after setting all properties.
function plume2D_CreateFcn(hObject, eventdata, handles)
% hObject    handle to plume2D (see GCBO)
% eventdata  reserved - to be defined in a future version of MATLAB
% handles    empty - handles not created until after all CreateFcns called
screen=get(0,'screensize');
posi=get(hObject,'position');
posi(1)=round((screen(3)-posi(3))/2);
posi(2)=round((screen(4)-posi(4))/2);
set(hObject,'position',posi);






% --- Executes when plume2D is resized.
function plume2D_SizeChangedFcn(hObject, eventdata, handles)
% hObject    handle to plume2D (see GCBO)
% eventdata  reserved - to be defined in a future version of MATLAB
% handles    structure with handles and user data (see GUIDATA)
