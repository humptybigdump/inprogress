function matches = feature_matching(I1, I2, num_features, search_area, window_size)
% Detect features in image I1 and find corresponding matches in image I2
% using block matching
% Arguments:
%   I1: left image
%   I2: right image
%   num_features: number of features to detect in I1
%   search_area: [height, width] of search area
%   window_size: [height, width] of window to use to compute the comparison
%                 metric 
% Output: 
%   matrix of size num_features x 4, where each row contains the
%   coordinates of one pair of matched points

    % detect the best features in I1
    features = detect_features(I1, num_features);        

    % save matches in an array with 4 columns: x, y coordinates of points
    matches = zeros(num_features, 4);
    for i = 1:num_features
        p = features(i,:); % point in I1
        m = match_point(I1, I2, p, search_area, window_size); % point in I2    
        if (size(m, 1) > 0)
            matches(i,1:2) = p;
            matches(i,3:4) = m;
        end
    end
end

