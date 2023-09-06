import util

from OCC.Core.TopoDS import TopoDS_Shape
from BruteForce import BruteForce
from GridsMap.GridsMap import GridsMap
from GridsMap.CollisionChecker.CollisionChecker import CollisionChecker
from LineBuilder.SplineBuilder import SplineBuilder
from GridsMap.Node import Node


class BackTracking(BruteForce):
    def __init__(self, startNode: Node, endNode: Node, pathNodeList: list[Node], spline: TopoDS_Shape, grids: GridsMap, num: int = 2) -> None:
        super().__init__(startNode, endNode, pathNodeList, spline, grids, num)
        self.CandidateSplineList: tuple[TopoDS_Shape, float] = []

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

    def __Dfs(self, n: int, candidateNodes: list[Node], ret: list[Node]):
        if (len(ret) == self.Num + 1 or self.Done == True):
            return
        print('.')
        if (len(ret) >= 1):
            self._PathNodeInsert(ret)
            newSpline = SplineBuilder(self._GetPathGpPnt(), 3).SplineShape
            chk = CollisionChecker(self.Grids, newSpline)
            if (not chk.Run()):
                for i in ret:
                    self.AdditivePoints.append(i)
                distance = self.__CalPathDistance(self.PathNodeList)
                self.CandidateSplineList.append((newSpline, distance))
                self.NewSpline = newSpline
                self.Done =True
                return
            else:
                self._PathNodeDelete(ret)

        for i in range(n + 1, len(candidateNodes)):
            if (ret):
                if (not self.__LineOfSight3D(ret[-1], candidateNodes[i], self.Grids.NodeMap)):
                    continue
            if (not self.__LineOfSight3D(self.__GetNextNode(candidateNodes[i]), candidateNodes[i], self.Grids.NodeMap)):
                continue
            ret.append(candidateNodes[i])
            self.__Dfs(i, candidateNodes, ret)
            ret.pop()

    def __GetNextNode(self, src: Node):
        for i in self.PathNodeList:
            if (src.CenterPoint.Distance(self.StartNode.CenterPoint) < i.CenterPoint.Distance(self.StartNode.CenterPoint)):
                return i

    def __LineOfSight3D(self, src: Node, dst: Node, nodeMap: list[list[list[Node]]]) -> bool:
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
                if (nodeMap[x1][y1][z1].Obstacle):
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
                if (nodeMap[x1][y1][z1].Obstacle):
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
                if (nodeMap[x1][y1][z1].Obstacle):
                    return False
        return True

    def __CalPathDistance(self, nodeList: list[Node]) -> float:
        ret = 0
        for i in range(len(nodeList) - 1):
            ret += nodeList[i].CenterPoint.Distance(
                nodeList[i + 1].CenterPoint)
        return ret

    def InitCandidateSplinePath(self) -> None:
        self.CandidateSplineList.sort(key=lambda x: x[1])
        return
