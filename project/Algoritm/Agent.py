# Python
import math
import time

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

class Agent:
    def __init__(self, startNode: Node = None, endNode: Node = None, gridMap: GridMap = None, display: Viewer3d = None) -> None:
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
        self.PathPoints: list[gp_Pnt] = None
        self.Degree: float = 0.0
        # start point and end point
        self.StartNode: Node = startNode
        self.EndNode: Node = endNode
        # node map
        self.NodeMap: list[list[list[Node]]] = gridMap.NodeMap
        # map size
        self.N: int = len(gridMap.NodeMap)
        # open set and closed set
        self.OpenList: list[Node] = []
        self.ClosedList: list[list[list[bool]]] = [[[False for _ in range(self.N)] for _ in range(self.N)] for _ in range(self.N)]
        # display
        self.Display: Viewer3d = display
        
        
    def IsOutOfRange(self, x: int, y: int, z: int) -> bool:
        return x < 0 or y < 0 or z < 0 or x >= self.N or y >= self.N or z >= self.N
    
    def IsDestination(self, src: Node) -> bool:
        return src == self.EndNode
    
    def IsObstacle(self, src: Node) -> bool:
        return src.Obstacle
    
    def InitClosedList(self, src: Node) -> None:
        self.ClosedList[src.x][src.y][src.z] = True
    
    def InitPath(self) -> None:
        stack: list[gp_Pnt] = []
        finder: Node = self.EndNode
        
        while (finder.Parent != None):
            stack.append(finder.CenterPoint)
            finder = finder.Parent
            
        stack.append(self.StartNode.CenterPoint)
        self.PathPoints = stack
        
    def InitTime(self, startTime: float) -> None:
        self.CalTime = startTime - time.time()
    
    def InitDistance(self) -> None:
        result: float = 0.0
        length: int = len(self.PathPoints)
        
        for i in range(length - 1):
            result += self.PathPoints[i].Distance(self.PathPoints[i + 1])    
        self.Distance = result
        
    def InitDegree(self) -> None:
        result: float = 0.0
        length: int = len(self.PathPoints)
        
        for i in range(length - 2):
            v1 = gp_Vec(self.PathPoints[i].XYZ() - self.PathPoints[i + 1].XYZ())
            v2 = gp_Vec(self.PathPoints[i + 1].XYZ() - self.PathPoints[i + 2].XYZ())
            v2.Reverse()
            
            dotVal: float = v1.Dot(v2)
            magnitude: float = v1.Magnitude() * v2.Magnitude()
            
            dotVal = round(dotVal, 8)
            magnitude = round(magnitude, 8)
            
            degree: float = math.degrees(math.acos(dotVal / magnitude))
            
            result += degree
            
        self.Degree = result

    def CalHeuristic(self, src: Node) -> float:
        return ((self.EndNode.x - src.x) ** 2 + (self.EndNode.y - src.y) ** 2 + (self.EndNode.z - src.z) ** 2) ** 0.5
    
    
    def DisplayPathByPipe(self, _transparency: float = 0, _color = 'blue', diameter:float = 3) -> None:
        finalShape: TopoDS_Shape = TopoDS_Shape()
        length = len(self.PathPoints)
        
        for i in range(length - 1):
            directionEdge: TopoDS_Edge = BRepBuilderAPI_MakeEdge(self.PathPoints[i], self.PathPoints[i + 1]).Edge()
            directionWire: TopoDS_Wire = BRepBuilderAPI_MakeWire(directionEdge).Wire()
            
            directionCircle: gp_Circ = gp_Circ(gp_Ax2(self.PathPoints[i], gp_Dir(self.PathPoints[i + 1].XYZ().Subtracted(self.PathPoints[i].XYZ()))), diameter)
            directionCircleEdge: TopoDS_Edge = BRepBuilderAPI_MakeEdge(directionCircle).Edge()
            directionCircleWire: TopoDS_Wire = BRepBuilderAPI_MakeWire(directionCircleEdge).Wire()
            
            pipeShape: TopoDS_Shape = BRepOffsetAPI_MakePipe(directionWire, directionCircleWire).Shape()
            
            if finalShape.IsNull():
                finalShape = pipeShape
            else:
                finalShape = BRepAlgoAPI_Fuse(finalShape, pipeShape).Shape()
                
        self.Display.DisplayShape(finalShape, transparency = _transparency ,color = _color)
            
            