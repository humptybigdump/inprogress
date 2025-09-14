function visualize_sift_light(I, features, name)
% function visualize_sift_light(I, features, name)
%
% This function visualizes the sift light interest points by
% plotting circles into the original image.
%   I refers to the original image
%   features is a list of interest points
%   name refers to the name fo the figure
%
figure('Name', name); hold on;
img = uint8(repmat(I, [1 1 3]));
for i = 1:size(features,1)
    img = insertShape(img, 'Circle', [features(i,2), features(i,1), features(i,5)], 'LineWidth', 3);
end
imshow(img);
end
