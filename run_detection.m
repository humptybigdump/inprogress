close all;
for i=1:5:34  % iterate over some images
    filename = sprintf('../images/%04d.png',  i);
    I(i).image = imread(filename);  % load image
    I(i).features = detect_sift_light_features(I(i).image);  % extract interest points
    visualize_sift_light(I(i).image, I(i).features, ['SIFT(light) ' num2str(i)]);  % visualize result
end
