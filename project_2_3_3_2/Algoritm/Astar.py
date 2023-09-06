# Python
import heapq
import time

# OCC
from OCC.Display.OCCViewer import Viewer3d

# Custom
from Agent import Agent
from Map.Node import Node
from Map.GridMap import GridMap



class Astar(Agent):
    def __init__(self, startNode: Node = None, endNode: Node = None, griMap: GridMap = None, agentName: str = 'astar', display: Viewer3d = None) -> None:
        """_summary_

        Args:
            startNode (Node): start point
            endNode (Node): end point
            griMap (GridMap): grid map
        """
        super().__init__(startNode, endNode, griMap, agentName, display)
        
        

                
        
    def Run(self):
        startTime: float = time.time()
        self.StartNode.Parent =self.StartNode
        heapq.heappush(self.OpenList, self.StartNode)
        
        while (self.OpenList):
            curNode: Node = heapq.heappop(self.OpenList)
            self.InitClosedList(curNode)
            
            if (self.IsDestination(curNode)):
                self.InitPath()
                self.InitTime(startTime)
                self.InitDistance()
                self.InitDegree()
                return None
            
            for i in range(-1, 2):
                for j in range(-1, 2):
                    for k in range(-1, 2):
                        if (i == 0 and j == 0 and k == 0):
                            continue
                        
                        nx: int = i + curNode.x
                        ny: int = j + curNode.y
                        nz: int = k + curNode.z
                        
                        if (self.IsOutOfRange(nx, ny, nz) or self.ClosedList[nx][ny][nz]):
                            continue
                        
                        nextNode: Node = self.NodeMap[nx][ny][nz]
                        
                        if (self.IsObstacle(nextNode)):
                            continue
                        
                        cost: float = (max(-i, i) + max(-j, j) + max(-k, k)) ** 0.5
                        ng: float = curNode.g + cost
                        
                        if (nextNode.Parent == None or ng < nextNode.g):
                            nextNode.g = ng
                            nextNode.h = self.CalHeuristic(nextNode)
                            nextNode.f = nextNode.g + nextNode.h
                            nextNode.Parent = curNode
                            
                            heapq.heappush(self.OpenList, nextNode)
                            
            