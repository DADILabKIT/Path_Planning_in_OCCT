import util

from OCC.Core.gp import gp_Pnt
from OCC.Display.SimpleGui import init_display


from GridsMap.GridsMap import GridsMap
from GridsMap.Node import Node

class NodeSeacher:
    def __init__(self) -> None:
        pass    
    
    def GetNode(self, port: gp_Pnt, direction: list[int], grids: GridsMap) -> Node:
        curPos = self.SearchNode(port ,grids)
        while (grids.NodeMap[curPos[0]][curPos[1]][curPos[2]].Obstacle):
            curPos[0] = direction[0] +curPos[0] 
            curPos[1] = direction[1] +curPos[1] 
            curPos[2] = direction[2] +curPos[2] 
            
        return grids.NodeMap[curPos[0]][curPos[1]][curPos[2]]
    
    def SearchNode(self, port:gp_Pnt, grids: GridsMap) -> list[int]:
        gap = (grids.MaxPoint.X() - grids.MinPoint.X()) / grids.MapSize
        x = int((port.X() - grids.MinPoint.X()) / gap)
        y = int((port.Y() - grids.MinPoint.Y()) / gap)
        z = int((port.Z() - grids.MinPoint.Z()) / gap)
        
        return [x, y, z]
    
    
