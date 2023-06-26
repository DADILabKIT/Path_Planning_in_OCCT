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
from Algoritm.ThetaC import ThetaC
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
        
        for i in range(startMapSize, endMapSize + 1, 10):
            while (dataNum):
                gridMap = GridMap(gp_Pnt(0, 0, 0), gp_Pnt(1000, 1000, 1000), mapSize = i)
                gridMap.InitNodeMapByRandom2(0.4)                  

                # 시작점과 끝점 정의
                e = gridMap.MapSize - 1
                s = 0
                startNode: Node = gridMap.NodeMap[s][s][s]
                endNode: Node = gridMap.NodeMap[e][e][e]
                
                


                theta: ThetaC = ThetaC(startNode, endNode, gridMap.NodeMap, 'theta_without_CL',display= None)
                thetac: Theta = Theta(startNode, endNode, gridMap.NodeMap, 'theta_with_CL',display= None)
                astar :Astar = Astar(startNode, endNode, gridMap.NodeMap, 'astar',display= None)
                thetac.Run()
                gridMap.RecycleNodeMap()
                theta.Run()
                gridMap.RecycleNodeMap()
                astar.Run()
                gridMap.RecycleNodeMap()
                self.InputRawData(thetac, i)
                self.InputRawData(theta, i)
                self.InputRawData(astar, i)
                print(i)
                dataNum -= 1
            dataNum = 100
                
                
        dataFrame = pd.DataFrame(self.RawData)
        excelTitle = "C:\\Users\\User\\Desktop\\LAB doc\\cableRouting\\Codes\\R project\\My_First_Project\\" + 'testReal' +".xlsx"
        dataFrame.to_excel(excelTitle, sheet_name='expriment')

                
    def InputRawData(self, agent:Agent, _mapSize: int) ->None:
        self.RawData['algorithm'].append(agent.AgentName)
        self.RawData['distance'].append(agent.Distance)
        self.RawData['map_size'].append(str(_mapSize))
        self.RawData['degree'].append(agent.Degree)
        self.RawData['time'].append(agent.CalTime)


if (__name__ == '__main__'):
    dataNum, startMapSize, endMapSize = 100, 10, 51

    

    ex = ExTest()
    ex.ExRun(dataNum, startMapSize, endMapSize)
    
    
        
        
