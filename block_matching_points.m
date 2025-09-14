close all; % close all figures that might still exist from a previous run

image_point_locations = [161, 297;  980, 350; ...
                         600,  26;  597,  87; ...
                         680, 109;  356, 121; ...
                         840, 101;  603, 262; ...
                        1046, 320; 1086,  86];

% adapt image path: 
I1 = imread('../images/left/0000.png');
I2 = imread('../images/right/0000.png');

search_area = [51 101];
window_size = [31 31]; % [height, width]

% For Exercise 2.2b
N = 10; % Pick any value between 1 and 10

for i = 1:size(image_point_locations,1)
    p = image_point_locations(i,:);
    % Exercise 2.2.a: 
    matches = match_point(I1, I2, p, search_area, window_size);
    % Exercise 2.2b: 
    %matches = match_point_bestN(I1, I2, p, N, search_area, window_size);
    % Exercise 2.5c:
    %matches = match_point_rect(I1, I2, p, window_size);
    visualize_matched_points(I1, I2, p, matches, ['Point_', int2str(i)]);
end