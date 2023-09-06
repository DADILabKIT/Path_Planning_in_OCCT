import util

from OCC.Core.gp import gp_Pnt

from OCC.Display.SimpleGui import init_display
from OCC.Display.OCCViewer import Viewer3d

from GridsMap.Node import Node
from LineBuilder.PipeBuilder import PipeBuilder
from LineBuilder.SplineBuilder import SplineBuilder


class Agent:
    def __init__(self, name: str = "agent") -> None:
        self.Name = name
        self.CalTime: float = 0.0
        self.Distance: float = 0.0
        self.Degree: float = 0.0
        self.PathNodeList: list[Node] = None
        pass

    def GetPathPoints(self) -> list[gp_Pnt]:
        ret = []
        for i in self.PathNodeList:
            ret.append(i.CenterPoint)
        return ret

    def DisplayPathNodeListByBox(self, display: Viewer3d, _transparency: float = 0.5, _color="red") -> None:
        for i in self.PathNodeList:
            i.DisplayBoxShape(
                display, _transparency=_transparency, _color=_color)
        return

    def DisplayPathNodeListByPipe(self, display: Viewer3d, _transparency: float = 0.5, _color="red", diameter: float = 3) -> None:
        pathPntList = self.GetPathPoints()
        pipeBuilder = PipeBuilder(pathPntList, diameter)
        pipeBuilder.DisplayPipeShape(
            display, _transparency=_transparency, _color=_color)
        return

    def DisplayPathNodeListBySpline(self, display: Viewer3d, _transparency: float = 0.5, _color="red", diameter: float = 3) -> None:
        pathPntList = self.GetPathPoints()
        splineBuilder = SplineBuilder(pathPntList, diameter)
        splineBuilder.DisplaySplineShape(
            display, _transparency=_transparency, _color=_color)
        return

    def _IsOutOfRange(self, i: int, j: int, k: int, mapSize: int) -> bool:
        return i >= mapSize or j >= mapSize or k >= mapSize or i < 0 or j < 0 or k < 0

    def _IsObstacle(self, src: Node) -> bool:
        return src.Obstacle

    def _CalEuclidDistance(self, src: Node, dst: Node) -> float:
        return src.CenterPoint.Distance(dst.CenterPoint)

    def _LineOfSight3D(self, src: Node, dst: Node, nodeMap: list[list[list[Node]]]) -> bool:
        x1, y1, z1 = src.I, src.J, src.K
        x2, y2, z2 = dst.I, dst.J, dst.K

        if (x2 > x1):
            xs = 1
            dx = x2 - x1
        else:
            xs = -1
            dx = x1 - x2

        if (y2 > y1):
            ys = 1
            dy = y2 - y1
        else:
            ys = -1
            dy = y1 - y2

        if (z2 > z1):
            zs = 1
            dz = z2 - z1
        else:
            zs = -1
            dz = z1 - z2

        if (dx >= dy and dx >= dz):
            p1 = 2 * dy - dx
            p2 = 2 * dz - dx
            while (x1 != x2):
                x1 += xs
                if (p1 >= 0):
                    y1 += ys
                    p1 -= 2 * dx
                if (p2 >= 0):
                    z1 += zs
                    p2 -= 2 * dx
                p1 += 2 * dy
                p2 += 2 * dz
                if (self._IsObstacle(nodeMap[x1][y1][z1])):
                    return False

        elif (dy >= dx and dy >= dz):
            p1 = 2 * dx - dy
            p2 = 2 * dz - dy
            while (y1 != y2):
                y1 += ys
                if (p1 >= 0):
                    x1 += xs
                    p1 -= 2 * dy
                if (p2 >= 0):
                    z1 += zs
                    p2 -= 2 * dy
                p1 += 2 * dx
                p2 += 2 * dz
                if (self._IsObstacle(nodeMap[x1][y1][z1])):
                    return False
        else:
            p1 = 2 * dy - dz
            p2 = 2 * dx - dz
            while (z1 != z2):
                z1 += zs
                if (p1 >= 0):
                    y1 += ys
                    p1 -= 2 * dz
                if (p2 >= 0):
                    x1 += xs
                    p2 -= 2 * dz
                p1 += 2 * dy
                p2 += 2 * dx
                if (self._IsObstacle(nodeMap[x1][y1][z1])):
                    return False
        return True

    def _PostSmoothing(self, src: Node, dst: Node, nodeMap: list[list[list[Node]]]) -> None:
        pathNodeList = []
        finder: Node = dst
        pathNodeList.append(finder)
        tmp: Node = finder.Parent

        while (finder != src):
            while (self._LineOfSight3D(finder, tmp.Parent, nodeMap)):
                tmp = tmp.Parent
                if (tmp == src):
                    break
            if (tmp == src):
                break
            finder = tmp
            tmp = finder.Parent
            pathNodeList.append(finder)
        pathNodeList.append(src)

        self.PathNodeList = pathNodeList

    def _InitPathNodeList(self, src: Node, dst: Node) -> None:
        stack: list[Node] = []
        finder: Node = dst

        while (finder.Parent != src):
            stack.append(finder)
            finder = finder.Parent
        stack.append(finder)
        stack.append(src)

        self.PathNodeList = stack


if (__name__ == "__main__"):
    a, b, c, d = init_display()
    agnet = Agent()
    agnet.PathNodeList = [Node(gp_Pnt(0, 0, 0), gp_Pnt(1, 1, 1), 1, 1, 1)]
    agnet.DisplayPathNodeListByBox(a)
    a.FitAll()
    b()
    pass
