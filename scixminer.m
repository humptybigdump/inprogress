%PLEASE COPY THIS FILE TO YOUR MATLAB WORK DIRECTORY - e.g. c:\programme\matlab\R2008b\work

clear; clear global;close all;
d = which('scixminer','-all');
if (~isempty(d))
   if (length(d) ~= 1)       warndlg('An additional SciXMiner installation was found in the search path (scixminer.m).');
   end;
end;

%PLEASE UPDATE ALL PATH NAMES TO YOUR LOCAL NAMES 
gaitcadpath = 'u:\scixminer';
addpath(gaitcadpath);
addpath([gaitcadpath filesep 'plugins' filesep 'einzuggenerierung']);
addpath([gaitcadpath filesep 'plugins' filesep 'mgenerierung']);
addpath([gaitcadpath filesep 'toolbox']);
addpath([gaitcadpath filesep 'standardmakros']);
addpath(fileparts(which('scixminer')));
scixminer_gui;
d = which('scixminer_gui','-all');
if (~isempty(d))
   if (length(d) ~= 1)       warndlg('An additional SciXMiner installation was found in the search path (scixminer_gui.m).','Warning Dialog','modal');
   end;
end;
