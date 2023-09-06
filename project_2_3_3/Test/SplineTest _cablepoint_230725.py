import util

from OCC.Core.gp import gp_Circ, gp_Ax2, gp_Dir, gp_Pnt, gp_Vec
from OCC.Core.Geom import Geom_BSplineCurve, Geom_Circle
from OCC.Core.TColStd import TColStd_Array1OfReal, TColStd_Array1OfInteger
from OCC.Core.TColgp import TColgp_Array1OfPnt
from OCC.Core.BRepBuilderAPI import BRepBuilderAPI_MakeEdge, BRepBuilderAPI_MakeWire
from OCC.Display.SimpleGui import init_display
from OCC.Core.BRepOffsetAPI import BRepOffsetAPI_MakePipe
from OCC.Core.Quantity import (
    Quantity_Color,
    Quantity_NOC_WHITE
)

a, b, c, d = init_display()
a.View.SetBgGradientColors(
    Quantity_Color(Quantity_NOC_WHITE),
    Quantity_Color(Quantity_NOC_WHITE),
    2,
    True,
)
# m = p + n + 1 # m: 다중도, p: 차수, n: poles=제어점 수=path points and weights
degree = 3  # p, n=10, m=14.


mults = TColStd_Array1OfInteger(1, 5)

mults.SetValue(1, 4)
mults.SetValue(2, 3)
mults.SetValue(3, 2)
mults.SetValue(4, 1)
mults.SetValue(5, 4)

# m 균일
knots = TColStd_Array1OfReal(1, 5)
knots.SetValue(1, 0.0)
knots.SetValue(2, 1*1.0/4)
knots.SetValue(3, 2*1.0/4)
knots.SetValue(4, 3*1.0/4)
knots.SetValue(5, 1.0)

# n
poles = TColgp_Array1OfPnt(1, 10)
weights = TColStd_Array1OfReal(1, 10)

# path points 임의 지정
pole_list = [gp_Pnt(0, 0, 0), gp_Pnt(100, 100, 0), gp_Pnt(100, 100, 100), gp_Pnt(200, 200, 500), gp_Pnt(500, 500, 30), gp_Pnt(
    600, 700, 900), gp_Pnt(700, 700, 1000), gp_Pnt(1100, 1100, 1000), gp_Pnt(1200, 2100, 1000), gp_Pnt(1500, 1500, 1800)]

for i in range(len(pole_list)):
    poles.SetValue(i+1, pole_list[i])
    weights.SetValue(i+1, 1)


# Make BSplineCurve
bc = Geom_BSplineCurve(poles, weights, knots, mults, 3)
ed = BRepBuilderAPI_MakeEdge(bc).Edge()
wire = BRepBuilderAPI_MakeWire(ed).Wire()


diameter = 200.0
direction_vec = gp_Vec(pole_list[1].XYZ()) - gp_Vec(pole_list[0].XYZ())
direction_dir = gp_Dir(direction_vec)

circle = Geom_Circle(gp_Ax2(pole_list[0], direction_dir), diameter / 2)
section = BRepBuilderAPI_MakeEdge(circle).Edge()

pipe = BRepOffsetAPI_MakePipe(wire, section).Shape()

a.DisplayShape(pipe, color='blue', transparency=0.7)
a.FitAll()
b()
