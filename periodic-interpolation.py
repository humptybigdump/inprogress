#!/usr/bin/python

import cagd.scene_2d as scene
from cagd.vec import Vec2
from cagd.spline import Spline, Knots
from cagd.polyline import Polyline


# returns a list of num_samples points that are uniformly distributed on the unit circle
def unit_circle_points(num_samples):
    return []


# calculates the deviation between the given spline and a unit circle
def calculate_circle_deviation(spline):
    pass


# interpolate 6 points with a periodic spline to create the number "8"
pts = [Vec2(0, 2.5), Vec2(-1, 1), Vec2(1, -1), Vec2(0, -2.5), Vec2(-1, -1), Vec2(1, 1)]
pts_line = Polyline()
pts_line.points = pts
pts_line.set_color("red")
s = Spline.interpolate_cubic_periodic(pts)
p = s.get_polyline_from_control_points()
p.set_color("blue")
sc = scene.Scene()
sc.set_resolution(900)
sc.add_element(s)
sc.add_element(p)

# generate a spline that approximates the unit circle
# n = 8
# circle_pts = unit_circle_points(n)
# circle = Spline.interpolate_cubic_periodic(circle_pts)
# sc.add_element(circle)
# calculate_circle_deviation(circle)

sc.write_image()
sc.show()
