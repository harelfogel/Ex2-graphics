# main.py
import tkinter as tk
from tkinter import ttk
from tractor_parts import RearWheel, FrontWheel, RearCurve, FrontCurve, ConnectingLine, FrontVerticalLine, \
    RearVerticalLine, HorizontalLine, CockpitVerticalLine, CockpitDiagonalLine, CockpitRoofLine, Chimney,ChimneyCircles
from PIL import Image, ImageDraw, ImageTk,ImageOps
from transform_tractor import move_tractor, scale_tractor, rotate_tractor, mirror_tractor

def reset_tractor(original_vertices, canvas, update_callback):
    update_callback(original_vertices, canvas)

def is_tractor_outside_canvas(vertices, canvas):
    canvas_width = canvas.winfo_width()
    canvas_height = canvas.winfo_height()

    for item in vertices:
        if len(item) == 4:
            x, y, _, _ = item
        elif len(item) == 5:
            x, y = item[0], item[1]

        if x < 0 or x > canvas_width or y < 0 or y > canvas_height:
            return True

    return False

def create_rotate_tab(notebook, tab_control, vertices, canvas, update_callback):
    rotate_frame = ttk.Frame(tab_control)
    tab_control.add(rotate_frame, text="Rotate")

    angle_label = tk.Label(rotate_frame, text="Angle:")
    angle_label.grid(row=0, column=0, padx=5, pady=5)
    angle_entry = tk.Entry(rotate_frame)
    angle_entry.grid(row=0, column=1, padx=5, pady=5)

    def on_rotate_click():
        try:
            angle = float(angle_entry.get())
            get_coordinates(notebook, lambda px, py: rotate_tractor(vertices, angle, (px, py), canvas, update_callback))
        except ValueError:
            tk.messagebox.showerror("Error", "Invalid angle. Please enter a valid number.")

    rotate_button = tk.Button(rotate_frame, text="Rotate Tractor", command=on_rotate_click)
    rotate_button.grid(row=1, columnspan=2, padx=5, pady=5)


def get_coordinates(notebook,callback):
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
            notebook.select(0)  # Switch back to the Drawing tab
        except ValueError:
            tk.messagebox.showerror("Error", "Invalid coordinates. Please enter valid numbers.")

    submit_button = tk.Button(coord_window, text="Submit", command=on_submit)
    submit_button.grid(row=2, columnspan=2, padx=5, pady=5)



def create_crop_tab(notebook, tab_control, canvas):
    crop_frame = ttk.Frame(tab_control)
    tab_control.add(crop_frame, text="Crop")

    left_label = tk.Label(crop_frame, text="Left:")
    left_label.grid(row=0, column=0, padx=5, pady=5)
    left_entry = tk.Entry(crop_frame)
    left_entry.grid(row=0, column=1, padx=5, pady=5)

    upper_label = tk.Label(crop_frame, text="Upper:")
    upper_label.grid(row=1, column=0, padx=5, pady=5)
    upper_entry = tk.Entry(crop_frame)
    upper_entry.grid(row=1, column=1, padx=5, pady=5)

    right_label = tk.Label(crop_frame, text="Right:")
    right_label.grid(row=2, column=0, padx=5, pady=5)
    right_entry = tk.Entry(crop_frame)
    right_entry.grid(row=2, column=1, padx=5, pady=5)

    lower_label = tk.Label(crop_frame, text="Lower:")
    lower_label.grid(row=3, column=0, padx=5, pady=5)
    lower_entry = tk.Entry(crop_frame)
    lower_entry.grid(row=3, column=1, padx=5, pady=5)

    def on_crop_click():
        try:
            left = int(left_entry.get())
            upper = int(upper_entry.get())
            right = int(right_entry.get())
            lower = int(lower_entry.get())
            img = Image.open("temp_tractor_image.png")
            img_cropped = ImageOps.crop(img, (left, upper, right, lower))
            img_cropped.save("temp_tractor_image.png")
            photo = ImageTk.PhotoImage(file="temp_tractor_image.png")
            canvas.delete("all")
            canvas.create_image(0, 0, image=photo, anchor=tk.NW)
            canvas.image = photo
            notebook.select(0)  # Switch back to the Drawing tab

        except ValueError:
            tk.messagebox.showerror("Error", "Invalid crop values. Please enter valid integers.")

    crop_button = tk.Button(crop_frame, text="Crop Image", command=on_crop_click)
    crop_button.grid(row=4, columnspan=2, padx=5, pady=5)

def create_move_tab(notebook, tab_control, vertices, canvas, update_callback):
    move_frame = ttk.Frame(tab_control)
    tab_control.add(move_frame, text="Move")

    def on_move_click():
        get_coordinates(lambda dx, dy: move_tractor(vertices, dx, dy, canvas, update_callback))

    move_button = tk.Button(move_frame, text="Move Tractor",
                            command=lambda: get_coordinates(notebook,
                                                            lambda dx, dy: move_tractor(vertices, dx, dy, canvas,
                                                                                        update_callback)))
    move_button.pack(padx=10, pady=10)

    reset_button = tk.Button(move_frame, text="Reset Tractor",
                             command=lambda: reset_tractor(original_vertices, canvas, update_callback))
    reset_button.pack(padx=10, pady=10)

def create_mirror_tab(notebook, tab_control, vertices, canvas, update_callback):
    mirror_frame = ttk.Frame(tab_control)
    tab_control.add(mirror_frame, text="Mirror")

    mirror_var = tk.StringVar()
    mirror_var.set("x")

    mirror_x_radio = tk.Radiobutton(mirror_frame, text="Mirror around X-axis", variable=mirror_var, value="x")
    mirror_x_radio.pack(padx=10, pady=5)

    mirror_y_radio = tk.Radiobutton(mirror_frame, text="Mirror around Y-axis", variable=mirror_var, value="y")
    mirror_y_radio.pack(padx=10, pady=5)

    def on_mirror_click():
        mirror_tractor(vertices, canvas, update_callback, axis=mirror_var.get())
        notebook.select(0)  # Switch back to the Drawing tab

    mirror_button = tk.Button(mirror_frame, text="Mirror Tractor",
                              command=on_mirror_click)
    mirror_button.pack(padx=10, pady=10)




def create_scale_tab(notebook, tab_control, vertices, canvas, update_callback):
    scale_frame = ttk.Frame(tab_control)
    tab_control.add(scale_frame, text="Scale")

    scale_label = tk.Label(scale_frame, text="Scale Factor:")
    scale_label.grid(row=0, column=0, padx=5, pady=5)
    scale_entry = tk.Entry(scale_frame)
    scale_entry.grid(row=0, column=1, padx=5, pady=5)

    def on_scale_click():
        try:
            scale_factor = float(scale_entry.get())
            if scale_factor <= 0:
                raise ValueError
            get_coordinates(notebook, lambda px, py: scale_tractor(vertices, scale_factor, (px, py), canvas, update_callback))
        except ValueError:
            tk.messagebox.showerror("Error", "Invalid scale factor. Please enter a positive number.")

    scale_button = tk.Button(scale_frame, text="Scale Tractor", command=on_scale_click)
    scale_button.grid(row=1, columnspan=2, padx=5, pady=5)



def create_scaled_image(vertices, scale_factor,offset_x=0, offset_y=0):
    img = Image.new("RGBA", (1000 * scale_factor, 800 * scale_factor), "white")
    draw = ImageDraw.Draw(img)

    last_point = None
    for item in vertices:
        if len(item) == 4:
            x, y, radius, bit = item
            draw_wheel(draw, (x * scale_factor) + offset_x, (y * scale_factor) + offset_y, radius * scale_factor, bit,
                       fill_color='#5b9bd5' if bit == 0 and item in front_curve.get_drawing_data() else '#41719C')
        elif len(item) == 5:
            x1, y1, x2, y2, bit = item
            if bit == 1:
                if last_point is not None:
                    draw.line([((x1 * scale_factor) + offset_x, (y1 * scale_factor) + offset_y), last_point],
                              fill='#000000', width=10 * scale_factor)
                draw.line([((x1 * scale_factor) + offset_x, (y1 * scale_factor) + offset_y),
                           ((x2 * scale_factor) + offset_x, (y2 * scale_factor) + offset_y)],
                          fill='#000000', width=10 * scale_factor)
                last_point = ((x2 * scale_factor) + offset_x, (y2 * scale_factor) + offset_y)
            elif bit == 2:
                draw.line([((x1 * scale_factor) + offset_x, (y1 * scale_factor) + offset_y),
                           ((x2 * scale_factor) + offset_x, (y2 * scale_factor) + offset_y)],
                          fill='#808080', width=5 * scale_factor)
                last_point = None
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

    img = img.resize((1000, 800), Image.ANTIALIAS)
    return img

def update_tractor_drawing(vertices, canvas=None, offset_x=0, offset_y=0):
    if is_tractor_outside_canvas(vertices, canvas):
        tk.messagebox.showerror("Error", "Tractor drawing is out of the window frame. Please adjust the position.")
        return

    img = create_scaled_image(vertices, scale_factor=4, offset_x=offset_x, offset_y=offset_y)
    img.save("temp_tractor_image.png")
    photo = ImageTk.PhotoImage(file="temp_tractor_image.png")
    canvas.delete("all")
    canvas.create_image(0, 0, image=photo, anchor=tk.NW)
    canvas.image = photo
    canvas.vertices = vertices

    # Draw the vertical lines of the chimneys
    for i in range(len(vertices) - 1):
        item1 = vertices[i]
        item2 = vertices[i + 1]
        if len(item1) == 5 and len(item2) == 5 and item1[-1] == 3 and item2[-1] == 3:
            canvas.create_line(item1[0], item1[1], item2[0], item2[1], fill='#000000', width=10)


def create_window(vertices, update_callback=None):
    scale_factor = 4
    window = tk.Tk()
    window.title("Tractor Drawing")
    window.geometry("1000x800")
    global original_vertices
    original_vertices = vertices.copy()


    img = Image.new("RGBA", (1000 * scale_factor, 800 * scale_factor), "white")
    draw = ImageDraw.Draw(img)

    # Create a Notebook (tabbed interface)
    notebook = ttk.Notebook(window)
    notebook.pack(fill='both', expand=True)

    # Create the Drawing tab
    drawing_frame = tk.Frame(notebook)
    notebook.add(drawing_frame, text="Drawing")

    # Create the canvas object
    canvas = tk.Canvas(drawing_frame, width=1000, height=800)
    canvas.pack()

    # Create the Move tab using the create_move_tab function
    create_move_tab(notebook, notebook, vertices, canvas, update_callback)
    # Create the Scale tab using the create_scale_tab function
    create_scale_tab(notebook, notebook, vertices, canvas, update_callback)
    # Create the Rotate tab using the create_rotate_tab function
    create_rotate_tab(notebook, notebook, vertices, canvas, update_callback)
    create_mirror_tab(notebook, notebook, vertices, canvas, update_callback)
    create_crop_tab(notebook, notebook, canvas)

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

def draw_curve(canvas, curve_data, color='black'):
    for i in range(len(curve_data)):
        x1, y1, cp1_x, cp1_y, x2, y2 = curve_data[i]
        canvas.create_line(x1, y1, cp1_x, cp1_y, fill=color, smooth=True)
        canvas.create_line(cp1_x, cp1_y, x2, y2, fill=color, smooth=True)
        canvas.create_line(x1, y1, cp1_x, cp1_y, x2, y2, fill=color, smooth=True, width=2)


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
    window = create_window(data, update_callback=update_tractor_drawing)

    window.mainloop()
