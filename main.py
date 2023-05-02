# main.py
import tkinter as tk
from GUI import create_window, update_tractor_drawing
from tractor_parts import RearWheel, FrontWheel, RearCurve, FrontCurve, ConnectingLine, FrontVerticalLine, \
    RearVerticalLine, HorizontalLine, CockpitVerticalLine, CockpitDiagonalLine, CockpitRoofLine, Chimney,ChimneyCircles


def draw_arc(canvas, x1, y1, x2, y2, start, extent, width, fill):
    canvas.create_arc(x1, y1, x2, y2, start=start, extent=extent, width=width, outline=fill, style=tk.ARC)

def create_data_file(filename, data):
    with open(filename, 'w') as file:
        for item in data:
            file.write(','.join(str(i) for i in item) + '\n')

def load_data(filename):
    with open(filename, 'r') as file:
        data = [line.strip().split(',') for line in file.readlines()]

    loaded_data = []
    for item in data:
        if len(item) == 4:
            loaded_data.append((float(item[0]), float(item[1]), float(item[2]), int(item[3])))
        elif len(item) == 3:
            loaded_data.append((float(item[0]), float(item[1]), int(item[2])))

    return loaded_data


def draw_curve(canvas, curve_data, color='black'):
    for i in range(len(curve_data)):
        x1, y1, cp1_x, cp1_y, x2, y2 = curve_data[i]
        canvas.create_line(x1, y1, cp1_x, cp1_y, fill=color, smooth=True)
        canvas.create_line(cp1_x, cp1_y, x2, y2, fill=color, smooth=True)
        canvas.create_line(x1, y1, cp1_x, cp1_y, x2, y2, fill=color, smooth=True, width=2)


if __name__ == '__main__':
    rear_wheel = RearWheel(x=650, y=450, outer_radius=80, inner_radius=40)
    front_wheel = FrontWheel(x=400, y=450, outer_radius=40, inner_radius=20)
    ground_y = rear_wheel.y + rear_wheel.outer_radius
    front_wheel.y = ground_y - front_wheel.outer_radius
    rear_curve = RearCurve(rear_wheel)
    front_curve = FrontCurve(front_wheel)
    connecting_line = ConnectingLine(front_curve, rear_curve)
    front_vertical_line = FrontVerticalLine(front_curve, length=150)
    rear_vertical_line = RearVerticalLine(rear_curve, length=50, offset_x=50,
                                          offset_y=35)
    horizontal_line = HorizontalLine(front_vertical_line, rear_vertical_line)
    cockpit_vertical_line = CockpitVerticalLine(horizontal_line, length=85, offset_x=30)
    cockpit_diagonal_line = CockpitDiagonalLine(cockpit_vertical_line, horizontal_line, length=98, offset_x=170)
    cockpit_roof_line = CockpitRoofLine(cockpit_vertical_line, cockpit_diagonal_line)
    # In the main section, update the chimney instances and drawing_data
    chimney_line_1 = Chimney(horizontal_line, length=80, offset_x=270)
    chimney_line_2 = Chimney(horizontal_line, length=80, offset_x=310)
    chimney_circle1 = ChimneyCircles(horizontal_line, length=80, offset_x=280, circle_radius=15)
    chimney_circle2 = ChimneyCircles(horizontal_line, length=80, offset_x=300, circle_radius=15)


    cockpit_vertical_line = CockpitVerticalLine(horizontal_line, length=85, offset_x=30)

    drawing_data = (
            rear_wheel.get_drawing_data() +
            front_wheel.get_drawing_data() +
            rear_curve.get_drawing_data() +
            front_curve.get_drawing_data() +
            connecting_line.get_drawing_data() +
            front_vertical_line.get_drawing_data() +
            rear_vertical_line.get_drawing_data() +
            horizontal_line.get_drawing_data() +
            cockpit_vertical_line.get_drawing_data() +
            cockpit_diagonal_line.get_drawing_data() +
            cockpit_roof_line.get_drawing_data() +
            chimney_line_1.get_drawing_data() +
            chimney_line_2.get_drawing_data() +
            chimney_circle1.get_drawing_data()+ chimney_circle1.draw_chimney_circle() +
            chimney_circle2.get_drawing_data() + chimney_circle2.draw_chimney_circle()

    )
    data_filename = "tractor_data.txt"
    create_data_file(data_filename, drawing_data)
    data = load_data(data_filename)
    window = create_window(data, data_filename,update_callback=update_tractor_drawing)

    window.mainloop()
