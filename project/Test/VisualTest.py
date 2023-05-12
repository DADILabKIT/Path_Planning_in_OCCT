# for import 
from util import sys

# OCC
# for 3D Data
from OCC.Core.gp import gp_Pnt

# for visual
from OCC.Display.SimpleGui import init_display


# Map
from Map.GridMap import GridMap
from Map.Node import Node
from Algoritm.Astar import Astar
from Algoritm.Theta import Theta

# display instance
display, start_display, add_menu, add_menu_function = init_display()

# init grid map
gridmap = GridMap(gp_Pnt(0, 0, 0), gp_Pnt(1000, 1000, 1000), display, 6)
gridmap.InitNodeMapByIntMap()

# astar run
startNode:Node = gridmap.NodeMap[0][0][0]
endNode:Node = gridmap.NodeMap[5][5][5]

#astar = Astar(startNode, endNode, gridmap, display)
astar = Astar(startNode, endNode, gridmap, display)
theta = Theta(startNode, endNode, gridmap, display)

theta.Run()
theta.DisplayPathByPipe()
gridmap.DisplayObstaclesInMap()

# Camera Fitt all
display.FitAll()

start_display()

