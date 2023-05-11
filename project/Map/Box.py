# OCC
# for 3D Data
from OCC.Core.gp import gp_Pnt
from OCC.Core.TopoDS import TopoDS_Shape
from OCC.Core.BRepPrimAPI import BRepPrimAPI_MakeBox

# for visual
from OCC.Display.OCCViewer import Viewer3d


class Box:
    def __init__(self, startPoint: gp_Pnt = None, endPoint: gp_Pnt = None, display: Viewer3d = None) -> None:
        # box points
        self.MaxPoint: gp_Pnt = endPoint
        self.MinPoint: gp_Pnt = startPoint
        self.CenterPoint: gp_Pnt = self.InitCenterPoint()

        # display
        self.Display: Viewer3d = display

    # for path points
    def InitCenterPoint(self) -> gp_Pnt:
        CenterPoint: gp_Pnt = gp_Pnt(0, 0, 0)

        CenterPoint.SetX((self.MaxPoint.X() + self.MinPoint.X()) / 2)
        CenterPoint.SetY((self.MaxPoint.Y() + self.MinPoint.Y()) / 2)
        CenterPoint.SetZ((self.MaxPoint.Z() + self.MinPoint.Z()) / 2)

        return CenterPoint

    # display box shape
    def DisplayBoxShape(self, _transparency: float = 0.5, _color: str = 'black') -> None:
        boxShape = BRepPrimAPI_MakeBox(self.MinPoint, self.MaxPoint).Shape()
        self.Display.DisplayShape(boxShape, transparency = _transparency, color = _color)

