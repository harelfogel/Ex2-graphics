import tkinter as tk
from tkinter import ttk, messagebox
import math

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


def scale_tractor(vertices, scale_factor, pivot, canvas, update_callback):
    new_vertices = []

    for item in vertices:
        if len(item) == 4:
            x, y, radius, group = item
            dx = x - pivot[0]
            dy = y - pivot[1]
            new_x = pivot[0] + dx * scale_factor
            new_y = pivot[1] + dy * scale_factor
            new_radius = radius * scale_factor
            new_vertices.append((new_x, new_y, new_radius, group))
        elif len(item) == 5:
            x1, y1, x2, y2, group = item
            dx1 = x1 - pivot[0]
            dy1 = y1 - pivot[1]
            dx2 = x2 - pivot[0]
            dy2 = y2 - pivot[1]
            new_x1 = pivot[0] + dx1 * scale_factor
            new_y1 = pivot[1] + dy1 * scale_factor
            new_x2 = pivot[0] + dx2 * scale_factor
            new_y2 = pivot[1] + dy2 * scale_factor
            new_vertices.append((new_x1, new_y1, new_x2, new_y2, group))

    update_callback(new_vertices, canvas)

def rotate_tractor(vertices, angle, pivot, canvas, update_callback):
    new_vertices = []
    angle_rad = math.radians(angle)

    for item in vertices:
        if len(item) == 4:
            x, y, radius, group = item
            dx = x - pivot[0]
            dy = y - pivot[1]
            new_x = pivot[0] + (dx * math.cos(angle_rad) - dy * math.sin(angle_rad))
            new_y = pivot[1] + (dx * math.sin(angle_rad) + dy * math.cos(angle_rad))
            new_vertices.append((new_x, new_y, radius, group))
        elif len(item) == 5:
            x1, y1, x2, y2, group = item
            dx1 = x1 - pivot[0]
            dy1 = y1 - pivot[1]
            dx2 = x2 - pivot[0]
            dy2 = y2 - pivot[1]
            new_x1 = pivot[0] + (dx1 * math.cos(angle_rad) - dy1 * math.sin(angle_rad))
            new_y1 = pivot[1] + (dx1 * math.sin(angle_rad) + dy1 * math.cos(angle_rad))
            new_x2 = pivot[0] + (dx2 * math.cos(angle_rad) - dy2 * math.sin(angle_rad))
            new_y2 = pivot[1] + (dx2 * math.sin(angle_rad) + dy2 * math.cos(angle_rad))
            new_vertices.append((new_x1, new_y1, new_x2, new_y2, group))

    update_callback(new_vertices, canvas)

def mirror_tractor(vertices, canvas, update_callback, axis="x"):
    new_vertices = []
    for item in vertices:
        if len(item) == 4:
            x, y, radius, group = item
            if axis == "x":
                new_vertices.append((canvas.winfo_width() - x, y, radius, group))
            else:
                new_vertices.append((x, canvas.winfo_height() - y, radius, group))
        elif len(item) == 5:
            x1, y1, x2, y2, group = item
            if axis == "x":
                new_vertices.append((canvas.winfo_width() - x1, y1, canvas.winfo_width() - x2, y2, group))
            else:
                new_vertices.append((x1, canvas.winfo_height() - y1, x2, canvas.winfo_height() - y2, group))
    update_callback(new_vertices, canvas)

