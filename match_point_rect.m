function match = match_point_rect(I1, I2, p, window_size) 
% Find the best match (in image I2) for a given point p (from Image I1) 
% under the assumption that the images are rectified. 
% Arguments:
%   I1: left image
%   I2: right image
%   p:  The image point coordinates (x, y) of a point in the left image
%       (I1).
%   window_size: [height, width] of window to use to compute the comparison
%                 metric
%   Output: image coordinates (match = [u, v]) of a point in the right
%           image (I2) that match point p
% Note: the height and width parameters of the window_size arguments are
% expected to be odd.

%% Step 1: Perform quality checks on input arguments

% Get dimensions of images and check if they are identical
if ~(all(size(I1) == size(I2)))
    error('The image dimensions are not identical');
end
[height, width] = size(I1);

% Check whether point p is within image I1
if (p(1) <= 0 || p(2) <= 0 || p(1) > width || p(2) > height)
    error('The point is not within the image');
end

% Check the input for the window_size
if (mod(window_size(1),2) == 0 || mod(window_size(2),2) == 0)
    error('The width and height of the window size must be odd');
end

%% Part 2: Perform Search

% Compute number of pixels within search area:
size_search_area = width;                 

% We want to save all match results in an array:
match_value = zeros(size_search_area, 3);  % each row will contain [u v sum_of_absolute_diff]
% Get the image patch from the left image:
patch1 = extract_image_patch(I1, p, window_size); 

% iterate over all pixels within the search boundary
counter = 1;
v = p(2);
for u = 1:width
    % extract an image patch from I2
    patch2 = extract_image_patch(I2, [u v], window_size); 

    % compute the sum of absolute differences
    % the conversion to double is required here
    sum_of_absolute_diff = sum(sum(abs((double(patch1) - double(patch2))))); 

    % Save the result
    match_value(counter,:) = [u v sum_of_absolute_diff];
    counter = counter + 1;
end

% sort the match_value matrix by the third column (= sum_of_absolute_diff)
% order: ascending
match_value = sortrows(match_value, 3);
% get the pixel location with minimal difference
match = match_value(1, 1:2);

end


