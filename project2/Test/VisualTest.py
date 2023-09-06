# for import 
from util import sys

# OCC
# for 3D Data
from OCC.Core.gp import gp_Pnt

# for visual
from OCC.Display.OCCViewer import Viewer3d
from OCC.Display.SimpleGui import init_display
from OCC.Core.BRepPrimAPI import BRepPrimAPI_MakeSphere

# Map
from Map.GridMap import GridMap
from Map.Node import Node
from Algoritm.Astar import Astar
from Algoritm.Theta import Theta
from Algoritm.ThetaC import ThetaC
from Algoritm.Jps import Jps
from Algoritm.JpsTheta import JpsTheta

class VisualTest:
    def __init__(self, gridMap: GridMap, display: Viewer3d) -> None:
        self.gridMap: GridMap = gridMap
        self.Display: Viewer3d  = display
        
    def InitRandomMap(self, randomBox: int = 3) -> None:
        self.gridMap.InitNodeMapByRandom(int(randomBox / 2))
    def InitRandomMap2(self, percent: float= 0.4) -> None:
        self.gridMap.InitNodeMapByRandom2(percent)
        
    def InitInputIntMap(self) -> None:
        self.gridMap.InitNodeMapByIntMap()
    
        
    def AstarRun(self, _transparency = 0, _color = 'blue') -> None:
        s = 0
        e = self.gridMap.MapSize - 1
        startNode: Node = self.gridMap.NodeMap[s][s][s]
        endNode: Node = self.gridMap.NodeMap[e][e][e]
        
        astar = Astar(startNode,endNode, self.gridMap.NodeMap, 'astar',self.Display)
        astar.Run()
        
        astar.DisplayPathBySplinePipe(_transparency, _color)

        self.gridMap.DisplayObstaclesInMap()
        print(astar.CalTime)
        self.gridMap.RecycleNodeMap()
        
        
        
    def AstarPsRun(self, _transparency = 0, _color = 'blue') -> None:
        s = 0
        e = self.gridMap.MapSize - 1
        startNode: Node = self.gridMap.NodeMap[s][s][s]
        endNode: Node = self.gridMap.NodeMap[e][e][e]
        
        astar = Astar(startNode,endNode, self.gridMap.NodeMap, 'astar_ps',self.Display)
        astar.Run()
        astar.PostSmoothing()
        astar.DisplayPathByPipe(_transparency, _color)
        astar.DisplayPathBySplinePipe(_transparency, _color)

        self.gridMap.DisplayObstaclesInMap()
        
        self.gridMap.RecycleNodeMap()
        
    def ThetaRun(self, _transparency = 0, _color = 'red') -> None:
        s = 0
        e = self.gridMap.MapSize - 1
        startNode: Node = self.gridMap.NodeMap[s][s][s]
        endNode: Node = self.gridMap.NodeMap[e][e][e]
        
        theta = Theta(startNode,endNode, self.gridMap.NodeMap, 'theta',self.Display)
        theta.Run()
        theta.DisplayPathByPipe(_transparency, _color)
        self.gridMap.DisplayObstaclesInMap()
        print(theta.CalTime)

        self.gridMap.RecycleNodeMap()
        
    def ThetaCRun(self, _transparency = 0, _color = 'red') -> None:
        s = 0
        e = self.gridMap.MapSize - 1
        startNode: Node = self.gridMap.NodeMap[s][s][s]
        endNode: Node = self.gridMap.NodeMap[e][e][e]
        
        thetaC = ThetaC(startNode,endNode, self.gridMap.NodeMap, 'theta',self.Display)
        thetaC.Run()
        thetaC.DisplayPathByPipe(_transparency, _color)
        self.gridMap.DisplayObstaclesInMap()
        print(thetaC.CalTime)

        self.gridMap.RecycleNodeMap()


    def JpsRun(self, _transparency = 0, _color = 'red'):
        s = 0
        e = self.gridMap.MapSize - 1
        startNode: Node = self.gridMap.NodeMap[s][s][s]
        endNode: Node = self.gridMap.NodeMap[e][e][e]
        
        jps = Jps(startNode,endNode, self.gridMap.NodeMap, 'jps' ,self.Display)
        jps.Run()
        print(jps.CalTime)
        jps.DisplayPathBySplinePipe(_transparency, _color)
        self.gridMap.DisplayObstaclesInMap()
        
        self.gridMap.RecycleNodeMap()
        
    def JpsPsRun(self, _transparency = 0, _color = 'blue') -> None:
        s = 0
        e = self.gridMap.MapSize - 1
        startNode: Node = self.gridMap.NodeMap[s][s][s]
        endNode: Node = self.gridMap.NodeMap[e][e][e]
        
        jps = Jps(startNode,endNode, self.gridMap.NodeMap, 'jps_ps', self.Display)
        jps.Run()
        jps.PostSmoothing()
        jps.DisplayPathByPipe(_transparency, _color)
        self.gridMap.DisplayObstaclesInMap()
        
        self.gridMap.RecycleNodeMap()
        
    def JpsThetaRun(self, _transparency = 0, _color = 'red'):
        s = 0
        e = self.gridMap.MapSize - 1
        startNode: Node = self.gridMap.NodeMap[s][s][s]
        endNode: Node = self.gridMap.NodeMap[e][e][e]
        
        jps = JpsTheta(startNode,endNode, self.gridMap.NodeMap, 'jps_theta' ,self.Display)
        jps.Run()
        print(jps.CalTime)
        for x in jps.PathPoints:
            self.Display.DisplayShape(x.CenterPoint)
        
        #jps.DisplayPathBySplinePipe2(_transparency, _color, 5, gap = self.gridMap.Gap)
        #jps.DisplayPathBySplinePipe(_transparency, "green", 3, gap = self.gridMap.Gap)
        #jps.DisplayPathByPipe(gap = self.gridMap.Gap)

        self.gridMap.DisplayObstaclesInMap()
        self.gridMap.RecycleNodeMap() 
        
        self.gridMap.NodeMap[e][e][e].DisplayBoxShape(_color = 'red')
        self.gridMap.NodeMap[s][s][s].DisplayBoxShape(_color = 'blue')
         


        

if (__name__ == '__main__'):
    print("Visaul Test..") 
    # display instance
    display, start_display, add_menu, add_menu_function = init_display()

    gridmap = GridMap(gp_Pnt(0, 0, 0), gp_Pnt(1000, 1000, 1000), display, 20)
    gridmap.InitNodeMapByRandom(15,True)
    
    
    vt = VisualTest(gridmap, display)
    
    vt.JpsThetaRun()

    
    display.FitAll()

    start_display()

