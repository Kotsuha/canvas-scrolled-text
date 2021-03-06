# Demo 1
# General testing with CanvasScrolledText

import cProfile
import random
from tkinter import *
from tkinter.font import Font

import numpy as np
from PIL import Image, ImageTk

from canvas_scrolled_text import CanvasScrolledText


WINDOW_SIZE = "640x480"
CANVAS_SIZE = [400, 300]
C = (  # https://colorhunt.co/palette/e9d5da8273974d4c7d363062
    "#E9D5DA",
    "#827397",
    "#4D4C7D",
    "#363062",
)


root = Tk()
root.geometry(WINDOW_SIZE)
root.configure(background=C[3])
title = Label(root, text="CanvasScrolledText", bg=C[3], fg="white", pady=8)
title.pack()
frame = Frame(root, borderwidth=0, highlightthickness=0, highlightbackground="white")
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


# lorem = "Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua. Ut enim ad minim veniam, quis nostrud exercitation ullamco laboris nisi ut aliquip ex ea commodo consequat. Duis aute irure dolor in reprehenderit in voluptate velit esse cillum dolore eu fugiat nulla pariatur. Excepteur sint occaecat cupidatat non proident, sunt in culpa qui officia deserunt mollit anim id est laborum."
lorem = """What is Lorem Ipsum?

Lorem Ipsum is simply dummy text of the printing and typesetting industry. Lorem Ipsum has been the industry's standard dummy text ever since the 1500s, when an unknown printer took a galley of type and scrambled it to make a type specimen book. It has survived not only five centuries, but also the leap into electronic typesetting, remaining essentially unchanged. It was popularised in the 1960s with the release of Letraset sheets containing Lorem Ipsum passages, and more recently with desktop publishing software like Aldus PageMaker including versions of Lorem Ipsum.

Where does it come from?

Contrary to popular belief, Lorem Ipsum is not simply random text. It has roots in a piece of classical Latin literature from 45 BC, making it over 2000 years old. Richard McClintock, a Latin professor at Hampden-Sydney College in Virginia, looked up one of the more obscure Latin words, consectetur, from a Lorem Ipsum passage, and going through the cites of the word in classical literature, discovered the undoubtable source. Lorem Ipsum comes from sections 1.10.32 and 1.10.33 of "de Finibus Bonorum et Malorum" (The Extremes of Good and Evil) by Cicero, written in 45 BC. This book is a treatise on the theory of ethics, very popular during the Renaissance. The first line of Lorem Ipsum, "Lorem ipsum dolor sit amet..", comes from a line in section 1.10.32.

The standard chunk of Lorem Ipsum used since the 1500s is reproduced below for those interested. Sections 1.10.32 and 1.10.33 from "de Finibus Bonorum et Malorum" by Cicero are also reproduced in their exact original form, accompanied by English versions from the 1914 translation by H. Rackham.

Why do we use it?

It is a long established fact that a reader will be distracted by the readable content of a page when looking at its layout. The point of using Lorem Ipsum is that it has a more-or-less normal distribution of letters, as opposed to using 'Content here, content here', making it look like readable English. Many desktop publishing packages and web page editors now use Lorem Ipsum as their default model text, and a search for 'lorem ipsum' will uncover many web sites still in their infancy. Various versions have evolved over the years, sometimes by accident, sometimes on purpose (injected humour and the like).

Where can I get some?

There are many variations of passages of Lorem Ipsum available, but the majority have suffered alteration in some form, by injected humour, or randomised words which don't look even slightly believable. If you are going to use a passage of Lorem Ipsum, you need to be sure there isn't anything embarrassing hidden in the middle of text. All the Lorem Ipsum generators on the Internet tend to repeat predefined chunks as necessary, making this the first true generator on the Internet. It uses a dictionary of over 200 Latin words, combined with a handful of model sentence structures, to generate Lorem Ipsum which looks reasonable. The generated Lorem Ipsum is therefore always free from repetition, injected humour, or non-characteristic words etc."""
article1 = lorem  # "\n\n".join([lorem] * 1) + "\n\n"
article2 = "\n\n--------\n\n" + article1
o = CanvasScrolledText(canvas, text_width=0, padx=16, pady=14, scrollx=True, scrolly=True, text=article1)
# o.set_debug(True)


p = cProfile.Profile()
p.runcall(print, "Test")
p.print_stats()
p.clear()


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

    def command_add_text():
        p.runcall(o.append_text, article2)
        p.print_stats()
        p.clear()

    def command_reset_text():
        p.runcall(o.set_text, article1)
        p.print_stats()
        p.clear()

    def command_random_text_style():
        p.runcall(random_text_style)
        p.print_stats()
        p.clear()

    def command_random_bg():
        p.runcall(random_bg)
        p.print_stats()
        p.clear()

    def command_scroll_down():
        p.runcall(o.scroll, 0, -10)
        p.print_stats()
        p.clear()

    def command_scroll_up():
        p.runcall(o.scroll, 0, 10)
        p.print_stats()
        p.clear()

    def command_scroll_right():
        p.runcall(o.scroll, 10, 0)
        p.print_stats()
        p.clear()

    def command_scroll_left():
        p.runcall(o.scroll, -10, 0)
        p.print_stats()
        p.clear()

    def command_toggle_debug():
        p.runcall(o.set_debug, not o.debug)
        p.print_stats()
        p.clear()

    def command_update_scroll():
        p.runcall(o.update_scroll)
        p.print_stats()
        p.clear()

    def command_print_tag():
        p.runcall(print, o.tag)
        p.print_stats()
        p.clear()

    # https://stackoverflow.com/questions/69846517/how-to-auto-wrap-widget-in-tkinter
    # https://stackoverflow.com/questions/42560585/how-do-i-center-text-in-the-tkinter-text-widget
    # ???????????? Text Widdget ?????????????????? wrap?????????????????????
    # (1) ????????????????????????????????????????????????????????????????????? Text Widget?????????????????????????????????????????? Text Widget ????????????????????????????????????????????? (??????????????????????????????) ??? tag_add()???
    # (2) ???????????? cursor hover ????????????????????? I ?????????Button master ????????? root ?????? text????????? Button ???????????? root ?????? pack()??????????????? text.window_create(INSERT, window=btn) ??????????????? Text Widget ?????????

    container = Text(root, wrap=WORD, width=1, height=6)
    container.tag_configure("center", justify=CENTER)
    buttons = [
        # ????????????????????????
        Button(root, text="Add Text", command=command_add_text),
        Button(root, text="Reset Text", command=command_reset_text),
        Button(root, text="Random Text Style", command=command_random_text_style),
        Button(root, text="Random BG", command=command_random_bg),
        Button(root, text="Scroll Down 10 px", command=command_scroll_down),
        Button(root, text="Scroll Up 10 px", command=command_scroll_up),
        Button(root, text="Scroll Right 10 px", command=command_scroll_right),
        Button(root, text="Scroll Left 10 px", command=command_scroll_left),
        Button(root, text="(Dev) Toggle Debug", command=command_toggle_debug),
        Button(root, text="(Dev) Update Scroll", command=command_update_scroll),
        Button(root, text="(Dev) Print Tag", command=command_print_tag),
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
