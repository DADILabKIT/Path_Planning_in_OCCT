import util
import random
from random import randint

from OCC.Core.gp import gp_Pnt
from OCC.Display.SimpleGui import init_display

from Node import Node


class RandomBoxGenerator:
    def __init__(self, start: int, end: int, boxNumber: int = 3) -> None:
        random.seed(21)#43, 21이 복잡
        self.BoxNumber = boxNumber
        self.Start = start
        self.End = end - 1
        self.RandBox: list[tuple] = self.__InitedRomdomBox()
        

    def __InitedRomdomBox(self):
        result = []
        for _ in range(self.BoxNumber * 2):
            x = randint(self.Start + 1, self.End - 2)
            y = randint(self.Start + 1, self.End - 2)
            z = randint(self.Start + 1, self.End - 2)
            result.append((x, y, z))
        result.sort()
        return result

    def Run(self, nodeMap: list[list[list[Node]]]) -> None:
        for i in range(0, len(self.RandBox) - 1, 2):
            s1, t1 = min(self.RandBox[i][0], self.RandBox[i + 1][0]), max(
                self.RandBox[i][0], self.RandBox[i + 1][0]) + 1
            for x in range(s1, t1):
                s2, t2 = min(self.RandBox[i][1], self.RandBox[i + 1][1]), max(
                    self.RandBox[i][1], self.RandBox[i + 1][1]) + 1
                for y in range(s2, t2):
                    s3, t3 = min(self.RandBox[i][2], self.RandBox[i + 1][2]), max(
                        self.RandBox[i][2], self.RandBox[i + 1][2]) + 1
                    for z in range(s3, t3):
                        nodeMap[x][y][z].Obstacle = True


if (__name__ == "__main__"):
    pass
