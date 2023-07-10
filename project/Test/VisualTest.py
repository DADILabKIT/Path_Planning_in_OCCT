# for import 
from util import sys

# OCC
# for 3D Data
from OCC.Core.gp import gp_Pnt

# for visual
from OCC.Display.OCCViewer import Viewer3d
from OCC.Display.SimpleGui import init_display


# Map
from Map.GridMap import GridMap
from Map.Node import Node
from Algoritm.Astar import Astar
from Algoritm.Theta import Theta
from Algoritm.Jps import Jps
from Algoritm.JpsTheta import JpsTheta

class VisualTest:
    def __init__(self, gridMap: GridMap, display: Viewer3d) -> None:
        self.gridMap: GridMap = gridMap
        self.Display: Viewer3d  = display
        
    def InitRandomMap(self, randomBox: int = 3) -> None:
        self.gridMap.InitNodeMapByRandom(int(randomBox / 2))
    def InitInputIntMap(self) -> None:
        self.gridMap.InitNodeMapByIntMap()
    
        
    def AstarRun(self, _transparency = 0, _color = 'blue') -> None:
        s = 0
        e = self.gridMap.MapSize - 1
        startNode: Node = self.gridMap.NodeMap[s][s][s]
        endNode: Node = self.gridMap.NodeMap[e][e][e]
        
        astar = Astar(startNode,endNode, self.gridMap.NodeMap, 'astar',self.Display)
        astar.Run()
        
        astar.DisplayPathByPipe(_transparency, _color)
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
        theta.DisplayPathBySplinePipe2()
        print(theta.CalTime)
        

        self.gridMap.RecycleNodeMap()


    def JpsRun(self, _transparency = 0, _color = 'red'):
        s = 0
        e = self.gridMap.MapSize - 1
        startNode: Node = self.gridMap.NodeMap[s][s][s]
        endNode: Node = self.gridMap.NodeMap[e][e][e]
        
        jps = Jps(startNode,endNode, self.gridMap.NodeMap, 'jps' ,self.Display)
        jps.Run()
        print(jps.CalTime)
        jps.DisplayPathByPipe(_transparency, _color)
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
        
        
    def TestFunc(self) -> None:
        self.InitInputIntMap()    
        for i in range(5):
            for j in range(5):
                for k in range(5):
                    if (i == 0 and j ==0 and k ==0):
                        self.gridMap.NodeMap[i][j][k].DisplayBoxShape(_color = 'green', _transparency = 0.5)
                        continue
                    elif (i == 4 and j == 4 and k ==4):
                        self.gridMap.NodeMap[i][j][k].DisplayBoxShape(_color = 'green', _transparency = 0.5)
                        continue
                    elif (k == 4 and j == 0):
                        self.gridMap.NodeMap[i][j][k].DisplayBoxShape(_color = 'blue', _transparency = 0.5)
                        continue
                    elif (k == 4 and i == 4):
                        self.gridMap.NodeMap[i][j][k].DisplayBoxShape(_color = 'blue', _transparency = 0.5)
                        continue
                    elif (j == 0 and i == 0):
                        self.gridMap.NodeMap[i][j][k].DisplayBoxShape(_color = 'blue', _transparency = 0.5)
                        continue
                    self.gridMap.NodeMap[i][j][k].DisplayBoxShape(_color = 'red', _transparency = 0)


        

if (__name__ == '__main__'):
    print("Visaul Test..") 
    # display instance
    display, start_display, add_menu, add_menu_function = init_display()

    gridmap = GridMap(gp_Pnt(0, 0, 0), gp_Pnt(1000, 1000, 1000), display, 10)
    vt = VisualTest(gridmap, display)


    vt.InitRandomMap(int(5))
    # vt.AstarPsRun(_color= 'red')
    # vt.JpsPsRun(_color= 'green')
    vt.ThetaRun(_color = 'blue')
    
    display.FitAll()

    start_display()

