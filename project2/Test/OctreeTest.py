from collections import deque
import util


from OCC.Core.BRepPrimAPI import BRepPrimAPI_MakeSphere
from OCC.Core.gp import gp_Pnt
from OCC.Display.SimpleGui import init_display
from OCC.Core.Quantity import (
    Quantity_Color,
    Quantity_NOC_WHITE
)

from Map.GridMap import GridMap
from Map.Octree import Octree
from Map.Node import Node
from Render.TessellatorShape import TessellatorShape
from Render.TessellatorCompound import TessellatorCompound
from Render.STPRender import STPRender
from Developing.OcAstar import OcAstar
from Map.NodeSeracher import NodeSearcher
a, b, c, d = init_display()

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


grids = GridMap(gp_Pnt(-400, -400, -400), gp_Pnt(400, 400, 400), a, 8**2)
grids.InitNodeByPnt(tl.mesh.GetPoints())
grids.UpdateNodeMapByPnt(t2.mesh.GetPoints())
grids.UpdateNodeMapByPnt(t3.mesh.GetPoints())
grids.UpdateNodeMapByPnt(t4.mesh.GetPoints())
grids.UpdateNodeMapByPnt(t5.mesh.GetPoints())


oc = Octree(gp_Pnt(-400, -400, -400), gp_Pnt(400, 400, 400), a, 30)

for i in range(grids.MapSize):
    for j in range(grids.MapSize):
        for k in range(grids.MapSize):
            if (grids.NodeMap[i][j][k].Obstacle):
                oc.InsertNode(grids.NodeMap[i][j][k])


def bfs(oc: Octree, findNode: Node):
    q = deque()
    cl = []
    q.append(oc)

    while (q):
        cur: Octree = q.popleft()
        cl.append(cur)
        if (cur.Parent != None and (not cur.Parent in cl)):
            if ((cur.Parent.mainNode != None and cur.Parent.mainNode.Obstacle)):
                continue
            if (cur.Parent != None and cur.Parent.mainNode == findNode):
                return ch
            q.append(cur.Parent)

        if (cur.children == None):
            continue
        for ch in cur.children:
            if (ch in cl or (ch.mainNode != None and ch.mainNode.Obstacle)):
                continue
            if (ch.mainNode != None and ch.mainNode == findNode):
                ch.Path = cur
                return ch
            q.append(ch)


ns = NodeSearcher(grids.MinPoint, grids.Gap)
p1 = ns.GetIndex(stp.Port)
p2 = ns.GetIndex(stp2.Port)
oc.InsertNode(grids.NodeMap[p1[0] + 2][p1[1]][p1[2]])
oc.InsertNode(grids.NodeMap[p2[0] - 1][p2[1]][p2[2]])

grids.NodeMap[p1[0] + 2][p1[1]][p1[2]].DisplayBoxShape(0.5, _color="green")
grids.NodeMap[p2[0] - 1][p2[1]][p2[2]].DisplayBoxShape(0.5, _color="green")


startOcNode = bfs(oc, grids.NodeMap[p1[0] + 2][p1[1]][p1[2]])
endOcNode = bfs(oc, grids.NodeMap[p2[0] - 1][p2[1]][p2[2]])
# startOcNode.DisplayBoxShape(0.5, "blue")
# endOcNode.DisplayBoxShape(0.5, "blue")
# print(startOcNode)
# print(startOcNode)
# ocbfs = OcBFS(startOcNode, endOcNode)
# ocbfs.Run()

ocastar = OcAstar(startOcNode, endOcNode, a)
ocastar.Run()

ocastar.DisplayPathByPipe(diameter=1)


a.FitAll()
b()
