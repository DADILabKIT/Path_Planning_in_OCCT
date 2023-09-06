import util

from time import time
import heapq

from OCC.Core.gp import gp_Pnt
from OCC.Core.Quantity import (
    Quantity_Color,
    Quantity_TOC_RGB,
    Quantity_NOC_WHITE
)

from OCC.Display.SimpleGui import init_display

from Agent import Agent
from LineBuilder.SplineBuilder import SplineBuilder, SplineBuilderExtended
from GridsMap.GridsMap import GridsMap
from GridsMap.Node import Node
from SplineOptimizer.BruteForce import BruteForce
from SplineOptimizer.BackTracking import BackTracking
from CurvatureReducer import CurvatureReducer

from OCC.Core.GeomAPI import GeomAPI_ProjectPointOnCurve
from OCC.Core.BRepPrimAPI import BRepPrimAPI_MakeSphere

class Astar(Agent):
    def __init__(self, name: str = "agent") -> None:
        super().__init__(name)

    def Run(self, src: Node, dst: Node, nodeMap: list[list[list[Node]]]) -> None:
        startTime: float = time()
        openList: list[Node] = []
        closedList: set[Node] = set()

        src.Parent = src
        heapq.heappush(openList, src)

        while (openList):
            curNode: Node = heapq.heappop(openList)
            closedList.add(curNode)

            if (curNode == dst):
                self.CalTime = startTime
                self._InitPathNodeList(src, dst)
                return

            for i in range(-1, 2):
                for j in range(-1, 2):
                    for k in range(-1, 2):
                        if (i == 0 and j == 0 and k == 0):
                            continue
                        nx: int = i + curNode.I
                        ny: int = j + curNode.J
                        nz: int = k + curNode.K

                        if (self._IsOutOfRange(nx, ny, nz, len(nodeMap))):
                            continue

                        nextNode: Node = nodeMap[nx][ny][nz]
                        if (self._IsObstacle(nextNode) or nextNode in closedList):
                            continue

                        cost: float = (
                            max(-i, i) + max(-j, j) + max(-k, k)) ** 0.5
                        ng: float = curNode.G + cost

                        if (nextNode.Parent == None or ng < nextNode.G):
                            nextNode.G = ng
                            nextNode.F = self._CalEuclidDistance(
                                nextNode, dst) + ng
                            nextNode.Parent = curNode

                            heapq.heappush(openList, nextNode)


if (__name__ == "__main__"):

    a, b, c, d = init_display()
    a.View.SetBackgroundColor(Quantity_TOC_RGB, 0, 0, 0)
    a.hide_triedron()

    a.View.SetBgGradientColors(
        Quantity_Color(Quantity_NOC_WHITE),
        Quantity_Color(Quantity_NOC_WHITE),
        2,
        True,
    )

    grids = GridsMap(gp_Pnt(0, 0, 0), gp_Pnt(1000, 1000, 1000), 10)
    grids.InitRandomBoxObstacle(10)
    grids.DisplayGridsMapInObstacle(a, _color="black", _transparency=0)

    start = grids.NodeMap[0][0][0]
    end = grids.NodeMap[9][9][9]

    astar = Astar("astar")
    astar.Run(start, end, grids.NodeMap)
    astar._PostSmoothing(start, end, grids.NodeMap)
    diameter = 3
    sb = SplineBuilder(astar.GetPathPoints(), diameter)
    sb.DisplaySplineShape(a, _color="black")

    # 여기서, sb의 Spline의 curve에 접근해서 곡률을 계산하고, 곡률이 클 때 점을 보간하여 곡률을 완화.
    min_bend_rad = 3 * 6 # 통상적으로 직경의 6~8배의 최소 곡률 반경을 가짐.
    threshold = 0.01  # 임의의 임계치 값
    #threshold = 1 / min_bend_rad # 사용해야할 임계치 값

    sb_extended = SplineBuilderExtended(astar.GetPathPoints(), diameter)
    
    # Create an instance of CurvatureReducer and reduce the curvature
    curvature_reducer = CurvatureReducer(sb_extended, threshold)
    curvature_reducer.reduce_curvature()

    # You can retrieve the updated path points if needed
    path_points = curvature_reducer.get_updated_path_points()
            
    # Update node center points
    for node, point in zip(astar.PathNodeList, path_points):
        node.CenterPoint = point
        sphere = BRepPrimAPI_MakeSphere(point, 10).Shape()  # 반지름 10인 구 생성
        a.DisplayShape(sphere, color='red')

    # Recreate the spline with the modified path points
    sb = SplineBuilderExtended(path_points, 3)
    sb.DisplaySplineShape(a, _color="blue")
    
    print("Collision!!")
    bf = BackTracking(start, end, astar.PathNodeList,
                        sb.SplineShape, grids, 2)
    bf.Run()
    if (bf.NewSpline):
        bf.InitCandidateSplinePath()

        # bf.PathNodeList에서 gp_Pnt 추출
        extracted_points = [node.CenterPoint for node in bf.PathNodeList]

        # 최소 굽힘 반경에 따른 보간점 추가 적용 (for the new spline)
        sb_extended_new = SplineBuilderExtended(extracted_points, diameter)
        curvature_reducer_new = CurvatureReducer(sb_extended_new, threshold)
        curvature_reducer_new.reduce_curvature()
        updated_path_points = curvature_reducer_new.get_updated_path_points()

        # Update node center points (for the new spline)
        for node, point in zip(bf.PathNodeList, updated_path_points):  # Using bf.PathNodeList here
            node.CenterPoint = point
            sphere = BRepPrimAPI_MakeSphere(point, 10).Shape()  # 반지름 10인 구 생성
            a.DisplayShape(sphere, color='red')

        # Recreate the spline with the updated path points (for the new spline)
        sb_new = SplineBuilderExtended(updated_path_points, 3)
        sb_new.DisplaySplineShape(a, _color="blue")
        
        a.DisplayShape(bf.CandidateSplineList[0][0], color="green")
        # bf.DisplayAdditivePoints(a)
    else:
        print("Not Collision")

    # astar.DisplayPathNodeListByPipe(a, _color="green", diameter=1.5)
    # astar.DisplayPathNodeListBySpline(a, _color="red", diameter=1.5)
    a.FitAll()
    b()
    pass
