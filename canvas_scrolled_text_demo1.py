# Demo 1
# General testing with CanvasScrolledText

import random
from tkinter import *
from tkinter.font import Font
from canvas_scrolled_text import CanvasScrolledText

root = Tk()

root.geometry("800x600")
CANVAS_SIZE = [640, 480]
canvas = Canvas(root, width=CANVAS_SIZE[0], height=CANVAS_SIZE[1],
                background="#ffffdd")
canvas.pack()

bg_gallery = [
    PhotoImage(file="img/myLogo2_1.png"),
    PhotoImage(file="img/myLogo2_2.png"),
    PhotoImage(file="img/myLogo2_3.png"),
]
def get_bg_img():
    return random.choice(bg_gallery)
def get_bg_pos():
    x = CANVAS_SIZE[0] / 2 + random.randrange(-CANVAS_SIZE[0] / 4, CANVAS_SIZE[0] / 4)
    y = CANVAS_SIZE[1] / 2 + random.randrange(-CANVAS_SIZE[1] / 4, CANVAS_SIZE[1] / 4)
    return (x, y)
bg_x, bg_y = get_bg_pos()
bg_id = canvas.create_image(bg_x, bg_y, image=get_bg_img(), anchor = CENTER)



lorem = "Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua. Ut enim ad minim veniam, quis nostrud exercitation ullamco laboris nisi ut aliquip ex ea commodo consequat. Duis aute irure dolor in reprehenderit in voluptate velit esse cillum dolore eu fugiat nulla pariatur. Excepteur sint occaecat cupidatat non proident, sunt in culpa qui officia deserunt mollit anim id est laborum."
article = " ".join([lorem] * 2)
o = CanvasScrolledText(
    canvas, CANVAS_SIZE, text_width=0, scrollx=True, scrolly=True, text=article)
o.set_debug(True)


def create_buttons():

    def random_font():
        # Random color
        rand_color = random.choice(
            ["red", "orange", "yellow", "green", "blue", "indigo", "violet"])
        canvas.itemconfigure(o.id_text, fill=rand_color)
        # Random font
        rand_font_name = random.choice(
            ["Arial", "Comic Sans MS", "Fixedsys", "Georgia", "Times New Roman"])
        rand_font_size = random.choice([12, 18, 24, 32, 36])
        rand_font_weight = random.choice(["normal", "bold"])
        canvas.itemconfigure(o.id_text, font=Font(
            family=rand_font_name, size=rand_font_size, weight=rand_font_weight))
        o.update_debug_rect()

    def random_bg():
        bg_x, bg_y = get_bg_pos()
        bg_img = get_bg_img()
        canvas.itemconfigure(bg_id, image=bg_img)
        canvas.coords(bg_id, bg_x, bg_y)

    button_frame = Frame(root)
    button_frame.pack(fill=X)
    buttons = [
        # 加按鈕加這裡即可
        Button(button_frame, text="Add Text", command=lambda: o.append_text(article)),
        Button(button_frame, text="Reset Text", command=lambda: o.set_text(article)),
        Button(button_frame, text="Print Tag", command=lambda: print(o.tag)),
        Button(button_frame, text="Random Font", command=random_font),
        Button(button_frame, text="Random BG", command=random_bg),
        Button(button_frame, text="Scroll (0, 0)", command=lambda: o.scroll(0, 0)),
        Button(button_frame, text="Scroll (10, 0)", command=lambda: o.scroll(10, 0)),
        Button(button_frame, text="Scroll (-10, 0)", command=lambda: o.scroll(-10, 0)),
        Button(button_frame, text="Scroll (0, 10)", command=lambda: o.scroll(0, 10)),
        Button(button_frame, text="Scroll (0, -10)", command=lambda: o.scroll(0, -10)),
        Button(button_frame, text="Toggle Debug", command=lambda: o.set_debug(not o.debug)),
    ]
    for i in range(len(buttons)):
        buttons[i].grid(row=0, column=i+1)

    button_frame.grid_columnconfigure(0, weight=1)
    button_frame.grid_columnconfigure(len(buttons)+1, weight=1)


create_buttons()

print("before mainloop()")
root.mainloop()
print("after mainloop()")
