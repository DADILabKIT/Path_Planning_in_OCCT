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
from itertools import combinations_with_replacement



a,b,c,d = init_display()
a.View.SetBgGradientColors(
    Quantity_Color(Quantity_NOC_GRAY),
    Quantity_Color(Quantity_NOC_GRAY),
    2,
    True,
)
# m = p + n + 1 # m: 다중도, p: 차수, n: poles=제어점 수=path points and weights
degree = 3 # p, n=10, m=14.



# Define possible values for the multiplicity
possible_values = range(1, 4)

# Define the number of intermediate multiplicity values
num_intermediate_values = 6

# Find all combinations with a sum of 3
combinations = [seq for i in range(1, num_intermediate_values+1) for seq in combinations_with_replacement(possible_values, i) if sum(seq) == num_intermediate_values and max(seq) <= 3]

# Iterate through each combination
for idx, mults_values in enumerate(combinations):

    # Define multiplicities
    mults = TColStd_Array1OfInteger(1, 2+len(mults_values))
    mults.SetValue(1, 4)
    for i, value in enumerate(mults_values, start=2):
        mults.SetValue(i, value)
    mults.SetValue(2+len(mults_values), 4)

    # Print mults values for debugging
    print("Mults:")
    for i in range(1, 2+len(mults_values)+1):
        print(mults.Value(i))

    # Uniform knot vector
    knots = TColStd_Array1OfReal(1, 2+len(mults_values))
    for i in range(1, 2+len(mults_values) + 1):
        knots.SetValue(i, (i-1)*1.0/(2+len(mults_values)-1))

    # Print knots values for debugging
    print("Knots:")
    for i in range(1, 2+len(mults_values) + 1):
        print(knots.Value(i))
    
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
    a.DisplayShape(pipe, color='black', transparency=0.7)

    # Draw the poles as small boxes in a different color (e.g., yellow)
    for pole in pole_list:
        box = BRepPrimAPI_MakeBox(pole, 10,10,10).Shape()
        a.DisplayShape(box, color='yellow')

    # Draw the knots as solid spheres in a different color (e.g., purple)
    for j in range(1, knots.Length() + 1):  
        u = knots.Value(j)
        pnt = bc.Value(u)
        sphere = BRepPrimAPI_MakeSphere(pnt, 30).Shape()
        a.DisplayShape(sphere, color='orange')

    # Dump the view to a file
    a.FitAll()
    filename = "mults_" + "_".join(map(str, mults_values)) + ".png"
    a.View.Dump(filename)
    a.EraseAll()


