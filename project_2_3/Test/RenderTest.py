import util

from Render.STPRender import STPRender
from Render.TessellatorCompound import TessellatorCompound
from Algoritm.JpsTheta import JpsTheta
from Map.NodeSeracher import NodeSearcher

from OCC.Core.BRepPrimAPI import BRepPrimAPI_MakeSphere
from OCC.Core.gp import gp_Pnt
from OCC.Display.SimpleGui import init_display
from Map.GridMap import GridMap
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

# file name, port crood, display
stp = STPRender("AB6M-M1P-G.stp", gp_Pnt(-4.901, 0, 1.4),
                gp_Pnt(4.599, 0, 1.4), a)
stp2 = STPRender("LA38-11D-R.stp", gp_Pnt(15.169, -37.86, -
                 8.852), gp_Pnt(18.169, -37.86, -8.852), a)
stp3 = STPRender("LA38-11D-R.stp", gp_Pnt(15.169, -37.86, -
                 8.852), gp_Pnt(18.169, -37.86, -8.852), a)
stp4 = STPRender("LA38-11D-R.stp", gp_Pnt(15.169, -37.86, -
                 8.852), gp_Pnt(18.169, -37.86, -8.852), a)
stp5 = STPRender("LA38-11D-R.stp", gp_Pnt(15.169, -37.86, -
                 8.852), gp_Pnt(18.169, -37.86, -8.852), a)

# translation move
stp.Move(1, 1, 1)
stp.Rotate(0, 1, 0, -90)
stp2.Move(300, 100, 0)
stp3.Move(50, -100, 0)
stp4.Move(150, 50, 0)
stp5.Move(100, -50, 0)

stp2.Rotate(0, 0, 1, -90)

stp.DisplaySTPShape()

stp2.DisplaySTPShape()
stp3.DisplaySTPShape()
stp4.DisplaySTPShape()
stp5.DisplaySTPShape()


# tesselating
tl = TessellatorCompound(stp.Shape, a)
t2 = TessellatorCompound(stp2.Shape, a)
t3 = TessellatorCompound(stp3.Shape, a)
t4 = TessellatorCompound(stp4.Shape, a)
t5 = TessellatorCompound(stp5.Shape, a)

# tl.mesh.DisplayEdges()
# t2.mesh.DisplayEdges()
# t3.mesh.DisplayEdges()
# t4.mesh.DisplayEdges()
# t5.mesh.DisplayEdges()

grids = GridMap(gp_Pnt(-400, -400, -400), gp_Pnt(400, 400, 400),  a, 50)


grids.InitNodeByPnt(tl.mesh.GetPoints())
grids.UpdateNodeMapByPnt(t2.mesh.GetPoints())
grids.UpdateNodeMapByPnt(t3.mesh.GetPoints())
grids.UpdateNodeMapByPnt(t4.mesh.GetPoints())
grids.UpdateNodeMapByPnt(t5.mesh.GetPoints())

# grids.DisplayObstaclesInMap(1)

ns = NodeSearcher(grids.MinPoint, grids.Gap)
p1 = ns.GetIndex(stp.Port)
p2 = ns.GetIndex(stp2.Port)
# grids.NodeMap[p1[0] + 2][p1[1]][p1[2]].DisplayBoxShape(0.5, _color='blue')
# grids.NodeMap[p2[0] - 2][p2[1]][p2[2]].DisplayBoxShape(0.5, _color='green')

jp = JpsTheta(grids.NodeMap[p1[0] + 2][p1[1]][p1[2]],
              grids.NodeMap[p2[0] - 2][p2[1]][p2[2]], grids.NodeMap, 'd', a)

jp.Run()

# jp.DisplayPathByPipe(diameter=1)
jp.DisplayPathBySplinePipe(diameter=1, _color='red',
                           startGp=stp.Port, endGp=stp2.Port)
b()
