import tkinter as tk
from tkinter import ttk, messagebox




def apply_move(vertices, x_offset, y_offset):
    new_vertices = []
    for item in vertices:
        if len(item) == 4:
            new_vertices.append((item[0] + x_offset, item[1] + y_offset, item[2], item[3]))
        elif len(item) == 5:
            new_vertices.append((item[0] + x_offset, item[1] + y_offset, item[2] + x_offset, item[3] + y_offset, item[4]))
    return new_vertices

def move_tractor(vertices, dx, dy, canvas, update_callback):
    new_vertices = []
    for item in vertices:
        if len(item) == 4:
            x, y, radius, group = item
            new_vertices.append((x + dx, y + dy, radius, group))
        elif len(item) == 5:
            x1, y1, x2, y2, group = item
            new_vertices.append((x1 + dx, y1 + dy, x2 + dx, y2 + dy, group))
    update_callback(new_vertices, canvas)






