from scipy.interpolate import BSpline
import numpy as np
import matplotlib.pyplot as plt

# 제어점의 좌표
control_points = np.array([(0, 0, 0), (1, 2, 3), (3, 1, 2)])

# Knot 벡터 생성
knots = np.array([0, 0, 0, 1, 1, 1])

# B-스플라인 차수
degree = 2

# B-스플라인 생성
bspline = BSpline(knots, control_points, degree)

# 곡선을 평가할 파라미터 범위
t = np.linspace(0, 1, 100)

# B-스플라인 곡선 평가
curve = bspline(t)

# 제어점과 곡선 그리기
fig = plt.figure()
ax = fig.add_subplot(111, projection='3d')

# 제어점 그리기
ax.scatter(control_points[:, 0], control_points[:, 1], control_points[:, 2], color='red', label='Control Points')

# 곡선 그리기
ax.plot(curve[:, 0], curve[:, 1], curve[:, 2], label='B-Spline Curve')

ax.legend()
plt.show()