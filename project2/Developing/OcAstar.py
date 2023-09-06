from Map.Octree import Octree
import heapq
from OCC.Core.gp import gp_Pnt, gp_Vec, gp_Ax2, gp_Circ, gp_Dir
from OCC.Display.OCCViewer import Viewer3d
from OCC.Core.TopoDS import TopoDS_Edge, TopoDS_Wire, TopoDS_Shape
from OCC.Core.BRepBuilderAPI import BRepBuilderAPI_MakeEdge, BRepBuilderAPI_MakeWire
from OCC.Core.BRepOffsetAPI import BRepOffsetAPI_MakePipe
from OCC.Core.BRepAlgoAPI import BRepAlgoAPI_Fuse

# Custom
from Map.Node import Node
from Map.GridMap import GridMap
from Algoritm.Spline.Spline import SplineBuilder


class OcAstar:
    def __init__(self, startOcNode: Octree, endOcNode: Octree, display: Viewer3d) -> None:
        self.StartOcNode = startOcNode
        self.EndOcNode = endOcNode
        self.PathPoints = []
        self.Display = display
        pass

    def Run(self):
        OpenList = []
        ClosedList = []

        heapq.heappush(OpenList, self.StartOcNode)

        while OpenList:
            cur: Octree = heapq.heappop(OpenList)
            ClosedList.append(cur)

            if (cur.mainNode and cur.mainNode == self.EndOcNode.mainNode):
                self.GetPath()
                return

            nodes: list[Octree] = cur.GetNeighbors()
            for node in nodes:
                if (node in ClosedList or (cur.mainNode and cur.mainNode.Obstacle)):
                    continue
                node.CalHValue(self.EndOcNode)
                ng = node.CalGValue(cur)

                if (node.f == 0.0 or ng < node.g):
                    node.f = node.g + node.h
                    node.PathPoint = cur
                    heapq.heappush(OpenList, node)

        pass

    def GetPath(self):
        self.EndOcNode.DisplayBoxShape(0.5, _color="red")
        cur = self.EndOcNode.PathPoint
        self.PathPoints.append(cur)
        while (cur.PathPoint != None):
            cur.DisplayBoxShape(0.5, _color="red")
            self.PathPoints.append(cur)
            cur = cur.PathPoint
            if (cur == None):
                break
        self.StartOcNode.DisplayBoxShape(0.5, _color="red")

    def DisplayPathByPipe(self, _transparency: float = 0, _color='blue', diameter: float = 3, gap: float = 0.0) -> None:
        finalShape: TopoDS_Shape = TopoDS_Shape()
        pointList: list[gp_Pnt] = []
        # pointList.append(gp_Pnt(self.PathPoints[0].CenterPoint.X(), self.PathPoints[0].CenterPoint.Y() + gap, self.PathPoints[0].CenterPoint.Z()))
        length = len(self.PathPoints)
        for i in range(length):
            pointList.append(self.PathPoints[i].CenterPoint)

        # pointList.append(gp_Pnt(self.PathPoints[-1].CenterPoint.X(), self.PathPoints[-1].CenterPoint.Y() - gap, self.PathPoints[-1].CenterPoint.Z()))
        for i in range(length - 1):
            directionEdge = BRepBuilderAPI_MakeEdge(
                pointList[i], pointList[i + 1])
            if (not directionEdge.IsDone()):
                continue
            desh = directionEdge.Shape()

            directionWire: TopoDS_Wire = BRepBuilderAPI_MakeWire(
                desh).Wire()

            directionCircle: gp_Circ = gp_Circ(gp_Ax2(self.PathPoints[i].CenterPoint, gp_Dir(
                pointList[i + 1].XYZ().Subtracted(pointList[i].XYZ()))), diameter)
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

        self.Display.DisplayShape(
            finalShape, transparency=_transparency, color=_color)

    def DisplayPathBySplinePipe(self, _transparency: float = 0, _color='blue', diameter: float = 3, gap: float = 0.0, startGp: gp_Pnt = None, endGp: gp_Pnt = None) -> None:
        pointList: list[gp_Pnt] = []
        pointList.append(endGp)
        for i in range(len(self.PathPoints)):
            pointList.append(self.PathPoints[i].CenterPoint)
        pointList.append(startGp)
        sb = SplineBuilder(pointList)
        sb.SplineBuild()

        edgeShape = BRepBuilderAPI_MakeEdge(sb.CurveShape).Shape()
        wireShape = BRepBuilderAPI_MakeWire(edgeShape).Shape()

        Circle: gp_Circ = gp_Circ(gp_Ax2(self.PathPoints[0].CenterPoint, gp_Dir(
            self.PathPoints[1].CenterPoint.XYZ().Subtracted(self.PathPoints[0].CenterPoint.XYZ()))), diameter)
        CircleEdge: TopoDS_Edge = BRepBuilderAPI_MakeEdge(Circle).Shape()
        CircleWire: TopoDS_Wire = BRepBuilderAPI_MakeWire(CircleEdge).Shape()

        pipeShape: TopoDS_Shape = BRepOffsetAPI_MakePipe(
            wireShape, CircleWire).Shape()

        if (not pipeShape.IsNull()):
            self.Display.DisplayShape(
                pipeShape, transparency=_transparency, color=_color)
