#!/usr/bin/python

from cagd.polyline import Polyline
from cagd.spline import Spline, Knots
from cagd.vec import Vec2
import cagd.scene_2d as scene_2d

# create an example spline to demonstrate how to create a spline
# you can use this to test your implementation of the de-boor algorithm
#    and the knot_index function
example_spline = Spline(3)
example_spline.control_points = [Vec2(0, 0), Vec2(0, 1), Vec2(1, 1), Vec2(1, 0), Vec2(2, 0)]
example_spline.knots = Knots(9)
example_spline.knots.knots = [0, 0, 0, 0, 1, 2, 2, 2, 2]
p = example_spline.get_polyline_from_control_points()
p.set_color("red")

# interpolate six points with the four different interpolation options to
#    draw a small letter "e"
# uncomment these lines once you implemented the spline interpolation
# pts = [Vec2(0,.4), Vec2(.8,.8), Vec2(.5,1.2), Vec2(-.03,.4), Vec2(.4,0), Vec2(1,.2)]
# s1 = Spline.interpolate_cubic(Spline.INTERPOLATION_EQUIDISTANT, pts, Knots(1))
# s2 = Spline.interpolate_cubic(Spline.INTERPOLATION_CHORDAL, pts, Knots(1))
# s3 = Spline.interpolate_cubic(Spline.INTERPOLATION_CENTRIPETAL, pts, Knots(1))
# s4 = Spline.interpolate_cubic(Spline.INTERPOLATION_FOLEY, pts, Knots(1))
# s1.set_color("#000066")
# s2.set_color("#0000aa")
# s3.set_color("#6666ff")
# s4.set_color("#aaaaff")
# p = Polyline()
# p.points = pts
# p.set_color("red")

# generate a scene and add elements to it
sc = scene_2d.Scene()
sc.set_resolution(900)
sc.add_element(example_spline)
sc.add_element(p)
# sc.add_element(s1)
# sc.add_element(s2)
# sc.add_element(s3)
# sc.add_element(s4)
sc.write_image()  # compose all elements in the scene
sc.show()  # tries to show the image with a default viewer
sc.write_to_file("test.png")  # saves the image to a file
