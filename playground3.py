import random
import time
from tkinter import *

from PIL import Image, ImageTk


root = Tk()


images = []  # to hold the newly created image

def create_rectangle(x1, y1, x2, y2, **kwargs):
    if 'alpha' in kwargs:
        alpha = int(kwargs.pop('alpha') * 255)
        fill = kwargs.pop('fill')
        fill = root.winfo_rgb(fill) + (alpha,)
        image = Image.new('RGBA', (x2-x1, y2-y1), fill)
        images.append(ImageTk.PhotoImage(image))
        canvas.create_image(x1, y1, image=images[-1], anchor='nw')
    canvas.create_rectangle(x1, y1, x2, y2, **kwargs)


CAN_WIDTH = 400
CAN_HEIGHT = 300
canvas = Canvas(root, width=CAN_WIDTH, height=CAN_HEIGHT)
canvas.pack()

lorem = "Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua. Ut enim ad minim veniam, quis nostrud exercitation ullamco laboris nisi ut aliquip ex ea commodo consequat. Duis aute irure dolor in reprehenderit in voluptate velit esse cillum dolore eu fugiat nulla pariatur. Excepteur sint occaecat cupidatat non proident, sunt in culpa qui officia deserunt mollit anim id est laborum."
article = "\n\n".join([lorem] * 10)

TARGET_FPS = 60
TARGET_FRAME_TIME = int(1000 / TARGET_FPS)
fps = 0
frame_time = 9999
id_text = canvas.create_text(0, 0, anchor=NW, text=article, width=CAN_WIDTH)
id_fps = canvas.create_text(4, 4, anchor=NW, text=f"{fps} FPS ({frame_time} ms)", fill="white", font=("Fixedsys", 18))
tmp = canvas.bbox(id_fps)
tmp = [2, tmp[1], CAN_WIDTH, tmp[3]]
create_rectangle(*tmp, fill="black", alpha=.6)
canvas.tag_raise(id_fps)
last_time = 0

v = 0
a = 0.98
p = 0


def update():
    global last_time, frame_time, fps, v, a, p

    curr_time = time.time() * 1000
    delta_time = curr_time - last_time
    last_time = curr_time

    frame_time = round(delta_time, 2)
    fps = round(1000 / delta_time, 2)
    canvas.itemconfigure(id_fps, text=f"{fps} FPS ({frame_time} ms)")

    v = v + a
    p = p + v
    if p > CAN_HEIGHT:
        p = CAN_HEIGHT
        v = v * -1 * random.uniform(1, 1.1)
    canvas.moveto(id_text, 0, p)
    root.after(TARGET_FRAME_TIME, update)


update()

root.mainloop()
