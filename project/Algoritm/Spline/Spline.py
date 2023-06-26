from OCC.Core.gp import gp_Pnt, gp_Vec, gp_Dir
from OCC.Core.BRepPrimAPI import BRepPrimAPI_MakeSphere
from OCC.Core.GeomAPI import GeomAPI_Interpolate
from OCC.Core.TColStd import TColStd_HArray1OfBoolean
from OCC.Core.TColgp import TColgp_HArray1OfPnt, TColgp_Array1OfVec
from OCC.Display.SimpleGui import init_display

class SplineBuilder:
    def __init__(self, pathPoints: list[gp_Pnt]) -> None:
        self.N = len(pathPoints)
        self.TOLERENCE = 1e-3
        self.PathPoints: list[gp_Pnt] = pathPoints
        self.PathArray: TColgp_HArray1OfPnt = TColgp_HArray1OfPnt(1, self.N)
        self.VectorArray: TColgp_Array1OfVec = TColgp_Array1OfVec(1, self.N)
        self.BoolArray: TColStd_HArray1OfBoolean = TColStd_HArray1OfBoolean(1, self.N)
        self.CurveShape = None
        
        
    def SplineBuild(self):
        for i in range(1, self.N):
            self.PathArray.SetValue(i, self.PathPoints[i - 1])
            self.VectorArray.SetValue(i, gp_Vec(self.PathPoints[i - 1], self.PathPoints[i]))
            self.BoolArray.SetValue(i, True)
            
        self.VectorArray.SetValue(self.N, gp_Vec(gp_Pnt(950, 950, 950), gp_Pnt(950, 1100, 950)))
        self.VectorArray.SetValue(0, gp_Vec(gp_Pnt(50 , 50, 50), gp_Pnt(50, -100, 50)))
        self.BoolArray.SetValue(self.N, True)
        self.BoolArray.SetValue(1, True)
        self.BoolArray.SetValue(self.N, True)
        interpolate = GeomAPI_Interpolate(self.PathArray, False, self.TOLERENCE)
        interpolate.Load(self.VectorArray, self.BoolArray)
        interpolate.Perform()
        
        self.CurveShape =  interpolate.Curve()
        
    def SplineBuild(self):
        for i in range(1, self.N + 1):
            self.PathArray.SetValue(i, self.PathPoints[i - 1])
            if (self.N == i):
                continue
            self.VectorArray.SetValue(i, gp_Vec(self.PathPoints[i - 1], self.PathPoints[i]))
            self.BoolArray.SetValue(i, True)
            
        self.VectorArray.SetValue(self.N, gp_Vec(self.PathPoints[self.N - 1], self.PathPoints[self.N - 2]))
        self.BoolArray.SetValue(self.N, True)
        self.BoolArray.SetValue(1, False)
        self.BoolArray.SetValue(self.N, False)
        interpolate = GeomAPI_Interpolate(self.PathArray, False, self.TOLERENCE)
        interpolate.Load(self.VectorArray, self.BoolArray)
        interpolate.Perform()
        
        self.CurveShape =  interpolate.Curve()
        
    def SplineBuild2(self):
        for i in range(1 ,self.N + 1):
            self.PathArray.SetValue(i, self.PathPoints[i - 1])
        
        interpolate = GeomAPI_Interpolate(self.PathArray, False, self.TOLERENCE)

        interpolate.Load(gp_Vec(gp_Pnt(50, 0, 50), gp_Pnt(50, 50, 50)), gp_Vec(gp_Pnt(950, 950, 950), gp_Pnt(950, 1000, 950)))
        
        interpolate.Perform()
        self.CurveShape = interpolate.Curve()
        
    def SplineBuild3(self):
        for i in range(1, self.N + 1):
            self.PathArray.SetValue(i, self.PathPoints[i - 1])
            if (self.N == i):
                continue
            self.VectorArray.SetValue(i, gp_Vec(self.PathPoints[i - 1], self.PathPoints[i]))
            self.BoolArray.SetValue(i, True)
            
        self.VectorArray.SetValue(self.N, gp_Vec(self.PathPoints[self.N - 1], self.PathPoints[self.N - 2]))
        self.BoolArray.SetValue(self.N, True)
        self.BoolArray.SetValue(1, False)
        self.BoolArray.SetValue(self.N, False)
        interpolate = GeomAPI_Interpolate(self.PathArray, False, self.TOLERENCE)
        interpolate.Load(self.VectorArray, self.BoolArray)
        interpolate.Perform()
        
        self.CurveShape =  interpolate.Curve()


if (__name__ == "__main__"):
    a, b, c, d = init_display()
    path = [gp_Pnt(0, 0, 500), gp_Pnt(500, 500, 500), gp_Pnt(1000, 500, 500), gp_Pnt(1000, 1000, 1000)]

    sb = SplineBuilder(path)
    sb.SplineBuild()
    a.DisplayShape(sb.CurveShape)
    a.FitAll()
    b()
