function [features_clean, descriptors] = extract_sift_light_descriptors(I, features)
% EXTRACT_SIFT_LIGHT_DESCRIPTORS Extracts SIFT (light) descriptors from the
% image given the interest points as returned by
% detect_sift_light_features(..). It eliminates all features points for
% which no descriptor can be calculated.
%
% function [features_clean, descriptors] = extract_sift_light_descriptors(I, features)
%   with        I: the input image (a graylevel image)
%        features: the list of interest points as N-by-5 matrix. Each row
%                  represents one interest point with entries
%                  [v u c(as integer) L-value scale(as double)]
%  features_clean: the subset of features for which descriptors could be
%                  calculated
%     descriptors: the descriptors calculated, represented as N-by-32
%                  matrix. Each row represents the descriptor for the
%                  corresponding interest point in features_clean

[height, width] = size(I);
[Gu, Gv] = gradient(double(I));  % calculate the graylevel gradient (Gu, Gv are partial derivatives)
n = size(features,1);     % number of interest points

descriptors = -ones(n, 4*8);  % initalize descriptors with negative numbers (negative numbers indicate invalid entries)

% iterate over all feature points
for i=1:n
    % calculate the size of the box around the interest point depending on
    % the scale value
    v = features(i,1);
    u = features(i,2);
    scale = features(i,5); 
    half_block_size = round(scale*5);
    
    % if the box extends over the image size, we do not calculate a
    % descriptor for this interest point
    if ((u-half_block_size<1) || (v-half_block_size<1) || (u+half_block_size>width) || (v+half_block_size>height))
        continue;  
    end
    
    descriptor(1:8)     = calculate_orientation_histogram(...
        Gu(v-half_block_size+1:v, u-half_block_size+1:u), ...
        Gv(v-half_block_size+1:v, u-half_block_size+1:u));

    descriptor(9:16)    = calculate_orientation_histogram(...
        Gu(v-half_block_size+1:v, u+1:u+half_block_size), ...
        Gv(v-half_block_size+1:v, u+1:u+half_block_size));

    descriptor(17:24)   = calculate_orientation_histogram(...
        Gu(v+1:v+half_block_size, u-half_block_size+1:u), ...
        Gv(v+1:v+half_block_size, u-half_block_size+1:u));

    descriptor(25:32)   = calculate_orientation_histogram(...
        Gu(v+1:v+half_block_size, u+1:u+half_block_size), ...
        Gv(v+1:v+half_block_size, u+1:u+half_block_size));
    
    % normalize descriptor (in order to get rid of scale)
    % Euclidean length of descriptor
    s = sqrt(sum(descriptor.^2))+1e-50;  % adding 1e-50 in order to avoid division by zero
    descriptors(i,:) = descriptor/s;
end

idx_select = (descriptors(:,1)>-1);   % filter features with valid descriptors
features_clean = features(idx_select,:);
descriptors = descriptors(idx_select,:);
end


function [ histogram ] = calculate_orientation_histogram (Gu, Gv) 
% function [ histogram ] = calculate_orientation_histogram (Gu, Gv)
%
% calculates an orientation histogram based on 8 direction sectors
% for a given image region with partial derivatives Gu and Gv

histogram = zeros(1, 8);
Glen = sqrt(Gu.^2+Gv.^2);          % the gradient length for each pixel
Gdir = atan2(Gv,Gu)*180/pi+180;    % the gradient direction in degree between 0° and 360° for each pixel
Gbin = mod(floor((Gdir)/45),8)+1;  % the orientation sector to which each pixel belongs (mod is necessary to map angles of 360° to the first sector) 
for v=1:size(Gu,1)
    for u=1:size(Gu,2)
        histogram(Gbin(v,u)) = histogram(Gbin(v,u)) + Glen(v,u);
    end
end
end
