BKFilenames = {'Working.Input.Input.FFT Analyzer.Time.txt'
    'Group1'
};

for BKIndex=1:2:length(BKFilenames)
   assignin('base',char(BKFilenames(BKIndex+1)),GetPulseAsciiFile(char(BKFilenames(BKIndex))))
end