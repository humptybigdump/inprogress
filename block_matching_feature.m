close all; % close all figures that might still exist from a previous run

% adapt image path: 
I1 = imread('../images/left/0000.png');
I2 = imread('../images/right/0000.png');

num_features = 10;

search_area = [51 101];
window_size = [31 31];

matches = feature_matching(I1, I2, num_features, search_area, window_size);
visualize_feature_matching(I1, I2, matches, '0000.png');
%plot_patches(I1, I2, matches, window_size);