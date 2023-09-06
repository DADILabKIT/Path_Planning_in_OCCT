from OCC.Core.gp import gp_Circ, gp_Ax2, gp_Dir, gp_Pnt, gp_Vec
from OCC.Core.Geom import Geom_BSplineCurve, Geom_Circle
from OCC.Core.TColStd import TColStd_Array1OfReal, TColStd_Array1OfInteger
from OCC.Core.TColgp import TColgp_Array1OfPnt
from OCC.Core.BRepBuilderAPI import BRepBuilderAPI_MakeEdge, BRepBuilderAPI_MakeWire
from OCC.Core.BRepPrimAPI import BRepPrimAPI_MakeSphere, BRepPrimAPI_MakeBox
from OCC.Display.SimpleGui import init_display
from OCC.Core.BRepExtrema import BRepExtrema_DistShapeShape
from OCC.Core.BRepOffsetAPI import BRepOffsetAPI_MakePipe
from OCC.Core.BRepClass3d import BRepClass3d_SolidClassifier
from OCC.Core.TopAbs import TopAbs_IN, TopAbs_ON, TopAbs_OUT
from OCC.Core.TopoDS import topods_Solid
from OCC.Core.TopExp import TopExp_Explorer
from OCC.Core.TopAbs import TopAbs_VERTEX
from OCC.Core.TopoDS import topods_Vertex
from OCC.Core.BRep import BRep_Tool
from OCC.Core.BRepMesh import BRepMesh_IncrementalMesh
import time
from OCC.Core.Quantity import (
    Quantity_Color,
    Quantity_NOC_BLACK,
    Quantity_NOC_GRAY,
    Quantity_NOC_WHITE,
    Quantity_NOC_WHITESMOKE
)
from Render.TessellatorShape import TessellatorShape
from Render.STPRender import STPRender
from Render.TessellatorCompound import TessellatorCompound



a,b,c,d = init_display()
a.View.SetBgGradientColors(
    Quantity_Color(Quantity_NOC_GRAY),
    Quantity_Color(Quantity_NOC_GRAY),
    2,
    True,
)
# m = p + n + 1 # m: 다중도, p: 차수, n: poles=제어점 수=path points and weights
degree = 3 # p, n=10, m=14.


mults = TColStd_Array1OfInteger(1, 5)

mults.SetValue(1, 4)
mults.SetValue(2, 2)
mults.SetValue(3, 2)
mults.SetValue(4, 2)
mults.SetValue(5, 4)

# Uniform knot vector
knots_uniform = TColStd_Array1OfReal(1, 5)
knots_uniform.SetValue(1, 0.0)
knots_uniform.SetValue(2, 1*1.0/4)
knots_uniform.SetValue(3, 2*1.0/4)
knots_uniform.SetValue(4, 3*1.0/4)
knots_uniform.SetValue(5, 1.0)

# Non-uniform knot vector (less curved)
knots_nonuniform_less_curved = TColStd_Array1OfReal(1, 5)
knots_nonuniform_less_curved.SetValue(1, 0.0)
knots_nonuniform_less_curved.SetValue(2, 0.1)
knots_nonuniform_less_curved.SetValue(3, 0.5)
knots_nonuniform_less_curved.SetValue(4, 0.9)
knots_nonuniform_less_curved.SetValue(5, 1.0)

# Non-uniform knot vector (more curved)
knots_nonuniform_more_curved = TColStd_Array1OfReal(1, 5)
knots_nonuniform_more_curved.SetValue(1, 0.0)
knots_nonuniform_more_curved.SetValue(2, 0.2)
knots_nonuniform_more_curved.SetValue(3, 0.8)
knots_nonuniform_more_curved.SetValue(4, 0.9)
knots_nonuniform_more_curved.SetValue(5, 1.0)

# n
poles = TColgp_Array1OfPnt(1, 10)
weights = TColStd_Array1OfReal(1, 10)

# path points 임의 지정
pole_list = [gp_Pnt(0,0,0), gp_Pnt(100,100,0), gp_Pnt(100,100,100), gp_Pnt(200,200,500), gp_Pnt(500,500,30), gp_Pnt(600,700,900), gp_Pnt(700,700,1000), gp_Pnt(1100,1100,1000), gp_Pnt(1200,2100,1000), gp_Pnt(1500,1500,1800)]
for i in range(len(pole_list)):
    poles.SetValue(i+1, pole_list[i])
    weights.SetValue(i+1, 1)

# Make Pipe
diameter = 200.0 # Diameter for the cable
direction_vec = gp_Vec(pole_list[1].XYZ()) - gp_Vec(pole_list[0].XYZ())
direction_dir = gp_Dir(direction_vec)

circle = Geom_Circle(gp_Ax2(pole_list[0], direction_dir), diameter / 2)
section = BRepBuilderAPI_MakeEdge(circle).Edge()

# Create and display the curves
i = 1
for knots, color in [(knots_uniform, 'black'), (knots_nonuniform_less_curved, 'blue'), (knots_nonuniform_more_curved, 'red')]:
    # display
    a.EraseAll()
    a.hide_triedron()
    a.View.SetBgGradientColors(                     
        Quantity_Color(Quantity_NOC_GRAY),
        Quantity_Color(Quantity_NOC_GRAY),
        2,
        True,
    )
    bc = Geom_BSplineCurve(poles, weights, knots, mults, 3)
    ed = BRepBuilderAPI_MakeEdge(bc).Edge()
    wire = BRepBuilderAPI_MakeWire(ed).Wire()
    pipe = BRepOffsetAPI_MakePipe(wire, section).Shape()
    a.DisplayShape(pipe, color=color, transparency=0.7)

    # Draw the poles as small boxes in a different color (e.g., yellow)
    for pole in pole_list:
        box = BRepPrimAPI_MakeBox(pole, 10,10,10).Shape()
        a.DisplayShape(box, color='yellow')

    # Draw the knots as solid spheres in a different color (e.g., purple)
    for j in range(1, knots.Length() + 1):  
        u = knots.Value(j)
        pnt = bc.Value(u)
        sphere = BRepPrimAPI_MakeSphere(pnt, 30).Shape()
        a.DisplayShape(sphere, color='purple')

    a.FitAll()
    a.View.Dump(r"{}.png".format(i))
    a.EraseAll()
    i += 1