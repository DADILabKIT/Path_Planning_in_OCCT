import util
from OCC.Core.Quantity import (
    Quantity_Color,
    Quantity_TOC_RGB,
    Quantity_NOC_WHITE
)
from OCC.Core.gp import gp_Pnt
from OCC.Display.SimpleGui import init_display
from GridsMap.GridsMap import GridsMap
from GridsMap.Node import Node
from SplineOptimizer.BruteForce import BruteForce

a, b, c, d = init_display()
a.View.SetBackgroundColor(Quantity_TOC_RGB, 0, 0, 0)
a.hide_triedron()

a.View.SetBgGradientColors(
    Quantity_Color(Quantity_NOC_WHITE),
    Quantity_Color(Quantity_NOC_WHITE),
    2,
    True,
)
grids = GridsMap(gp_Pnt(0, 0, 0), gp_Pnt(100, 100, 100), 10)
grids.DisplayGridsMapInAllNode(a, _transparency=1, _color="black")

chk = BruteForce(None, None, None, None, grids)
nodes: list[Node] = chk.__InitedCollapseArea(1, 1, 1)
for i in nodes:
    i.DisplayBoxShape(a)


a.FitAll()
b()
