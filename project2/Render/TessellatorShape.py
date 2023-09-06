# Cumtom
from Render.Mesh import Mesh

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

from OCC.Display.OCCViewer import Viewer3d




class TessellatorShape:
    def __init__(self, shape: TopoDS_Shape, display: Viewer3d) -> None:
        self.cnt = 0
        self.Display = display
        self.mesh = Mesh(display)
        self.Shape: TopoDS_Shape = shape
        self.BndBox: Bnd_Box = Bnd_Box()
        self.InitBndBox(self.BndBox, shape)
        self.angDeflection = self.InitAngDeflection()
        self.linDeflection = self.InitLinDeflection(self.BndBox)
        self.BRepMesh = self.InitBRepMesh(
            shape, self.angDeflection, self.linDeflection)
        self.GetVertexPnt()

    def GetVertexPnt(self):
        explorer = TopExp_Explorer()

        explorer.Init(self.Shape, TopAbs_FACE)

        if (self.BRepMesh.IsDone()):
            print("Mesh making is done")

        while (explorer.More()):
            face = explorer.Current()
            self.InitMesh(face, self.mesh, self.cnt)

            # self.Display.DisplayShape(face)

            explorer.Next()

    @staticmethod
    def InitBndBox(bndBox: Bnd_Box, shape: TopoDS_Shape):
        brepbndlib_Add(shape, bndBox)

    @staticmethod
    def InitAngDeflection():
        # init basic value
        angDeflection_max, angDeflection_min = 0.8, 0.2
        quality = 5.0

        # calculate angle deflection
        angDeflection_gap = (angDeflection_max - angDeflection_min) / 10
        angDeflection = max(angDeflection_max - (quality *
                                                 angDeflection_gap), angDeflection_min)
        return angDeflection

    @staticmethod
    def InitLinDeflection(bndBox: Bnd_Box):
        # calculate linear deflection
        gvec1 = Graphic3d_Vec3d(bndBox.CornerMin().X(),
                                bndBox.CornerMin().Y(), bndBox.CornerMin().Z())
        gvec2 = Graphic3d_Vec3d(bndBox.CornerMax().X(),
                                bndBox.CornerMax().Y(), bndBox.CornerMax().Z())
        deflection = prs3d_GetDeflection(gvec1, gvec2, 0.001)

        linDeflaction = max(deflection, precision_Confusion())

        return linDeflaction

    @staticmethod
    def InitBRepMesh(shape: TopoDS_Shape, angDeflection, linDeflaction):
        breptools_Clean(shape)
        bmesh = BRepMesh_IncrementalMesh(
            shape, linDeflaction, False, angDeflection, False)
        return bmesh

    @staticmethod
    def InitMesh(face, mesh, cnt):
        cnt += 1
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
