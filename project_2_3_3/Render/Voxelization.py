from OCC.Core.gp import gp_Pnt
import open3d as o3d


import numpy as np


class VoxelizationSTL:
    def __init__(self) -> None:
        self.pointCloud = None
        self.Points: list[gp_Pnt] = []
        pass

    def InitBySTL(self, fileName: str):
        mesh = o3d.io.read_triangle_mesh(fileName)        
        self.pointCloud = mesh.sample_points_uniformly(number_of_points=10000)
        
    def Move(self, x, y, z):
        self.pointCloud.points = o3d.utility.Vector3dVector(np.asarray(self.pointCloud.points) + [x, y, z])
        pass
    
    def Rotation(self, ang):
        pass
    
    def GetPoints(self):
        for i in range(len(self.pointCloud.points)):
            self.Points.append(gp_Pnt(self.pointCloud.points[i][0], self.pointCloud.points[i][1], self.pointCloud.points[i][2]))
        return self.Points


