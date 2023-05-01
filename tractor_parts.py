import math
from bezier import Bezier
from random import randint

def flip_y(y, canvas_height):
    return canvas_height - y

class TractorPart:
    def get_drawing_data(self):
        raise NotImplementedError

class RearWheel(TractorPart):
    def __init__(self, x, y, outer_radius, inner_radius):
        self.x = x
        self.y = y
        self.outer_radius = outer_radius
        self.inner_radius = inner_radius

    def get_drawing_data(self):
        outer_wheel = [
            (self.x, self.y, self.outer_radius, 0),
        ]

        inner_wheel = [
            (self.x, self.y, self.inner_radius, 0),
        ]

        return outer_wheel + inner_wheel

class FrontWheel(TractorPart):
    def __init__(self, x, y, outer_radius, inner_radius):
        self.x = x
        self.y = y
        self.outer_radius = outer_radius
        self.inner_radius = inner_radius

    def get_drawing_data(self):
        outer_wheel = [
            (self.x, self.y, self.outer_radius, 0),
        ]

        inner_wheel = [
            (self.x, self.y, self.inner_radius, 0),
        ]

        return outer_wheel + inner_wheel


class Body(TractorPart):
    def __init__(self, front_wheel, rear_wheel):
        super().__init__()
        self.front_wheel = front_wheel
        self.rear_wheel = rear_wheel

    def get_drawing_data(self):
        return []


class RearCurve(TractorPart):
    def __init__(self, rear_wheel):
        super().__init__()
        self.rear_wheel = rear_wheel

    def get_drawing_data(self):
        rear_curve_start_angle = 180
        rear_curve_end_angle = 320
        rear_margin = 30

        rear_curve_start = (
            self.rear_wheel.x + (self.rear_wheel.outer_radius + rear_margin) * math.cos(math.radians(rear_curve_start_angle)),
            self.rear_wheel.y + (self.rear_wheel.outer_radius + rear_margin) * math.sin(math.radians(rear_curve_start_angle)),
        )
        rear_curve_end = (
            self.rear_wheel.x + (self.rear_wheel.outer_radius + rear_margin) * math.cos(math.radians(rear_curve_end_angle)),
            self.rear_wheel.y + (self.rear_wheel.outer_radius + rear_margin) * math.sin(math.radians(rear_curve_end_angle)),
        )

        rear_curve_control = (
            self.rear_wheel.x + (self.rear_wheel.outer_radius + rear_margin + 70) * math.cos(math.radians((rear_curve_start_angle + rear_curve_end_angle) / 2)),
            self.rear_wheel.y + (self.rear_wheel.outer_radius + rear_margin + 90) * math.sin(math.radians((rear_curve_start_angle + rear_curve_end_angle) / 2)),
        )

        rear_curve = Bezier.draw_curve(rear_curve_start, rear_curve_control, rear_curve_end, steps=50, group_id=1)
        return rear_curve


class FrontCurve(TractorPart):
    def __init__(self, front_wheel):
        super().__init__()
        self.front_wheel = front_wheel

    def get_drawing_data(self):
        front_curve_start_angle = 320
        front_curve_end_angle = 230
        front_margin = 18

        front_curve_start = (
            self.front_wheel.x + (self.front_wheel.outer_radius + front_margin) * math.cos(math.radians(front_curve_start_angle)),
            self.front_wheel.y + (self.front_wheel.outer_radius + front_margin) * math.sin(math.radians(front_curve_start_angle)),
        )
        front_curve_end = (
            self.front_wheel.x + (self.front_wheel.outer_radius + front_margin) * math.cos(math.radians(front_curve_end_angle)),
            self.front_wheel.y + (self.front_wheel.outer_radius + front_margin) * math.sin(math.radians(front_curve_end_angle)),
        )

        front_curve_control = (
            self.front_wheel.x + (self.front_wheel.outer_radius + front_margin + 30) * math.cos(
                math.radians((front_curve_start_angle + front_curve_end_angle) / 2)),
            self.front_wheel.y + (self.front_wheel.outer_radius + front_margin + 50) * math.sin(
                math.radians((front_curve_start_angle + front_curve_end_angle) / 2)),
        )

        front_curve = Bezier.draw_curve(front_curve_start, front_curve_control, front_curve_end, steps=50, group_id=2)
        return front_curve

class ConnectingLine(TractorPart):
    def __init__(self, front_curve, rear_curve):
        super().__init__()
        self.front_curve = front_curve
        self.rear_curve = rear_curve

    def get_drawing_data(self):
        front_curve_rightmost_point = max(self.front_curve.get_drawing_data(), key=lambda point: point[0])
        rear_curve_leftmost_point = min(self.rear_curve.get_drawing_data(), key=lambda point: point[0])

        connecting_line = [
            (rear_curve_leftmost_point[0], rear_curve_leftmost_point[1], 0, 3),
            (front_curve_rightmost_point[0], rear_curve_leftmost_point[1], 0, 3)
        ]

        return connecting_line

class FrontVerticalLine(TractorPart):
    def __init__(self, front_curve, length):
        super().__init__()
        self.front_curve = front_curve
        self.length = length

    def get_drawing_data(self):
        front_curve_leftmost_point = min(self.front_curve.get_drawing_data(), key=lambda point: point[0])
        vertical_line_start = (front_curve_leftmost_point[0], front_curve_leftmost_point[1])
        vertical_line_end = (front_curve_leftmost_point[0], front_curve_leftmost_point[1] - self.length)

        vertical_line = [
            (vertical_line_start[0], vertical_line_start[1], 0, 4),
            (vertical_line_end[0], vertical_line_end[1], 0, 4),
        ]

        return vertical_line

class RearVerticalLine(TractorPart):
    def __init__(self, rear_curve, length, offset_x, offset_y):
        super().__init__()
        self.rear_curve = rear_curve
        self.length = length
        self.offset_x = offset_x
        self.offset_y = offset_y

    def get_drawing_data(self):
        rear_curve_rightmost_point = max(self.rear_curve.get_drawing_data(), key=lambda point: point[0])
        vertical_line_start = (rear_curve_rightmost_point[0] - self.offset_x, rear_curve_rightmost_point[1] - self.offset_y)  # Subtract the offset_y value
        vertical_line_end = (rear_curve_rightmost_point[0] - self.offset_x, rear_curve_rightmost_point[1] - self.length - self.offset_y)

        vertical_line = [
            (vertical_line_start[0], vertical_line_start[1], 0, 5),
            (vertical_line_end[0], vertical_line_end[1], 0, 5),
        ]

        return vertical_line

class HorizontalLine(TractorPart):
    def __init__(self, front_vertical_line, rear_vertical_line):
        super().__init__()
        self.front_vertical_line = front_vertical_line
        self.rear_vertical_line = rear_vertical_line

    def get_drawing_data(self):
        front_vertical_line_end = min(self.front_vertical_line.get_drawing_data(), key=lambda point: point[1])
        rear_vertical_line_end = min(self.rear_vertical_line.get_drawing_data(), key=lambda point: point[1])

        horizontal_line = [
            (front_vertical_line_end[0], front_vertical_line_end[1], 0, 6),
            (rear_vertical_line_end[0], front_vertical_line_end[1], 0, 6),
        ]

        return horizontal_line

class CockpitVerticalLine(TractorPart):
    def __init__(self, horizontal_line, length, offset_x):
        super().__init__()
        self.horizontal_line = horizontal_line
        self.length = length
        self.offset_x = offset_x

    def get_drawing_data(self):
        horizontal_line_rightmost_point = max(self.horizontal_line.get_drawing_data(), key=lambda point: point[0])
        vertical_line_start = (horizontal_line_rightmost_point[0] - self.offset_x, horizontal_line_rightmost_point[1])
        vertical_line_end = (horizontal_line_rightmost_point[0] - self.offset_x, horizontal_line_rightmost_point[1] - self.length)

        vertical_line = [
            (vertical_line_start[0], vertical_line_start[1], 0, 7),
            (vertical_line_end[0], vertical_line_end[1], 0, 7),
        ]

        return vertical_line

class CockpitDiagonalLine(TractorPart):
    def __init__(self, cockpit_vertical_line, horizontal_line, length, offset_x=0):
        super().__init__()
        self.cockpit_vertical_line = cockpit_vertical_line
        self.horizontal_line = horizontal_line
        self.length = length
        self.offset_x = offset_x

    def get_drawing_data(self):
        horizontal_line_end = max(self.horizontal_line.get_drawing_data(), key=lambda point: point[0])
        vertical_line_end = min(self.cockpit_vertical_line.get_drawing_data(), key=lambda point: point[1])

        diagonal_start = (horizontal_line_end[0] - self.offset_x, horizontal_line_end[1])
        diagonal_end = (
            diagonal_start[0] + self.length * math.cos(math.radians(-60)),
            diagonal_start[1] + self.length * math.sin(math.radians(-60)),
        )

        diagonal_line = [
            (diagonal_start[0], diagonal_start[1], 0, 10),
            (diagonal_end[0], diagonal_end[1], 0, 10),
        ]

        return diagonal_line

class CockpitRoofLine(TractorPart):
    def __init__(self, cockpit_vertical_line, cockpit_diagonal_line):
        super().__init__()
        self.cockpit_vertical_line = cockpit_vertical_line
        self.cockpit_diagonal_line = cockpit_diagonal_line

    def get_drawing_data(self):
        vertical_line_end = min(self.cockpit_vertical_line.get_drawing_data(), key=lambda point: point[1])
        diagonal_line_end = min(self.cockpit_diagonal_line.get_drawing_data(), key=lambda point: point[1])

        roof_line = [
            (vertical_line_end[0], vertical_line_end[1], 0, 11),
            (diagonal_line_end[0], diagonal_line_end[1], 0, 11),
        ]

        return roof_line


class ChimneyCircles(TractorPart):
    def __init__(self, horizontal_line, length, offset_x, circle_radius):
        super().__init__()
        self.horizontal_line = horizontal_line
        self.length = length
        self.offset_x = offset_x
        self.circle_radius = circle_radius

    def get_drawing_data(self):
        horizontal_line_rightmost_point = max(self.horizontal_line.get_drawing_data(), key=lambda point: point[0])
        vertical_line_start = (horizontal_line_rightmost_point[0] - self.offset_x, horizontal_line_rightmost_point[1])
        vertical_line_end = (vertical_line_start[0], vertical_line_start[1] - self.length)
        return [(vertical_line_start[0], vertical_line_start[1], vertical_line_end[0], vertical_line_end[1], 1)]

    def draw_chimney_circle(self):
        chimney_top = (self.get_drawing_data()[0][2], self.get_drawing_data()[0][3])
        chimney_circle_center = (chimney_top[0], chimney_top[1] - self.circle_radius)
        return [(chimney_circle_center[0], chimney_circle_center[1], self.circle_radius, 0)]

class Chimney(TractorPart):
    def __init__(self, horizontal_line, length, offset_x):
        super().__init__()
        self.horizontal_line = horizontal_line
        self.length = length
        self.offset_x = offset_x

    def get_drawing_data(self):
        horizontal_line_rightmost_point = max(self.horizontal_line.get_drawing_data(), key=lambda point: point[0])
        vertical_line_start = (horizontal_line_rightmost_point[0] - self.offset_x, horizontal_line_rightmost_point[1])
        vertical_line_end = (horizontal_line_rightmost_point[0] - self.offset_x, horizontal_line_rightmost_point[1] - self.length)

        vertical_line = [
            (vertical_line_start[0], vertical_line_start[1], 0, 7),
            (vertical_line_end[0], vertical_line_end[1], 0, 7),
        ]

        return vertical_line
