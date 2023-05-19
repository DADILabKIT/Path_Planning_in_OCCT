# for import 
from util import sys

# Python
import pandas as pd
from openpyxl import load_workbook
import math

# OCC
# for 3D Data
from OCC.Core.gp import gp_Pnt

# for visual
from OCC.Display.OCCViewer import Viewer3d

# Map
from Map.GridMap import GridMap
from Map.Node import Node
from Algoritm.Astar import Astar
from Algoritm.Theta import Theta
from Algoritm.Jps import Jps
from Algoritm.JpsTheta import JpsTheta
from Algoritm.Agent import Agent



class ExTest:
    def __init__(self) -> None:
        # data frame 정의
        # Algorithms, Map Size, Distance, Degree, Time
        self.RawData:dict[str, list[any]] = {}
        self.RawData['algorithm'] = []
        self.RawData['distance'] = []
        self.RawData['degree'] = []
        self.RawData['time'] = []
        self.RawData['map_size'] = []
        
    
    def ExRun(self, dataNum = 100, startMapSize = 10, endMapSize = 50) -> None:
        for _mapSize in range(startMapSize, endMapSize  + 1, 10):
            for _ in range(dataNum):   
                print(_mapSize)
                # 랜덤 맵 초기화
                gridMap = GridMap(gp_Pnt(0, 0, 0), gp_Pnt(1000, 1000, 1000), mapSize = _mapSize)
                gridMap.InitNodeMapByRandom(int(gridMap.MapSize / 2) + 5)
                # 시작점과 끝점 정의
                e = gridMap.MapSize - 1
                s = 0
                # 시작 노드, 도착 노드
                startNode: Node = gridMap.NodeMap[s][s][s]
                endNode: Node = gridMap.NodeMap[e][e][e]
                
                
                # 알고리즘 수행 객체 초기화
                jps: Jps = Jps(startNode, endNode, gridMap.NodeMap, 'jps',display= None)
                astar: Astar = Astar(startNode, endNode, gridMap.NodeMap, 'astar',display= None)
                                
                # 알고리즘 수행
                jps.Run()
                
                gridMap.RecycleNodeMap()
                                
                astar.Run()
                gridMap.RecycleNodeMap()
                
                self.InputRawData(jps, _mapSize)
                self.InputRawData(astar, _mapSize)
                
                
        dataFrame = pd.DataFrame(self.RawData)
        excelTitle = "C:\\Users\\User\\Desktop\\LAB doc\\cableRouting\\R project\\My_First_Project\\" + 'testReal' +".xlsx"
        dataFrame.to_excel(excelTitle, sheet_name='expriment')

                
    def InputRawData(self, agent:Agent, _mapSize: int) ->None:
        self.RawData['algorithm'].append(agent.AgentName)
        self.RawData['distance'].append(agent.Distance)
        self.RawData['map_size'].append(str(_mapSize))
        self.RawData['degree'].append(agent.Degree)
        self.RawData['time'].append(agent.CalTime)


if (__name__ == '__main__'):
    dataNum, startMapSize, endMapSize = 10, 10, 31

    

    ex = ExTest()
    ex.ExRun(dataNum, startMapSize, endMapSize)
    
    
        
        
