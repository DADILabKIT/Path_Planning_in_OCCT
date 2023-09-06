from OCC.Core.gp import gp_Pnt

class NodeSearcher:
    def __init__(self, minPoint: gp_Pnt, gap) -> None:
        self.MinPoint = minPoint
        self.Gap = gap
        pass
    def GetIndex(self, g: gp_Pnt):
        x = int(((g.X() - self.MinPoint.X()) / self.Gap))
        y = int(((g.Y() - self.MinPoint.Y()) / self.Gap))
        z = int(((g.Z() - self.MinPoint.Z()) / self.Gap))
        return  x, y , z