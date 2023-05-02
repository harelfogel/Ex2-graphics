import tkinter as tk
from tkinter import ttk, messagebox, filedialog
from PIL import Image, ImageDraw, ImageTk, ImageOps
from tractor_parts import FrontCurve, FrontWheel
from transform_tractor import mirror_tractor, rotate_tractor, move_tractor, scale_tractor


def create_help_tab(parent, notebook, vertices, canvas, update_callback):
    help_frame = tk.Frame(notebook)
    notebook.add(help_frame, text="Help")

    help_text = tk.Text(help_frame, wrap=tk.WORD, padx=10, pady=10, width=80, height=30)
    help_text.pack(expand=True, fill='both')

    help_content = """
    Move tab:
    - Use the "Manual" option to move the tractor by entering the desired X and Y coordinates.
    - Use the X and Y sliders to move the tractor horizontally and vertically by the mouse. You can Click on the mouse and drag the tractor vertically and horizontally.

    Scale tab:
    - Use the slider to scale the tractor proportionally.
    - You can also enter a custom scale factor in the input box.

    Rotate tab:
    - You can  enter a custom rotation angle in the input box.

    Mirror tab:
    - Use the "Horizontal" and "Vertical" buttons to flip the tractor horizontally and vertically.

    Crop tab:
    - "Crop" button: Automatically removes any white space around the tractor image.
    - "Manual" crop: Use the Top, Bottom, Left, and Right input boxes to enter custom crop values for each side of the tractor image. Press the "Apply" button to apply the manual crop.

    Download tab:
    - Use the "Upload" button to save the tractor image as a new data file.

    Reset tab:
    - Use the "Reset" button to reset the tractor image to its original state.

    Exit tab:
    - Use the "Exit" button to exit the application and save the changes to the tractor image.
    """

    help_text.insert(tk.INSERT, help_content)
    help_text.config(state=tk.DISABLED)


def create_upload_tab(notebook, tab_control, data_filename):
    upload_frame = ttk.Frame(tab_control)
    tab_control.add(upload_frame, text="Download")

    def on_download_click():
        try:
            save_file_path = filedialog.asksaveasfilename(defaultextension=".txt", filetypes=[("Text Files", "*.txt"), ("All Files", "*.*")])
            if not save_file_path:
                return

            with open(data_filename, 'r') as source_file:
                with open(save_file_path, 'w') as destination_file:
                    destination_file.write(source_file.read())

            tk.messagebox.showinfo("Success", "Tractor data file has been successfully downloaded.")
        except Exception as e:
            tk.messagebox.showerror("Error", f"An error occurred while downloading the file: {str(e)}")

    download_button = tk.Button(upload_frame, text="Download Tractor Data", command=on_download_click)
    download_button.pack(padx=150, pady=10)



def draw_wheel(draw, x, y, radius, bit, fill_color):
    if bit == 0:
        draw.ellipse([(x - radius, y - radius), (x + radius, y + radius)], outline=fill_color, width=40)

def change_cursor(event, canvas, cursor_type):
    canvas.config(cursor=cursor_type)

def create_exit_tab(notebook, parent, vertices, canvas, update_callback=None):
    exit_frame = ttk.Frame(notebook)
    notebook.add(exit_frame, text="Exit")

    def confirm_exit():
        response = messagebox.askyesno("Exit", "Are you sure you want to exit?")
        if response:
            parent.winfo_toplevel().destroy()

    exit_button = tk.Button(exit_frame, text="Exit Program", command=confirm_exit)
    exit_button.pack(padx=10, pady=10)




def reset_tractor(original_vertices, canvas, update_callback,notebook):
    update_callback(original_vertices, canvas)
    notebook.select(0)  # Switch back to the Drawing tab

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

def create_reset_tab(notebook, tab_control, vertices, canvas, update_callback):
    reset_frame = ttk.Frame(tab_control)
    tab_control.add(reset_frame, text="Reset")

    reset_button = tk.Button(reset_frame, text="Reset Tractor",
                             command=lambda: reset_tractor(original_vertices, canvas, update_callback,notebook))
    reset_button.pack(padx=10, pady=10)


def create_crop_tab(notebook, tab_control, canvas):
    crop_frame = ttk.Frame(tab_control)
    tab_control.add(crop_frame, text="Crop")

    def on_manual_crop():
        canvas.bind("<Button-1>", start_crop)
        canvas.bind("<B1-Motion>", drag_crop)
        canvas.bind("<ButtonRelease-1>", end_crop)
        notebook.select(0)  # Switch back to the Drawing tab

    help_label = tk.Label(crop_frame, text="For manual cropping using the mouse please enter: ")
    help_label.grid(row=0, column=0, padx=5, pady=20)

    left_label = tk.Label(crop_frame, text="Left:")
    left_label.grid(row=1, column=0, padx=12, pady=5)
    left_entry = tk.Entry(crop_frame)
    left_entry.grid(row=1, column=1, padx=12, pady=5)

    upper_label = tk.Label(crop_frame, text="Upper:")
    upper_label.grid(row=2, column=0, padx=12, pady=5)
    upper_entry = tk.Entry(crop_frame)
    upper_entry.grid(row=2, column=1, padx=12, pady=5)

    right_label = tk.Label(crop_frame, text="Right:")
    right_label.grid(row=3, column=0, padx=12, pady=5)
    right_entry = tk.Entry(crop_frame)
    right_entry.grid(row=3, column=1, padx=12, pady=5)

    lower_label = tk.Label(crop_frame, text="Lower:")
    lower_label.grid(row=4, column=0, padx=12, pady=5)
    lower_entry = tk.Entry(crop_frame)
    lower_entry.grid(row=4, column=1, padx=12, pady=5)

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
    crop_button.grid(row=6, columnspan=7, padx=150, pady=10)
    manual_crop_button = tk.Button(crop_frame, text="Manual Crop", command=on_manual_crop)
    manual_crop_button.grid(row=0, columnspan=7, padx=300, pady=5)



def start_crop(event):
    canvas = event.widget
    canvas.start_x = event.x
    canvas.start_y = event.y
    canvas.crop_rectangle = canvas.create_rectangle(event.x, event.y, event.x, event.y, outline="red")


def drag_crop(event):
    canvas = event.widget
    if canvas.crop_rectangle is not None:
        canvas.delete(canvas.crop_rectangle)
        max_y = max([vertex[1] for vertex in canvas.vertices])  # Get the largest Y value of the vertices
        fixed_lower_y = max(canvas.start_y, max_y)
        canvas.crop_rectangle = canvas.create_rectangle(canvas.start_x, canvas.start_y, event.x, fixed_lower_y, outline="red")

def end_crop(event):
    canvas = event.widget
    if canvas.crop_rectangle is not None:
        x1, y1, x2, y2 = canvas.coords(canvas.crop_rectangle)
        max_y = max([vertex[1] for vertex in canvas.vertices])  # Get the largest Y value of the vertices
        fixed_lower_y = max(y1, max_y)

        img = Image.open("temp_tractor_image.png")
        img_cropped = img.crop((x1, y1, x2, fixed_lower_y))
        img_cropped.save("temp_tractor_image.png")

        photo = ImageTk.PhotoImage(file="temp_tractor_image.png")
        canvas.delete("all")
        canvas.create_image(0, 0, image=photo, anchor=tk.NW)
        canvas.image = photo
        canvas.delete(canvas.crop_rectangle)
        canvas.crop_rectangle = None


def create_move_tab(notebook, tab_control, vertices, canvas, update_callback):
    move_frame = ttk.Frame(tab_control)
    tab_control.add(move_frame, text="Move")

    def on_move_click():
        get_coordinates(notebook, lambda dx, dy: move_tractor(vertices, dx, dy, canvas, update_callback))

    move_button = tk.Button(move_frame, text="Move Tractor by Points",
                            command=lambda: get_coordinates(notebook,
                                                            lambda dx, dy: move_tractor(vertices, dx, dy, canvas,
                                                                                        update_callback)))
    move_button.pack(padx=10, pady=10)

    def on_canvas_click(event):
        canvas.start_x = event.x
        canvas.start_y = event.y

    def on_canvas_release(event):
        dx = event.x - canvas.start_x
        dy = event.y - canvas.start_y
        move_tractor(vertices, dx, dy, canvas, update_callback)

    canvas.bind("<Button-1>", on_canvas_click)
    canvas.bind("<ButtonRelease-1>", on_canvas_release)


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
    front_wheel = FrontWheel(x=400, y=450, outer_radius=40, inner_radius=20)
    front_curve = FrontCurve(front_wheel)


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
    canvas.create_image(0, 0, image=photo, anchor=tk.NW, tags="tractor_image")  # Add the "tractor_image" tag
    canvas.image = photo
    canvas.vertices = vertices

    # Draw the vertical lines of the chimneys
    for i in range(len(vertices) - 1):
        item1 = vertices[i]
        item2 = vertices[i + 1]
        if len(item1) == 5 and len(item2) == 5 and item1[-1] == 3 and item2[-1] == 3:
            canvas.create_line(item1[0], item1[1], item2[0], item2[1], fill='#000000', width=10)


def create_window(vertices,data_filename, update_callback=None):
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
    create_upload_tab(notebook, notebook, data_filename)
    create_help_tab(notebook, notebook, vertices, canvas, update_callback)
    create_reset_tab(notebook, notebook, vertices, canvas, update_callback)
    create_exit_tab(notebook, notebook, vertices, canvas, update_callback)


    img = create_scaled_image(vertices, scale_factor)
    img.save("temp_tractor_image.png")
    photo = ImageTk.PhotoImage(file="temp_tractor_image.png")

    # Create the Move tab
    canvas.create_image(0, 0, image=photo, anchor=tk.NW)
    canvas.image = photo
    canvas.vertices = vertices
    # Add event bindings for the tractor image
    canvas.tag_bind("tractor_image", "<Enter>", lambda e: change_cursor(e, canvas, "fleur"))
    canvas.tag_bind("tractor_image", "<Leave>", lambda e: change_cursor(e, canvas, "arrow"))

    def on_canvas_motion(event):
        x, y = event.x, event.y
        img_coords = canvas.coords("tractor_image")

        if not img_coords:  # Check if img_coords is empty
            change_cursor(event, canvas, "arrow")
            return

        img_width = canvas.image.width()
        img_height = canvas.image.height()

        if img_coords[0] <= x <= img_coords[0] + img_width and img_coords[1] <= y <= img_coords[1] + img_height:
            change_cursor(event, canvas, "crosshair")
        else:
            change_cursor(event, canvas, "arrow")


    canvas.bind("<Motion>", on_canvas_motion)
    return window