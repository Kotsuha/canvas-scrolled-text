# Demo 2
# Minimal code to use CanvasScrolledText

from tkinter import *

from canvas_scrolled_text import CanvasScrolledText

root = Tk()

CAN_WIDTH = 400
CAN_HEIGHT = 300
canvas = Canvas(root, width=CAN_WIDTH, height=CAN_HEIGHT)
canvas.pack()

lorem = "Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua. Ut enim ad minim veniam, quis nostrud exercitation ullamco laboris nisi ut aliquip ex ea commodo consequat. Duis aute irure dolor in reprehenderit in voluptate velit esse cillum dolore eu fugiat nulla pariatur. Excepteur sint occaecat cupidatat non proident, sunt in culpa qui officia deserunt mollit anim id est laborum."
article = "\n\n".join([lorem] * 3)
o = CanvasScrolledText(canvas, [CAN_WIDTH, CAN_HEIGHT], text=article)

root.mainloop()
