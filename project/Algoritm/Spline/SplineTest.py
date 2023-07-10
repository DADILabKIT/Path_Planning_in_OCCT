from OCC.Core.gp import gp_Pnt
from OCC.Core.Geom import Geom_BSplineCurve
from OCC.Core.TColStd import TColStd_Array1OfReal, TColStd_Array1OfInteger
from OCC.Core.TColgp import TColgp_Array1OfPnt
from OCC.Core.BRepBuilderAPI import BRepBuilderAPI_MakeEdge
from OCC.Display.SimpleGui import init_display

degree = 3

mults = TColStd_Array1OfInteger(1, 5)
mults.SetValue(1, 4)
mults.SetValue(2, 2)
mults.SetValue(3, 2)
mults.SetValue(4, 2)
mults.SetValue(5, 4)



knots = TColStd_Array1OfReal(1, 5)
knots.SetValue(1, 0.0)
knots.SetValue(2, 250.0)
knots.SetValue(3, 1422.6039399558574)
knots.SetValue(4, 1672.6039399558574)
knots.SetValue(5, 1922.6039399558574)


# n
poles = TColgp_Array1OfPnt(1, 10)
poles.SetValue(1, gp_Pnt(0,0,0))
poles.SetValue(2, gp_Pnt(100,100,0))
poles.SetValue(3, gp_Pnt(100,100,100))
poles.SetValue(4, gp_Pnt(200,200,500))
poles.SetValue(5, gp_Pnt(500,500,30))
poles.SetValue(6, gp_Pnt(600,700,900))
poles.SetValue(7, gp_Pnt(700,700,1000))
poles.SetValue(8, gp_Pnt(1100,1100,1000))
poles.SetValue(9, gp_Pnt(1200,2100,1000))
poles.SetValue(10, gp_Pnt(1500,1500,1800))
# poles = TColgp_Array1OfPnt(1, 10)
# for i in range(1 ,9 + 1 + 1):
#     val = list(map(float, input().split()))
#     poles.SetValue(i, gp_Pnt(val[0], val[1], val[2]))



bc = Geom_BSplineCurve(poles, knots, mults, 3)
ed = BRepBuilderAPI_MakeEdge(bc).Edge()

a,b,c,d = init_display()
a.DisplayShape(ed)
a.FitAll()
b()