from OCC.Core.BRepPrimAPI import BRepPrimAPI_MakeSphere
from OCC.Core.gp import gp_Pnt

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
# STP 파일 읽기
stp = STPRender("RXM4AB1BD.stp", gp_Pnt(10, 10, 10), gp_Pnt(1, 1, 1), a)
# STP 파일은 Compound로 되어있음
# 일반 Shape은 TessellatorShape 으로 진행해야함
tlt2 = TessellatorCompound(stp.Shape, a)

# 삼각형 메쉬 간선 출력
# tlt2.mesh.DisplayEdges()
# 샘플링 개수 입력 후 샘플링 진행 
tlt2.mesh.RandomSampling(1000)

# 샘플링 점 가시화
tlt2.mesh.DisplayPoints()
# 점군을 리스트로 반환
#tlt2.mesh.GetPoints()

# shape Mesh 예제
# shape = BRepPrimAPI_MakeCylinder(10, 30).Shape()
# tlt = TessellatorShape(shape, a)
# tlt.GetVertexPnt()
# tlt.mesh.DisplayEdges()
# tlt.mesh.DisplayVertices()

a.FitAll()
b()
