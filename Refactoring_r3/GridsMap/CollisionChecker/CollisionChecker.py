import util

from OCC.Core.gp import gp_Pnt
from OCC.Core.TopoDS import TopoDS_Shape

from Tessellator.TessellatorShape import TessellatorShape
from GridsMap import GridsMap
from Node import Node


class CollisionChecker:
    def __init__(self, grids: GridsMap, shape: TopoDS_Shape) -> None:
        self.Grids: GridsMap = grids
        self.GpPntList: list[gp_Pnt] = TessellatorShape(
            shape).Mesh_.GetMeshPoints()
        pass

    def Run(self) -> bool:
        gap = (self.Grids.MaxPoint.X() - self.Grids.MinPoint.X()) / \
            self.Grids.MapSize
        for i in range(len(self.GpPntList)):
            g: gp_Pnt = self.GpPntList[i]
            x = int(((g.X() - self.Grids.MinPoint.X()) / gap))
            y = int(((g.Y() - self.Grids.MinPoint.Y()) / gap))
            z = int(((g.Z() - self.Grids.MinPoint.Z()) / gap))
            if (x >= self.Grids.MapSize or y >= self.Grids.MapSize or z >= self.Grids.MapSize or x < 0 or y < 0 or z < 0):
                continue
            if (self.Grids.NodeMap[x][y][z].Obstacle):
                return True
        return False

    def GetCollisionNode(self) -> list[Node]:
        ret = []
        gap = (self.Grids.MaxPoint.X() - self.Grids.MinPoint.X()) / \
            self.Grids.MapSize
        for i in range(len(self.GpPntList)):
            g: gp_Pnt = self.GpPntList[i]
            x = int(((g.X() - self.Grids.MinPoint.X()) / gap))
            y = int(((g.Y() - self.Grids.MinPoint.Y()) / gap))
            z = int(((g.Z() - self.Grids.MinPoint.Z()) / gap))
            if (x >= self.Grids.MapSize or y >= self.Grids.MapSize or z >= self.Grids.MapSize or x < 0 or y < 0 or z < 0):
                continue

            if (self.Grids.NodeMap[x][y][z].Obstacle and not self.Grids.NodeMap[x][y][z] in ret):
                ret.append(self.Grids.NodeMap[x][y][z])

        return ret
