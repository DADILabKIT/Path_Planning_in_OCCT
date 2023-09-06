# Python
import math
import time
import heapq

# OCC
# for 3D Data
from OCC.Core.gp import gp_Pnt, gp_Vec, gp_Ax2, gp_Circ, gp_Dir
from OCC.Display.OCCViewer import Viewer3d
from OCC.Core.TopoDS import TopoDS_Edge, TopoDS_Wire, TopoDS_Shape
from OCC.Core.BRepBuilderAPI import BRepBuilderAPI_MakeEdge, BRepBuilderAPI_MakeWire
from OCC.Core.BRepOffsetAPI import BRepOffsetAPI_MakePipe
from OCC.Core.BRepAlgoAPI import BRepAlgoAPI_Fuse

# Custom
from Map.Node import Node
from Map.GridMap import GridMap
from Spline.Spline import SplineBuilder

class Agent:
    def __init__(self, startNode: Node = None, endNode: Node = None, nodeMap: GridMap = None, agentName:str = ' ', display: Viewer3d = None) -> None:
        """_summary_

        Args:
            startNode (Node): start point
            endNode (Node): end point
            gridMap (GridMap): grid map
            display (Viewer3d): display instance
        """
        # results
        self.CalTime: float = 0.0
        self.Distance: float = 0.0
        self.PathPoints: list[Node] = None
        self.Degree: float = 0.0
        # start point and end point
        self.StartNode: Node = startNode
        self.EndNode: Node = endNode
        # node map
        self.NodeMap: list[list[list[Node]]] = nodeMap
        # map size
        self.N: int = len(nodeMap) if isinstance(nodeMap, list) else None
        # open set and closed set
        self.OpenList: list[Node] = []
        self.ClosedList: list[list[list[bool]]] = [[[False for _ in range(self.N)] for _ in range(self.N)] for _ in range(self.N)] if isinstance(self.N, int) else None
        # display
        self.Display: Viewer3d = display
        self.AgentName: str = agentName
        
    def reInit(self, startNode: Node = None, endNode: Node = None, griMap: GridMap = None, display: Viewer3d = None) -> None:
        self.__init__(startNode, endNode, griMap, display)
        
    def Run(self) -> None:
        return
        
        
    def IsOutOfRange(self, x: int, y: int, z: int) -> bool:
        return x < 0 or y < 0 or z < 0 or x >= self.N or y >= self.N or z >= self.N
    
    def IsDestination(self, src: Node) -> bool:
        return src == self.EndNode
    
    def IsObstacle(self, src: Node) -> bool:
        return src.Obstacle
    
    def InitClosedList(self, src: Node) -> None:
        self.ClosedList[src.x][src.y][src.z] = True
    
    def InitPath(self) -> None:
        stack: list[Node] = []
        finder: Node = self.EndNode
        
        while (finder.Parent != self.StartNode):
            stack.append(finder)
            finder = finder.Parent
            
        stack.append(finder)
        stack.append(self.StartNode)
        
        self.PathPoints = stack
     
    def InitTime(self, startTime: float) -> None:
        self.CalTime = time.time() - startTime
    
    def InitDistance(self) -> None:
        result: float = 0.0
        length: int = len(self.PathPoints)
        
        for i in range(length - 1):
            result += self.PathPoints[i].CenterPoint.Distance(self.PathPoints[i + 1].CenterPoint)    
        self.Distance = result
        
    def InitDegree(self) -> None:
        result: float = 0.0
        length: int = len(self.PathPoints)
        
        for i in range(length - 2):
            v1 = gp_Vec(self.PathPoints[i].CenterPoint.XYZ() - self.PathPoints[i + 1].CenterPoint.XYZ())
            v2 = gp_Vec(self.PathPoints[i + 1].CenterPoint.XYZ() - self.PathPoints[i + 2].CenterPoint.XYZ())
            v2.Reverse()
            
            dotVal: float = v1.Dot(v2)
            magnitude: float = v1.Magnitude() * v2.Magnitude()
            
            dotVal = round(dotVal, 8)
            magnitude = round(magnitude, 8)
            if (magnitude != 0):
                degree: float = math.degrees(math.acos(dotVal / magnitude))
            else:
                degree = 0
            
            result += degree
            
        self.Degree = result

    def CalHeuristic(self, src: Node) -> float:
        return ((self.EndNode.x - src.x) ** 2 + (self.EndNode.y - src.y) ** 2 + (self.EndNode.z - src.z) ** 2) ** 0.5
    
    def CalHeuristicDst(self, src: Node, dst: Node) -> float:
        return ((dst.x - src.x) ** 2 + (dst.y - src.y) ** 2 + (dst.z - src.z) ** 2) ** 0.5
    
    def DisplayPathByBox(self, _transparency: float = 0, _color = 'blue') -> None:
        length = len(self.PathPoints)
        for i in range(length):
            self.PathPoints[i].DisplayBoxShape(_transparency, _color)

    
    def DisplayPathByPipe(self, _transparency: float = 0, _color = 'blue', diameter:float = 3, gap: float = 0.0) -> None:
        finalShape: TopoDS_Shape = TopoDS_Shape()
        pointList: list[gp_Pnt] = []
        #pointList.append(gp_Pnt(self.PathPoints[0].CenterPoint.X(), self.PathPoints[0].CenterPoint.Y() + gap, self.PathPoints[0].CenterPoint.Z()))
        length = len(self.PathPoints)
        for i in range(length):
            pointList.append(self.PathPoints[i].CenterPoint)
        
        #pointList.append(gp_Pnt(self.PathPoints[-1].CenterPoint.X(), self.PathPoints[-1].CenterPoint.Y() - gap, self.PathPoints[-1].CenterPoint.Z()))
        
        for i in range(length - 1):
            directionEdge: TopoDS_Edge = BRepBuilderAPI_MakeEdge(pointList[i], pointList[i + 1]).Edge()
            directionWire: TopoDS_Wire = BRepBuilderAPI_MakeWire(directionEdge).Wire()
            
            directionCircle: gp_Circ = gp_Circ(gp_Ax2(self.PathPoints[i].CenterPoint, gp_Dir(pointList[i + 1].XYZ().Subtracted(pointList[i].XYZ()))), diameter)
            directionCircleEdge: TopoDS_Edge = BRepBuilderAPI_MakeEdge(directionCircle).Edge()
            directionCircleWire: TopoDS_Wire = BRepBuilderAPI_MakeWire(directionCircleEdge).Wire()
            
            pipeShape: TopoDS_Shape = BRepOffsetAPI_MakePipe(directionWire, directionCircleWire).Shape()
            
            if finalShape.IsNull():
                finalShape = pipeShape
            else:
                finalShape = BRepAlgoAPI_Fuse(finalShape, pipeShape).Shape()
                
        self.Display.DisplayShape(finalShape, transparency = _transparency ,color = _color)
        
    def DisplayPathBySplinePipe(self, _transparency: float = 0, _color = 'blue', diameter:float = 3, gap: float  = 0.0, startGp:gp_Pnt = None, endGp:gp_Pnt = None) -> None:
        pointList: list[gp_Pnt] = []
        pointList.append(endGp)
        for i in range(len(self.PathPoints)):
            pointList.append(self.PathPoints[i].CenterPoint)
        pointList.append(startGp)
        sb = SplineBuilder(pointList)
        sb.SplineBuild()
        
        edgeShape = BRepBuilderAPI_MakeEdge(sb.CurveShape).Shape()
        wireShape = BRepBuilderAPI_MakeWire(edgeShape).Shape()
        
        Circle: gp_Circ = gp_Circ(gp_Ax2(self.PathPoints[0].CenterPoint, gp_Dir(self.PathPoints[1].CenterPoint.XYZ().Subtracted(self.PathPoints[0].CenterPoint.XYZ()))), diameter)
        CircleEdge: TopoDS_Edge = BRepBuilderAPI_MakeEdge(Circle).Shape()
        CircleWire: TopoDS_Wire = BRepBuilderAPI_MakeWire(CircleEdge).Shape()
            
        pipeShape: TopoDS_Shape = BRepOffsetAPI_MakePipe(wireShape, CircleWire).Shape()
            
        if (not pipeShape.IsNull()):
            self.Display.DisplayShape(pipeShape, transparency = _transparency ,color = _color)
            
    def DisplayPathBySplinePipe2(self, _transparency: float = 0, _color = 'blue', diameter:float = 3, gap:float = 0.0) -> None:
        pointList: list[gp_Pnt] = []
        #pointList.append(gp_Pnt(self.PathPoints[0].CenterPoint.X(), self.PathPoints[0].CenterPoint.Y() + gap, self.PathPoints[0].CenterPoint.Z()))
        
        for i in range(len(self.PathPoints)):
            pointList.append(self.PathPoints[i].CenterPoint)
        #pointList.append(gp_Pnt(self.PathPoints[-1].CenterPoint.X(), self.PathPoints[-1].CenterPoint.Y() - gap, self.PathPoints[-1].CenterPoint.Z()))
        sb = SplineBuilder(pointList)
        sb.SplineBuild2()
        edgeShape = BRepBuilderAPI_MakeEdge(sb.CurveShape).Shape()
        wireShape = BRepBuilderAPI_MakeWire(edgeShape).Shape()
        
        Circle: gp_Circ = gp_Circ(gp_Ax2(self.PathPoints[0].CenterPoint, gp_Dir(self.PathPoints[1].CenterPoint.XYZ().Subtracted(self.PathPoints[0].CenterPoint.XYZ()))), diameter)
        CircleEdge: TopoDS_Edge = BRepBuilderAPI_MakeEdge(Circle).Shape()
        CircleWire: TopoDS_Wire = BRepBuilderAPI_MakeWire(CircleEdge).Shape()
            
        pipeShape: TopoDS_Shape = BRepOffsetAPI_MakePipe(wireShape, CircleWire).Shape()
            
        if (not pipeShape.IsNull()):
            self.Display.DisplayShape(pipeShape, transparency = _transparency ,color = _color)
    
    def LineOfSight3D(self, src: Node, dst: Node) -> bool:
        x1, y1, z1 = src.x, src.y, src.z
        x2, y2, z2 = dst.x, dst.y, dst.z
        
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
                if (self.IsObstacle(self.NodeMap[x1][y1][z1])):
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
                if (self.IsObstacle(self.NodeMap[x1][y1][z1])):
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
                if (self.IsObstacle(self.NodeMap[x1][y1][z1])):
                    return False
        return True
    
    def PostSmoothing(self) -> None:
        startTime = time.time()
        result = []
        finder: Node = self.EndNode
        result.append(finder)
        tmp: Node = finder.Parent
        
        while (finder != self.StartNode):
            while (self.LineOfSight3D(finder, tmp.Parent)):
                tmp = tmp.Parent
                if (tmp == self.StartNode):
                    break
            if (tmp == self.StartNode):
                break
            
            finder = tmp
            tmp = finder.Parent
            result.append(finder)
        result.append(self.StartNode)
        self.CalTime += (time.time() - startTime)
        self.PathPoints = result
        
    def EnqueueOpenList(self, src: Node):
        if (src is not None):
            if ((not self.ClosedList[src.x][src.y][src.z])):
                
                src.h = self.CalHeuristic(src)
                src.f = src.h + src.g
                heapq.heappush(self.OpenList, src)
        
    def EnqueueOpenList2(self, src: Node):
        if (src is not None):
            if ((not self.ClosedList[src.x][src.y][src.z])):
                while (self.LineOfSight3D(src.Parent.Parent, src)):
                    if (src.Parent == self.StartNode):
                        break
                    src.Parent = src.Parent.Parent
                    src.g = self.CalHeuristicDst(src.Parent, src) + src.Parent.g
                              
                src.h = self.CalHeuristic(src)
                src.f = src.h + src.g
                heapq.heappush(self.OpenList, src)
        