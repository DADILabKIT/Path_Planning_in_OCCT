import util

from OCC.Core.BRepPrimAPI import BRepPrimAPI_MakeSphere

from OCC.Display.SimpleGui import init_display
from OCC.Core.Quantity import (
    Quantity_Color,
    Quantity_NOC_WHITE
)

from Render.TessellatorShape import TessellatorShape
from Render.TessellatorCompound import TessellatorCompound
from Render.STPRender import STPRender

a, b, c, d = init_display()

a.View.SetBgGradientColors(
    Quantity_Color(Quantity_NOC_WHITE),
    Quantity_Color(Quantity_NOC_WHITE),
    2,
    True,
)


# Compound Mesh
stp = STPRender("RXM4AB1BD.stp", a)
tlt2 = TessellatorCompound(stp.GetShape(),a)

tlt2.mesh.DisplayEdges()

# shape Mesh
#shape = BRepPrimAPI_MakeCylinder(10, 30).Shape()
#tlt = TessellatorShape(shape, a)
#tlt.GetVertexPnt()
#tlt.mesh.DisplayEdges()
#tlt.mesh.DisplayVertices()

a.FitAll()
b()
