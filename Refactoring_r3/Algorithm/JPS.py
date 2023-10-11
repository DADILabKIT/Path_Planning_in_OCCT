import heapq
from time import time

from Agent import Agent
from GridsMap.Node import Node

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
from Algorithm.Routing import NodeSeacher

from OCC.Core.GeomAPI import GeomAPI_ProjectPointOnCurve
from OCC.Core.BRepPrimAPI import BRepPrimAPI_MakeSphere

IsEnd: bool = False
openList: list[Node] = []
closedList: set[Node] = set()
nodeMap = None


def SearchJumpPointDiagonal3D(src: Node, dx: int, dy: int, dz: int, dst: Node, nodeMap: list[list[list[Node]]]):
    global IsEnd
    if (src in closedList or IsEnd is True):
        return True
    x, y, z = src.I, src.J, src.K
    n = len(nodeMap)
    if (dz == 1):
        for i in range(2):
            if ((not _IsOutOfRange(x - dx, y + dy, z + i + 1, n)) and
                    nodeMap[x - dx][y + dy][z + i].Obstacle and
                    (not nodeMap[x - dx][y + dy][z + i + 1].Obstacle)):
                src.F = src.G + _CalEuclidDistance(src, dst)
                if (src in openList):
                    openList.remove(src)
                heapq.heappush(openList, src)
                return True

            if ((not _IsOutOfRange(x + dx, y - dy, z + i + 1, n)) and
                    nodeMap[x + dx][y - dy][z + i + 1].Obstacle and
                    (not nodeMap[x + dx][y - dy][z + i + 1].Obstacle)):
                src.F = src.G + _CalEuclidDistance(src, dst)
                if (src in openList):
                    openList.remove(src)
                heapq.heappush(openList, src)
                return True

        ExploreOrthogonal(src, dx, 0, 0, dst,  nodeMap)
        ExploreOrthogonal(src, 0, dy, 0, dst,  nodeMap)
        ExploreOrthogonal(src, 0, 0, dz, dst,  nodeMap)
        ExploreDiagonal2D(src, dx, dy, 0, dst, nodeMap)
        ExploreDiagonal2D(src, 0, dy, dz, dst,  nodeMap)
        ExploreDiagonal2D(src, dx, 0, dz, dst,  nodeMap)

        return False

    if (dz == -1):
        for i in range(0, -2, -1):
            if ((not _IsOutOfRange(x - dx, y + dy, z + i - 1, n)) and
                    nodeMap[x - dx][y + dy][z + i].Obstacle and
                    (not nodeMap[x - dx][y + dy][z + i - 1].Obstacle)):
                src.F = src.G + _CalEuclidDistance(src, dst)
                if (src in openList):
                    openList.remove(src)
                heapq.heappush(openList, src)
                return True

            if ((not _IsOutOfRange(x + dx, y - dy, z + i - 1, n)) and
                    nodeMap[x + dx][y - dy][z + i].Obstacle and
                    (not nodeMap[x + dx][y - dy][z + i - 1].Obstacle)):
                src.F = src.G + _CalEuclidDistance(src, dst)
                if (src in openList):
                    openList.remove(src)
                heapq.heappush(openList, src)
                return True

        ExploreOrthogonal(src, dx, 0, 0, dst,  nodeMap)
        ExploreOrthogonal(src, 0, dy, 0, dst,  nodeMap)
        ExploreOrthogonal(src, 0, 0, dz, dst,  nodeMap)
        ExploreDiagonal2D(src, dx, dy, 0, dst, nodeMap)
        ExploreDiagonal2D(src, 0, dy, dz, dst, nodeMap)
        ExploreDiagonal2D(src, dx, 0, dz, dst, nodeMap)

        return False


def SearchJumpPointDiagonal2D(src: Node, dx: int, dy: int, dz: int, dst: Node, nodeMap: list[list[list[Node]]]):
    global IsEnd
    if (src in closedList or IsEnd is True):
        return True
    x, y, z = src.I, src.J, src.K
    n = len(nodeMap)

    if (dz == 0):
        if (not _IsOutOfRange(x + dx, y, z, n) and nodeMap[x + dx][y][z].Obstacle):
            for i in range(-1, 2):
                if (i == 0):
                    continue
                if (not _IsOutOfRange(x + dx, y, z + i, n) and not nodeMap[x + dx][y][z + i].Obstacle):
                    src.F = src.G + _CalEuclidDistance(src, dst)
                    if (src in openList):
                        openList.remove(src)
                    heapq.heappush(openList, src)
                    return True

        if (not _IsOutOfRange(x, y + dy, z, n) and nodeMap[x][y + dy][z].Obstacle):
            for i in range(-1, 2):
                if (i == 0):
                    continue
                if (not _IsOutOfRange(x, y + dy, z + i, n) and not nodeMap[x][y + dy][z + i].Obstacle):
                    src.F = src.G + _CalEuclidDistance(src, dst)
                    if (src in openList):
                        openList.remove(src)
                    heapq.heappush(openList, src)
                    return True

        ExploreOrthogonal(src, dx, 0, 0, dst, nodeMap)
        ExploreOrthogonal(src, 0, dy, 0, dst, nodeMap)

        return False

    if (dx == 0):
        if (not _IsOutOfRange(x, y, z + dz, n) and nodeMap[x][y][z + dz].Obstacle):
            for i in range(-1, 2):
                if (i == 0):
                    continue
                if (not _IsOutOfRange(x + i, y, z + dz, n) and not nodeMap[x + i][y][z + dz].Obstacle):
                    src.F = src.G + _CalEuclidDistance(src, dst)
                    if (src in openList):
                        openList.remove(src)
                    heapq.heappush(openList, src)
                    return True

        if (not _IsOutOfRange(x, y + dy, z, n) and nodeMap[x][y + dy][z].Obstacle):
            for i in range(-1, 2):
                if (i == 0):
                    continue
                if (not _IsOutOfRange(x + i, y + dy, z, n) and not nodeMap[x + i][y + dy][z].Obstacle):
                    src.F = src.G + _CalEuclidDistance(src, dst)
                    if (src in openList):
                        openList.remove(src)
                    heapq.heappush(openList, src)
                    return True

        ExploreOrthogonal(src, 0, 0, dz, dst, nodeMap)
        ExploreOrthogonal(src, 0, dy, 0, dst, nodeMap)
        return False

    if (dy == 0):
        if (not _IsOutOfRange(x, y, z + dz, n) and nodeMap[x][y][z + dz].Obstacle):
            for i in range(-1, 2):
                if (i == 0):
                    continue
                if (not _IsOutOfRange(x, y + i, z + dz, n) and not nodeMap[x][y + i][z + dz].Obstacle):
                    src.F = src.G + _CalEuclidDistance(src, dst)
                    if (src in openList):
                        openList.remove(src)
                    heapq.heappush(openList, src)
                    return True

        if (not _IsOutOfRange(x + dx, y, z, n) and nodeMap[x + dx][y][z].Obstacle):
            for i in range(-1, 2):
                if (i == 0):
                    continue
                if (not _IsOutOfRange(x + dx, y + i, z + dz, n) and not nodeMap[x + dx][y + i][z].Obstacle):
                    src.F = src.G + _CalEuclidDistance(src, dst)
                    if (src in openList):
                        openList.remove(src)
                    heapq.heappush(openList, src)
                    return True

        ExploreOrthogonal(src, 0, 0, dz, dst, nodeMap)
        ExploreOrthogonal(src, dx, 0, 0, dst, nodeMap)

        return False


def SearchJumpPointOrthogonal(src: Node, dx: int, dy: int, dz: int, dst: Node, nodeMap: list[list[list[Node]]]):
    global IsEnd
    if (src in closedList or IsEnd is True):
        return True
    x, y, z = src.I, src.J, src.K
    n = len(nodeMap)

    if (dx):
        for i in range(-1, 2):
            if ((not _IsOutOfRange(x + dx, y + 1, z + i, n)) and
                    nodeMap[x][y + 1][z + i].Obstacle and
                    (not nodeMap[x + dx][y + 1][z + i].Obstacle)):
                src.F = src.G + _CalEuclidDistance(src, dst)
                if (src in openList):
                    openList.remove(src)
                heapq.heappush(openList, src)
                return True
            if ((not _IsOutOfRange(x + dx, y - 1, z + i, n)) and
                    nodeMap[x][y - 1][z + i].Obstacle and
                    (not nodeMap[x + dx][y - 1][z + i].Obstacle)):
                src.F = src.G + _CalEuclidDistance(src, dst)
                if (src in openList):
                    openList.remove(src)
                heapq.heappush(openList, src)
                return True
        return False

    if (dy):
        for i in range(-1, 2):
            if ((not _IsOutOfRange(x + 1, y + dy, z + i, n)) and
                    nodeMap[x + 1][y][z + i].Obstacle and
                    (not nodeMap[x + 1][y + dy][z + i].Obstacle)):
                src.F = src.G + _CalEuclidDistance(src, dst)
                if (src in openList):
                    openList.remove(src)
                heapq.heappush(openList, src)
                return True
            if ((not _IsOutOfRange(x - 1, y + dy, z + i, n)) and
                    nodeMap[x - 1][y][z + i].Obstacle and
                    (not nodeMap[x - 1][y + dy][z + i].Obstacle)):
                src.F = src.G + _CalEuclidDistance(src, dst)
                if (src in openList):
                    openList.remove(src)
                heapq.heappush(openList, src)
                return True
        return False

    if (dz):
        for i in range(-1, 2):
            if ((not _IsOutOfRange(x + 1, y + i, z + dz, n)) and
                    nodeMap[x + 1][y + i][z].Obstacle and
                    (not nodeMap[x + 1][y + i][z + dz].Obstacle)):
                src.F = src.G + _CalEuclidDistance(src, dst)
                heapq.heappush(openList, src)
                return True
            if ((not _IsOutOfRange(x - 1, y + i, z + dz, n)) and
                    nodeMap[x - 1][y + i][z].Obstacle and
                    (not nodeMap[x - 1][y + i][z + dz].Obstacle)):
                src.F = src.G + _CalEuclidDistance(src, dst)
                if (src in openList):
                    openList.remove(src)
                heapq.heappush(openList, src)
                return True
        return False


def _IsOutOfRange(i: int, j: int, k: int, mapSize: int) -> bool:
    return i >= mapSize or j >= mapSize or k >= mapSize or i < 0 or j < 0 or k < 0


def _CalEuclidDistance(src: Node, dst: Node) -> float:
    return src.CenterPoint.Distance(dst.CenterPoint)


def ExploreDiagonal3D(src: Node, dx: int, dy: int, dz: int, dst: Node, nodeMap: list[list[list[Node]]]):
    global IsEnd
    if (IsEnd is True or src.Obstacle):
        return

    parNode: Node = src
    n = len(nodeMap)
    if (src == dst):
        IsEnd = True
        return
    g = src.G
    x, y, z = src.I, src.J, src.K
    while (IsEnd is False):
        nx: int = dx + x
        ny: int = dy + y
        nz: int = dz + z
        x, y, z = nx, ny, nz
        ng: float = g + (3) ** 0.5
        g = ng

        if (_IsOutOfRange(nx, ny, nz, n) or nodeMap[nx][ny][nz].Obstacle or nodeMap[nx][ny][nz].G != 0.0):
            return
        nodeMap[nx][ny][nz].Parent = parNode
        nodeMap[nx][ny][nz].G = ng

        if (nodeMap[nx][ny][nz] == dst):
            IsEnd = True
            return

        if (SearchJumpPointDiagonal3D(nodeMap[nx][ny][nz], dx, dy, dz, dst, nodeMap)):
            return

    return


def ExploreDiagonal2D(src: Node, dx: int, dy: int, dz: int, dst: Node,  nodeMap: list[list[list[Node]]]):
    global IsEnd
    if (IsEnd is True or src.Obstacle):
        return

    parNode: Node = src
    if (src == dst):
        IsEnd = True
        return
    n = len(nodeMap)
    g = src.G
    x, y, z = src.I, src.J, src.K
    while (IsEnd is False):
        nx: int = dx + x
        ny: int = dy + y
        nz: int = dz + z
        x, y, z = nx, ny, nz
        ng: float = g + (2) ** 0.5
        g = ng

        if (_IsOutOfRange(nx, ny, nz, n) or nodeMap[nx][ny][nz].Obstacle or nodeMap[nx][ny][nz].G != 0.0):
            return

        nodeMap[nx][ny][nz].Parent = parNode
        nodeMap[nx][ny][nz].G = ng

        if (nodeMap[nx][ny][nz] == dst):
            IsEnd = True
            return

        if (SearchJumpPointDiagonal2D(nodeMap[nx][ny][nz], dx, dy, dz, dst, nodeMap)):
            return

    return


def ExploreOrthogonal(src: Node, dx: int, dy: int, dz: int, dst: Node, nodeMap: list[list[list[Node]]]):
    global IsEnd
    if (IsEnd == True or src.Obstacle):
        return None
    parNode: Node = src
    x, y, z = src.I, src.J, src.K

    if (src == dst):
        IsEnd = True
        return

    n = len(nodeMap)
    g = src.G
    while (IsEnd is False):
        nx: int = dx + x
        ny: int = dy + y
        nz: int = dz + z
        x, y, z = nx, ny, nz

        ng: float = g + 1
        g = ng

        if (_IsOutOfRange(nx, ny, nz, n) or nodeMap[nx][ny][nz].Obstacle or nodeMap[nx][ny][nz].G != 0.0):
            return
        nodeMap[nx][ny][nz].Parent = parNode
        nodeMap[nx][ny][nz].G = ng
        if (nodeMap[nx][ny][nz] == dst):
            IsEnd = True
            return
        if (SearchJumpPointOrthogonal(nodeMap[nx][ny][nz], dx, dy, dz, dst,  nodeMap)):
            return
    return


class Jps(Agent):
    def __init__(self, agentName: str = 'Jps') -> None:
        super().__init__(agentName)

    def Run(self, src: Node, dst: Node, nodeMap: list[list[list[Node]]]):
        global IsEnd

        closedList.clear()
        openList.clear()
        IsEnd = False
        startTime: float = time()
        src.Parent = src
        src.F = _CalEuclidDistance(src, dst)
        heapq.heappush(openList, src)

        while (openList and not IsEnd):
            curNode: Node = heapq.heappop(openList)
            closedList.add(curNode)

            ExploreOrthogonal(curNode, 1, 0, 0, dst, nodeMap)
            ExploreOrthogonal(curNode, -1, 0, 0, dst, nodeMap)
            ExploreOrthogonal(curNode, 0, 1, 0, dst, nodeMap)
            ExploreOrthogonal(curNode, 0, -1, 0, dst,  nodeMap)
            ExploreOrthogonal(curNode, 0, 0, 1, dst, nodeMap)
            ExploreOrthogonal(curNode, 0, 0, -1, dst,  nodeMap)

            ExploreDiagonal2D(curNode, 1, -1, 0, dst,  nodeMap)
            ExploreDiagonal2D(curNode, -1, -1, 0, dst, nodeMap)
            ExploreDiagonal2D(curNode, 1, 1, 0, dst, nodeMap)
            ExploreDiagonal2D(curNode, -1, 1, 0, dst,  nodeMap)

            ExploreDiagonal2D(curNode, 1, 0, -1, dst,  nodeMap)
            ExploreDiagonal2D(curNode, -1, 0, -1, dst,  nodeMap)
            ExploreDiagonal2D(curNode, 1, 0, 1, dst, nodeMap)
            ExploreDiagonal2D(curNode, -1, 0, 1, dst,  nodeMap)

            ExploreDiagonal2D(curNode, 0, -1, -1, dst, nodeMap)
            ExploreDiagonal2D(curNode, 0, 1, -1, dst,  nodeMap)
            ExploreDiagonal2D(curNode, 0, -1, 1, dst,  nodeMap)
            ExploreDiagonal2D(curNode, 0, 1, 1, dst, nodeMap)

            # 3d diagonal
            ExploreDiagonal3D(curNode, 1, 1, 1, dst, nodeMap)

            ExploreDiagonal3D(curNode, 1, 1, -1, dst,  nodeMap)
            ExploreDiagonal3D(curNode, 1, -1, 1, dst,  nodeMap)
            ExploreDiagonal3D(curNode, -1, 1, 1, dst,  nodeMap)

            ExploreDiagonal3D(curNode, 1, -1, -1, dst, nodeMap)
            ExploreDiagonal3D(curNode, -1, 1, -1, dst, nodeMap)
            ExploreDiagonal3D(curNode, -1, -1, 1, dst, nodeMap)

            ExploreDiagonal3D(curNode, -1, -1, -1, dst, nodeMap)

        # if (IsEnd):
        self.CalTime = time() - startTime
        self._InitPathNodeList(src, dst)
        #self._InitDistance()
        #self._InitDegree()

if __name__ == "__main__":

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

    jps = Jps("jps")
    jps.Run(start, end, grids.NodeMap)
    jps._PostSmoothing(start, end, grids.NodeMap)
    diameter = 3
    sb = SplineBuilderExtended(jps.GetPathPoints(), diameter)
    sb.DisplaySplineShape(a, _color="black")
    path_points = jps.GetPathPoints()
    
    print("JPS PS 경로")
    for point in path_points:
        print('X: ', point.X(), 'Y: ', point.Y(), 'Z: ', point.Z())        

    # Update node center points (for the new spline)
    for node in jps.PathNodeList:  # Using bf.PathNodeList here
        point = node.CenterPoint
        #sphere = BRepPrimAPI_MakeSphere(point, 10).Shape()  # 반지름 10인 구 생성
        #a.DisplayShape(sphere, color='blue')

    # 여기서, sb의 Spline의 curve에 접근해서 곡률을 계산하고, 곡률이 클 때 점을 보간하여 곡률을 완화.
    min_bend_rad = 3 * 6 # 통상적으로 직경의 6~8배의 최소 곡률 반경을 가짐.
    threshold = 0.01  # 임의의 임계치 값
    #threshold = 1 / min_bend_rad # 사용해야할 임계치 값
    
    print("Collision!!")
    bf = BackTracking(start, end, jps.PathNodeList,
                        sb.SplineShape, grids, 2)
    bf.Run()
    if (bf.NewSpline):
        bf.InitCandidateSplinePath()

        # bf.PathNodeList에서 gp_Pnt 추출
        extracted_points = [node.CenterPoint for node in bf.PathNodeList]

        # 최소 굽힘 반경에 따른 보간점 추가 적용 (for the new spline)
        sb = SplineBuilderExtended(extracted_points, diameter)
        curvature_reducer = CurvatureReducer(sb, threshold)
        curvature_reducer.reduce_curvature()
        updated_path_points = curvature_reducer.get_updated_path_points()
        path_points = updated_path_points

        # Update node center points (for the new spline)
        for node, point in zip(bf.PathNodeList, path_points):  # Using bf.PathNodeList here
            node.CenterPoint = point
            # sphere = BRepPrimAPI_MakeSphere(point, 10).Shape()  # 반지름 10인 구 생성
            # a.DisplayShape(sphere, color='red')

        # Recreate the spline with the updated path points (for the new spline)
        sb = SplineBuilderExtended(path_points, 3)
        sb.DisplaySplineShape(a, _color="green")

        print("백트래킹 후 곡률 보간점 경로")
        for point in path_points:
            print('X: ', point.X(), 'Y: ', point.Y(), 'Z: ', point.Z())
            sphere = BRepPrimAPI_MakeSphere(point, 10).Shape()  # 반지름 10인 구 생성
            a.DisplayShape(sphere, color='blue')
        
        #a.DisplayShape(bf.CandidateSplineList[0][0], color="green")
        bf.DisplayAdditivePoints(a)
        
    else:
        print("Not Collision")

    # Step 2: Calculate length of each spline segment and check against straight line segment length
    u_values = []
    curve = sb.get_curve()
    proj = GeomAPI_ProjectPointOnCurve()

    for point in path_points:
        proj.Init(point, curve)
        if proj.NbPoints() > 0:
            u_values.append(proj.LowerDistanceParameter())
        else:
            u_values.append(0)  # If projection fails, set a high value

    new_path_points = path_points.copy()

    for i in range(len(u_values)-1):
        print(i,"~",i+1)
        start_u = u_values[i]
        end_u = u_values[i+1]
        
        # 스플라인 세그먼트 길이 계산
        spline_length = sb.spline_segment_length(start_u, end_u)
        print("곡선 길이: ", spline_length)
        
        # 직선 세그먼트 길이 계산
        straight_length = path_points[i].Distance(path_points[i+1])
        print("직선 길이: ", straight_length)

        # 길이 차이 계산
        gap_length = abs(spline_length - straight_length)
        print("길이 차이: ", gap_length)

        # 길이 차이가 10% 초과하는지 확인
        if (gap_length / straight_length) > 0.1:
            print("10% 초과!!!!!")
            insert_point = gp_Pnt((path_points[i].X()+path_points[i+1].X())/2,(path_points[i].Y()+path_points[i+1].Y())/2, (path_points[i].Z()+path_points[i+1].Z())/2)
            new_path_points.insert(i+1,insert_point)
            sphere = BRepPrimAPI_MakeSphere(insert_point, 30).Shape()  # 반지름 10인 구 생성
            a.DisplayShape(sphere, color='red')
        else:
            pass

    for point in new_path_points:
        print('X: ', point.X(), 'Y: ', point.Y(), 'Z: ', point.Z())
    sb = SplineBuilderExtended(new_path_points, 3)
    sb.DisplaySplineShape(a, _color="red")


    a.FitAll()
    b()
    pass