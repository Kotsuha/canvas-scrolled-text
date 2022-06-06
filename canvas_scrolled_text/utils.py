from tkinter import Canvas
from PIL import Image, ImageTk


images = []  # to hold the newly created image


def create_rectangle(canvas: Canvas, x1, y1, x2, y2, **kwargs):
    ret = []
    if 'alpha' in kwargs:
        alpha = int(kwargs.pop('alpha') * 255)
        fill = kwargs.pop('fill')
        fill = canvas.master.winfo_rgb(fill) + (alpha,)
        image = Image.new('RGBA', (x2-x1, y2-y1), fill)
        images.append(ImageTk.PhotoImage(image))
        ret.append(canvas.create_image(x1, y1, image=images[-1], anchor='nw', **kwargs))
    ret.insert(0, canvas.create_rectangle(x1, y1, x2, y2, **kwargs))
    return ret


def restrict(val, minval, maxval):
    if val < minval:
        return minval
    if val > maxval:
        return maxval
    return val


