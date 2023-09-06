import util

from OCC.Core.gp import gp_Pnt, gp_Vec

import math as m
import numpy as np
import random


class Mesh:
    def __init__(self) -> None:
        self.Vertices: list[list[gp_Pnt]] = [[None]]
        self.FaceIndexs = [(None)]
        self.TriArea: np.ndarray = []
        self.SamplingPoints = []
        pass

    def GetMeshPoints(self):
        points = []
        for vertex in self.Vertices:
            if (vertex == None):
                continue
            for i in vertex:
                if (i == None):
                    continue
                points.append(i)

        for point in self.SamplingPoints:
            points.append(point)

        return points

    def AddVertexPnt(self, vertices: list[gp_Pnt]):
        self.Vertices.append(vertices)

    def AddFaceIndex(self, index):
        self.FaceIndexs.append(index)

    def __InitTriangleArea(self):

        for i in range(1, len(self.FaceIndexs)):
            for index in self.FaceIndexs[i]:
                v1 = gp_Vec(self.Vertices[i][index[0] - 1],
                            self.Vertices[i][index[1] - 1])
                v2 = gp_Vec(self.Vertices[i][index[0] - 1],
                            self.Vertices[i][index[2] - 1])
                area = (0.5) * (v1.CrossMagnitude(v2))
                self.TriArea.append(area)

    def RandomSampling(self, num):
        self.__InitTriangleArea()
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

        for i in range(num):
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
            self.SamplingPoints.append(pnt)
