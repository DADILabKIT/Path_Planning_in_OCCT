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
    Quantity_NOC_WHITE
)
from Render.TessellatorShape import TessellatorShape
from Render.STPRender import STPRender
from Render.TessellatorCompound import TessellatorCompound



a,b,c,d = init_display()
a.View.SetBgGradientColors(
    Quantity_Color(Quantity_NOC_WHITE),
    Quantity_Color(Quantity_NOC_WHITE),
    2,
    True,
)
# m = p + n + 1
degree = 3 # p, n=10, m=14.


mults = TColStd_Array1OfInteger(1, 5)

mults.SetValue(1, 4)
mults.SetValue(2, 2)
mults.SetValue(3, 2)
mults.SetValue(4, 2)
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

pole_list = [gp_Pnt(0,0,0), gp_Pnt(100,100,0), gp_Pnt(100,100,100), gp_Pnt(200,200,500), gp_Pnt(500,500,30), gp_Pnt(600,700,900), gp_Pnt(700,700,1000), gp_Pnt(1100,1100,1000), gp_Pnt(1200,2100,1000), gp_Pnt(1500,1500,1800)]
for i in range(len(pole_list)):
    poles.SetValue(i+1, pole_list[i])
    if (i==4):
        weights.SetValue(i+1, 1)
        #continue
    weights.SetValue(i+1, 1)


bc = Geom_BSplineCurve(poles, weights, knots, mults, 3)
ed = BRepBuilderAPI_MakeEdge(bc).Edge()
wire = BRepBuilderAPI_MakeWire(ed).Wire()

# Diameter for the cable
diameter = 200.0
direction_vec = gp_Vec(pole_list[1].XYZ()) - gp_Vec(pole_list[0].XYZ())
direction_dir = gp_Dir(direction_vec)

circle = Geom_Circle(gp_Ax2(pole_list[0], direction_dir), diameter / 2)
section = BRepBuilderAPI_MakeEdge(circle).Edge()

pipe = BRepOffsetAPI_MakePipe(wire, section).Shape()

obstacle_radius = diameter * 1.1  # Make the sphere a bit larger than the diameter of the cable


# 장애물
middle_pnt = bc.Value(bc.FirstParameter() + ((bc.LastParameter() - bc.FirstParameter()) / 2.5))  
obstacle2 = BRepPrimAPI_MakeSphere(middle_pnt, obstacle_radius).Shape()
a.DisplayShape(obstacle2, color='red', transparency=0.6)

start = time.time()

tlt = TessellatorShape(obstacle2, a)

# 샘플링 개수 입력 후 샘플링 진행
tlt.mesh.RandomSampling(100)

# 샘플링 점 가시화
vertices = tlt.mesh.Points
#print(vertices)

# 가시화
# for vertex in vertices:
#     sphere = BRepPrimAPI_MakeSphere(vertex, 10).Shape()
#     a.DisplayShape(sphere, color='black')



# Create solid classifier
classifier = BRepClass3d_SolidClassifier(pipe)

# Check which vertices are inside the cable
inside_vertices = []
for vertex in vertices:
    classifier.Perform(vertex, 1e-6)  # 1e-6 is the precision, adjust as needed
    state = classifier.State()
    if state in (TopAbs_ON, TopAbs_IN):
        inside_vertices.append(vertex)

print("수정 코드 걸린 추가 시간: ",time.time()-start)

for vertex in inside_vertices:
    sphere = BRepPrimAPI_MakeBox(vertex, 5,5,5).Shape()
    a.DisplayShape(sphere, color='black')












# display
for i in range(len(pole_list)):
    s = BRepPrimAPI_MakeSphere(pole_list[i], 30).Shape()
    #if (i==4):
        #a.DisplayShape(s, color = 'red',transparency=0.7)
        #continue
    a.DisplayShape(s,color='blue')

for i in range(1, knots.Length() + 1):  
    u = knots.Value(i)
    pnt = bc.Value(u)
    s = BRepPrimAPI_MakeSphere(pnt, 30).Shape()
    # if (i==4):
    #     a.DisplayShape(s, color='red',transparency=0.7)
    #     continue
    a.DisplayShape(s, color='green')


a.DisplayShape(ed)
a.DisplayShape(pipe, color='black',transparency=0.6)
a.FitAll()
b()