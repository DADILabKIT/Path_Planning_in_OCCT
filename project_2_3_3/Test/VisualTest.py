# for import
from util import sys

# OCC
# for 3D Data
from Algoritm.Agent import Agent
from OCC.Core.gp import gp_Pnt
from OCC.Core.Quantity import (
    Quantity_Color,
    Quantity_TOC_RGB,
    Quantity_NOC_WHITE
)
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
        self.d = True
        self.N = 0

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
        jps.DisplayPathBySplinePipe(_color="black", d=True)
        ret = self.GetCollapse(jps.PipeShape)
        n_ = len(ret)
        print(n_)
        vl: list[Node] = []
        for i in ret:
            tmp = self.InitCollapseArea(i.x, i.y, i.z)
            for t in tmp:
                vl.append(t)
        rl: list[Node] = []
        print(len(vl))
        self.NodeSortByDis(vl)
        if len(vl) >= 2:
            self.dfs(-1, vl, rl, jps, n_)
        #Uniform Spline
        #jps.DisplayUnifromedSpline(d=True)

        for i in jps.PathPoints:
            s1 = BRepPrimAPI_MakeSphere(i.CenterPoint, 10).Shape()
            self.gridMap.Display.DisplayShape(s1)

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
        e_obstacles: list[Node] = []
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

    def GetCollapse(self, pipeShape: TopoDS_Shape):
        e_obstacles = []
        self.gridMap.InitTlt(pipeShape)
        for i in range(self.gridMap.MapSize):
            for j in range(self.gridMap.MapSize):
                for k in range(self.gridMap.MapSize):
                    if (self.gridMap.NodeMap[i][j][k].Obstacle):
                        if (self.gridMap.CheckCollapse(self.gridMap.NodeMap[i][j][k].BoxShape)):
                            self.gridMap.NodeMap[i][j][k].DisplayBoxShape(
                                1, "red")
                            e_obstacles.append(
                                self.gridMap.NodeMap[i][j][k])

        return e_obstacles

    def InitCollapseArea(self, x, y, z):
        dx = [-1, 1, 0, 0, 0, 0, -1, -1, 1, 1, -
              1, -1, 1, 1, -1, -1, 1, 1, 0, 0, 0, 0, -1, 1, -1, 1]
        dy = [0, 0, -1, 1, 0, 0, -1, 1, -1, 1, -1,
              1, -1, 1, -1, 1, -1, 1, -1, 1, -1, 1, 0, 0, 0, 0]
        dz = [0, 0, 0, 0, 1, -1, 1, 1, 1, 1, -
              1, -1, -1, -1, 0, 0, 0, 0, -1, -1, 1, 1, 1, 1, -1, -1]
        ret = []
        for i in range(len(dx)):
            nx = dx[i] + x
            ny = dy[i] + y
            nz = dz[i] + z

            if (nx >= self.gridMap.MapSize or ny >= self.gridMap.MapSize or ny >= self.gridMap.MapSize or nx < 0 or ny < 0 or nz < 0):
                continue
            if (self.gridMap.NodeMap[nx][ny][nz].Obstacle == False):
                ret.append(self.gridMap.NodeMap[nx][ny][nz])
        return ret

    def dfs(self, n_, vl_: list[Node], rl_: list[Node], jps: Agent, re):
        if (len(rl_) == re + 1 or self.d == False):
            return

        if (len(rl_) >= 1):
            for i in rl_:
                if (i in jps.PathPoints):
                    continue
                jps.PathPoints.append(i)
            self.NodeSortByDis(jps.PathPoints)
            jps.DisplayPathBySplinePipe(_color="red", d=False)
            cl = self.GetCollapse(jps.PipeShape)
            print(len(cl), len(rl_))
            if (len(cl) == 0):
                jps.DisplayPathBySplinePipe(_color="red", d=True)
                for i in rl_:
                    ll = BRepPrimAPI_MakeSphere(i.CenterPoint, 20).Shape()
                    print(i.CenterPoint.X(), i.CenterPoint.Y(), i.CenterPoint.Z(),"i")
                    self.Display.DisplayShape(ll, color="blue")
                # self.d = False
                print("done")
                # self.N += 1
                # if (self.N == 8):
                self.d = False
                return
            for i in rl_:
                if (i in jps.PathPoints):
                    jps.PathPoints.remove(i)
            print("next")

        for i in range(n_ + 1, len(vl_)):
            if (rl_):
                if (not jps.LineOfSight3D(rl_[-1], vl_[i])):
                    print("pruning")
                    continue
                if (not jps.LineOfSight3D(self.GetNextNode(vl_[i], jps), vl_[i])):
                    print("pruning")
                    continue
                rl_.append(vl_[i])

                self.dfs(i, vl_, rl_, jps, re)
                if (self.d == False):
                    return
                rl_.pop()
            else:
                if (not jps.LineOfSight3D(self.GetNextNode(vl_[i], jps), vl_[i])):
                    print("pruning")
                    continue
                rl_.append(vl_[i])
                self.dfs(i, vl_, rl_, jps, re)
                if (self.d == False):
                    return
                rl_.pop()

        return

    def GetNextNode(self, src: Node, jps: Agent):
        for i in jps.PathPoints:
            if (src.CenterPoint.Distance(self.gridMap.NodeMap[0][0][0].CenterPoint) < i.CenterPoint.Distance(self.gridMap.NodeMap[0][0][0].CenterPoint)):
                return i

    def NodeSortByDis(self, nodeList: list[Node]):
        for i in range(len(nodeList) - 1):
            min_idx = i
            for j in range(i + 1, len(nodeList)):
                if (self.CheckDis(nodeList[min_idx], nodeList[j], self.gridMap.NodeMap[0][0][0])):
                    min_idx = j
            nodeList[i], nodeList[min_idx] = nodeList[min_idx], nodeList[i]
        pass

    def CheckDis(self, n1: Node, n2: Node, src: Node):
        return (n1.CenterPoint.Distance(src.CenterPoint) > n2.CenterPoint.Distance(src.CenterPoint))


if (__name__ == '__main__'):
    print("Visaul Test..")

    # display instance
    display, start_display, add_menu, add_menu_function = init_display()
    display.View.SetBackgroundColor(Quantity_TOC_RGB, 0, 0, 0)
    display.hide_triedron()

    display.View.SetBgGradientColors(
        Quantity_Color(Quantity_NOC_WHITE),
        Quantity_Color(Quantity_NOC_WHITE),
        2,
        True,
    )
    gridmap = GridMap(gp_Pnt(0, 0, 0), gp_Pnt(1000, 1000, 1000), display, 10)
    gridmap.InitNodeMapByRandom(10)

    vt = VisualTest(gridmap, display)

    # vt.JpsThetaRun()
    # 여기서 수정
    vt.JpsPsRun()

    display.FitAll()

    start_display()
