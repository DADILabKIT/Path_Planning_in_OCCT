# for import
from util import sys

# OCC
# for 3D Data
from OCC.Core.gp import gp_Pnt

# for visual
from OCC.Display.OCCViewer import Viewer3d
from OCC.Display.SimpleGui import init_display
from OCC.Core.BRepPrimAPI import BRepPrimAPI_MakeSphere
from OCC.Core.TopoDS import TopoDS_Shape

# Map
from Map.GridMap import GridMap
from Map.Node import Node
from Algoritm.Astar import Astar
from Algoritm.Theta import Theta
from Algoritm.ThetaC import ThetaC
from Algoritm.Jps import Jps
from Algoritm.JpsTheta import JpsTheta


class VisualTest:
    def __init__(self, gridMap: GridMap, display: Viewer3d) -> None:
        self.gridMap: GridMap = gridMap
        self.Display: Viewer3d = display

    def InitRandomMap(self, randomBox: int = 3) -> None:
        self.gridMap.InitNodeMapByRandom(int(randomBox / 2))

    def InitRandomMap2(self, percent: float = 0.4) -> None:
        self.gridMap.InitNodeMapByRandom2(percent)

    def InitInputIntMap(self) -> None:
        self.gridMap.InitNodeMapByIntMap()

    def AstarRun(self, _transparency=0, _color='blue') -> None:
        s = 0
        e = self.gridMap.MapSize - 1
        startNode: Node = self.gridMap.NodeMap[s][s][s]
        endNode: Node = self.gridMap.NodeMap[e][e][e]

        astar = Astar(startNode, endNode, self.gridMap.NodeMap,
                      'astar', self.Display)
        astar.Run()

        astar.DisplayPathBySplinePipe(_transparency, _color)

        self.gridMap.DisplayObstaclesInMap()
        print(astar.CalTime)
        self.gridMap.RecycleNodeMap()

    def AstarPsRun(self, _transparency=0, _color='blue') -> None:
        s = 0
        e = self.gridMap.MapSize - 1
        startNode: Node = self.gridMap.NodeMap[s][s][s]
        endNode: Node = self.gridMap.NodeMap[e][e][e]

        astar = Astar(startNode, endNode, self.gridMap.NodeMap,
                      'astar_ps', self.Display)
        astar.Run()
        astar.PostSmoothing()
        astar.DisplayPathByPipe(_transparency, _color)
        astar.DisplayPathBySplinePipe(_transparency, _color)

        self.gridMap.DisplayObstaclesInMap()

        self.gridMap.RecycleNodeMap()

    def ThetaRun(self, _transparency=0, _color='red') -> None:
        s = 0
        e = self.gridMap.MapSize - 1
        startNode: Node = self.gridMap.NodeMap[s][s][s]
        endNode: Node = self.gridMap.NodeMap[e][e][e]

        theta = Theta(startNode, endNode, self.gridMap.NodeMap,
                      'theta', self.Display)
        theta.Run()
        theta.DisplayPathByPipe(_transparency, _color)
        self.gridMap.DisplayObstaclesInMap()
        print(theta.CalTime)

        self.gridMap.RecycleNodeMap()

    def ThetaCRun(self, _transparency=0, _color='red') -> None:
        s = 0
        e = self.gridMap.MapSize - 1
        startNode: Node = self.gridMap.NodeMap[s][s][s]
        endNode: Node = self.gridMap.NodeMap[e][e][e]

        thetaC = ThetaC(startNode, endNode,
                        self.gridMap.NodeMap, 'theta', self.Display)
        thetaC.Run()
        thetaC.DisplayPathByPipe(_transparency, _color)
        self.gridMap.DisplayObstaclesInMap()
        print(thetaC.CalTime)

        self.gridMap.RecycleNodeMap()

    def JpsRun(self, _transparency=0, _color='red'):
        s = 0
        e = self.gridMap.MapSize - 1
        startNode: Node = self.gridMap.NodeMap[s][s][s]
        endNode: Node = self.gridMap.NodeMap[e][e][e]

        jps = Jps(startNode, endNode, self.gridMap.NodeMap,
                  'jps', self.Display)
        jps.Run()
        print(jps.CalTime)
        jps.DisplayPathBySplinePipe(_transparency, _color)
        self.gridMap.DisplayObstaclesInMap()

        self.gridMap.RecycleNodeMap()

    def JpsPsRun(self, _transparency=0, _color='blue') -> None:
        s = 0
        e = self.gridMap.MapSize - 1
        startNode: Node = self.gridMap.NodeMap[s][s][s]
        endNode: Node = self.gridMap.NodeMap[e][e][e]

        jps = Jps(startNode, endNode, self.gridMap.NodeMap,
                  'jps_ps', self.Display)
        jps.Run()
        jps.PostSmoothing()
        self.gridMap.DisplayObstaclesInMap()

        # jps.DisplayPathByPipe(_transparency, _color="green")
        # 보간 Spline
        #jps.DisplayPathBySplinePipe(_color="black", d=True)
        # Uniform Spline
        jps.DisplayUnifromedSpline(d=True)

        # 충돌 지점과 가까운 지점 가져오기
        # a = self.GetCollapse(jps.PipeShape, jps.PathPoints)
        # if (len(a) != 0):
        #   jps.DisplayUnifromedSpline(idx=a, _color="blue", d=True)

        self.gridMap.RecycleNodeMap()

    def JpsThetaRun(self, _transparency=0, _color='red'):
        s = 0
        e = self.gridMap.MapSize - 1
        startNode: Node = self.gridMap.NodeMap[s][s][s]
        endNode: Node = self.gridMap.NodeMap[e][e][e]

        jps = JpsTheta(startNode, endNode, self.gridMap.NodeMap,
                       'jps_theta', self.Display)
        jps.Run()
        print(jps.CalTime)

        # jps.DisplayPathBySplinePipe2(
        #   _transparency, _color, 5, gap=self.gridMap.Gap)
        jps.DisplayPathBySplinePipe(
            _transparency, "green", 3, gap=self.gridMap.Gap)
        self.gridMap.DisplayObstaclesInMap()
        e_obstacles = []
        # jps.DisplayPathByPipe(gap=self.gridMap.Gap, _color="blue")
        for i in range(self.gridMap.MapSize):
            for j in range(self.gridMap.MapSize):
                for k in range(self.gridMap.MapSize):
                    if (self.gridMap.NodeMap[i][j][k].Obstacle):
                        if (self.gridMap.CheckCollapse(jps.PipeShape, self.gridMap.NodeMap[i][j][k].BoxShape)):
                            self.gridMap.NodeMap[i][j][k].DisplayBoxShape(
                                1, "red")
                            e_obstacles.append(
                                self.gridMap.NodeMap[i][j][k].CenterPoint)
        if (e_obstacles):
            min_pnt = jps.PathPoints[0].CenterPoint.Distance(e_obstacles[0])
            min_idx = 0
            for i in range(1, len(jps.PathPoints)):
                if (min_pnt > jps.PathPoints[i].CenterPoint.Distance(e_obstacles[0])):
                    min_pnt = jps.PathPoints[i].CenterPoint.Distance(
                        e_obstacles[0])
                    min_idx = i
            sp1 = BRepPrimAPI_MakeSphere(
                jps.PathPoints[min_idx].CenterPoint, 10).Shape()
            inPnt1 = self.getCenterPnt(
                jps.PathPoints[min_idx].CenterPoint, jps.PathPoints[min_idx + 1].CenterPoint)
            inPnt2 = self.getCenterPnt(
                jps.PathPoints[min_idx - 1].CenterPoint, jps.PathPoints[min_idx].CenterPoint)
            n1 = Node()
            n2 = Node()
            n1.CenterPoint = inPnt1
            n2.CenterPoint = inPnt2

            jps.PathPoints.insert(min_idx, n2)
            jps.PathPoints.insert(min_idx + 2, n1)

            sp2 = BRepPrimAPI_MakeSphere(
                inPnt2, 10).Shape()
            sp3 = BRepPrimAPI_MakeSphere(
                inPnt1, 10).Shape()
            jps.DisplayPathBySplinePipe(
                _transparency, "red", 3, gap=self.gridMap.Gap, d=True)
            # self.Display.DisplayShape(sp1)
            # self.Display.DisplayShape(sp2, color="red")
            # self.Display.DisplayShape(sp3, color="red")

        self.gridMap.RecycleNodeMap()

        # self.gridMap.NodeMap[e][e][e].DisplayBoxShape(_color='red')
        # self.gridMap.NodeMap[s][s][s].DisplayBoxShape(_color='blue')

    def getCenterPnt(self, g1: gp_Pnt, g2: gp_Pnt):
        Center = gp_Pnt((g1.X() + g2.X()) / 2, (g1.Y() +
                        g2.Y()) / 2, (g1.Z() + g2.Z()) / 2)
        return Center

    def GetCollapse(self, pipeShape: TopoDS_Shape, pathNode: list[Node]):
        e_obstacles = []

        for i in range(self.gridMap.MapSize):
            for j in range(self.gridMap.MapSize):
                for k in range(self.gridMap.MapSize):
                    if (self.gridMap.NodeMap[i][j][k].Obstacle):
                        if (self.gridMap.CheckCollapse(pipeShape, self.gridMap.NodeMap[i][j][k].BoxShape)):
                            self.gridMap.NodeMap[i][j][k].DisplayBoxShape(
                                1, "red")
                            e_obstacles.append(
                                self.gridMap.NodeMap[i][j][k].CenterPoint)

        idxlist = []
        for e in e_obstacles:
            min_pnt = pathNode[0].CenterPoint.Distance(e)
            min_idx = 0
            for i in range(1, len(pathNode)):
                if (min_pnt > pathNode[i].CenterPoint.Distance(e)):
                    min_pnt = pathNode[i].CenterPoint.Distance(e)
                    min_idx = i
            if (min_idx in idxlist):
                continue
            sp1 = BRepPrimAPI_MakeSphere(
                pathNode[min_idx].CenterPoint, 10).Shape()

            inPnt1 = self.getCenterPnt(
                pathNode[min_idx].CenterPoint, pathNode[min_idx + 1].CenterPoint)
            inPnt2 = self.getCenterPnt(
                pathNode[min_idx - 1].CenterPoint, pathNode[min_idx].CenterPoint)
            n1 = Node()
            n2 = Node()
            n1.CenterPoint = inPnt1
            n2.CenterPoint = inPnt2

            pathNode.insert(min_idx, n2)
            pathNode.insert(min_idx + 2, n1)

            sp2 = BRepPrimAPI_MakeSphere(
                inPnt2, 10).Shape()
            sp3 = BRepPrimAPI_MakeSphere(
                inPnt1, 10).Shape()
            # self.Display.DisplayShape(sp2, color="green")
            # self.Display.DisplayShape(sp3, color="green")
            # self.Display.DisplayShape(sp1, color="red")
            for j in range(len(idxlist)):
                if (idxlist[j] > min_idx):
                    idxlist[j] += 2
            idxlist.append(min_idx + 1)

        print(idxlist)
        return idxlist


if (__name__ == '__main__'):
    print("Visaul Test..")
    # display instance
    display, start_display, add_menu, add_menu_function = init_display()

    gridmap = GridMap(gp_Pnt(0, 0, 0), gp_Pnt(1000, 1000, 1000), display, 20)
    gridmap.InitNodeMapByRandom(20)

    vt = VisualTest(gridmap, display)

    # vt.JpsThetaRun()
    # 여기서 수정
    vt.JpsPsRun()

    display.FitAll()

    start_display()
