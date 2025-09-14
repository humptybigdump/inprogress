close all;

for i=1:5  
    % loading of images
    filename = sprintf('../images/%04d.png',  i);
    I(i).image = imread(filename);  

    % Compute SIFT feature detection
    I(i).features = detect_sift_light_features(I(i).image);  

    % Compute SIFT feature descriptors
    [f, d] = extract_sift_light_descriptors(I(i).image, I(i).features);   
    I(i).features = f;  % f is a subset of the previous feature set
    I(i).descriptors = d;
    
    if (i>=2)
        % for each interest point in image i, calculate the most similar
        % interest point in image i-1 by comparing their descriptors
        [idx_neighbors, dist] = nearest_neighbor(I(i).descriptors, I(i-1).descriptors);  
        seq = (1:size(f,1))';
        M = [seq idx_neighbors dist];
        idx_select = (dist<0.1);  % select only matches with a small Euclidean distance between the descriptors
        I(i).back_matches = M(idx_select,:);  % store the remaining matches
        visualize_feature_matching (I(i).image, I(i-1).image, I(i).features, I(i-1).features, I(i).back_matches, ['Matches ' num2str(i) '->' num2str(i-1)] );  % visualize matches
    end
end
