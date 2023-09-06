import util

# Cumtom
from Mesh.Mesh import Mesh

# OCC
from OCC.Core.BRepMesh import BRepMesh_IncrementalMesh
from OCC.Core.BRep import BRep_Tool_Triangulation
from OCC.Core.BRepTools import breptools_Clean

from OCC.Core.TopoDS import TopoDS_Shape
from OCC.Core.TopExp import TopExp_Explorer
from OCC.Core.TopAbs import TopAbs_FACE
from OCC.Core.TopLoc import TopLoc_Location

from OCC.Core.BRepBndLib import brepbndlib_Add
from OCC.Core.Bnd import Bnd_Box

from OCC.Core.Graphic3d import Graphic3d_Vec3d
from OCC.Core.Prs3d import prs3d_GetDeflection
from OCC.Core.Precision import precision_Confusion
from OCC.Core.gp import gp_Pnt

from LineBuilder.PipeBuilder import PipeBuilder
from OCC.Display.SimpleGui import init_display
from OCC.Display.OCCViewer import Viewer3d


class TessellatorShape:
    def __init__(self, shape: TopoDS_Shape) -> None:
        bndBox: Bnd_Box = Bnd_Box()
        self.__InitBndBox(bndBox, shape)
        bRepMesh = self.__InitedBRepMesh(bndBox, shape)
        self.Mesh_: Mesh = Mesh()
        self.__InitedMesh(shape)
        self.Mesh_.RandomSampling(1000)
        pass

    def __InitedMesh(self, shape):
        explorer = TopExp_Explorer()

        explorer.Init(shape, TopAbs_FACE)

        while (explorer.More()):
            face = explorer.Current()
            self.__InitMesh(face, self.Mesh_)
            explorer.Next()

    def __InitBndBox(self, bndBox: Bnd_Box, shape: TopoDS_Shape):
        brepbndlib_Add(shape, bndBox)

    def __InitedAngDeflection(self):
        # init basic value
        angDeflection_max, angDeflection_min = 0.8, 0.2
        quality = 5.0

        # calculate angle deflection
        angDeflection_gap = (angDeflection_max - angDeflection_min) / 10
        angDeflection = max(angDeflection_max - (quality *
                                                 angDeflection_gap), angDeflection_min)
        return angDeflection

    def __InitedLinDeflection(self, bndBox: Bnd_Box):
        # calculate linear deflection
        gvec1 = Graphic3d_Vec3d(bndBox.CornerMin().X(),
                                bndBox.CornerMin().Y(), bndBox.CornerMin().Z())
        gvec2 = Graphic3d_Vec3d(bndBox.CornerMax().X(),
                                bndBox.CornerMax().Y(), bndBox.CornerMax().Z())
        deflection = prs3d_GetDeflection(gvec1, gvec2, 0.001)

        linDeflaction = max(deflection, precision_Confusion())

        return linDeflaction

    def __InitedBRepMesh(self, bndBox, shape):
        angDeflection = self.__InitedAngDeflection()
        linDeflaction = self.__InitedLinDeflection(bndBox)
        breptools_Clean(shape)
        bmesh = BRepMesh_IncrementalMesh(
            shape, linDeflaction, False, angDeflection, False)
        return bmesh

    def __InitMesh(self, face, mesh):
        loc = TopLoc_Location()

        poly = BRep_Tool_Triangulation(face, loc)

        nodeNumbers = poly.NbNodes()
        nodes = poly.InternalNodes()

        vertices = []
        for i in range(0, nodeNumbers):
            pnt = nodes.Value(i).Transformed(loc.Transformation())
            vertices.append(pnt)

        mesh.AddVertexPnt(vertices)

        triangles = poly.InternalTriangles()
        indexs = []
        for i in range(triangles.Lower(), triangles.Upper() + 1):
            index = triangles.Value(i).Get()
            indexs.append(index)
        mesh.AddFaceIndex(indexs)


if (__name__ == "__main__"):
    a, b, c, d = init_display()
    x = [gp_Pnt(0, 0, 0), gp_Pnt(1, 1, 1), gp_Pnt(2, 2, 2)]
    pb = PipeBuilder(x, 3)
    tlt = TessellatorShape(pb.PipeShape)

    points = tlt.Mesh_.GetMeshPoints()
    for i in points:
        a.DisplayShape(i)
    a.FitAll()
    b()

    pass
