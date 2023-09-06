# for import
from util import sys
# Custom
from Render.Voxelization import VoxelizationSTL
from Map.GridMap import GridMap
from Render.STPRender import STPRender
from Render.TessellatorCompound import TessellatorCompound

# OCC
from OCC.Core.gp import gp_Pnt
from OCC.Display.SimpleGui import init_display
from OCC.Core.Quantity import (
    Quantity_Color,
    Quantity_TOC_RGB,
    Quantity_NOC_WHITE
)

a, b, c, d = init_display()
a.View.SetBackgroundColor(Quantity_TOC_RGB, 0, 0, 0)
a.hide_triedron()

a.View.SetBgGradientColors(
    Quantity_Color(Quantity_NOC_WHITE),
    Quantity_Color(Quantity_NOC_WHITE),
    2,
    True,
)

stp = STPRender("RXM4AB1BD.stp", gp_Pnt(0, 0, 0), gp_Pnt(0, 0, 0), a)
stp.DisplaySTPShape()

ts = TessellatorCompound(stp.Shape, a)
ts.mesh.RandomSampling()

grid = GridMap(gp_Pnt(-100, -100, -100), gp_Pnt(100, 100, 100), a, 30)
grid.InitNodeByPnt(ts.mesh.GetPoints())

ts.mesh.DisplayPoints()
grid.DisplayObstaclesInMap(1)

a.FitAll()
b()
