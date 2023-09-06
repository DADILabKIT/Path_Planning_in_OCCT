import random
from random import randint


class RandomBoxGenerator:
    def __init__(self, boxNumber: int, startIndex: int, endIndex) -> None:
        self.BoxNumber = boxNumber
        self.StartIndex = startIndex
        self.EndIndex = endIndex
        self.RandBox: list[tuple] = []
        self.InitRomdomBox()

    def InitRomdomBox(self):
        random.seed(69)
        result = []
        for i in range(self.BoxNumber * 2):
            x = randint(self.StartIndex + 1, self.EndIndex - 2)
            y = randint(self.StartIndex + 1, self.EndIndex - 2)
            z = randint(self.StartIndex + 1, self.EndIndex - 2)
            result.append((x, y, z))
        result.sort()
        self.RandBox = result
