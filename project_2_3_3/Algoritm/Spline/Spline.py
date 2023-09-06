from OCC.Core.gp import gp_Pnt, gp_Vec, gp_Dir
from OCC.Core.BRepPrimAPI import BRepPrimAPI_MakeSphere
from OCC.Core.GeomAPI import GeomAPI_Interpolate, GeomAPI_PointsToBSpline
from OCC.Core.TColStd import TColStd_HArray1OfBoolean, TColStd_Array1OfReal, TColStd_Array1OfInteger
from OCC.Core.TColgp import TColgp_HArray1OfPnt, TColgp_Array1OfVec, TColgp_Array1OfPnt
from OCC.Display.SimpleGui import init_display
from OCC.Core.Geom import Geom_BSplineCurve



class SplineBuilder:
    def __init__(self, pathPoints: list[gp_Pnt]) -> None:
        self.N = len(pathPoints)
        self.TOLERENCE = 1e-3
        self.PathPoints: list[gp_Pnt] = pathPoints
        self.PathArray: TColgp_HArray1OfPnt = TColgp_HArray1OfPnt(1, self.N)
        self.VectorArray: TColgp_Array1OfVec = TColgp_Array1OfVec(1, self.N)
        self.BoolArray: TColStd_HArray1OfBoolean = TColStd_HArray1OfBoolean(
            1, self.N)
        self.CurveShape = None
        self._initialize_arrays()

    def _initialize_arrays(self):
        """PathPoints의 크기에 따라 배열들을 초기화합니다."""
        self.N = len(self.PathPoints)

        self.PathArray: TColgp_HArray1OfPnt = TColgp_HArray1OfPnt(1, self.N)
        self.VectorArray: TColgp_Array1OfVec = TColgp_Array1OfVec(1, self.N)
        self.BoolArray: TColStd_HArray1OfBoolean = TColStd_HArray1OfBoolean(
            1, self.N)

    # def SplineBuild(self):
    #     for i in range(1, self.N):
    #         self.PathArray.SetValue(i, self.PathPoints[i - 1])
    #         self.VectorArray.SetValue(i, gp_Vec(self.PathPoints[i - 1], self.PathPoints[i]))
    #         self.BoolArray.SetValue(i, True)

    #     self.VectorArray.SetValue(self.N, gp_Vec(gp_Pnt(950, 950, 950), gp_Pnt(950, 1100, 950)))
    #     self.VectorArray.SetValue(0, gp_Vec(gp_Pnt(50 , 50, 50), gp_Pnt(50, -100, 50)))
    #     self.BoolArray.SetValue(1, False)
    #     self.BoolArray.SetValue(self.N, False)
    #     self.PathArray.SetValue(self.N, self.PathPoints[self.N - 1])
    #     interpolate = GeomAPI_Interpolate(self.PathArray, False, self.TOLERENCE)
    #     if (interpolate.IsDone()):

    #         interpolate.Load(self.VectorArray, self.BoolArray)
    #         interpolate.Perform()

    #         self.CurveShape =  interpolate.Curve()

    def SplineBuild(self):
        # 제어점 추가
        # 마지막과 그 앞 점
        last_point = self.PathPoints[-1]
        prev_point = self.PathPoints[-2]

        # 4:1 내분점 계산
        t = 1/5
        inner_point_x = (1 - t) * last_point.X() + t * prev_point.X()
        inner_point_y = (1 - t) * last_point.Y() + t * prev_point.Y()
        inner_point_z = (1 - t) * last_point.Z() + t * prev_point.Z()
        inner_point = gp_Pnt(inner_point_x, inner_point_y, inner_point_z)

        # 내분점을 self.PathPoints에 추가.
        self.PathPoints.insert(-1, inner_point)

        # 배열들의 크기를 업데이트합니다.
        self._initialize_arrays()

        for i in range(1, self.N + 1):
            self.PathArray.SetValue(i, self.PathPoints[i - 1])
            if (self.N == i):
                continue
            if (i == 1):
                self.VectorArray.SetValue(
                    i, gp_Vec(self.PathPoints[i - 1], self.PathPoints[i]))
            else:
                self.VectorArray.SetValue(i, gp_Vec(self.PathPoints[i-2], self.PathPoints[i]))
            self.BoolArray.SetValue(i, True)

        # 첫 번째와 끝 포인트를 가져옵니다.
        first_point = self.PathPoints[0]
        last_point = self.PathPoints[-1]

        # 첫 번째와 끝 포인트 사이의 벡터를 생성합니다.
        direction_vector = gp_Vec(first_point, last_point)

        # 이 벡터를 VectorArray의 마지막 요소로 설정합니다.
        self.VectorArray.SetValue(self.N, direction_vector)


        self.BoolArray.SetValue(1, False)
        self.BoolArray.SetValue(self.N, False)
        interpolate = GeomAPI_Interpolate(
            self.PathArray, False, self.TOLERENCE)

        interpolate.Load(self.VectorArray, self.BoolArray)
        interpolate.Perform()

        self.CurveShape =  interpolate.Curve()

    def SplineBuild2(self):
        for i in range(1, self.N + 1):
            self.PathArray.SetValue(i, self.PathPoints[i - 1])
            if (self.N == i):
                continue
            self.VectorArray.SetValue(
                i, gp_Vec(self.PathPoints[i - 1], self.PathPoints[i]))
            self.BoolArray.SetValue(i, True)

        self.VectorArray.SetValue(self.N, gp_Vec(
            self.PathPoints[self.N - 1], self.PathPoints[self.N - 2]))

        self.BoolArray.SetValue(1, False)
        self.BoolArray.SetValue(self.N, False)
        interpolate = GeomAPI_PointsToBSpline(self.PathArray,)

        interpolate.Load(self.VectorArray, self.BoolArray)
        interpolate.Perform()

        self.CurveShape =  interpolate.Curve()

    def SplineBuild3(self):
        for i in range(1, self.N + 1):
            self.PathArray.SetValue(i, self.PathPoints[i - 1])
            if (self.N == i):
                continue
            self.VectorArray.SetValue(
                i, gp_Vec(self.PathPoints[i - 1], self.PathPoints[i]))
            self.BoolArray.SetValue(i, True)

        self.VectorArray.SetValue(self.N, gp_Vec(
            self.PathPoints[self.N - 1], self.PathPoints[self.N - 2]))
        self.BoolArray.SetValue(self.N, True)
        self.BoolArray.SetValue(1, False)
        self.BoolArray.SetValue(self.N, False)
        interpolate = GeomAPI_Interpolate(
            self.PathArray, False, self.TOLERENCE)
        interpolate.Load(self.VectorArray, self.BoolArray)
        interpolate.Perform()

        self.CurveShape = interpolate.Curve()

    def SplineBuild4(self):
        self.PathPoints = [gp_Pnt(50.0, 50.0, 50.0),
        gp_Pnt(150.0, 50.0, 50.0),
        gp_Pnt(450.0, 350.0, 350.0),
        gp_Pnt(350.0, 650.0, 550.0),
        gp_Pnt(350.0, 650.0, 750.0),
        gp_Pnt(950.0, 950.0, 950.0)]
        poles = TColgp_Array1OfPnt(1, len(self.PathPoints))

        for i, p in enumerate(self.PathPoints, start=1):
            poles.SetValue(i, p)

        num_poles = poles.Length()

        # weights 설정
        weights = TColStd_Array1OfReal(1, num_poles)
        for i in range(1, num_poles + 1):
            if i!=1 and i!=num_poles:
                weights.SetValue(i, 100.0)
            else:
                weights.SetValue(i, 1.0)
            

        # knots 수 설정
        degree = 3
        
        # num_knots = num_poles + degree + 1 - 2 * degree = num_poles - degree + 1
        num_knots = num_poles - degree + 1
        knots = TColStd_Array1OfReal(1, num_knots)
        for i in range(1, num_knots + 1):
            knots.SetValue(i, (i-1)/(num_knots - 1))

        # multiplicities 설정
        mults = TColStd_Array1OfInteger(1, num_knots)
        mults.SetValue(1, degree + 1)
        mults.SetValue(num_knots, degree + 1)
        for i in range(2, num_knots):
            mults.SetValue(i, 1)

        # B-Spline 커브 생성
        self.CurveShape = Geom_BSplineCurve(poles, weights, knots, mults, degree)

            


if (__name__ == "__main__"):

    a, b, c, d = init_display()
    path = [gp_Pnt(50.0, 50.0, 50.0),
    gp_Pnt(150.0, 50.0, 50.0),
    gp_Pnt(450.0, 350.0, 350.0),
    gp_Pnt(350.0, 650.0, 550.0),
    gp_Pnt(350.0, 650.0, 750.0),
    gp_Pnt(950.0, 950.0, 950.0)]

    for pnt in path:
        sp = BRepPrimAPI_MakeSphere(pnt, 10).Shape()
        a.DisplayShape(sp, color='blue')

    sb = SplineBuilder(path)
    sb.SplineBuild()


    sp_added = BRepPrimAPI_MakeSphere(sb.PathPoints[-2], 10).Shape()
    a.DisplayShape(sp_added, color='red')


    a.DisplayShape(sb.CurveShape)
    a.FitAll()
    b()
