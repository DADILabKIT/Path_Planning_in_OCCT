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

# 충돌을 감지하고 새로운 제어점을 추가하는 함수
def adjust_poles_and_create_bspline(original_bc, obstacle, original_poles, weights, knots, mults, degree):
    from OCC.Core.BRepClass3d import BRepClass3d_SolidClassifier
    from OCC.Core.TopAbs import TopAbs_ON, TopAbs_OUT, TopAbs_IN

    # SolidClassifier를 이용해 각 pole이 장애물 내부에 있는지 확인
    classifier = BRepClass3d_SolidClassifier(obstacle)
    new_poles = TColgp_Array1OfPnt(1, original_poles.Length()*2)  # 충돌이 감지된 곳에 새로운 pole을 추가할 수 있는 최대 길이
    new_weights = TColStd_Array1OfReal(1, original_poles.Length()*2)
    j = 1
    for i in range(1, original_poles.Length() + 1):
        classifier.Perform(original_poles.Value(i), 1e-6)  # 첫 번째 인자: 점, 두 번째 인자: 오차 허용 범위
        new_poles.SetValue(j, original_poles.Value(i))
        new_weights.SetValue(j, weights.Value(i))
        state = classifier.State()
        # 장애물 내부에 있는지 확인
        if state == TopAbs_IN or state == TopAbs_ON:
            if i < original_poles.Length():  # 마지막 pole이 아닌 경우에만 새로운 pole 추가
                # 현재 pole과 다음 pole 사이의 중간점을 새로운 pole로 추가
                mid_pnt = gp_Pnt(0.5 * (original_poles.Value(i).X() + original_poles.Value(i + 1).X()),
                                  0.5 * (original_poles.Value(i).Y() + original_poles.Value(i + 1).Y()),
                                  0.5 * (original_poles.Value(i).Z() + original_poles.Value(i + 1).Z()))
                j += 1
                new_poles.SetValue(j, mid_pnt)
                new_weights.SetValue(j, 1)  # 가중치는 일단 1로 설정
        j += 1
    # 충돌이 없었다면 original_bspline 그대로 반환
    if j == original_poles.Length() + 1:
        return original_bc
    # 충돌이 있었다면 poles와 weights를 재설정하고 새로운 bspline 생성
    else:
        new_poles.Resize(1, j - 1, False)
        new_weights.Resize(1, j - 1, False)
        new_bc = Geom_BSplineCurve(new_poles, new_weights, knots, mults, degree)
        return new_bc

def get_collision_points_and_poles(shape1, shape2, poles):
    dist_shape_shape = BRepExtrema_DistShapeShape(shape1, shape2)
    collision_points = []
    colliding_poles = []
    solid2 = topods_Solid(shape2)
    classifier = BRepClass3d_SolidClassifier(solid2)
    if abs(dist_shape_shape.Value()) < 0.001:  # 충돌이 발생한 경우
        for i in range(1, dist_shape_shape.NbSolution() + 1):
            point1, point2 = dist_shape_shape.PointOnShape1(i), dist_shape_shape.PointOnShape2(i)
            avg_point = gp_Pnt(0.5 * (point1.X() + point2.X()),
                                0.5 * (point1.Y() + point2.Y()),
                                0.5 * (point1.Z() + point2.Z()))
            collision_points.append(avg_point)
            classifier.Perform(avg_point, True)
            if classifier.State() in [TopAbs_IN, TopAbs_ON]:
                for i in range(1, poles.Length() + 1):
                    pole = poles.Value(i)
                    if pole.Distance(avg_point) < 0.001: # Pole이 충돌 지점에 가까운지 확인
                        colliding_poles.append(i)
    return collision_points, colliding_poles

def get_collision_points(shape1, shape2):
    dist_shape_shape = BRepExtrema_DistShapeShape(shape1, shape2)
    collision_points = []

    if abs(dist_shape_shape.Value()) < 0.001:  # 충돌이 발생한 경우
        for i in range(1, dist_shape_shape.NbSolution() + 1):
            point1, point2 = dist_shape_shape.PointOnShape1(i), dist_shape_shape.PointOnShape2(i)
            avg_point = gp_Pnt(0.5 * (point1.X() + point2.X()),
                                0.5 * (point1.Y() + point2.Y()),
                                0.5 * (point1.Z() + point2.Z()))
            collision_points.append(avg_point)
    return collision_points  # 충돌 위치 리스트 반환



# m = p + n + 1
degree = 3 # p, n=10, m=14.


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
diameter = 200.0
direction_vec = gp_Vec(pole_list[1].XYZ()) - gp_Vec(pole_list[0].XYZ())
direction_dir = gp_Dir(direction_vec)

circle = Geom_Circle(gp_Ax2(pole_list[0], direction_dir), diameter / 2)
section = BRepBuilderAPI_MakeEdge(circle).Edge()

pipe = BRepOffsetAPI_MakePipe(wire, section).Shape()

obstacle_radius = diameter * 1.1  # Make the sphere a bit larger than the diameter of the cable

# 장애물 1
middle_pnt = bc.Value(bc.FirstParameter() + ((bc.LastParameter() - bc.FirstParameter()) / 3.0))  # 1/3 위치
obstacle1 = BRepPrimAPI_MakeSphere(middle_pnt, obstacle_radius).Shape()
a.DisplayShape(obstacle1, color='red', transparency=0.6)

# # 장애물 2
# middle_pnt = bc.Value(bc.FirstParameter() + ((bc.LastParameter() - bc.FirstParameter()) / 2.0))  # 1/2 위치
# obstacle2 = BRepPrimAPI_MakeSphere(middle_pnt, obstacle_radius).Shape()
# a.DisplayShape(obstacle2, color='red', transparency=0.6)

# # 장애물 3
# middle_pnt = bc.Value(bc.FirstParameter() + ((bc.LastParameter() - bc.FirstParameter()) * 2 / 3.0))  # 2/3 위치
# obstacle3 = BRepPrimAPI_MakeSphere(middle_pnt, obstacle_radius).Shape()
# a.DisplayShape(obstacle3, color='red', transparency=0.6)


# new_bc = adjust_poles_and_create_bspline(bc, obstacle1, poles, weights, knots, mults, degree)

# ed = BRepBuilderAPI_MakeEdge(new_bc).Edge()
# wire = BRepBuilderAPI_MakeWire(ed).Wire()

# Diameter for the cable
diameter = 200.0
direction_vec = gp_Vec(pole_list[1].XYZ()) - gp_Vec(pole_list[0].XYZ())
direction_dir = gp_Dir(direction_vec)

circle = Geom_Circle(gp_Ax2(pole_list[0], direction_dir), diameter / 2)
section = BRepBuilderAPI_MakeEdge(circle).Edge()

pipe = BRepOffsetAPI_MakePipe(wire, section).Shape()







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