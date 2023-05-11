# OCC
# for 3D Data
from OCC.Core.gp import gp_Pnt
# for visual
from OCC.Display.OCCViewer import Viewer3d

# Custom
from Box import Box
from Node import Node

class GridMap(Box):
    def __init__(self, startPoint: gp_Pnt = None, endPoint: gp_Pnt = None, display: Viewer3d = None ,mapSize: int = 0) -> None:
        # grid map boundary
        super().__init__(startPoint, endPoint, display)
        
        # display field
        self.display: Viewer3d = display
        
        # grid field
        self.MapSize: int = mapSize
        
        self.NodeMap: list[list[list[Node]]] = self.InitNodeMap()
        
    # for init
    def InitNodeMap(self) -> list[list[list[Node]]]:
        nodeMap = [[[None for _ in range(self.MapSize)] for _ in range(self.MapSize)] for _ in range(self.MapSize)]
        gap: float = (self.MaxPoint.X() - self.MinPoint.X()) / self.MapSize
        
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
                    
                    nodeMap[i][j][k] = Node(minPoint, maxPoint, self.Display, i, j, k)
                    
        return nodeMap
    
    # for visual
    def DisplayAllNodeInMap(self, _transparency = 0, _color = 'black') -> None:
        for i in range(self.MapSize):
            for j in range(self.MapSize):
                for k in range(self.MapSize):
                    self.NodeMap[i][j][k].DisplayBoxShape(_transparency, _color)