# Demo 1
# General testing with CanvasScrolledText

import random
from tkinter import *
from tkinter.font import Font

import numpy as np
from PIL import Image, ImageTk

from canvas_scrolled_text import CanvasScrolledText

C = (  # https://colorhunt.co/palette/e9d5da8273974d4c7d363062
    "#E9D5DA",
    "#827397",
    "#4D4C7D",
    "#363062",
)

WINDOW_SIZE = "640x480"
CANVAS_SIZE = [400, 300]
root = Tk()
root.geometry(WINDOW_SIZE)
root.configure(background=C[3])
title = Label(root, text="CanvasScrolledText", bg=C[3], fg="white", pady=8)
title.pack()
frame = Frame(root, borderwidth=0, highlightthickness=4, highlightbackground="white")
frame.pack()
canvas = Canvas(frame,
                width=CANVAS_SIZE[0], height=CANVAS_SIZE[1],
                background=C[1],
                borderwidth=0, highlightthickness=0)
canvas.pack()


def randbool():
    return bool(random.getrandbits(1))


bg_raw_imgs = [
    Image.open("img/myLogo2_1.png"),
    Image.open("img/myLogo2_2.png"),
    Image.open("img/myLogo2_3.png"),
]
opacity_choices = [0.3, 0.6, 1]
bg_gallery = []
for raw_img in bg_raw_imgs:
    if raw_img.mode != "RGBA":
        raw_img = raw_img.convert("RGBA")
    data = np.asanyarray(raw_img)
    data_alpha_bak = np.empty(data.shape[:2])
    # Bad
    for i in range(data.shape[0]):
        for j in range(data.shape[1]):
            data_alpha_bak[i, j] = data[i, j, 3]
    for opacity in opacity_choices:
        # Bad
        for i in range(data.shape[0]):
            for j in range(data.shape[1]):
                data[i, j, 3] = int(data_alpha_bak[i, j] * opacity)
        new_raw_img = Image.fromarray(data)
        tk_img = ImageTk.PhotoImage(new_raw_img)
        bg_gallery.append(tk_img)


def get_random_bg_img():
    return random.choice(bg_gallery)


def get_random_bg_pos():
    x = random.randint(CANVAS_SIZE[0] * 0.2, CANVAS_SIZE[0] * 0.8)
    y = random.randint(CANVAS_SIZE[1] * 0.2, CANVAS_SIZE[1] * 0.8)
    return [x, y]


canvas_bg = canvas.create_image(*get_random_bg_pos(), image=get_random_bg_img(), anchor=CENTER)


lorem = "Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua. Ut enim ad minim veniam, quis nostrud exercitation ullamco laboris nisi ut aliquip ex ea commodo consequat. Duis aute irure dolor in reprehenderit in voluptate velit esse cillum dolore eu fugiat nulla pariatur. Excepteur sint occaecat cupidatat non proident, sunt in culpa qui officia deserunt mollit anim id est laborum."
article = "\n\n".join([lorem] * 2) + "\n\n"
o = CanvasScrolledText(canvas, CANVAS_SIZE, text_width=0, scrollx=True, scrolly=True, text=article)
# o.set_debug(True)


def create_buttons():

    color_choices = ["red", "orange", "yellow", "green", "blue", "indigo", "violet", "black"]
    font_name_choices = ["Arial", "Comic Sans MS", "Fixedsys", "Georgia", "Times New Roman"]
    font_size_choices = [6, 12, 18, 24, 30, 36]
    font_weight_choices = ["normal", "bold"]

    def random_text_style():
        # Random color
        rand_color = random.choice(color_choices)
        canvas.itemconfigure(o.id_text, fill=rand_color)
        # Random font
        rand_font_name = random.choice(font_name_choices)
        rand_font_size = random.choice(font_size_choices)
        rand_font_weight = random.choice(font_weight_choices)
        rand_font = Font(family=rand_font_name, size=rand_font_size, weight=rand_font_weight)
        canvas.itemconfigure(o.id_text, font=rand_font)
        o.update_debug_rect()

    def random_bg():
        canvas.itemconfigure(canvas_bg, image=get_random_bg_img())
        canvas.coords(canvas_bg, *get_random_bg_pos())

    # https://stackoverflow.com/questions/69846517/how-to-auto-wrap-widget-in-tkinter
    # https://stackoverflow.com/questions/42560585/how-do-i-center-text-in-the-tkinter-text-widget
    # 這裡使用 Text Widdget 達成按鈕自動 wrap，遇到兩個問題
    # (1) 做完以後按鈕排列置左，我希望置中：由於現在使用 Text Widget，這個問題換句話說就是如何讓 Text Widget 文字置中。爬文結果：先插入文字 (我們的情況是插入按鈕) 再 tag_add()。
    # (2) 做完以後 cursor hover 按鈕呈現打字的 I 樣式：Button master 要傳入 root 不是 text。注意 Button 雖然傳入 root 但不 pack()，而是利用 text.window_create(INSERT, window=btn) 讓它呈現在 Text Widget 裡面。

    container = Text(root, wrap=WORD, width=1, height=6)
    container.tag_configure("center", justify=CENTER)
    buttons = [
        # 加按鈕加這裡即可
        Button(root, text="Add Text", command=lambda: o.append_text(article)),
        Button(root, text="Reset Text", command=lambda: o.set_text(article)),
        Button(root, text="Random Text Style", command=random_text_style),
        Button(root, text="Random BG", command=random_bg),
        Button(root, text="Scroll Right 10 px", command=lambda: o.scroll(10, 0)),
        Button(root, text="Scroll Left 10 px", command=lambda: o.scroll(-10, 0)),
        Button(root, text="Scroll Up 10 px", command=lambda: o.scroll(0, 10)),
        Button(root, text="Scroll Down 10 px", command=lambda: o.scroll(0, -10)),
        Button(root, text="(Dev) Toggle Debug", command=lambda: o.set_debug(not o.debug)),
        Button(root, text="(Dev) Update Scroll", command=o.update_scroll),
        Button(root, text="(Dev) Print Tag", command=lambda: print(o.tag)),
    ]
    for btn in buttons:
        container.window_create(INSERT, window=btn)
    container.tag_add("center", "1.0", END)
    container.configure(state=DISABLED)
    container.pack(side=BOTTOM, fill=X, expand=False)


create_buttons()

print("before mainloop()")
root.mainloop()
print("after mainloop()")
