# Python
import time
import heapq

# OCC
from OCC.Display.OCCViewer import Viewer3d


# Custom
from Agent import Agent
from Map.GridMap import GridMap
from Map.Node import Node


class JpsTheta(Agent):
    def __init__(self, startNode: Node = None, endNode: Node = None, nodeMap: GridMap = None, agentName: str = 'Jps',display: Viewer3d = None) -> None:
        super().__init__(startNode, endNode, nodeMap, agentName, display)
        self.IsEnd: bool = False
    
        
    def Run(self):
        startTime: float = time.time()
        self.StartNode.Parent = self.StartNode
        self.StartNode.h = self.CalHeuristic(self.StartNode)
        self.StartNode.f = self.StartNode.h
        self.EnqueueOpenList(self.StartNode)
        
        while (self.OpenList):
            cur: Node = heapq.heappop(self.OpenList)
            self.InitClosedList(cur)
            
            self.ExploreOrthogonal(cur, 1, 0, 0)
            self.ExploreOrthogonal(cur, -1, 0, 0)
            self.ExploreOrthogonal(cur, 0, 1, 0)
            self.ExploreOrthogonal(cur, 0, -1, 0)
            self.ExploreOrthogonal(cur, 0, 0, 1)
            self.ExploreOrthogonal(cur, 0, 0, -1)
            
            
            self.ExploreDiagonal2D(cur, 1, -1, 0)
            self.ExploreDiagonal2D(cur, -1, -1, 0)
            self.ExploreDiagonal2D(cur, 1, 1, 0)
            self.ExploreDiagonal2D(cur, -1, 1, 0)
            
            self.ExploreDiagonal2D(cur, 1, 0, -1)
            self.ExploreDiagonal2D(cur, -1, 0, -1)
            self.ExploreDiagonal2D(cur, 1, 0, 1)
            self.ExploreDiagonal2D(cur, -1, 0, 1)
            
            self.ExploreDiagonal2D(cur, 0, -1, -1)
            self.ExploreDiagonal2D(cur, 0, 1, -1)
            self.ExploreDiagonal2D(cur, 0, -1, 1)
            self.ExploreDiagonal2D(cur, 0, 1, 1)
            
            # 3d diagonal
            self.ExploreDiagonal3D(cur, 1, 1, 1)

            self.ExploreDiagonal3D(cur, 1, 1, -1)
            self.ExploreDiagonal3D(cur, 1, -1, 1)
            self.ExploreDiagonal3D(cur, -1, 1, 1)

            self.ExploreDiagonal3D(cur, 1, -1, -1)
            self.ExploreDiagonal3D(cur, -1, 1, -1)
            self.ExploreDiagonal3D(cur, -1, -1, 1)

            self.ExploreDiagonal3D(cur, -1, -1, -1)
            

 
        if (self.IsEnd):
            self.InitPath()
            self.InitDegree()
            self.InitDistance()
            self.InitTime(startTime)
    
    def SearchJumpPointDiagonal3D(self, src: Node, dx: int, dy: int, dz: int):
        x, y, z = src.x, src.y, src.z
        
        if (dz == 1):
            for i in range(2):
                if ((not self.IsOutOfRange(x - dx, y + dy, z + i)) and \
                        self.IsObstacle(self.NodeMap[x - dx][y][z + i]) and \
                            (not self.IsObstacle(self.NodeMap[x - dx][y + dy][z + i]))):
                    self.EnqueueOpenList(src)
                    return True
                if ((not self.IsOutOfRange(x + dx, y - dy, z + i)) and \
                        self.IsObstacle(self.NodeMap[x][y - dy][z + i]) and \
                            (not self.IsObstacle(self.NodeMap[x + dx][y - dy][z + i]))):
                    self.EnqueueOpenList(src)
                    return True
                
                if (i == 1):
                    if ((not self.IsOutOfRange(x + dx, y + dy, z + i)) and \
                            self.IsObstacle(self.NodeMap[x][y][z + i]) and \
                                (not self.IsObstacle(self.NodeMap[x + dx][y + dy][z + i])) or (not self.IsObstacle(self.NodeMap[x][y + dy][z + i]))\
                                    or (not self.IsObstacle(self.NodeMap[x + dx][y][z + i]))):
                        self.EnqueueOpenList(src)
                        return True
                    
            self.ExploreOrthogonal(src, dx, 0, 0)
            self.ExploreOrthogonal(src, 0, dy, 0)
            self.ExploreOrthogonal(src, 0, 0, dz)
            self.ExploreDiagonal2D(src, dx, dy, 0)
            self.ExploreDiagonal2D(src, 0, dy, dz)
            self.ExploreDiagonal2D(src, 0, dy, dz)
            return False
        
        if (dz == 1):
            for i in range(0, -2, -1):
                if ((not self.IsOutOfRange(x - dx, y + dy, z + i)) and \
                        self.IsObstacle(self.NodeMap[x - dx][y][z + i]) and \
                            (not self.IsObstacle(self.NodeMap[x - dx][y + dy][z + i]))):
                    self.EnqueueOpenList(src)
                    return True
                if ((not self.IsOutOfRange(x + dx, y - dy, z + i)) and \
                        self.IsObstacle(self.NodeMap[x][y - dy][z + i]) and \
                            (not self.IsObstacle(self.NodeMap[x + dx][y - dy][z + i]))):
                    self.EnqueueOpenList(src)
                    return True
            
                if (i == 1):
                    if ((not self.IsOutOfRange(x + dx, y + dy, z + i)) and \
                            self.IsObstacle(self.NodeMap[x][y][z + i]) and \
                                (not self.IsObstacle(self.NodeMap[x + dx][y + dy][z + i])) or (not self.IsObstacle(self.NodeMap[x + dx][y][z + i]))\
                                    (not self.IsObstacle(self.NodeMap[x][y + dy][z + i]))):
                        self.EnqueueOpenList(src)
                        return True
            self.ExploreOrthogonal(src, dx, 0, 0)
            self.ExploreOrthogonal(src, 0, dy, 0)
            self.ExploreOrthogonal(src, 0, 0, dz)
            self.ExploreDiagonal2D(src, dx, dy, 0)
            self.ExploreDiagonal2D(src, 0, dy, dz)
            self.ExploreDiagonal2D(src, 0, dy, dz)
            return False
                    
        return False
        
    def SearchJumpPointDiagonal2D(self, src: Node, dx: int, dy: int, dz: int):
        x, y, z = src.x, src.y, src.z
        
        if (dz == 0):
            for i in range(-1, 1):                
                if ((not self.IsOutOfRange(x - dx, y + dy, z + i)) and \
                        self.IsObstacle(self.NodeMap[x - dx][y][z + i]) and \
                            (not self.IsObstacle(self.NodeMap[x - dx][y + dy][z + i]))):
                    self.EnqueueOpenList(src)
                    return True
                    
                if ((not self.IsOutOfRange(x + dx, y - dy, z + i)) and \
                        self.IsObstacle(self.NodeMap[x][y - dy][z + i]) and \
                            (not self.IsObstacle(self.NodeMap[x + dx][y - dy][z + i]))):
                    self.EnqueueOpenList(src)
                    return True                  
                if (i != 0):
                    if ((not self.IsOutOfRange(x + dx, y + dy, z + i)) and \
                            self.IsObstacle(self.NodeMap[x][y][z + i]) and \
                                ((not self.IsObstacle(self.NodeMap[x + dx][y + dy][z + i])) or (not self.IsObstacle(self.NodeMap[x][y - dy][z + i])) or (not self.IsObstacle(self.NodeMap[x - dx][y][z + i])))):
                        self.EnqueueOpenList(src)
                        return True
                    
                self.ExploreOrthogonal(src, dx, 0, 0)
                self.ExploreOrthogonal(src, 0, dy, 0)

                return False
            
        if (dx == 0):
            for i in range(-1, 1):
                if ((not self.IsOutOfRange(x + i, y - dy, z + dz)) and \
                        self.IsObstacle(self.NodeMap[x + i][y - dy][z]) and \
                            (not self.IsObstacle(self.NodeMap[x + i][y - dy][z + dz]))):
                    self.EnqueueOpenList(src)
                    return True

                if ((not self.IsOutOfRange(x + i, y + dy, z - dz)) and \
                        self.IsObstacle(self.NodeMap[x + i][y][z - dz]) and \
                            (not self.IsObstacle(self.NodeMap[x + i][y + dy][z - dz]))):
                    self.EnqueueOpenList(src)
                    return True

                if (i != 0):
                    if ((not self.IsOutOfRange(x + i, y + dy, z + dz)) and \
                            self.IsObstacle(self.NodeMap[x + i][y][z]) and \
                                (not self.IsObstacle(self.NodeMap[x + i][y + dy][z + dz])) or (not self.IsObstacle(self.NodeMap[x + i][y][z + dz])) or (not self.IsObstacle(self.NodeMap[x + i][y + dy][z]))):
                        self.EnqueueOpenList(src)
                        return True
                        
                self.ExploreOrthogonal(src, 0, 0, dz)
                self.ExploreOrthogonal(src, 0, dy, 0)

                return False
            
        if (dz == 0):
            for i in range(-1, 1):
                if ((not self.IsOutOfRange(x - dx, y + i, z + dz)) and \
                        self.IsObstacle(self.NodeMap[x - dx][y + i][z]) and \
                            (not self.IsObstacle(self.NodeMap[x - dx][y + i][z + dz]))):
                    self.EnqueueOpenList(src)
                    return True

                if ((not self.IsOutOfRange(x + dx, y + i, z - dz)) and \
                        self.IsObstacle(self.NodeMap[x][y + i][z - dz]) and \
                            (not self.IsObstacle(self.NodeMap[x + dx][y + i][z - dz]))):
                    self.EnqueueOpenList(src)
                    return True

                if (i != 0):
                    if ((not self.IsOutOfRange(x + dx, y + i, z + dz)) and \
                            self.IsObstacle(self.NodeMap[x][y + i][z]) and \
                                (not self.IsObstacle(self.NodeMap[x + dx][y + i][z + dz])) or (not self.IsObstacle(self.NodeMap[x][y + i][z + dz]))\
                                    (not self.IsObstacle(self.NodeMap[x + dx][y + i][z]))):
                        self.EnqueueOpenList(src)
                        return True

                self.ExploreOrthogonal(src, 0, 0, dz)
                self.ExploreOrthogonal(src, dx, 0, 0)

                return False
            
                
    
    def SearchJumpPointOrthogonal(self, src: Node, dx: int, dy: int, dz: int):
        x, y, z = src.x, src.y, src.z
        
        if (dx):
            
            for i in range(-1, 2):
                if ((not self.IsOutOfRange(x + dx, y + 1, z + i)) and \
                        self.IsObstacle(self.NodeMap[x][y + 1][z + i]) and \
                            (not self.IsObstacle(self.NodeMap[x + dx][y + 1][z + i]))):
                    self.EnqueueOpenList(src)
                    return True
                if ((not self.IsOutOfRange(x + dx, y - 1, z + i)) and \
                        self.IsObstacle(self.NodeMap[x][y - 1][z + i]) and \
                            (not self.IsObstacle(self.NodeMap[x + dx][y - 1][z + i]))):
                    self.EnqueueOpenList(src)
                    return True
                if (i != 0):
                    if ((not self.IsOutOfRange(x + dx, y, z + i)) and \
                            self.IsObstacle(self.NodeMap[x][y][z + i]) and \
                                (not self.IsObstacle(self.NodeMap[x + dx][y][z + i]))):
                        self.EnqueueOpenList(src)
                        return True
                    
        if (dy):
            
            for i in range(-1, 2):     
                if ((not self.IsOutOfRange(x + 1, y + dy, z + i)) and \
                        self.IsObstacle(self.NodeMap[x + 1][y + dy][z + i]) and \
                            (not self.IsObstacle(self.NodeMap[x + 1][y + dy][z + i]))):
                    self.EnqueueOpenList(src)
                    return True
                if ((not self.IsOutOfRange(x - 1, y + dy, z + i)) and \
                        self.IsObstacle(self.NodeMap[x - 1][y + dy][z + i]) and \
                            (not self.IsObstacle(self.NodeMap[x - 1][y + dy][z + i]))):
                    self.EnqueueOpenList(src)
                    return True
                if (i != 0):
                    if ((not self.IsOutOfRange(x, y + dy, z + i)) and \
                            self.IsObstacle(self.NodeMap[x][y][z + i]) and \
                                (not self.IsObstacle(self.NodeMap[x][y + dy][z + i]))):
                        self.EnqueueOpenList(src)
                        return True
                    
                    
        if (dz):
            
            for i in range(-1, 2):
                if ((not self.IsOutOfRange(x + 1, y + i, z + dz)) and \
                        self.IsObstacle(self.NodeMap[x + 1][y + i][z]) and \
                            (not self.IsObstacle(self.NodeMap[x + 1][y + i][z + dz]))):
                    self.EnqueueOpenList(src)
                    return True
                if ((not self.IsOutOfRange(x - 1, y + i, z + dz)) and \
                        self.IsObstacle(self.NodeMap[x - 1][y + i][z]) and \
                            (not self.IsObstacle(self.NodeMap[x - 1][y + i][z + dz]))):
                    self.EnqueueOpenList(src)
                    return True
                if (i != 0):
                    if ((not self.IsOutOfRange(x, y + i, z + dz)) and \
                            self.IsObstacle(self.NodeMap[x][y + i][z]) and \
                                (not self.IsObstacle(self.NodeMap[x][y + i][z + dz]))):
                        self.EnqueueOpenList(src)
                        return True
                    
        return False
        
                    
    def ExploreDiagonal3D(self, cur: Node, dx: int, dy: int, dz: int):
        if (self.IsEnd is True or self.IsObstacle(cur)):
            return None
        
        parNode: Node = cur
        
        while (self.IsEnd is False):
            nx: int = dx + cur.x
            ny: int = dy + cur.y
            nz: int = dz + cur.z
            
            ng: float = cur.g + (3) ** 0.5
            
            if (self.IsOutOfRange(nx, ny, nz)):
                return False
            
            nextNode: Node = self.NodeMap[nx][ny][nz]
            
            if (self.IsObstacle(nextNode)):
                return False
            
            if (self.LineOfSight3D(nextNode, cur.Parent) and nextNode.g == 0.0):
                nextNode.Parent = cur.Parent
                nextNode.g = cur.Parent.g + self.CalHeuristicDst(nextNode, cur.Parent)
            elif (nextNode.g == 0.0):
                nextNode.Parent = parNode
                nextNode.g = ng
            else:
                return False

                
            if (self.IsDestination(nextNode)):
                self.IsEnd = True
                return True
            
            if (self.SearchJumpPointDiagonal3D(nextNode, dx, dy, dz)):
                return True
                

            cur = nextNode
            
        return False

                    
                    
    def ExploreDiagonal2D(self, cur: Node, dx: int, dy: int, dz: int):
        if (self.IsEnd is True or self.IsObstacle(cur)):
            return None

        parNode: Node = cur
        
        while (self.IsEnd is False):
            nx: int =  dx + cur.x
            ny: int = dy + cur.y
            nz: int = dz + cur.z
            
            ng: float = cur.g + (2) ** 0.5

            
            if (self.IsOutOfRange(nx, ny , nz)):
                return False
            nextNode: Node = self.NodeMap[nx][ny][nz]

            if (self.IsObstacle(nextNode)):
                return False
            
            
            
            if (self.LineOfSight3D(nextNode, cur.Parent) and nextNode.g == 0.0):
                nextNode.Parent = cur.Parent
                nextNode.g = cur.Parent.g + self.CalHeuristicDst(nextNode, cur.Parent)
            elif (nextNode.g == 0.0):
                nextNode.Parent = parNode
                nextNode.g = ng
            else:
                return False

            
            if (self.IsDestination(nextNode)):
                self.IsEnd = True
                return True
            
            if (self.SearchJumpPointDiagonal2D(nextNode, dx, dy, dz)):
                return True
                
            cur = nextNode
            
        return False


    

    def ExploreOrthogonal(self, cur: Node, dx:int, dy: int, dz: int):
        if (self.IsEnd == True or self.IsObstacle(cur)):
            return None
        parNode: Node = cur
        
        while (self.IsEnd is False):

            nx: int =  dx + cur.x
            ny: int = dy + cur.y
            nz: int = dz + cur.z
            
            ng: float = cur.g + 1
            
            if (self.IsOutOfRange(nx, ny , nz)):
                return False
            nextNode: Node = self.NodeMap[nx][ny][nz]
            
            
            if (self.LineOfSight3D(nextNode, cur.Parent) and nextNode.g == 0.0):
                nextNode.Parent = cur.Parent
                nextNode.g = cur.Parent.g + self.CalHeuristicDst(nextNode, cur.Parent)
            elif (nextNode.g == 0.0):
                nextNode.Parent = parNode
                nextNode.g = ng
            else:
                return False


        
            if (self.IsDestination(nextNode)):
                self.IsEnd = True
                return True
            
            if (self.SearchJumpPointOrthogonal(nextNode, dx, dy, dz)):
                return True
            
            
            cur = nextNode
            
        return False
            
        
            
    