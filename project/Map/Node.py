# OCC
# for 3D Data
from OCC.Core.gp import gp_Pnt
# for visual
from OCC.Display.OCCViewer import Viewer3d

# Custom
from Box import Box

class Node(Box):
    def __init__(self, startPoint: gp_Pnt = None, endPoint: gp_Pnt = None, display: Viewer3d = None, i: int = 0, j: int = 0, k: int = 0) -> None:
        super().__init__(startPoint, endPoint, display)

        self.x: int = i
        self.y: int = j
        self.z: int = k

        self.Parent: 'Node' = None

        self.Obstacle: bool = False
        
        self.f = 0.0
        self.h = 0.0
        self.g = 0.0
        
    # for reset and recycle
    def ResetNode(self):
        self.x = 0
        self.y = 0
        self.z = 0
        
        self.f = 0.0
        self.h = 0.0
        self.g = 0.0

        self.Parent = None

        self.Obstacle = False
        
    def RecycleNode(self):
        self.f = 0.0
        self.h = 0.0
        self.g = 0.0
        
        self.Parent = None
        
    # for heap
    def __lt__(self, other: 'Node'):
        return self.f < other.f
    
    # for algorithm
    def __eq__(self, other: 'Node') -> bool:
        if (other is not None):
            return self.x == other.x and self.y == other.y and self.z == other.z
        
