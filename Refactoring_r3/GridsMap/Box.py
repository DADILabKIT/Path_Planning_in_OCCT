from OCC.Core.gp import gp_Pnt
from OCC.Core.TopoDS import TopoDS_Shape
from OCC.Core.BRepPrimAPI import BRepPrimAPI_MakeBox

from OCC.Display.OCCViewer import Viewer3d
from OCC.Display.SimpleGui import init_display


class Box:
    def __init__(self, minPoint: gp_Pnt, maxPoint: gp_Pnt) -> None:
        self.MinPoint: gp_Pnt = minPoint
        self.MaxPoint: gp_Pnt = maxPoint
        self.CenterPoint: gp_Pnt = self.__InitedCenterPoint()
        # self.BoxShape: TopoDS_Shape = None
        pass

    def __InitedCenterPoint(self) -> gp_Pnt:
        centerPoint: gp_Pnt = gp_Pnt(0, 0, 0)
        centerPoint.SetX((self.MinPoint.X() + self.MaxPoint.X()) / 2)
        centerPoint.SetY((self.MinPoint.Y() + self.MaxPoint.Y()) / 2)
        centerPoint.SetZ((self.MinPoint.Z() + self.MaxPoint.Z()) / 2)
        return centerPoint

    def DisplayBoxShape(self, display: Viewer3d, _transparency=0.5, _color="red") -> None:
        boxShape: TopoDS_Shape = BRepPrimAPI_MakeBox(
            self.MinPoint, self.MaxPoint).Shape()
        display.DisplayShape(
            boxShape, transparency=_transparency, color=_color)
        return


if (__name__ == "__main__"):
    a, b, c, d = init_display()
    print("display test")
    box = Box(gp_Pnt(0, 0, 0), gp_Pnt(1, 1, 1))
    box.DisplayBoxShape(a)
    a.FitAll()
    b()
    pass
