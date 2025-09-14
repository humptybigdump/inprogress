function [ STATISTICS ] = rc_particle_filter( L, num_particles, num_uniform, sigma_xy, sigma_yaw, sigma_observation, field_geometry )
%RC_PARTICLE_FILTER implements a particle filter for self localization for
%robot soccer applications and visualizes the progress.
%
%   STATISTICS = RC_PARTICLE_FILTER ( L, num_particles, num_uniform,
%                                     sigma_xy, sigma_yaw, 
%                                     sigma_observation,
%                                     field_geometry )
%   with L                   a list of structs that contains for each cycle
%                            an element 'time' that provides the timestamp
%                            of the measurement in seconds, an element
%                            'observation' that contains an n x 2 matrix
%                            of n observed points on field markings (given
%                            in meters in the robocentric coordinate
%                            system), an element 'odometry' that contains
%                            in its first two entries the velocity of the
%                            robot in robocentric coordinates (in meters).
%                            Furthermore, it contains an element
%                            'reference' that provides a reference position
%                            and orientation of the robot determined with
%                            another self-localization algorithm. The first
%                            two entries provide the robot position in
%                            the world coordinate system (in meters) while
%                            the third entry provides the yaw angle in rad.
%                            The reference information is only used to
%                            calculate the self-localization error of the
%                            particle filter.
%                            and in its third entry the yaw rate in rad/s
%        num_particles       the number of particles to use
%        num_uniform         the number of particles that are uniformly
%                            sampled over the whole field in each cycle
%        sigma_xy            the standard deviation of the noise in
%                            translation
%        sigma_yaw           the standard deviation of the noise in the
%                            rotation
%        sigma_observation   the standard deviation of the measurement
%                            noise
%        field_geometry      a struct that describes the field dimensions
%  The function yields a matrix with one row per cycle and 5 columns. The
%  first and second column provide the estimated robot position, the third
%  column provides the estimated yaw angle, the fourth column contains the
%  positioning error (in meters) and the fifth column provides the
%  orientation error (in rad).
%

% represent particles in a global variable. Its entries are: 
% 1. weight, 2. x-position (in m), 3. y-position (in m), 
% 4. yaw angle (in rad between 0 and 2pi)
STATISTICS = zeros(length(L),5);

% initialize the particles by sampling uniform over one half of the field
% (for symmetry reasons we do not need to sample over the whole field).
particles = pf_init (num_particles, field_geometry);
t = L(1).time;
for i=1:length(L)
    % main loop, one cycle per measurement time step
    dt = L(i).time-t;  % determine the time passed since last cycle
    
    % prediction step based on predicted ego movement of the robot
    particles = pf_predict (particles, L(i).odometry(1)*dt, L(i).odometry(2)*dt, L(i).odometry(3)*dt, sigma_xy, sigma_xy, sigma_yaw);
    
    % innovation step based on observed points on field markings
    particles = pf_innovate (particles, L(i).observation, sigma_observation, field_geometry);
    
    % analyze and visualize estimated robot position
    [avpos, avyaw] = pf_average (particles);
    [errpos, erryaw] = pf_error(particles, L(i).reference);
    STATISTICS (i,:) = [ avpos, avyaw, errpos, erryaw ];
    subplot(1,2,1);
    pf_visualize (particles, L(i).reference, L(i).observation, field_geometry);
    axis manual;
    subplot(1,2,2);
    pf_error_plot (STATISTICS(1:i,:));
    pause (0.01);
    
    % resampling step
    particles = pf_resample (particles, num_uniform, field_geometry);
    
    t = L(i).time;
end

end



function [particles] = pf_init (num_particles, field_geometry)
% function pf_init initializes all particles with random positions sampled
% uniformely over one half of the field (due to symmetry reasons we ignore
% the other half).
%   num_particles: the number of particles to sample
particles = zeros (num_particles, 4);  % create matrix of adequate size
particles (:,1) = 1/num_particles;     % set equal particle weights
particles (:,2) = unifrnd (-field_geometry.field_width/2-1, field_geometry.field_width/2+1, num_particles, 1);   % sample uniformly x-positions
particles (:,3) = unifrnd (0, field_geometry.field_length/2+1, num_particles, 1);    % sample uniformly y-positions
particles (:,4) = unifrnd (0, 2*pi, num_particles, 1); % sample uniformly yaw angles
end


function [particles] = pf_predict (particles, delta_x, delta_y, delta_phi, sigma_x, sigma_y, sigma_phi)
% function pf_predict implements the prediction step.
% 'adds' translation and rotation to the robot pose and adds random noise

%%% add your code here!

end


function [particles] = pf_innovate (particles, observations, sigma_observations, field_geometry)
% function pf_innovate implements the innovation step.
% reweights the particles depending on how well the observed points on
% field markings fit to the model of the soccer field.

%%% add your code here!

% normalize weights
ws = sum(particles(:,1));
particles(:,1) = particles(:,1)/ws;
end


function [particles_resampled] = pf_resample (particles, num_uniform, field_geometry)
% function pf_resample implements the resampling step.
% if num_uniform>0 it creates the respective number of new particles that 
% are not resampled from previous particles but generated by uniformly
% sampling over half of the field.
num_particles = size(particles,1);
particles_resampled = zeros(size(particles));
particles_resampled (:,1)=1/size(particles,1);
sel = mnrnd (num_particles-num_uniform, particles(:,1)');
j=1;
for i=1:length(sel)
    while (sel (i)>0)
        particles_resampled (j,2:4) = particles (i,2:4);
        j = j+1;
        sel (i) = sel (i) -1;
    end
end
if (num_uniform>0)
    particles_resampled (num_particles-num_uniform+1:num_particles,2) = unifrnd (-field_geometry.field_width/2-1, field_geometry.field_width/2+1, num_uniform, 1);
    particles_resampled (num_particles-num_uniform+1:num_particles,3) = unifrnd (0, field_geometry.field_length/2+1, num_uniform, 1);
    particles_resampled (num_particles-num_uniform+1:num_particles,4) = unifrnd (0, 2*pi, num_uniform, 1);
end
end


function [ pos, yaw ] = pf_average (particles)
% function pf_average calculates the weighted mean of the particle
% positions and particle orientations
pos = [sum(particles(:,1).*particles(:,2)), sum(particles(:,1).*particles(:,3))];
d = [ sum(particles(:,1).*cos(particles(:,4))), sum(particles(:,1).*sin(particles(:,4))) ];
yaw = atan2 (d(2), d(1));
end


function [ error_pos, error_yaw ] = pf_error (particles, gt_pos)
% function pf_error compares the weighted average pose of the particles
% with the reference pose (gt_pos) and determines the error in position and
% the error in orientation.
[pos, yaw] = pf_average (particles);
error_pos = hypot(pos(1)-gt_pos(1), pos(2)-gt_pos(2));
error_yaw = abs(acos(cos(yaw)*cos(gt_pos(3))+sin(yaw)*sin(gt_pos(3))));
end


function [] = plot_field (field_geometry);
% function plot_field creates a topview of the soccer field with the field 
% markings in black on a white background.
flen2 = field_geometry.field_length/2;
fwid2 = field_geometry.field_width/2;
plen = field_geometry.penalty_area_length;
pwid2 = field_geometry.penalty_area_width/2;
glen = field_geometry.goal_area_length;
gwid2 = field_geometry.goal_area_width/2;
pmd = field_geometry.penalty_marker_distance;
mrad = field_geometry.center_circle_radius;
crad = field_geometry.corner_arc_radius;
circle_lut = [cos([0:120]'*pi/60) sin([0:120]'*pi/60)];
hold on
plot ([-fwid2, fwid2, fwid2, -fwid2, -fwid2], [-flen2, -flen2, flen2, flen2, -flen2], 'k-');
plot ([-fwid2, fwid2], [0, 0], 'k-');
plot ([-gwid2, -gwid2, gwid2, gwid2], [flen2, flen2-glen, flen2-glen, flen2], 'k-');
plot ([-gwid2, -gwid2, gwid2, gwid2], [-flen2, -flen2+glen, -flen2+glen, -flen2], 'k-');
plot ([-pwid2, -pwid2, pwid2, pwid2], [flen2, flen2-plen, flen2-plen, flen2], 'k-');
plot ([-pwid2, -pwid2, pwid2, pwid2], [-flen2, -flen2+plen, -flen2+plen, -flen2], 'k-');
plot ([0 0], [flen2-pmd -flen2+pmd], 'k.');
plot (mrad*circle_lut(:,1), mrad*circle_lut(:,2), 'k-');
plot (-fwid2+crad*circle_lut(1:31,1), -flen2+crad*circle_lut(1:31,2), 'k-');
plot (fwid2+crad*circle_lut(31:61,1), -flen2+crad*circle_lut(31:61,2), 'k-');
plot (fwid2+crad*circle_lut(61:91,1), flen2+crad*circle_lut(61:91,2), 'k-');
plot (-fwid2+crad*circle_lut(91:121,1), flen2+crad*circle_lut(91:121,2), 'k-');
end


function [] = pf_visualize (particles, gt_pos, observations, field_geometry)
% function pf_visualize visualizes the present state of the particle
% filter in a topview of the soccer field.
% black: field markings
% blue:  position of particles
% green: weighted average position of all particles
% red:   reference position of the robot
% gray:  observed points on field markings mapped onto the field using as
%        robot pose the weighted average position and yaw angle calculated
%        from all particles.
plot (0,0,'Color',[1 1 1]);
plot_field (field_geometry);
hold on
[pos, yaw] = pf_average (particles);
cs = cos(yaw);
ss = sin(yaw);
plot (pos(1)+cs*observations(:,1)-ss*observations(:,2), pos(2)+ss*observations(:,1)+cs*observations(:,2), 'o', 'Color', [0.5 0.5 0.5], 'MarkerSize', 2);
plot (particles(:,2), particles(:,3), 'bo', 'MarkerSize', 2);
plot (pos(1), pos(2), 'x', 'Color', [0 0.7 0]);
plot (gt_pos(1), gt_pos(2), 'r*');
hold off
axis ([-field_geometry.field_width/2-1, field_geometry.field_width/2+1, -field_geometry.field_length/2-1, field_geometry.field_length/2+1]);
axis equal;
end


function [] = pf_error_plot (statistics)
% function pf_error_plot visualizes the development of the localization
% error over time
% blue: position error in decimeters
% red:  orientation error in degrees
hold off
plot(10*statistics(:,4), 'b-'); 
hold on; 
plot(statistics(:,5)*180/pi, 'r-');
legend ('position error in dm', 'yaw angle error in degree');

axis_y_range_influence = max(size(statistics,1) - ceil(size(statistics,1) * 0.75), 1):size(statistics,1);
axis ([0.99, size(statistics, 1), 0, 1+max(10*max(statistics(axis_y_range_influence,4)), 180/pi*max(statistics(axis_y_range_influence,5)))]); 
hold off
end
