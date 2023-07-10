from OCC.Core.gp import gp_Circ, gp_Ax2, gp_Dir, gp_Pnt, gp_Vec
from OCC.Core.Geom import Geom_BSplineCurve, Geom_Circle
from OCC.Core.TColStd import TColStd_Array1OfReal, TColStd_Array1OfInteger
from OCC.Core.TColgp import TColgp_Array1OfPnt
from OCC.Core.BRepBuilderAPI import BRepBuilderAPI_MakeEdge, BRepBuilderAPI_MakeWire
from OCC.Core.BRepPrimAPI import BRepPrimAPI_MakeSphere
from OCC.Display.SimpleGui import init_display
from OCC.Core.BRepExtrema import BRepExtrema_DistShapeShape
from OCC.Core.BRepOffsetAPI import BRepOffsetAPI_MakePipe



def get_collision_point(shape1, shape2):
    dist_shape_shape = BRepExtrema_DistShapeShape(shape1, shape2)
    if dist_shape_shape.Value() == 0:  # 충돌이 발생한 경우
        point1, point2 = dist_shape_shape.PointOnShape1(1), dist_shape_shape.PointOnShape2(1)
        return point1, point2  # 충돌 위치 반환
    else:
        return None  # 충돌이 발생하지 않은 경우

# m = p + n + 1
degree = 3 # p


mults = TColStd_Array1OfInteger(1, 5)
# mults.SetValue(1, 3)
# mults.SetValue(2, 2)
# mults.SetValue(3, 2)
# mults.SetValue(4, 3)
# mults.SetValue(5, 4)
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

# # m 비균일
# knots = TColStd_Array1OfReal(1, 5)
# knots.SetValue(1, 0.0)
# knots.SetValue(2, 0.25)
# knots.SetValue(3, 0.5)
# knots.SetValue(4, 0.75)
# knots.SetValue(5, 1.0)

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
diameter = 10.0
direction_vec = gp_Vec(pole_list[1].XYZ()) - gp_Vec(pole_list[0].XYZ())
direction_dir = gp_Dir(direction_vec)

circle = Geom_Circle(gp_Ax2(pole_list[0], direction_dir), diameter / 2)
section = BRepBuilderAPI_MakeEdge(circle).Edge()

pipe = BRepOffsetAPI_MakePipe(wire, section).Shape()










# display
a,b,c,d = init_display()
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
a.DisplayShape(pipe)
a.FitAll()
b()