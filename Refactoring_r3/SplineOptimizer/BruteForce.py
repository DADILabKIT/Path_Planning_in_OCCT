import util

from OCC.Core.gp import gp_Pnt
from OCC.Core.TopoDS import TopoDS_Shape
from OCC.Core.BRepPrimAPI import BRepPrimAPI_MakeSphere
from OCC.Display.SimpleGui import init_display
from OCC.Display.OCCViewer import Viewer3d
from OCC.Core.Quantity import (
    Quantity_Color,
    Quantity_TOC_RGB,
    Quantity_NOC_WHITE
)

from GridsMap.GridsMap import GridsMap
from GridsMap.CollisionChecker.CollisionChecker import CollisionChecker
from GridsMap.Node import Node
from LineBuilder.SplineBuilder import SplineBuilder
from Tessellator.TessellatorShape import TessellatorShape


class BruteForce:
    def __init__(self, startNode: Node, endNode: Node, pathNodeList: list[Node], spline: TopoDS_Shape, grids: GridsMap, num: int = 2) -> None:
        self.StartNode: Node = startNode
        self.EndNode: Node = endNode
        self.PathNodeList: list[Node] = pathNodeList
        self.Spline: TopoDS_Shape = spline
        self.Grids: GridsMap = grids
        self.Done = False
        self.Num = num
        self.NewSpline = None
        self.AdditivePoints = []
        pass

    def Run(self) -> TopoDS_Shape:
        chk = CollisionChecker(self.Grids, self.Spline)
        if (not chk.Run()):
            return None

        cObstacleNodeList = chk.GetCollisionNode()
        candidateNodeList = []
        for i in cObstacleNodeList:
            candidateNodeList.extend(self._InitedCollapseArea(i.I, i.J, i.K))
        self._SortNodeByDist(candidateNodeList)
        ret = []
        self.__Dfs(-1, candidateNodeList, ret)

        return self.NewSpline

    def _InitedCollapseArea(self, x, y, z):
        dx = [-1, 1, 0, 0, 0, 0, -1, -1, 1, 1, -
              1, -1, 1, 1, -1, -1, 1, 1, 0, 0, 0, 0, -1, 1, -1, 1]
        dy = [0, 0, -1, 1, 0, 0, -1, 1, -1, 1, -1,
              1, -1, 1, -1, 1, -1, 1, -1, 1, -1, 1, 0, 0, 0, 0]
        dz = [0, 0, 0, 0, 1, -1, 1, 1, 1, 1, -
              1, -1, -1, -1, 0, 0, 0, 0, -1, -1, 1, 1, 1, 1, -1, -1]
        ret = []
        for i in range(len(dx)):
            nx = dx[i] + x
            ny = dy[i] + y
            nz = dz[i] + z

            if (nx >= self.Grids.MapSize or ny >= self.Grids.MapSize or nz >= self.Grids.MapSize or nx < 0 or ny < 0 or nz < 0):
                continue
            if (self.Grids.NodeMap[nx][ny][nz].Obstacle == False):
                ret.append(self.Grids.NodeMap[nx][ny][nz])
        return ret

    def _GetNodeDist(self, n1: Node, n2: Node, src: Node):
        return (n1.CenterPoint.Distance(src.CenterPoint) > n2.CenterPoint.Distance(src.CenterPoint))

    def _SortNodeByDist(self, nodeList: list[Node]) -> None:
        for i in range(len(nodeList) - 1):
            min_idx = i
            for j in range(i + 1, len(nodeList)):
                if (self._GetNodeDist(nodeList[min_idx], nodeList[j], self.StartNode)):
                    min_idx = j
            nodeList[i], nodeList[min_idx] = nodeList[min_idx], nodeList[i]

    def _PathNodeInsert(self, ret: list[Node]) -> None:
        for i in ret:
            if (i in self.PathNodeList):
                continue
            self.PathNodeList.append(i)
        self._SortNodeByDist(self.PathNodeList)

    def _PathNodeDelete(self, ret: list[Node]) -> None:
        for i in ret:
            if (i in self.PathNodeList):
                self.PathNodeList.remove(i)

    def _GetPathGpPnt(self) -> list[gp_Pnt]:
        ret = []
        for i in self.PathNodeList:
            ret.append(i.CenterPoint)
        return ret

    def DisplayAdditivePoints(self, display: Viewer3d, diameter: float = 20.0) -> None:
        for i in self.AdditivePoints:
            sphere = BRepPrimAPI_MakeSphere(i.CenterPoint, diameter).Shape()
            display.DisplayShape(sphere)
        return

    def __Dfs(self, n: int, candidateNodes: list[Node], ret: list[Node]):
        if (len(ret) == self.Num + 1 or self.Done == True):
            return
        if (len(ret) >= 1):
            self._PathNodeInsert(ret)
            newSpline = SplineBuilder(self._GetPathGpPnt(), 3).SplineShape
            chk = CollisionChecker(self.Grids, newSpline)
            if (not chk.Run()):
                for i in ret:
                    self.AdditivePoints.append(i)
                self.Done = True
                self.NewSpline = newSpline
                return
            else:
                self._PathNodeDelete(ret)

        for i in range(n + 1, len(candidateNodes)):
            ret.append(candidateNodes[i])
            self.__Dfs(i, candidateNodes, ret)
            ret.pop()


if (__name__ == "__main__"):

    a, b, c, d = init_display()
    a.View.SetBackgroundColor(Quantity_TOC_RGB, 0, 0, 0)
    a.hide_triedron()

    a.View.SetBgGradientColors(
        Quantity_Color(Quantity_NOC_WHITE),
        Quantity_Color(Quantity_NOC_WHITE),
        2,
        True,
    )

    def InitedCollapseArea(x, y, z):
        dx = [-1, 1, 0, 0, 0, 0, -1, -1, 1, 1, -
              1, -1, 1, 1, -1, -1, 1, 1, 0, 0, 0, 0, -1, 1, -1, 1]
        dy = [0, 0, -1, 1, 0, 0, -1, 1, -1, 1, -1,
              1, -1, 1, -1, 1, -1, 1, -1, 1, -1, 1, 0, 0, 0, 0]
        dz = [0, 0, 0, 0, 1, -1, 1, 1, 1, 1, -
              1, -1, -1, -1, 0, 0, 0, 0, -1, -1, 1, 1, 1, 1, -1, -1]
        ret = []
        for i in range(len(dx)):
            nx = dx[i] + x
            ny = dy[i] + y
            nz = dz[i] + z

            if (nx >= grids.MapSize or ny >= grids.MapSize or nz >= grids.MapSize or nx < 0 or ny < 0 or nz < 0):
                continue
            if (grids.NodeMap[nx][ny][nz].Obstacle == False):
                ret.append(grids.NodeMap[nx][ny][nz])
        return ret
    grids = GridsMap(gp_Pnt(0, 0, 0), gp_Pnt(10, 10, 10), 10)
    ret: list[Node] = InitedCollapseArea(1, 1, 1)
    for i in ret:
        i.DisplayBoxShape(a)
    ret: list[Node] = InitedCollapseArea(4, 4, 4)
    for i in ret:
        i.DisplayBoxShape(a)
    ret: list[Node] = InitedCollapseArea(1, 7, 8)
    for i in ret:
        i.DisplayBoxShape(a)

    a.FitAll()
    b()

    pass
