function visualize_matched_points(I1, I2, p, matches, name)
% VISUALIZE_MATCHED_POINTS Visualizes the matches for a point p (of image
% I1)
    figure('Name', name); hold on;
    [height1, width1] = size(I1);
    [height2, width2] = size(I2);
    if (width1 ~= width2 || height1 ~= height2)
       error('Mismatching image sizes provided'); 
    end
    I = 255*zeros(height1 + height2, width1, 3, 'uint8');
    I(1:height1,:,:) = repmat(I1, [1 1  3]);
    I(height1+1:height1+height2,:,:) = repmat(I2, [1 1 3]);
    I = insertShape(I, 'Circle', [p(1), p(2), 3], 'LineWidth', 3);
    for i = 1:size(matches, 1)
        m = matches(i, 1:2) + [0 height1];
        I = insertShape(I, 'Line', [p(1), p(2), m(1), m(2)], 'LineWidth', 2, 'Color', 'red');
        I = insertShape(I, 'Circle', [m(1), m(2), 3], 'LineWidth', 3);
    end
    imshow(I);
end

