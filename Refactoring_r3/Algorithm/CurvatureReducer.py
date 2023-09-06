from LineBuilder.SplineBuilder import SplineBuilderExtended
from OCC.Core.GeomAPI import GeomAPI_ProjectPointOnCurve

from OCC.Core.gp import gp_Pnt


class CurvatureReducer:
    def __init__(self, spline_builder: SplineBuilderExtended, threshold: float):
        self.spline_builder = spline_builder
        self.threshold = threshold
        self.exceeding_u_values = []
        self.added_intervals = set()
        self.projected_u_values = []
        self.intervals = []

    def compute_curvature_over_spline(self):
        self.exceeding_u_values = self.spline_builder.compute_curvature_over_spline(self.threshold)

    def project_path_points(self):
        curve = self.spline_builder.get_curve()
        proj = GeomAPI_ProjectPointOnCurve()
        path_points = self.spline_builder.GpPntList

        for idx, point in enumerate(path_points):
            proj.Init(point, curve)
            if proj.NbPoints() > 0:
                self.projected_u_values.append(proj.LowerDistanceParameter())
            elif idx == len(path_points) - 1:
                self.projected_u_values.append(curve.LastParameter())
            else:
                print(f"Failed to project point: ({point.X()}, {point.Y()}, {point.Z()})")

        for i in range(len(self.projected_u_values) - 1):
            self.intervals.append((self.projected_u_values[i], self.projected_u_values[i+1]))

    def reorder_within_interpolate(self, curve, path_points):
        proj = GeomAPI_ProjectPointOnCurve()

        # Project each path point on the curve and get its parameter value
        param_values = []
        for point in path_points:
            proj.Init(point, curve)
            if proj.NbPoints() > 0:
                param_values.append(proj.LowerDistanceParameter())
            else:
                param_values.append(float('inf'))  # If projection fails, set a high value

        # Pair each point with its parameter value
        paired_points = list(zip(param_values, path_points))
        
        # Sort by parameter value
        sorted_points = sorted(paired_points, key=lambda x: x[0])
        
        # Return reordered points
        return [p[1] for p in sorted_points]

    def interpolate_points(self):
        curve = self.spline_builder.get_curve()
        path_points = self.spline_builder.GpPntList
        interpolated_points = []

        for u in self.exceeding_u_values:
            in_added_interval = any(u1 <= u <= u2 for u1, u2 in self.added_intervals)
            if in_added_interval:
                continue

            for idx, (u1, u2) in enumerate(self.intervals):
                if u1 <= u <= u2:
                    point_prev = curve.Value(u1)
                    point_next = curve.Value(u2)
                    
                    midpoint_x = (point_prev.X() + point_next.X()) / 2
                    midpoint_y = (point_prev.Y() + point_next.Y()) / 2
                    midpoint_z = (point_prev.Z() + point_next.Z()) / 2
                    
                    interp_point = gp_Pnt(midpoint_x, midpoint_y, midpoint_z)
                    interpolated_points.append((idx+1, interp_point))
                    self.added_intervals.add((u1, u2))
                    break
        # Insert the interpolated points at the correct positions
        for idx, point in reversed(interpolated_points):
            path_points.insert(idx+1, point)

        # Reorder the path points
        reordered_path_points = self.reorder_within_interpolate(curve, path_points)

        # Update the GpPntList in spline_builder with the new path_points
        self.spline_builder.GpPntList = reordered_path_points

    def reduce_curvature(self):
        self.compute_curvature_over_spline()
        self.project_path_points()
        self.interpolate_points()

    def get_updated_path_points(self):
        return self.spline_builder.GpPntList
