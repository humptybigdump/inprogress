%% Exercise 1.7

%% Read the image
img1 = imread('../exercises/Images/0001.png');
imshow(img1);

%% Inspect image
img1_size = size(img1);
img1_min = min(img1(:));
img1_max = max(img1(:));
img1_mean = mean(img1(:));

%% Read second image and transform into gray-level image
img2 = imread('../exercises/Images/0002.png');

img2_gray = rgb2gray(img2);

% display rgb and gray-level image
montage({img2, img2_gray});

% optional: add visualizations of the color-channels to the figure
%montage({img2,img2_gray,img2(:,:,1),img2(:,:,2),img2(:,:,3)});

%% Sobel Filters
img1 = double(img1);

% don't forget to rotate the sobel filters:
sobel_u = rot90(rot90([1 0 -1; 2 0 -2; 1 0 -1])); % derivative in horizontal (u) direction 
sobel_v = sobel_u'; % derivative in vertical (v) direction 
% Note: as we don't need the absolute values of the gradients but are
% rather interested in differences between gradient values, we can omit 
% the scaling factor 1/8

[n_rows, n_cols] = size(img1);

% Prepare two matrices two save the results
output_u = zeros(size(img1));
output_v = zeros(size(img1));

for row = 2:n_rows-1
    for col = 2:n_cols-1
        output_u(row, col) = sum(sum(img1(row-1:row+1, col-1:col+1).*sobel_u));
        output_v(row, col) = sum(sum(img1(row-1:row+1, col-1:col+1).*sobel_v));
    end
end

% If we want to create several visualizations, it is useful to initalize
% each new one with the command 'figure'
figure;
clims = [-120 120]; % specifies the data values that map to the first and last elements of the colormap
imagesc(output_u, clims);
colorbar; % add a colorbar
colormap(jet(256)); % change the colormap
title('Vertical Edges')

figure;
imagesc(output_v, clims);
colorbar
colormap(jet(256));
title('Horizontal Edges')