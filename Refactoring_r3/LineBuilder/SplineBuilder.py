import util
from OCC.Core.gp import gp_Pnt, gp_Circ, gp_Dir, gp_Ax2,  gp_Vec
from OCC.Core.TopoDS import TopoDS_Shape, TopoDS_Edge, TopoDS_Wire
from OCC.Core.GeomAPI import GeomAPI_Interpolate
from OCC.Core.BRepAlgoAPI import BRepAlgoAPI_Fuse
from OCC.Core.BRepOffsetAPI import BRepOffsetAPI_MakePipe
from OCC.Core.BRepBuilderAPI import BRepBuilderAPI_MakeWire, BRepBuilderAPI_MakeEdge
from OCC.Core.TColStd import TColStd_HArray1OfBoolean
from OCC.Core.TColgp import TColgp_HArray1OfPnt, TColgp_Array1OfVec
from OCC.Display.OCCViewer import Viewer3d

from OCC.Core.Geom import Geom_Curve
from OCC.Core.BRep import BRep_Tool
from OCC.Core.TopExp import TopExp_Explorer
from OCC.Core.TopAbs import TopAbs_EDGE
from OCC.Core.GeomLProp import GeomLProp_CLProps, GeomLProp_CurveTool



class SplineBuilder:
    def __init__(self, gpPntList: list[gp_Pnt], diameter: float = 3) -> None:
        self.GpPntList: list[gp_Pnt] = gpPntList
        self.SplineShape: TopoDS_Shape = self.__InitedSplineShape(diameter)
        pass

    def DisplaySplineShape(self, display: Viewer3d, _transparency=0.5, _color="red") -> None:
        display.DisplayShape(
            self.SplineShape, transparency=_transparency, color=_color)

    def InitSplineShape(self, gpPntList: list[gp_Pnt], diameter: float) -> None:
        self.GpPntList = gpPntList
        self.SplineShape = self.__InitedSplineShape(diameter)
        return

    def __InitedSplineShape(self, diameter: float) -> TopoDS_Shape:
        tColgpPnt = TColgp_HArray1OfPnt(1, len(self.GpPntList))
        tColgpVec = TColgp_Array1OfVec(1, len(self.GpPntList))
        tColstdBool = TColStd_HArray1OfBoolean(1, len(self.GpPntList))
        for i in range(1, len(self.GpPntList) + 1):
            tColgpPnt.SetValue(i, self.GpPntList[i - 1])
            if (len(self.GpPntList) == i):
                continue
            tColgpVec.SetValue(
                i, gp_Vec(self.GpPntList[i - 1], self.GpPntList[i]))
            tColstdBool.SetValue(i, True)

        tColgpVec.SetValue(len(self.GpPntList), gp_Vec(
            self.GpPntList[len(self.GpPntList) - 1], self.GpPntList[len(self.GpPntList) - 2]))

        tColstdBool.SetValue(1, False)
        tColstdBool.SetValue(len(self.GpPntList), False)
        tolenrance = 1e-3
        interpolate = GeomAPI_Interpolate(tColgpPnt, False, tolenrance)

        interpolate.Load(tColgpVec, tColstdBool)
        interpolate.Perform()

        curveEdge = interpolate.Curve()

        edgeShape = BRepBuilderAPI_MakeEdge(curveEdge).Shape()
        wireShape = BRepBuilderAPI_MakeWire(edgeShape).Shape()

        circle: gp_Circ = gp_Circ(gp_Ax2(self.GpPntList[0], gp_Dir(
            self.GpPntList[1].XYZ().Subtracted(self.GpPntList[0].XYZ()))), diameter)
        circleEdge: TopoDS_Edge = BRepBuilderAPI_MakeEdge(circle).Shape()
        circleWire: TopoDS_Wire = BRepBuilderAPI_MakeWire(circleEdge).Shape()

        splineShape: TopoDS_Shape = BRepOffsetAPI_MakePipe(
            wireShape, circleWire).Shape()
        return splineShape
    
class SplineBuilderExtended(SplineBuilder):
    def get_curve(self) -> Geom_Curve:
        """
        Extract the Geom_Curve object from the SplineShape.
        """
        explorer = TopExp_Explorer(self.SplineShape, TopAbs_EDGE)
        while explorer.More():
            edge = explorer.Current()
            curve, _, _ = BRep_Tool.Curve(edge)
            if curve is not None:
                return curve
            explorer.Next()
        return None

    def curvature_at_parameter(self, u: float) -> float:
        """
        Compute the curvature of the spline at a given parameter u.
        """
        curve = self.get_curve()
        if curve:
            return curve.Curvature(u)
        else:
            raise ValueError("No valid curve found in the spline shape.")
        
    def compute_curvature_over_spline(self, threshold: float, delta_u: float = 1) -> list[float]:
        """
        Compute the curvature of the spline over its entire length and 
        return the parameter values where the curvature exceeds the given threshold.

        Args:
        - threshold: Curvature threshold.
        - delta_u: The step size for parameter sampling.

        Returns:
        - A list of parameter values where the curvature exceeds the threshold.
        """
        curve = self.get_curve()
        if not curve:
            raise ValueError("No valid curve found in the spline shape.")
        
        u_start, u_end = curve.FirstParameter(), curve.LastParameter()
        exceeding_u_values = []

        props = GeomLProp_CLProps(curve, 2, 1e-6)

        u = u_start
        while u <= u_end:
            props.SetParameter(u)
            curvature = props.Curvature()
            if abs(curvature) > threshold:
                exceeding_u_values.append(u)
            u += delta_u

        return exceeding_u_values