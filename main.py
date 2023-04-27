# main.py
import tkinter as tk
from tractor_parts import RearWheel, FrontWheel, RearCurve, FrontCurve, ConnectingLine, FrontVerticalLine, \
    RearVerticalLine, HorizontalLine, CockpitVerticalLine, CockpitDiagonalLine, CockpitRoofLine, ChimneyLine
from PIL import Image, ImageDraw, ImageTk


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

def draw_wheel(draw, x, y, radius, bit):
    if bit == 0:
        draw.ellipse([(x - radius, y - radius), (x + radius, y + radius)], outline='#41719C', width=10)

def create_window(vertices):
    window = tk.Tk()
    window.title("Tractor Drawing")
    window.geometry("800x600")

    img = Image.new("RGBA", (800, 600), "white")
    draw = ImageDraw.Draw(img)

    for item in vertices:
        if len(item) == 4:
            x, y, radius, bit = item
            draw_wheel(draw, x, y, radius, bit)
        elif len(item) == 5 or len(item) == 6:  # Check if the point has color information
            x1, y1, x2, y2, color = item[:5]
            draw.line([(x1, y1), (x2, y2)], fill=color, width=10)

        # elif len(item) == 5:  # Check if the point has color information
        #     x1, y1, x2, y2, color = item
        #     draw.line([(x1, y1), (x2, y2)], fill=color, width=10)
        # elif len(item) == 6:
        #     x1, y1, x2, y2, bit, group = item
        #     line_color = '#41719C'
        #     draw.line([(x1, y1), (x2, y2)], fill=line_color, width=10)

    for i in range(len(vertices) - 1):
        item1 = vertices[i]
        item2 = vertices[i + 1]
        if len(item1) == 4 and len(item2) == 4:
            _, _, bit1, group1 = item1
            _, _, bit2, group2 = item2
            if bit1 == 0 and bit2 == 0 and group1 == group2:
                draw.line([(item1[0], item1[1]), (item2[0], item2[1])], fill='#41719C', width=10)

    # Save the image temporarily
    img.save("temp_tractor_image.png")

    # Load the image using PhotoImage
    photo = tk.PhotoImage(file="temp_tractor_image.png")

    # Create a canvas and add the image to the canvas
    canvas = tk.Canvas(window, width=800, height=600)
    canvas.pack()
    canvas.create_image(0, 0, image=photo, anchor=tk.NW)

    # To keep the reference to the PhotoImage object
    canvas.image = photo

    return window

if __name__ == '__main__':
    rear_wheel = RearWheel(x=500, y=400, outer_radius=80, inner_radius=40)
    front_wheel = FrontWheel(x=230, y=400, outer_radius=40, inner_radius=20)

    ground_y = rear_wheel.y + rear_wheel.outer_radius
    front_wheel.y = ground_y - front_wheel.outer_radius

    rear_curve = RearCurve(rear_wheel)
    front_curve = FrontCurve(front_wheel)
    front_curve1 = FrontCurve(front_wheel)


    connecting_line = ConnectingLine(front_curve, rear_curve)
    front_vertical_line = FrontVerticalLine(front_curve, length=150)
    rear_vertical_line = RearVerticalLine(rear_curve, length=50, offset_x=50,
                                          offset_y=35)
    horizontal_line = HorizontalLine(front_vertical_line, rear_vertical_line)
    cockpit_vertical_line = CockpitVerticalLine(horizontal_line, length=85, offset_x=30)
    cockpit_diagonal_line = CockpitDiagonalLine(cockpit_vertical_line, horizontal_line, length=98, offset_x=170)
    cockpit_roof_line = CockpitRoofLine(cockpit_vertical_line, cockpit_diagonal_line)
    chimney_line = ChimneyLine(horizontal_line, length=120, offset_x=100)

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
            chimney_line.get_drawing_data()

    )

    data_filename = "tractor_data.txt"
    create_data_file(data_filename, drawing_data)
    data = load_data(data_filename)
    window = create_window(data)
    window.mainloop()
