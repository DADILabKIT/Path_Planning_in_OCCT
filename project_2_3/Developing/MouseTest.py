from OCC.Core.TopoDS import TopoDS_Shape
from OCC.Core.TopLoc import TopLoc_Location
from OCC.Core.gp import gp_Pnt
from OCC.Core.BRepPrimAPI import BRepPrimAPI_MakeBox
from OCC.Display.SimpleGui import init_display


def on_mouse_click(shape, x, y):
    if (shape[0] != None):
        Tshape: TopoDS_Shape = shape[0]
        loc: TopLoc_Location = Tshape.Location()
        tran = loc.Transformation().TranslationPart()
        print(tran.Coord())

    print("클릭된 위치: ({}, {})".format(x, y))
    # 추가로 처리할 작업을 수행합니다.


display, start_display, _, _ = init_display()

# 마우스 클릭 이벤트 콜백 함수를 디스플레이 창에 등록합니다.
display.register_select_callback(on_mouse_click)
box = BRepPrimAPI_MakeBox(gp_Pnt(0, 0, 0), gp_Pnt(10, 10, 10)).Shape()

display.DisplayShape(box)
# 디스플레이 창을 실행합니다.
start_display()
