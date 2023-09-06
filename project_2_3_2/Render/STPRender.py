from OCC.Core.STEPControl import STEPControl_Reader
from OCC.Display.OCCViewer import Viewer3d
from OCC.Core.gp import gp_Pnt
from Render.Movement import MovementShape
from OCC.Core.TopoDS import TopoDS_Compound


class STPRender:
    def __init__(self, fileName: str, port: gp_Pnt, port2: gp_Pnt, display: Viewer3d) -> None:
        self.FileName = fileName
        self.Display = display
        self.Port = port
        self.Port2 = port2
        self.Shape: TopoDS_Compound = None

        self.StpReader = STEPControl_Reader()
        self.InitStpShape()

        pass

    def InitStpShape(self):
        self.StpReader.ReadFile(self.FileName)
        self.StpReader.TransferRoots()
        self.Shape = self.StpReader.Shape()

    def DisplaySTPShape(self):
        self.Display.DisplayShape(self.Shape, update=True)

    def Move(self, dx, dy, dz):
        shapeMove = MovementShape(
            self.Shape, self.Port, self.Port2, self.Display)
        shapeMove.Move(dx, dy, dz)
        # shapeMove.DisplayUpdate()

    def Rotate(self, x, y, z, degree):
        shapeMove = MovementShape(
            self.Shape, self.Port, self.Port2, self.Display)
        shapeMove.Rotate(x, y, z, degree)
