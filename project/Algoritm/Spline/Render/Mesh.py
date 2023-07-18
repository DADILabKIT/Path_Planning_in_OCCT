from OCC.Core.BRepBuilderAPI import BRepBuilderAPI_MakeEdge

from OCC.Core.gp import gp_Pnt, gp_Vec

from OCC.Core.TopoDS import TopoDS_Face, TopoDS_Edge
from OCC.Core.TopExp import TopExp_Explorer
from OCC.Core.TopAbs import TopAbs_EDGE

from OCC.Display.OCCViewer import Viewer3d

import math as m
import numpy as np
import random


class Mesh:
    def __init__(self, display: Viewer3d) -> None:
        self.Vertices: list[list[gp_Pnt]] = [[None]]
        self.Display: Viewer3d = display
        self.FaceIndexs = [(None)]
        self.TriArea: np.ndarray = []
        self.Points = []
        pass

    def GetPoints(self):
        vertices = []
        for vertex in self.Vertices:
            if (vertex == None):
                continue
            for i in vertex:
                if (i == None):
                    continue
                vertices.append(i)

        for point in self.Points:
            vertices.append(point)

        return vertices

    def AddVertexPnt(self, vertices):
        self.Vertices.append(vertices)

    def AddFaceIndex(self, index):
        self.FaceIndexs.append(index)

    def GetTriangleArea(self):
        cnt = 0
        for i in range(1, len(self.FaceIndexs)):
            for index in self.FaceIndexs[i]:
                v1 = gp_Vec(self.Vertices[i][index[0] - 1],
                            self.Vertices[i][index[1] - 1])
                v2 = gp_Vec(self.Vertices[i][index[0] - 1],
                            self.Vertices[i][index[2] - 1])
                area = (0.5) * (v1.CrossMagnitude(v2))
                self.TriArea.append(area)
                cnt += 1

        pass

    def RandomSampling(self, pntNumber: int):
        self.GetTriangleArea()
        self.TriArea = np.asarray(self.TriArea)

        cumSumArea = np.cumsum(self.TriArea)
        totalArea = cumSumArea[-1]

        triList = []
        verList = []

        for i in range(1, len(self.FaceIndexs)):
            b = []
            for index in self.FaceIndexs[i]:
                triList.append(index)
                b.append(self.Vertices[i][index[0] - 1])
                b.append(self.Vertices[i][index[1] - 1])
                b.append(self.Vertices[i][index[2] - 1])
                verList.append(b)
                b = []

        cnt = [0 for _ in range(len(triList))]

        for i in range(pntNumber):
            randomArea = random.uniform(0, totalArea)

            triIndex = np.searchsorted(cumSumArea, randomArea)

            cnt[triIndex] += 1
            A = gp_Vec(verList[triIndex][0].XYZ())
            B = gp_Vec(verList[triIndex][1].XYZ())
            C = gp_Vec(verList[triIndex][2].XYZ())

            r1 = random.random()
            r2 = random.random()

            A.Multiply(1 - m.sqrt(r1))
            B.Multiply(m.sqrt(r1) * (1 - r2))
            C.Multiply((m.sqrt(r1)) * r2)

            pnt = A + B + C
            pnt = gp_Pnt(pnt.XYZ())
            self.Points.append(pnt)

    def DisplayEdges(self):
        for i in range(1, len(self.FaceIndexs)):
            for index in self.FaceIndexs[i]:

                e1 = BRepBuilderAPI_MakeEdge(
                    self.Vertices[i][index[0] - 1], self.Vertices[i][index[1] - 1])

                e2 = BRepBuilderAPI_MakeEdge(
                    self.Vertices[i][index[1] - 1], self.Vertices[i][index[2] - 1])

                e3 = BRepBuilderAPI_MakeEdge(
                    self.Vertices[i][index[2] - 1], self.Vertices[i][index[0] - 1])

                if (e1.IsDone()):
                    self.Display.DisplayShape(e1.Shape())

                if (e2.IsDone()):
                    self.Display.DisplayShape(e2.Shape())

                if (e3.IsDone()):
                    self.Display.DisplayShape(e3.Shape())

    def DisplayVertices(self):
        for vertex in self.Vertices:
            if (vertex == None):
                continue
            for i in vertex:
                if (i == None):
                    continue
                self.Display.DisplayShape(i)

    def DisplayPoints(self):
        for pnt in self.Points:
            self.Display.DisplayShape(pnt)
