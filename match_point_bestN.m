function matches = match_point_bestN(I1, I2, p, N, search_area, window_size)
% Find the best N matches (in image I2) for a given point p (from Image I1). 
% Arguments:
%   I1: left image
%   I2: right image
%   p:  The image point coordinates (x, y) of a point in the left image
%       (I1).
%   N: number of best matches to return (between 1 and 10)
%   search_area: [height, width] of search area
%   window_size: [height, width] of window to use to compute the comparison
%                 metric
%   Output: image coordinates (matches = [u1, v1; ... ; uN, vN]) for the
%           best N points in the right image (I2) that match point p
%
% Note: the height and width parameters of the search_area and window_size
% arguments are expected to be odd.

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

% Check the input for the search_area and window_size
if (mod(search_area(1),2) == 0 || mod(search_area(2),2) == 0)
    error('The width and height of the search area must be odd');
end
if (mod(window_size(1),2) == 0 || mod(window_size(2),2) == 0)
    error('The width and height of the window size must be odd');
end

% Check N
if (N < 1 || N > 10)
    error('N is not within the range of 1 and 10');
end
% round N to the nearest integer
N = round(N);

%% Part 2: Perform Search

% Since the dimensions of the search area are odd, its width and height 
% can be expressed by: 2n+1 and 2m+1, respectively. Then, n 
% (search_sz_half_u) and m (search_sz_half_v) represent the number of
% pixels from the center of the search area to its edge in u and v
% direction.
search_sz_half_u = (search_area(2)-1) / 2;
search_sz_half_v = (search_area(1)-1) / 2;

% When the search area ranges over the image, we have to further restrict
% our search boundaries:
search_boundaries_u = [max(1, p(1) - search_sz_half_u), min(width, p(1) + search_sz_half_u)];
search_boundaries_v = [max(1, p(2) - search_sz_half_v), min(height, p(2) + search_sz_half_v)];

% Compute number of pixels within search area:
size_search_area = (search_boundaries_u(2) - search_boundaries_u(1) + 1) * ...
    (search_boundaries_v(2) - search_boundaries_v(1) + 1); 

% If N is larger then the restricted search area, we have to adapt N
if N > size_search_area
    N = size_search_area;
end

% We want to save all match results in an array:
match_value = zeros(size_search_area, 3);  % each row will contain [u v sum_of_absolute_diff]
% Get the image patch from the left image:
patch1 = extract_image_patch(I1, p, window_size);    

% iterate over all pixels within the search boundary
counter = 1;
for u = search_boundaries_u(1):search_boundaries_u(2)
    for v = search_boundaries_v(1):search_boundaries_v(2)
        % extract an image patch from I2
        patch2 = extract_image_patch(I2, [u v], window_size); 

        % compute the sum of absolute differences
        % the conversion to double is required here
        sum_of_absolute_diff = sum(sum(abs((double(patch1) - double(patch2))))); 

        % Save the result
        match_value(counter,:) = [u v sum_of_absolute_diff];
        counter = counter + 1;
    end
end

% sort the match_value matrix by the thrid column (= sum_of_absolute_diff)
% order: ascending
match_value = sortrows(match_value, 3);

% get the N pixel locations with minimal difference
matches = match_value(1:N, 1:2);
end
