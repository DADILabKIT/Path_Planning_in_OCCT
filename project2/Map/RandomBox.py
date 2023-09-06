from random import randint
import numpy as np


class RandomBoxGenerator:
    def __init__(self, boxNumber: int, startIndex: int, endIndex, seed) -> None:
        self.BoxNumber = boxNumber
        self.StartIndex = startIndex
        self.EndIndex = endIndex
        self.RandBox: list[tuple] = []
        self.InitRomdomBox(seed)

    def InitRomdomBox(self,seed):
        if seed:
            np.random.seed(42)
        result = []
        for i in range(self.BoxNumber * 2):
            x = randint(self.StartIndex + 1, self.EndIndex - 2)
            y = randint(self.StartIndex + 1, self.EndIndex - 2)
            z = randint(self.StartIndex + 1, self.EndIndex - 2)
            result.append((x, y, z))
        result.sort()
        self.RandBox = result
