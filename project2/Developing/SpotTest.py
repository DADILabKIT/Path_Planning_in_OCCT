import util

from OCC.Core.Quantity import (
    Quantity_Color,
    Quantity_TOC_RGB,
    Quantity_NOC_WHITE
)
from OCC.Core.TopoDS import TopoDS_Compound
from Map.GridMap import GridMap
from OCC.Display.SimpleGui import init_display
from OCC.Core.BRepPrimAPI import BRepPrimAPI_MakeBox
from OCC.Core.gp import gp_Pnt
from Render.TessellatorShape import TessellatorShape
from Render.TessellatorCompound import TessellatorCompound
from Render.STPRender import STPRender


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
stp = STPRender("RXM4AB1BD.stp", gp_Pnt(-4.901, 0, 1.4),
                gp_Pnt(4.599, 0, 1.4), a)

box = BRepPrimAPI_MakeBox(gp_Pnt(0, 0, 0), gp_Pnt(10, 10, 10)).Shape()

tl = TessellatorShape(box, a)
# g = stp.Shape()
# tl = TessellatorCompound(stp.Shape, a)
tl.mesh.RandomSampling(4000)
# tl.mesh.DisplayVertices()
tl.mesh.DisplayPoints()
# tl.mesh.DisplayEdges()


b()
