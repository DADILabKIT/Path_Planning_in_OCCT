import util
from OCC.Core.gp import gp_Pnt, gp_Circ, gp_Dir, gp_Ax2
from OCC.Core.TopoDS import TopoDS_Shape, TopoDS_Edge, TopoDS_Wire
from OCC.Core.BRepAlgoAPI import BRepAlgoAPI_Fuse
from OCC.Core.BRepOffsetAPI import BRepOffsetAPI_MakePipe
from OCC.Core.BRepBuilderAPI import BRepBuilderAPI_MakeWire, BRepBuilderAPI_MakeEdge

from OCC.Display.OCCViewer import Viewer3d


class PipeBuilder:
    def __init__(self, gpPntList: list[gp_Pnt], diameter: float = 3) -> None:
        self.GpPntList: list[gp_Pnt] = gpPntList
        self.PipeShape: TopoDS_Shape = self.__InitedPipeShape(diameter)
        pass

    def DisplayPipeShape(self, display: Viewer3d, _transparency=0.5, _color="red") -> None:
        display.DisplayShape(
            self.PipeShape, transparency=_transparency, color=_color)

    def InitPipeShape(self, gpPntList: list[gp_Pnt], diameter: float) -> None:
        self.GpPntList = gpPntList
        self.PipeShape = self.__InitedPipeShape(diameter)
        return

    def __InitedPipeShape(self, diameter: float) -> TopoDS_Shape:
        finalShape: TopoDS_Shape = TopoDS_Shape()

        for i in range(len(self.GpPntList) - 1):
            directionEdge: TopoDS_Edge = BRepBuilderAPI_MakeEdge(
                self.GpPntList[i], self.GpPntList[i + 1]).Edge()
            directionWire: TopoDS_Wire = BRepBuilderAPI_MakeWire(
                directionEdge).Wire()

            directionCircle: gp_Circ = gp_Circ(gp_Ax2(self.GpPntList[i], gp_Dir(
                self.GpPntList[i + 1].XYZ().Subtracted(self.GpPntList[i].XYZ()))), diameter)
            directionCircleEdge: TopoDS_Edge = BRepBuilderAPI_MakeEdge(
                directionCircle).Edge()
            directionCircleWire: TopoDS_Wire = BRepBuilderAPI_MakeWire(
                directionCircleEdge).Wire()

            pipeShape: TopoDS_Shape = BRepOffsetAPI_MakePipe(
                directionWire, directionCircleWire).Shape()

            if finalShape.IsNull():
                finalShape = pipeShape
            else:
                finalShape = BRepAlgoAPI_Fuse(finalShape, pipeShape).Shape()
        return finalShape
