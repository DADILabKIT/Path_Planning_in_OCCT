

from OCC.Core.gp import gp_Pnt
from OCC.Core.TopoDS import TopoDS_Shape

from OCC.Display.OCCViewer import Viewer3d
from OCC.Display.SimpleGui import init_display

from RandomGenerator.RandomBoxGenerator import RandomBoxGenerator
from CollisionChecker.CollisionChecker import CollisionChecker
from Node import Node
from Box import Box


class GridsMap(Box):
    def __init__(self, minPoint: gp_Pnt, maxPoint: gp_Pnt, mapSize: int) -> None:
        super().__init__(minPoint, maxPoint)
        self.MapSize: int = mapSize
        self.NodeMap: list[list[list[Node]]] = self.__InitedNodeMap()
        pass

    def CollisionCheck(self, shape: TopoDS_Shape) -> bool:
        chk = CollisionChecker(self, shape)
        return (chk.Run())

    def DisplayGridsMapInObstacle(self, display: Viewer3d, _transparency=0.5, _color="red") -> None:
        for i in range(self.MapSize):
            for j in range(self.MapSize):
                for k in range(self.MapSize):
                    if (self.NodeMap[i][j][k].Obstacle):
                        self.NodeMap[i][j][k].DisplayBoxShape(
                            display, _transparency=_transparency, _color=_color)
        return

    def DisplayGridsMapInAllNode(self, display: Viewer3d, _transparency=0.5, _color="red") -> None:
        for i in range(self.MapSize):
            for j in range(self.MapSize):
                for k in range(self.MapSize):
                    self.NodeMap[i][j][k].DisplayBoxShape(
                        display, _transparency=_transparency, _color=_color)
        return

    def __InitedNodeMap(self) -> list[list[list[Node]]]:
        gap: float = (self.MaxPoint.X() - self.MinPoint.X()) / self.MapSize
        nodeMap = [[[None for _ in range(self.MapSize)] for _ in range(
            self.MapSize)] for _ in range(self.MapSize)]

        for i in range(self.MapSize):
            for j in range(self.MapSize):
                for k in range(self.MapSize):
                    minPoint = gp_Pnt((self.MinPoint.X(
                    ) + i*gap), (self.MinPoint.Y() + j*gap), (self.MinPoint.Z() + k*gap))
                    maxPoint = gp_Pnt((self.MinPoint.X(
                    ) + (i + 1)*gap), (self.MinPoint.Y() + (j + 1)*gap), (self.MinPoint.Z() + (k + 1)*gap))
                    nodeMap[i][j][k] = Node(minPoint, maxPoint, i, j, k)
        return nodeMap

    def InitRandomBoxObstacle(self, boxNumber: int = 3) -> None:
        randomBox = RandomBoxGenerator(0, len(self.NodeMap), boxNumber)
        randomBox.Run(self.NodeMap)


if (__name__ == "__main__"):
    a, b, c, d = init_display()
    gridsMap = GridsMap(gp_Pnt(0, 0, 0), gp_Pnt(1000, 1000, 1000), 10)
    gridsMap.DisplayGridsMapInAllNode(a, _transparency=1, _color="black")
    a.FitAll()
    b()
    pass
