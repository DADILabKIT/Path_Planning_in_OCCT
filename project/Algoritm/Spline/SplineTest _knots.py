from OCC.Core.gp import gp_Circ, gp_Ax2, gp_Dir, gp_Pnt, gp_Vec
from OCC.Core.Geom import Geom_BSplineCurve, Geom_Circle
from OCC.Core.TColStd import TColStd_Array1OfReal, TColStd_Array1OfInteger
from OCC.Core.TColgp import TColgp_Array1OfPnt
from OCC.Core.BRepBuilderAPI import BRepBuilderAPI_MakeEdge, BRepBuilderAPI_MakeWire
from OCC.Core.BRepPrimAPI import BRepPrimAPI_MakeSphere
from OCC.Display.SimpleGui import init_display
from OCC.Core.BRepExtrema import BRepExtrema_DistShapeShape
from OCC.Core.BRepOffsetAPI import BRepOffsetAPI_MakePipe
from OCC.Core.BRepClass3d import BRepClass3d_SolidClassifier
from OCC.Core.TopAbs import TopAbs_IN, TopAbs_ON, TopAbs_OUT
from OCC.Core.TopoDS import topods_Solid

a,b,c,d = init_display()

# m = p + n + 1
degree = 3 # p, n=10, m=14.

pole_list = [gp_Pnt(0,0,0), gp_Pnt(100,100,0), gp_Pnt(100,100,100), gp_Pnt(200,200,500), gp_Pnt(500,500,30), gp_Pnt(600,700,900), gp_Pnt(700,700,1000), gp_Pnt(1100,1100,1000), gp_Pnt(1200,2100,1000), gp_Pnt(1500,1500,1800)]

# Define multiplicity array
mults = TColStd_Array1OfInteger(1, 5)
mults.SetValue(1, 4)
mults.SetValue(2, 2)
mults.SetValue(3, 2)
mults.SetValue(4, 2)
mults.SetValue(5, 4)

# Define knot arrays for uniform and non-uniform B-Splines
knots_uniform = TColStd_Array1OfReal(1, 5)
knots_nonuniform = TColStd_Array1OfReal(1, 5)

# Uniform knot vector
knots_uniform.SetValue(1, 0.0)
knots_uniform.SetValue(2, 1*1.0/4)
knots_uniform.SetValue(3, 2*1.0/4)
knots_uniform.SetValue(4, 3*1.0/4)
knots_uniform.SetValue(5, 1.0)

# Non-uniform knot vector
knots_nonuniform.SetValue(1, 0.0)
knots_nonuniform.SetValue(2, 0.3)
knots_nonuniform.SetValue(3, 0.5)
knots_nonuniform.SetValue(4, 0.65)
knots_nonuniform.SetValue(5, 1.0)

# Define control points and weights
poles = TColgp_Array1OfPnt(1, 10)
weights = TColStd_Array1OfReal(1, 10)

for i in range(len(pole_list)):
    poles.SetValue(i+1, pole_list[i])
    if (i==4):
        weights.SetValue(i+1, 2) # 1대신 특정점에 다른 weight 주려고 만든 line.
    else:
        weights.SetValue(i+1, 1)

# Create B-Splines
bc_uniform = Geom_BSplineCurve(poles, weights, knots_uniform, mults, degree)
bc_nonuniform = Geom_BSplineCurve(poles, weights, knots_nonuniform, mults, degree)

ed_uniform = BRepBuilderAPI_MakeEdge(bc_uniform).Edge()
ed_nonuniform = BRepBuilderAPI_MakeEdge(bc_nonuniform).Edge()

wire_uniform = BRepBuilderAPI_MakeWire(ed_uniform).Wire()
wire_nonuniform = BRepBuilderAPI_MakeWire(ed_nonuniform).Wire()

# Diameter for the cable
diameter = 200.0
direction_vec = gp_Vec(pole_list[1].XYZ()) - gp_Vec(pole_list[0].XYZ())
direction_dir = gp_Dir(direction_vec)

circle = Geom_Circle(gp_Ax2(pole_list[0], direction_dir), diameter / 2)
section = BRepBuilderAPI_MakeEdge(circle).Edge()

pipe_uniform = BRepOffsetAPI_MakePipe(wire_uniform, section).Shape()
pipe_nonuniform = BRepOffsetAPI_MakePipe(wire_nonuniform, section).Shape()

#```python
# display
for i in range(len(pole_list)):
    s = BRepPrimAPI_MakeSphere(pole_list[i], 30).Shape()
    a.DisplayShape(s, color='blue')

for i in range(1, knots_uniform.Length() + 1):  
    u = knots_uniform.Value(i)
    pnt = bc_uniform.Value(u)
    s = BRepPrimAPI_MakeSphere(pnt, 30).Shape()
    a.DisplayShape(s, color='red',transparency=0.6)

for i in range(1, knots_nonuniform.Length() + 1):  
    u = knots_nonuniform.Value(i)
    pnt = bc_nonuniform.Value(u)
    s = BRepPrimAPI_MakeSphere(pnt, 30).Shape()
    a.DisplayShape(s, color='blue',transparency=0.6)

a.DisplayShape(ed_uniform, color='red')
a.DisplayShape(ed_nonuniform, color='blue')
a.DisplayShape(pipe_uniform, color='red', transparency=0.9)
a.DisplayShape(pipe_nonuniform, color='blue', transparency=0.9)
a.FitAll()
b()
