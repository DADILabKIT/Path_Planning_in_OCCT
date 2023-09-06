from Map.Node import Node
from OCC.Core.gp import gp_Pnt
from OCC.Display.SimpleGui import init_display


def facto(n):
    if (n == 1):
        return 1
    d = [1 for _ in range(1000000)]
    for i in range(2, n):
        d[i] = d[i - 1] * i
    return d[n - 1]


def combi(n, r):
    if (r == 1):
        return n
    return ((facto(n)) / (facto(r) * facto(n - r)))


def selc(n):
    if (n == 0):
        return 0
    return selc(n - 1) + combi(9, n) * 2


def NodeSortByDis(nodeList: list[Node], src: Node):
    for i in range(len(nodeList) - 1):
        min_idx = i
        for j in range(i + 1, len(nodeList)):
            if (CheckDis(nodeList[min_idx], nodeList[j], src)):
                min_idx = j
        nodeList[i], nodeList[min_idx] = nodeList[min_idx], nodeList[i]


def CheckDis(n1: Node, n2: Node, src: Node):
    return (n1.CenterPoint.Distance(src.CenterPoint) > n2.CenterPoint.Distance(src.CenterPoint))


print(combi(26 * 4, 4))
