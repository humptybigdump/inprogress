d_orgs(7,5:9,:) = NaN;
d_orgs(5,16:21,:) = NaN;
d_orgs(:,:,9) = NaN;
d_org(7,5) = NaN;
d_org(5,2) = NaN;
d_org(45,19:20) = -1;

%save project under new name 
next_function_parameter = 'ausreisser_fehlende_werte.prjz';
saveprj_g;