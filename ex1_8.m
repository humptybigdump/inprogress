%% Exercise 1.8

%% Part 1: Use built-in functions for Sobel Filtering
img1 = imread('../exercises/Images/0001.png');
img1 = double(img1);

sobel_v = fspecial('sobel'); % derivative in horizontal (u) direction
sobel_u = sobel_v';          % derivative in vertical (v) direction

out_v = imfilter(img1, sobel_v, 'conv');
out_u = imfilter(img1, sobel_u, 'conv');

figure;
clims = [-120 120]; 
imagesc(out_u, clims);
colorbar; 
colormap(jet(256)); 
title('Vertical Edges')

figure;
imagesc(out_v, clims);
colorbar
colormap(jet(256));
title('Horizontal Edges')

%% Part 2: Compute gradient length

% initialize an empty black (zeros) image to populate with values
derivative_img = zeros(size(out_v));
[n_rows, n_cols] = size(out_v);
for x=1:n_rows
    for y=1:n_cols    
        derivative_img(x,y) = sqrt(out_u(x,y)^2 + out_v(x,y)^2);          
    end
end

figure;
imagesc(derivative_img);
colorbar;
title('Gradient Length');

%% Part 3: Gaussian Filter

% Here we will create a figure with three subplots. 
figure;
sgtitle('Gaussian Blur'); % set main title

subplot(3,1,1); % subplot(number rows, number columns, index)
f = fspecial('gaussian',11,4);
out = imfilter(img1,f, 'conv');
imshow(uint8(out)) 
title('size=11, sigma=4');

subplot(3,1,2);
f = fspecial('gaussian',20,4);
out = imfilter(img1,f, 'conv');
imshow(uint8(out))
title('size=20, sigma=4');

subplot(3,1,3);
f = fspecial('gaussian',20,10);
out = imfilter(img1,f, 'conv');
imshow(uint8(out))
title('size=20, sigma=10');

%% Canny operator
im1 = imread('../exercises/Images/0001.png');
im2 = imread('../exercises/Images/2176.png');
im3 = imread('../exercises/Images/3526.png');
im4 = imread('../exercises/Images/3964.png');
im5 = imread('../exercises/Images/4083.png');
im6 = imread('../exercises/Images/4886.png');

% create a cell array such that we can access each image with an index
images = {im1, im2, im3, im4, im5, im6}; 
n = length(images);

% Plot all RGB images
fig = figure; 
fig.Position = [100, 100, 1300, 1000]; % adapt the figure size
% position parameters: [x y width height]
% x and y: distance from the lower-left corner of the screen to the lower-left corner of the figure
% width and height: width and height of figure

sgtitle('Images');
for i=1:n
    subplot(n/2, 2, i);
    imshow(images{i});
end

%% Plot with 5.image and canny edge detector
idx = 5;
% define a set of lower and upper thresholds to test out
thrs = [0.05 0.2; ...
        0.1  0.2; ...
        0.05 0.5; ...
        0.3  0.5; ...
        0.05 0.8; ...
        0.3  0.8];

fig = figure; 
fig.Position = [100, 100, 1300, 1000];
sgtitle('Canny Edge Detection');
for i=1:6
    subplot(3, 2, i);

    thrs_low = thrs(i,1);
    thrs_high = thrs(i,2);

    img_ca = edge(images{idx},'canny',[thrs_low thrs_high]);
    imshow(img_ca);
    title("threshold low: " + thrs_low + ', threshold high: ' + thrs_high);
end

% there is no clear best parameter set
% a good set is for instance: [0.1, 0.2]
%% Apply canny operator to all images:
fig = figure; 
fig.Position = [100, 100, 1300, 1000];
sgtitle('Images');
for i=1:n
    subplot(n/2, 2, i);
    imshow(edge(images{i},'canny',[0.1, 0.2]));
end

% figure;
% imshow(edge(images{1},'canny',[0.05, 0.2]))