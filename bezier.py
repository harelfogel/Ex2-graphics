import math

class Bezier:
    @staticmethod
    def calculate_point(t, p0, p1, p2):
        return (
            math.pow(1 - t, 2) * p0[0] + 2 * (1 - t) * t * p1[0] + t * t * p2[0],
            math.pow(1 - t, 2) * p0[1] + 2 * (1 - t) * t * p1[1] + t * t * p2[1],
        )

    @staticmethod
    def draw_curve(start, control, end, steps=100, group_id=0):
        points = []
        for i in range(steps + 1):
            t = i / steps
            point = Bezier.calculate_point(t, start, control, end)
            points.append((point[0], point[1], 0, group_id))  # Set the radius to 0
        return points
