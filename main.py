# main.py
import tkinter as tk
from tkinter import ttk

from tractor_parts import RearWheel, FrontWheel, RearCurve, FrontCurve, ConnectingLine, FrontVerticalLine, \
    RearVerticalLine, HorizontalLine, CockpitVerticalLine, CockpitDiagonalLine, CockpitRoofLine, Chimney
from PIL import Image, ImageDraw, ImageTk
from transform_tractor import  move_tractor


def reset_tractor(original_vertices, canvas, update_callback):
    update_callback(original_vertices, canvas)


def get_coordinates(callback):
    coord_window = tk.Toplevel()
    coord_window.title("Enter Coordinates")

    x_label = tk.Label(coord_window, text="X:")
    x_label.grid(row=0, column=0, padx=5, pady=5)
    x_entry = tk.Entry(coord_window)
    x_entry.grid(row=0, column=1, padx=5, pady=5)

    y_label = tk.Label(coord_window, text="Y:")
    y_label.grid(row=1, column=0, padx=5, pady=5)
    y_entry = tk.Entry(coord_window)
    y_entry.grid(row=1, column=1, padx=5, pady=5)

    def on_submit():
        try:
            x = float(x_entry.get())
            y = float(y_entry.get())
            callback(x, y)
            coord_window.destroy()
        except ValueError:
            tk.messagebox.showerror("Error", "Invalid coordinates. Please enter valid numbers.")

    submit_button = tk.Button(coord_window, text="Submit", command=on_submit)
    submit_button.grid(row=2, columnspan=2, padx=5, pady=5)


def create_move_tab(tab_control, vertices, canvas, update_callback):
    move_frame = ttk.Frame(tab_control)
    tab_control.add(move_frame, text="Move")

    def on_move_click():
        get_coordinates(lambda dx, dy: move_tractor(vertices, dx, dy, canvas, update_callback))

    move_button = tk.Button(move_frame, text="Move Tractor", command=on_move_click)
    move_button.pack(padx=10, pady=10)

    reset_button = tk.Button(move_frame, text="Reset Tractor",
                             command=lambda: reset_tractor(original_vertices, canvas, update_callback))
    reset_button.pack(padx=10, pady=10)



def create_scaled_image(vertices, scale_factor):
    img = Image.new("RGBA", (800 * scale_factor, 600 * scale_factor), "white")
    draw = ImageDraw.Draw(img)

    last_point = None
    for item in vertices:
        if len(item) == 4:
            x, y, radius, bit = item
            draw_wheel(draw, x * scale_factor, y * scale_factor, radius * scale_factor, bit,
                       fill_color='#5b9bd5' if bit == 0 and item in front_curve.get_drawing_data() else '#41719C')
        elif len(item) == 5:
            x1, y1, x2, y2, bit = item
            if last_point is not None and bit == 1:
                draw.line([last_point, (x1 * scale_factor, y1 * scale_factor)], fill='#000000', width=10 * scale_factor)
            if bit == 1:
                draw.line([(x1 * scale_factor, y1 * scale_factor), (x2 * scale_factor, y2 * scale_factor)],
                          fill='#000000', width=10 * scale_factor)
                last_point = (x2 * scale_factor, y2 * scale_factor)
            else:
                last_point = None

    for i in range(len(vertices) - 1):
        item1 = vertices[i]
        item2 = vertices[i + 1]
        if len(item1) == 4 and len(item2) == 4:
            _, _, bit1, group1 = item1
            _, _, bit2, group2 = item2
            if bit1 == 0 and bit2 == 0 and group1 == group2:
                fill_color = '#5b9bd5' if group1 in [2, 3, 8] else '#41719C'
                draw.line([(item1[0] * scale_factor, item1[1] * scale_factor),
                           (item2[0] * scale_factor, item2[1] * scale_factor)], fill=fill_color,
                          width=10 * scale_factor)

    img = img.resize((800, 600), Image.ANTIALIAS)
    return img

def update_tractor_drawing(vertices, canvas=None):
    img = create_scaled_image(vertices, scale_factor=4)
    img.save("temp_tractor_image.png")
    photo = ImageTk.PhotoImage(file="temp_tractor_image.png")
    canvas.delete("all")
    canvas.create_image(0, 0, image=photo, anchor=tk.NW)
    canvas.image = photo
    canvas.vertices = vertices

def create_window(vertices, update_callback=None):
    scale_factor = 4
    window = tk.Tk()
    window.title("Tractor Drawing")
    window.geometry("800x600")
    global original_vertices
    original_vertices = vertices.copy()


    img = Image.new("RGBA", (800 * scale_factor, 600 * scale_factor), "white")
    draw = ImageDraw.Draw(img)

    # Create a Notebook (tabbed interface)
    notebook = ttk.Notebook(window)
    notebook.pack(fill='both', expand=True)

    # Create the Drawing tab
    drawing_frame = tk.Frame(notebook)
    notebook.add(drawing_frame, text="Drawing")

    # Create the canvas object
    canvas = tk.Canvas(drawing_frame, width=800, height=600)
    canvas.pack()

    # Create the Move tab using the create_move_tab function
    create_move_tab(notebook, vertices, canvas, update_callback)

    img = create_scaled_image(vertices, scale_factor)
    img.save("temp_tractor_image.png")
    photo = ImageTk.PhotoImage(file="temp_tractor_image.png")

    # Create the Move tab
    canvas.create_image(0, 0, image=photo, anchor=tk.NW)
    canvas.image = photo
    canvas.vertices = vertices
    return window



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

def draw_wheel(draw, x, y, radius, bit, fill_color):
    if bit == 0:
        draw.ellipse([(x - radius, y - radius), (x + radius, y + radius)], outline=fill_color, width=40)



if __name__ == '__main__':
    rear_wheel = RearWheel(x=500, y=400, outer_radius=80, inner_radius=40)
    front_wheel = FrontWheel(x=230, y=400, outer_radius=40, inner_radius=20)
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
    chimney = Chimney(horizontal_line, length=85, offset_x=280)


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
            chimney.get_drawing_data()
    )

    data_filename = "tractor_data.txt"
    create_data_file(data_filename, drawing_data)
    data = load_data(data_filename)
    window = create_window(data, update_callback=update_tractor_drawing)

    window.mainloop()
