# for import 
from util import sys

# OCC
# for 3D Data
from OCC.Core.gp import gp_Pnt

# for visual
from OCC.Display.SimpleGui import init_display


# Map
from Map.GridMap import GridMap

display, start_display, add_menu, add_menu_function = init_display()

gridmap = GridMap(gp_Pnt(0, 0, 0), gp_Pnt(1000, 1000, 1000), display, 10)
gridmap.DisplayAllNodeInMap()

display.FitAll()

start_display()