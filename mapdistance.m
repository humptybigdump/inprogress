function [ d ] = mapdistance( xy, field_geometry )
%MAPDISTANCE calculate the distance of a point on the robot soccer field to
%the closest field marking
%   d = mapdistance (xy)
%       with xy a position on the field xy=[x,y]
%       where x is the lateral position and y the longitudinal position

if (abs(xy(1))<field_geometry.field_width/2)
    if (abs(xy(2))<field_geometry.field_length/2)
        d = field_geometry.lut (round(abs(xy(1))/field_geometry.lut_resolution)+1, round(abs(xy(2))/field_geometry.lut_resolution)+1);
    else
        d = abs(xy(2))-field_geometry.field_length/2;
    end
else
    if (abs(xy(2))<field_geometry.field_length/2)
        d = abs(xy(1))-field_geometry.field_width/2;
    else
        d = hypot (abs(xy(1))-field_geometry.field_width/2, abs(xy(2))-field_geometry.field_length/2);
    end
end
end
