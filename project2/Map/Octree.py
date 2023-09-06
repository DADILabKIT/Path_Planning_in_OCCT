from OCC.Core.gp import gp_Pnt
from OCC.Display.OCCViewer import Viewer3d
from Map.Node import Node
from Map.Box import Box
from enum import *

DLB = 0
DRB = 1
DLF = 2
DRF = 3
ULB = 4
URB = 5
ULF = 6
URF = 7

class Octree(Box):
    class Octant(IntEnum):
        DLB = 0
        DRB = 1
        DLF = 2
        DRF = 3
        ULB = 4
        URB = 5
        ULF = 6
        URF = 7

    class Direction(IntEnum):
        Up = 0
        Down = 1
        Right = 2
        Left = 3
        Front = 4
        Back = 5
        
    def __init__(self, startPoint: gp_Pnt = None, endPoint: gp_Pnt = None, display: Viewer3d = None, gap: float = 0.0) -> None:
        super().__init__(startPoint, endPoint, display)
        # None 일 경우 메인 Octree이거나 빈 Octree
        self.mainNode: Node = None
        self.Parent:Octree = None
        self.children: list[Octree] = None
        self.gap = gap
        self.PathPoint = None
        self.f = 0.0
        self.g = 0.0
        self.h = 0.0
        
        pass

    def CalHValue(self, endNode:"Octree"):
        self.h = self.CenterPoint.Distance(endNode.CenterPoint)
    def CalGValue(self, curNode: "Octree"):
        return self.CenterPoint.Distance(curNode.CenterPoint)
    
    def InsertNode(self, insertNode: Node) -> None:
        x, y, z = insertNode.CenterPoint.X(), insertNode.CenterPoint.Y(), insertNode.CenterPoint.Z()
        #insertNode.DisplayBoxShape(0.9)
        
        # Octree 범위를 벗어나면 종료
        if (self.IsOutofRange(self.MinPoint, self.MaxPoint, x, y, z)):
            print("Is out of range!!")
            return
        
        # 이미 insertNode가 Octree에 존재하면 종료
        if (self.FindNode(insertNode)):
            print("already exists!!")
            return
        
        # 중점을 기준으로 이동
        midX, midY, midZ = self.GetMidRange(self.MinPoint, self.MaxPoint)

        pos = self.DecidingPos(x, y, z, midX, midY, midZ)
        if (self.children == None):
            self.children = self.InitChildren(self.MinPoint, self.CenterPoint, self.MaxPoint, self.Display)
            for i in range(len(self.children)):
                self.children[i].Parent = self
                #self.children[i].DisplayBoxShape(1)
            self.children[pos].mainNode = insertNode
            return
        elif (self.children[pos].mainNode == None and self.children[pos].gap != -1):
                
            self.children[pos].mainNode = insertNode

            #self.children[pos].DisplayBoxShape(1)
            return
        elif (self.children[pos].mainNode == None and self.children[pos].gap == -1):
            self.children[pos].InsertNode(insertNode)
            return
        else:
            _insertNode = self.children[pos].mainNode
            self.children[pos].gap = -1
            self.children[pos].mainNode = None
            self.children[pos].InitChildren(self.children[pos].MinPoint,self.children[pos].CenterPoint, self.children[pos].MaxPoint,self.children[pos].Display)

            self.children[pos].InsertNode(_insertNode)
            self.children[pos].InsertNode(insertNode)
            return
    
    def FindNode(self, src: Node) -> bool:
        x, y, z= src.CenterPoint.X(), src.CenterPoint.Y(), src.CenterPoint.Z()
        # 범위를 벗어나면 False
        if (self.IsOutofRange(self.MinPoint, self.MaxPoint, x, y, z)):
            return False
        # 현재 위치에서의 메인 노드가 찾고자하는 메인 노드의 위치면 True
        if (self.mainNode != None and self.mainNode == src):
            return True
            
        # 중점을 기준으로 다음 행선지 탐색
        midX, midY, midZ = self.GetMidRange(self.MinPoint, self.MaxPoint)
        
        pos = self.DecidingPos(x, y, z, midX, midY, midZ)
        
        # 다음 행선지가 없다면 False
        if (self.children == None):
            return False
        
        # 다음 행선지로 이동
        return self.children[pos].FindNode(src)
        
        
    @staticmethod
    def InitChildren(minPoint: gp_Pnt, centerPoint: gp_Pnt, maxPoint: gp_Pnt, display: Viewer3d, gap: float = 0.0) -> None:
        children:list[Octree] = []
        #DLB
        children.append(Octree(minPoint, centerPoint, display, gap))
        #DRB
        children.append(Octree(gp_Pnt(centerPoint.X(), minPoint.Y(), minPoint.Z()), gp_Pnt(maxPoint.X(), centerPoint.Y(), centerPoint.Z()), display, gap))
        # DLF
        children.append(Octree(gp_Pnt(minPoint.X(), centerPoint.Y(), minPoint.Z()), gp_Pnt(centerPoint.X(), maxPoint.Y(), centerPoint.Z()), display, gap))
        # DRF
        children.append(Octree(gp_Pnt(centerPoint.X(), centerPoint.Y(), minPoint.Z()), gp_Pnt(maxPoint.X(), maxPoint.Y(), centerPoint.Z()), display, gap))
        #DLB
        children.append(Octree(gp_Pnt(minPoint.X(), minPoint.Y(), centerPoint.Z()), gp_Pnt(centerPoint.X(), centerPoint.Y(), maxPoint.Z()), display, gap))
        #DRB
        children.append(Octree(gp_Pnt(centerPoint.X(), minPoint.Y(), centerPoint.Z()), gp_Pnt(maxPoint.X(), centerPoint.Y(), maxPoint.Z()), display, gap))
        # DLF
        children.append(Octree(gp_Pnt(minPoint.X(), centerPoint.Y(), centerPoint.Z()), gp_Pnt(centerPoint.X(), maxPoint.Y(), maxPoint.Z()), display, gap))
        # DRF
        children.append(Octree(gp_Pnt(centerPoint.X(), centerPoint.Y(), centerPoint.Z()), gp_Pnt(maxPoint.X(), maxPoint.Y(), maxPoint.Z()), display, gap))
        
        return children
        
    
    @staticmethod
    def IsOutofRange(min: gp_Pnt, max: gp_Pnt, x: float, y: float, z: float) -> None:
        return (min.X() > x or min.Y() > y or min.Z() > z) or (max.X() < x or max.Y() < y or max.Z() < z)
    

    @staticmethod
    def GetMidRange(minPoint:gp_Pnt, maxPoint:gp_Pnt) -> tuple[float, float, float]:
        midX = (maxPoint.X() + minPoint.X()) / 2
        midY = (maxPoint.Y() + minPoint.Y()) / 2
        midZ = (maxPoint.Z() + minPoint.Z()) / 2
        
        return midX, midY, midZ
    
    @staticmethod
    def DecidingPos(x, y, z, midX: float, midY: float, midZ: float) -> int:
        if (x <= midX):
            if (y <= midY):
                if (z<= midZ):
                    return DLB
                else:
                    return ULB
            else:
                if (z<= midZ):
                    return DLF
                else:
                    return ULF
        else:
            if (y <= midY):
                if (z<= midZ):
                    return DRB
                else:
                    return URB
            else:
                if (z <= midZ):
                    return DRF
                else:
                    return URF
                
    # neighbor finding
    def isLeaf(self):
        return not self.children
    
    def GetNeighborOfGreaterOrEqualSize(self, direction) -> "Octree" or None:
        if (direction == self.Direction.Down):
            if (self.Parent == None):
                return None
                
            if (self.Parent.children[self.Octant.ULB] == self):
                return self.Parent.children[self.Octant.DLB]
            if (self.Parent.children[self.Octant.ULF] == self):
                return self.Parent.children[self.Octant.DLF]
            if (self.Parent.children[self.Octant.URB] == self):
                return self.Parent.children[self.Octant.DRB]
            if (self.Parent.children[self.Octant.URF] == self):
                return self.Parent.children[self.Octant.DRF]
            
            node:Octree = self.Parent.GetNeighborOfGreaterOrEqualSize(direction)

            if (node is None or node.isLeaf()):
                return node
            # self is Down
            if (self.Parent.children[self.Octant.DLB] == self):
                return node.children[self.Octant.ULB]
            elif (self.Parent.children[self.Octant.DLF] == self):
                return node.children[self.Octant.ULF]
            elif (self.Parent.children[self.Octant.DRB] == self):
                return node.children[self.Octant.URB]
            else:
                return node.children[self.Octant.DRF]
            
        if (direction == self.Direction.Up):
            if (self.Parent == None):
                return None
                
            if (self.Parent.children[self.Octant.DLB] == self):
                return self.Parent.children[self.Octant.ULB]
            if (self.Parent.children[self.Octant.DLF] == self):
                return self.Parent.children[self.Octant.ULF]
            if (self.Parent.children[self.Octant.DRB] == self):
                return self.Parent.children[self.Octant.URB]
            if (self.Parent.children[self.Octant.DRF] == self):
                return self.Parent.children[self.Octant.URF]
            
            node:Octree = self.Parent.GetNeighborOfGreaterOrEqualSize(direction)

            if (node is None or node.isLeaf()):
                return node
            # self is Down
            if (self.Parent.children[self.Octant.ULB] == self):
                return node.children[self.Octant.DLB]
            elif (self.Parent.children[self.Octant.ULF] == self):
                return node.children[self.Octant.DLF]
            elif (self.Parent.children[self.Octant.URB] == self):
                return node.children[self.Octant.DRB]
            else:
                return node.children[self.Octant.DRF]
            
        if (direction == self.Direction.Back):
            if (self.Parent == None):
                return None
                
            if (self.Parent.children[self.Octant.DLF] == self):
                return self.Parent.children[self.Octant.DLB]
            if (self.Parent.children[self.Octant.DRF] == self):
                return self.Parent.children[self.Octant.DRB]
            if (self.Parent.children[self.Octant.ULF] == self):
                return self.Parent.children[self.Octant.ULB]
            if (self.Parent.children[self.Octant.URF] == self):
                return self.Parent.children[self.Octant.URB]
            
            node:Octree = self.Parent.GetNeighborOfGreaterOrEqualSize(direction)

            if (node is None or node.isLeaf()):
                return node
            # self is Down
            if (self.Parent.children[self.Octant.ULB] == self):
                return node.children[self.Octant.ULF]
            elif (self.Parent.children[self.Octant.DLB] == self):
                return node.children[self.Octant.DLF]
            elif (self.Parent.children[self.Octant.URB] == self):
                return node.children[self.Octant.URF]
            else:
                return node.children[self.Octant.DRF]
            
        if (direction == self.Direction.Front):
            if (self.Parent == None):
                return None
                
            if (self.Parent.children[self.Octant.DLB] == self):
                return self.Parent.children[self.Octant.DLF]
            if (self.Parent.children[self.Octant.DRB] == self):
                return self.Parent.children[self.Octant.DRF]
            if (self.Parent.children[self.Octant.ULB] == self):
                return self.Parent.children[self.Octant.ULF]
            if (self.Parent.children[self.Octant.URB] == self):
                return self.Parent.children[self.Octant.URF]
            
            node:Octree = self.Parent.GetNeighborOfGreaterOrEqualSize(direction)

            if (node is None or node.isLeaf()):
                return node
            # self is Down
            if (self.Parent.children[self.Octant.ULF] == self):
                return node.children[self.Octant.ULB]
            elif (self.Parent.children[self.Octant.DLF] == self):
                return node.children[self.Octant.DLB]
            elif (self.Parent.children[self.Octant.URF] == self):
                return node.children[self.Octant.URB]
            else:
                return node.children[self.Octant.DRB]
            
        if (direction == self.Direction.Right):
            if (self.Parent == None):
                return None
                ##
            if (self.Parent.children[self.Octant.DLB] == self):
                return self.Parent.children[self.Octant.DRB]
            if (self.Parent.children[self.Octant.DLF] == self):
                return self.Parent.children[self.Octant.DRF]
            if (self.Parent.children[self.Octant.ULB] == self):
                return self.Parent.children[self.Octant.URB]
            if (self.Parent.children[self.Octant.ULF] == self):
                return self.Parent.children[self.Octant.URF]
            
            node:Octree = self.Parent.GetNeighborOfGreaterOrEqualSize(direction)

            if (node is None or node.isLeaf()):
                return node
            # self is Down
            if (self.Parent.children[self.Octant.URF] == self):
                return node.children[self.Octant.ULF]
            elif (self.Parent.children[self.Octant.DRF] == self):
                return node.children[self.Octant.DLF]
            elif (self.Parent.children[self.Octant.URB] == self):
                return node.children[self.Octant.ULB]
            else:
                return node.children[self.Octant.DLB]
            
        if (direction == self.Direction.Left):
            if (self.Parent == None):
                return None
                ##
            if (self.Parent.children[self.Octant.DRB] == self):
                return self.Parent.children[self.Octant.DLB]
            if (self.Parent.children[self.Octant.DRF] == self):
                return self.Parent.children[self.Octant.DLF]
            if (self.Parent.children[self.Octant.URB] == self):
                return self.Parent.children[self.Octant.ULB]
            if (self.Parent.children[self.Octant.URF] == self):
                return self.Parent.children[self.Octant.ULF]
            
            node:Octree = self.Parent.GetNeighborOfGreaterOrEqualSize(direction)

            if (node is None or node.isLeaf()):
                return node
            # self is Down
            if (self.Parent.children[self.Octant.ULF] == self):
                return node.children[self.Octant.URF]
            elif (self.Parent.children[self.Octant.DLF] == self):
                return node.children[self.Octant.DRF]
            elif (self.Parent.children[self.Octant.ULB] == self):
                return node.children[self.Octant.URB]
            else:
                return node.children[self.Octant.DRB]

            
    def GetNeighborSmallerSize(self, neighbor, direction):
        candidate: list[Octree] = [] if neighbor is None else [neighbor]
        neighbors = []
        if (direction == self.Direction.Down):
            
            while len(candidate) > 0:
                if (candidate[0].isLeaf()):
                    neighbors.append(candidate[0])
                else:
                    candidate.append(candidate[0].children[self.Octant.ULB])
                    candidate.append(candidate[0].children[self.Octant.URB])
                    candidate.append(candidate[0].children[self.Octant.ULF])
                    candidate.append(candidate[0].children[self.Octant.URF])
                candidate.remove(candidate[0])

            return neighbors
        

        if (direction == self.Direction.Up):
            
            while len(candidate) > 0:
                if (candidate[0].isLeaf()):
                    neighbors.append(candidate[0])
                else:
                    candidate.append(candidate[0].children[self.Octant.DLB])
                    candidate.append(candidate[0].children[self.Octant.DRB])
                    candidate.append(candidate[0].children[self.Octant.DLF])
                    candidate.append(candidate[0].children[self.Octant.DRF])
                candidate.remove(candidate[0])

            return neighbors
        
        if (direction == self.Direction.Back):
            
            while len(candidate) > 0:
                if (candidate[0].isLeaf()):
                    neighbors.append(candidate[0])
                else:
                    candidate.append(candidate[0].children[self.Octant.DLF])
                    candidate.append(candidate[0].children[self.Octant.DRF])
                    candidate.append(candidate[0].children[self.Octant.ULF])
                    candidate.append(candidate[0].children[self.Octant.URF])
                candidate.remove(candidate[0])

            return neighbors
        
        if (direction == self.Direction.Front):
            
            while len(candidate) > 0:
                if (candidate[0].isLeaf()):
                    neighbors.append(candidate[0])
                else:
                    candidate.append(candidate[0].children[self.Octant.DLB])
                    candidate.append(candidate[0].children[self.Octant.DRB])
                    candidate.append(candidate[0].children[self.Octant.ULB])
                    candidate.append(candidate[0].children[self.Octant.URB])
                candidate.remove(candidate[0])

            return neighbors
        
        if (direction == self.Direction.Right):
            
            while len(candidate) > 0:
                if (candidate[0].isLeaf()):
                    neighbors.append(candidate[0])
                else:
                    candidate.append(candidate[0].children[self.Octant.DLF])
                    candidate.append(candidate[0].children[self.Octant.DLB])
                    candidate.append(candidate[0].children[self.Octant.ULB])
                    candidate.append(candidate[0].children[self.Octant.ULF])
                candidate.remove(candidate[0])

            return neighbors
        
        if (direction == self.Direction.Left):
            
            while len(candidate) > 0:
                if (candidate[0].isLeaf()):
                    neighbors.append(candidate[0])
                else:
                    candidate.append(candidate[0].children[self.Octant.DRF])
                    candidate.append(candidate[0].children[self.Octant.DRB])
                    candidate.append(candidate[0].children[self.Octant.URB])
                    candidate.append(candidate[0].children[self.Octant.URF])
                candidate.remove(candidate[0])

            return neighbors
        
    def GetNeighbors(self):
        result = []

        neighborUp = self.GetNeighborOfGreaterOrEqualSize(self.Direction.Up)
        neighborsUp = self.GetNeighborSmallerSize(neighborUp, self.Direction.Up)
        
        for nei in neighborsUp:
            result.append(nei)

        neighborDown = self.GetNeighborOfGreaterOrEqualSize(self.Direction.Down)
        neighborsDown = self.GetNeighborSmallerSize(neighborDown, self.Direction.Down)

        for nei in neighborsDown:
            result.append(nei)

        neighborFront = self.GetNeighborOfGreaterOrEqualSize(self.Direction.Front)
        neighborsFront = self.GetNeighborSmallerSize(neighborFront, self.Direction.Front)

        for nei in neighborsFront:
            result.append(nei)
            
        neighborBack = self.GetNeighborOfGreaterOrEqualSize(self.Direction.Back)
        neighborsBack = self.GetNeighborSmallerSize(neighborBack, self.Direction.Back)

        for nei in neighborsBack:
            result.append(nei)

        neighborRight = self.GetNeighborOfGreaterOrEqualSize(self.Direction.Right)
        neighborsRight = self.GetNeighborSmallerSize(neighborRight, self.Direction.Right)

        for nei in neighborsRight:
            result.append(nei)

        neighborLeft = self.GetNeighborOfGreaterOrEqualSize(self.Direction.Left)
        neighborsLeft = self.GetNeighborSmallerSize(neighborLeft, self.Direction.Left)

        for nei in neighborsLeft:
            result.append(nei)

        return result
    # for heap
    def __lt__(self, other: 'Octree'):
        return self.f < other.f


        