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
# m = p + n + 1 # m: 다중도, p: 차수, n: poles=제어점 수=path points and weights
degree = 3 # p, n=10, m=14.


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
pole_list = [gp_Pnt(0,0,0), gp_Pnt(100,100,0), gp_Pnt(100,100,100), gp_Pnt(200,200,500), gp_Pnt(500,500,30), gp_Pnt(600,700,900), gp_Pnt(700,700,1000), gp_Pnt(1100,1100,1000), gp_Pnt(1200,2100,1000), gp_Pnt(1500,1500,1800)]
for i in range(len(pole_list)):
    poles.SetValue(i+1, pole_list[i])
    if (i==4):
        weights.SetValue(i+1, 1)
        #continue
    weights.SetValue(i+1, 1)


# Make BSplineCurve
bc = Geom_BSplineCurve(poles, weights, knots, mults, 3)
ed = BRepBuilderAPI_MakeEdge(bc).Edge()
wire = BRepBuilderAPI_MakeWire(ed).Wire()

# Make Pipe
diameter = 200.0 # Diameter for the cable
direction_vec = gp_Vec(pole_list[1].XYZ()) - gp_Vec(pole_list[0].XYZ())
direction_dir = gp_Dir(direction_vec)

circle = Geom_Circle(gp_Ax2(pole_list[0], direction_dir), diameter / 2)
section = BRepBuilderAPI_MakeEdge(circle).Edge()

pipe = BRepOffsetAPI_MakePipe(wire, section).Shape()

# 장애물
obstacle_radius = diameter * 1.1  # Make the sphere a bit larger than the diameter of the cable # 그냥, 그린 장애물
middle_pnt = bc.Value(bc.FirstParameter() + ((bc.LastParameter() - bc.FirstParameter()) / 2.5))  
obstacle2 = BRepPrimAPI_MakeSphere(middle_pnt, obstacle_radius).Shape()
a.DisplayShape(obstacle2, color='red', transparency=0.6)

start = time.time()

# 샘플링
tlt = TessellatorShape(pipe, a)

# 샘플링 개수 입력 후 샘플링 진행
tlt.mesh.RandomSampling(100)

# # 샘플링 점 가시화
vertices = tlt.mesh.Points
# print(vertices)

# # 가시화
# for vertex in vertices:
#     sphere = BRepPrimAPI_MakeSphere(vertex, 10).Shape()
#     a.DisplayShape(sphere, color='black')



# Create solid classifier
classifier = BRepClass3d_SolidClassifier(obstacle2)

# Check which vertices are inside the cable
inside_vertices = []
for vertex in vertices:
    classifier.Perform(vertex, 1e-6)  # 1e-6 is the precision, adjust as needed
    state = classifier.State()
    if state in (TopAbs_ON, TopAbs_IN):
        inside_vertices.append(vertex)

print("수정 코드 걸린 추가 시간: ",time.time()-start)

# 점 삽입, 충돌 점들을 구하는 건 했는데 충돌 점 위치로 중간점 삽입하는거 귀찮 + 시간복잡도 심할거 같아 그냥 평균 구함용.
# 1
# 평균 점 삽입
# Calculate the average point
if len(inside_vertices) > 0:
    avg_x = 0
    avg_y = 0
    avg_z = 0
    for vertex in inside_vertices:
        avg_x += vertex.X()
        avg_y += vertex.Y()
        avg_z += vertex.Z()
    avg_x = avg_x/len(inside_vertices)
    avg_y = avg_y/len(inside_vertices)
    avg_z = avg_z/len(inside_vertices)
    avg_vertex = gp_Pnt(0,0,0)
    avg_vertex.SetX(avg_x)
    avg_vertex.SetY(avg_y)
    avg_vertex.SetZ(avg_z)

# Display the average point
average_point_shape = BRepPrimAPI_MakeSphere(avg_vertex, 20).Shape()
a.DisplayShape(average_point_shape, color='black')

# 보간 점 삽입
# Insert the average point into pole_list
pole_list.insert(5, avg_vertex) # assuming you want to insert it at index 5

# n+1 due to new pole
poles = TColgp_Array1OfPnt(1, 11)
weights = TColStd_Array1OfReal(1, 11)

for i in range(len(pole_list)):
    poles.SetValue(i+1, pole_list[i])
    weights.SetValue(i+1, 1)

# 다중도는 m=p+n+1 만 충족시키기
mults = TColStd_Array1OfInteger(1, 9)

mults.SetValue(1, 4)
mults.SetValue(2, 1)
mults.SetValue(3, 1)
mults.SetValue(4, 1)
mults.SetValue(5, 1)
mults.SetValue(6, 1)
mults.SetValue(7, 1)
mults.SetValue(8, 1)
mults.SetValue(9, 4)


# m 균일
knots = TColStd_Array1OfReal(1, 9)
knots.SetValue(1, 0.0)
knots.SetValue(2, 1*1.0/8)
knots.SetValue(3, 2*1.0/8)
knots.SetValue(4, 3*1.0/8)
knots.SetValue(5, 4*1.0/8)
knots.SetValue(6, 5*1.0/8)
knots.SetValue(7, 6*1.0/8)
knots.SetValue(8, 7*1.0/8)
knots.SetValue(9, 1.0)


# Make new BSplineCurve
bc_new = Geom_BSplineCurve(poles, weights, knots, mults, 3)
ed_new = BRepBuilderAPI_MakeEdge(bc_new).Edge()
wire_new = BRepBuilderAPI_MakeWire(ed_new).Wire()

# Create new pipe
pipe_new = BRepOffsetAPI_MakePipe(wire_new, section).Shape()

# Display new pipe
a.DisplayShape(pipe_new, color='yellow', transparency=0.3)






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
a.DisplayShape(pipe, color='blue',transparency=0.7)
a.FitAll()
b()