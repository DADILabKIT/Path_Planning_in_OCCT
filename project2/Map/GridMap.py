import random
import math
# OCC
# for 3D Data
from OCC.Core.gp import gp_Pnt
# for visual
from OCC.Display.OCCViewer import Viewer3d
from OCC.Core.TColgp import TColgp_Array1OfPnt

# Custom
from Box import Box
from Node import Node
from RandomBox import RandomBoxGenerator


class GridMap(Box):
    def __init__(self, startPoint: gp_Pnt = None, endPoint: gp_Pnt = None, display: Viewer3d = None, mapSize: int = 0) -> None:
        """
        GridMap을 사용하기 위해서 InitNodeMapByIntMap함수를 통해서 NodeMap을 초기화해야한다.

        Args:
            startPoint (gp_Pnt, optional): minimum vertex in grid map . Defaults to None.
            endPoint (gp_Pnt, optional): maximum vertex in grid map. Defaults to None.
            display (Viewer3d, optional): instance from occt to display. Defaults to None.
            mapSize (int, optional): grid map size. Defaults to 0.
        """
        # grid map boundary
        super().__init__(startPoint, endPoint, display)

        # display field
        self.display: Viewer3d = display

        # grid field
        self.MapSize: int = mapSize

        self.NodeMap: list[list[list[Node]]] = [
            [[None for _ in range(mapSize)] for _ in range(mapSize)] for _ in range(mapSize)]
        self.Gap: float = 0.0

    # for init
    def InitNodeMapByIntMap(self) -> None:
        intMap: list[list[list[int]]] = [[list(map(int, input().split())) for _ in range(
            self.MapSize)] for _ in range(self.MapSize)]

        nodeMap: list[list[list[Node]]] = [[[None for _ in range(
            self.MapSize)] for _ in range(self.MapSize)] for _ in range(self.MapSize)]
        gap: float = (self.MaxPoint.X() - self.MinPoint.X()) / self.MapSize
        self.Gap = gap

        for i in range(self.MapSize):
            for j in range(self.MapSize):
                for k in range(self.MapSize):
                    minX = self.MinPoint.X() + (i * gap)
                    minY = self.MinPoint.Y() + (j * gap)
                    minZ = self.MinPoint.Z() + (k * gap)
                    minPoint: gp_Pnt = gp_Pnt(minX, minY, minZ)

                    maxX = self.MinPoint.X() + ((i + 1) * gap)
                    maxY = self.MinPoint.Y() + ((j + 1) * gap)
                    maxZ = self.MinPoint.Z() + ((k + 1) * gap)
                    maxPoint: gp_Pnt = gp_Pnt(maxX, maxY, maxZ)

                    nodeMap[i][j][k] = Node(
                        minPoint, maxPoint, self.Display, i, j, k)

                    if (intMap[i][j][k] == 1):
                        nodeMap[i][j][k].Obstacle = True

        self.NodeMap = nodeMap

    def InitNodeMapByRandom(self, boxNumber=3, seed=True):
        gap: float = (self.MaxPoint.X() - self.MinPoint.X()) / self.MapSize
        self.Gap = gap
        for i in range(self.MapSize):
            for j in range(self.MapSize):
                for k in range(self.MapSize):
                    minX = self.MinPoint.X() + (i * gap)
                    minY = self.MinPoint.Y() + (j * gap)
                    minZ = self.MinPoint.Z() + (k * gap)
                    minPoint: gp_Pnt = gp_Pnt(minX, minY, minZ)

                    maxX = self.MinPoint.X() + ((i + 1) * gap)
                    maxY = self.MinPoint.Y() + ((j + 1) * gap)
                    maxZ = self.MinPoint.Z() + ((k + 1) * gap)
                    maxPoint: gp_Pnt = gp_Pnt(maxX, maxY, maxZ)

                    self.NodeMap[i][j][k] = Node(
                        minPoint, maxPoint, self.Display, i, j, k)

        randomBox = RandomBoxGenerator(boxNumber, 0, self.MapSize - 1,seed)

        for i in range(0, len(randomBox.RandBox) - 1, 2):
            s1, t1 = min(randomBox.RandBox[i][0], randomBox.RandBox[i + 1][0]), max(
                randomBox.RandBox[i][0], randomBox.RandBox[i + 1][0]) + 1
            for x in range(s1, t1):
                s2, t2 = min(randomBox.RandBox[i][1], randomBox.RandBox[i + 1][1]), max(
                    randomBox.RandBox[i][1], randomBox.RandBox[i + 1][1]) + 1
                for y in range(s2, t2):
                    s3, t3 = min(randomBox.RandBox[i][2], randomBox.RandBox[i + 1][2]), max(
                        randomBox.RandBox[i][2], randomBox.RandBox[i + 1][2]) + 1
                    for z in range(s3, t3):
                        self.NodeMap[x][y][z].Obstacle = True

    def InitNodeMapByRandom2(self, percent: float) -> None:
        gap: float = (self.MaxPoint.X() - self.MinPoint.X()) / self.MapSize
        self.Gap = gap
        for i in range(self.MapSize):
            for j in range(self.MapSize):
                for k in range(self.MapSize):
                    minX = self.MinPoint.X() + (i * gap)
                    minY = self.MinPoint.Y() + (j * gap)
                    minZ = self.MinPoint.Z() + (k * gap)
                    minPoint: gp_Pnt = gp_Pnt(minX, minY, minZ)

                    maxX = self.MinPoint.X() + ((i + 1) * gap)
                    maxY = self.MinPoint.Y() + ((j + 1) * gap)
                    maxZ = self.MinPoint.Z() + ((k + 1) * gap)
                    maxPoint: gp_Pnt = gp_Pnt(maxX, maxY, maxZ)

                    self.NodeMap[i][j][k] = Node(
                        minPoint, maxPoint, self.Display, i, j, k)

        for i in range(self.MapSize):
            for j in range(self.MapSize):
                for k in range(self.MapSize):
                    if (i == 0 and j == 0 and k == 0):
                        continue
                    elif (i == self.MapSize - 1 and j == self.MapSize - 1 and k == self.MapSize - 1):
                        continue
                    elif (k == self.MapSize - 1 and j == 0):
                        continue
                    elif (k == self.MapSize - 1 and i == self.MapSize - 1):
                        continue
                    elif (j == 0 and i == 0):
                        continue
                    if (self.PercentChance(percent)):
                        self.NodeMap[i][j][k].Obstacle = True

    # for visual

    def DisplayAllNodeInMap(self, _transparency=0, _color='black') -> None:
        for i in range(self.MapSize):
            for j in range(self.MapSize):
                for k in range(self.MapSize):
                    self.NodeMap[i][j][k].DisplayBoxShape(
                        _transparency, _color)

    def DisplayObstaclesInMap(self, _transparency=0, _color='black') -> None:
        for i in range(self.MapSize):
            for j in range(self.MapSize):
                for k in range(self.MapSize):
                    if (self.NodeMap[i][j][k].Obstacle == True):
                        self.NodeMap[i][j][k].DisplayBoxShape(
                            _transparency, _color)

    def RecycleNodeMap(self) -> None:
        for i in range(self.MapSize):
            for j in range(self.MapSize):
                for k in range(self.MapSize):
                    self.NodeMap[i][j][k].RecycleNode()

    def PercentChance(self, percent: float) -> bool:
        if random.random() < percent:
            return True
        else:
            return False

    def InitNodeByPnt(self, gpList: list[gp_Pnt]) -> None:
        gap: float = (self.MaxPoint.X() - self.MinPoint.X()) / self.MapSize

        nodeMap: list[list[list[Node]]] = [[[None for _ in range(
            self.MapSize)] for _ in range(self.MapSize)] for _ in range(self.MapSize)]
        gap: float = (self.MaxPoint.X() - self.MinPoint.X()) / self.MapSize
        self.Gap = gap

        for i in range(self.MapSize):
            for j in range(self.MapSize):
                for k in range(self.MapSize):
                    minX = self.MinPoint.X() + (i * gap)
                    minY = self.MinPoint.Y() + (j * gap)
                    minZ = self.MinPoint.Z() + (k * gap)
                    minPoint: gp_Pnt = gp_Pnt(minX, minY, minZ)

                    maxX = self.MinPoint.X() + ((i + 1) * gap)
                    maxY = self.MinPoint.Y() + ((j + 1) * gap)
                    maxZ = self.MinPoint.Z() + ((k + 1) * gap)
                    maxPoint: gp_Pnt = gp_Pnt(maxX, maxY, maxZ)

                    nodeMap[i][j][k] = Node(
                        minPoint, maxPoint, self.Display, i, j, k)

        self.NodeMap = nodeMap
        
        size = len(gpList)
        for i in range(size):
            g: gp_Pnt = gpList[i]
            x = int(((g.X() - self.MinPoint.X()) / gap))
            y = int(((g.Y() - self.MinPoint.Y()) / gap))
            z = int(((g.Z() - self.MinPoint.Z()) / gap))

            self.NodeMap[x][y][z].Obstacle = True
        self.Gap = gap
        pass
    
    def UpdateNodeMapByPnt(self, gpList: list[gp_Pnt]):
        size = len(gpList)
        for i in range(size):
            g: gp_Pnt = gpList[i]
            x = int(((g.X() - self.MinPoint.X()) / self.Gap))
            y = int(((g.Y() - self.MinPoint.Y()) / self.Gap))
            z = int(((g.Z() - self.MinPoint.Z()) / self.Gap))

            self.NodeMap[x][y][z].Obstacle = True



