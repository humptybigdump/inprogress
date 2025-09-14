function visualize_feature_matching(I1, I2, F1, F2, matches, name)
% VISUALIZE_FEATURE_MATCHING Visualizes the feature matches for two images
% I1 and I2 with interest points F1 and F2 and given matches 
    figure('Name', name); hold on;
    [height1, width1] = size(I1);
    [height2, width2] = size(I2);
    if (width1 ~= width2 || height1 ~= height2)
       error('Mismatching image sizes provided'); 
    end
    I = 255*zeros(height1 + height2, width1, 3, 'uint8');
    I(1:height1,:,:) = repmat(I1, [1 1 3]);
    I(height1+1:height1+height2,:,:) = repmat(I2, [1 1 3]);
    for i = 1:size(matches, 1)
        p1 = F1(matches(i,1), 1:2);
        p2 = F2(matches(i,2), 1:2) + [height1 0];
        I = insertShape(I, 'Line', [p1(2), p1(1), p2(2), p2(1)], 'LineWidth', 2, 'Color', 'red');
        I = insertShape(I, 'Circle', [p1(2), p1(1), 3; p2(2), p2(1), 3], 'LineWidth', 3);
    end
    imshow(I);
end

