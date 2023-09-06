from OCC.Core.gp import gp_Pnt

from Box import Box

# for test
from OCC.Display.SimpleGui import init_display


class Node(Box):
    def __init__(self, minPoint: gp_Pnt, maxPoint: gp_Pnt, i: int = 0, j: int = 0, k: int = 0) -> None:
        super().__init__(minPoint, maxPoint)
        self.I = i
        self.J = j
        self.K = k

        self.Obstacle = False
        self.Parent = None
        self.F = 0.0
        self.G = 0.0
        pass

    def __lt__(self, other: 'Node') -> bool:
        return self.F < other.F

    def __eq__(self, other: 'Node') -> bool:
        if (other is not None):
            return self.I == other.I and self.J == other.J and self.K == other.K
        return False

    def __hash__(self) -> int:
        return super().__hash__()


if (__name__ == "__main__"):
    a, b, c, d = init_display()
    node = Node(gp_Pnt(0, 0, 0), gp_Pnt(1, 1, 1))
    print(node.MinPoint.Coord())
    print(node.CenterPoint.Coord())
    print(node.MaxPoint.Coord())
    node.DisplayBoxShape(a)
    a.FitAll()
    b()
    pass
