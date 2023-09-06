from OCC.Core.gp import gp_Trsf, gp_Vec, gp_Pnt, gp_Ax1, gp_Dir
from OCC.Core.TopLoc import TopLoc_Location
from OCC.Core.BRepPrimAPI import BRepPrimAPI_MakeBox
from OCC.Core.TopoDS import TopoDS_Shape
from OCC.Display.OCCViewer import Viewer3d
from OCC.Display.SimpleGui import init_display

import math

class MovementShape:
    def __init__(self, shape: TopoDS_Shape = None, port: gp_Pnt = gp_Pnt(0,0, 0), port2: gp_Pnt= gp_Pnt(0,0, 0), display: Viewer3d = None) -> None:
        self.Trans = gp_Trsf()
        self.Shape = shape
        self.Display = display
        self.Port: gp_Pnt = port
        self.Port2: gp_Pnt = port2
        pass
    
    def Move(self, dx: float, dy: float, dz: float):
        # shape move
        self.Trans.SetTranslation(gp_Vec(dx, dy, dz))
        moveLocation = TopLoc_Location(self.Trans)
        
        self.Shape.Move(moveLocation)
        
        # dot move
        self.Port.Translate(gp_Vec(dx, dy, dz))
        self.Port2.Translate(gp_Vec(dx, dy, dz))
        pass
    def Rotate(self, x, y, z, degree):
        axis = gp_Ax1(gp_Pnt(self.Shape.Location().Transformation().TranslationPart()), gp_Dir(x, y, z))
        angle = math.radians(degree)
        
        rotation = gp_Trsf()
        rotation.SetRotation(axis, angle)
        
        
        self.Shape.Move(TopLoc_Location(rotation))
        
        self.Port.Transform(rotation)
        self.Port2.Transform(rotation)
        
        
    
    def DisplayUpdate(self):
        self.Display.DisplayShape(self.Shape, update= True)
        pass
    
    


if (__name__ == "__main__"):
    a,b, c, d = init_display()
    
    box = BRepPrimAPI_MakeBox(gp_Pnt(0, 0, 0), gp_Pnt(1, 1, 1)).Shape()

    print(box.Location().Transformation().TranslationPart().Coord())
    move = MovementShape(box, gp_Pnt(1, 1, 2), a)
    
    move.Move(1,2,3)
    move.DisplayUpdate()
    
    b()
    