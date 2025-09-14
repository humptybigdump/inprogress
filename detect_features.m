function features = detect_features(I, number)
%DETECT_FEATURES This function computes image features given the specified
%method. The list of features is returned as [u1 v1; u2 v2; ...; uN vN]   
    corners = detectHarrisFeatures(I);
    strongest = corners.selectStrongest(number);   % select best corners
    features = zeros(strongest.Count, 2);
    for i = 1:strongest.Count
       features(i,:) = round(strongest.Location(i,:));
    end
end

