
# #!/usr/bin/python

# import tkinter as tk
# from PIL import Image, ImageTk

# window = tk.Tk()
# window.geometry("640x640")
# # Code to add widgets will go here...

# frame = tk.Frame(window, bd=8, bg="black")
# frame.pack()

# text1 = tk.Text(frame)
# text1.pack()

# canvas = tk.Canvas(frame, border=4, bg="red")
# canvas.pack()
# canvas.place(bordermode=tk.INSIDE, relheight=0.8, relwidth=0.8)

# # img = ImageTk.PhotoImage(Image.open("myLogo2_3.png"))

# # # Add image to the Canvas Items
# # canvas.create_image(10,10,anchor=tk.NW,image=img)

# # bgimg = ImageTk.PhotoImage(file = "myLogo2_3.png")

# window.mainloop()


# Import module 
from ctypes import windll
import random
from tkinter import *
from datetime import datetime
  
# Create object 
root = Tk()
  
# Adjust size 
root.geometry("800x600")
  
# Add image file
bg = PhotoImage(file = "myLogo2_3.png")
  
# Create Canvas
canvas = Canvas( root, width = 400,
                 height = 300, background="yellow")

is_down = False
last_down_pos = [0, 0]
last_down_ct_pos = [0, 0]
def on_drag(e):
    print(e)
    global cty
    global last_down_pos
    global is_down
    global last_down_ct_pos
    if is_down is False:
        is_down = True
        last_down_pos = [e.x, e.y]
        last_down_ct_pos = [ctx, cty]
    else:
        drag = [e.x - last_down_pos[0], e.y - last_down_pos[1]]
        new_y = last_down_ct_pos[1] + drag[1]
        box = canvas.bbox(canvas_text)
        w, h = box[2]-box[0], box[3]-box[1]
        print(box)
        if new_y < 8:
            new_y = 8
        if new_y + h > 300 - 8:
            new_y = 300 - 8 - h
        cty = new_y

        canvas.moveto("foo", y=cty)
        # canvas.moveto(canvas_text, x=ctx, y=cty)
        pass

def on_release(e):
    global is_down
    print("ButtonRelease-1")
    is_down = False
    pass

canvas.bind("<B1-Motion>", on_drag)
canvas.bind('<ButtonRelease-1>', on_release)

# canvas1.pack(fill = "both", expand = True)
canvas.pack()
  
# Display image
canvas.create_image( 0, 0, image = bg, 
                     anchor = "nw")
  
# Add Text
# canvas1.create_text( 200, 250, text = "Welcome")
ctx = 32
cty = 32
# https://stackoverflow.com/questions/9408195/python-tkinter-text-background
canvas_text = canvas.create_text( ctx, cty, anchor = "nw", text = "Hello World", width=350, tags=("foo",))
canvas_text_bg = canvas.create_rectangle(canvas.bbox(canvas_text), fill="red", tags=("foo",))
canvas.tag_lower(canvas_text_bg, canvas_text)

fake_text = "!!!!!"

def xxxxx():
    global fake_text
    fake_text = fake_text + "How to enable Dark Mode on Facebook, Amazon, YouTube, \nGoogle Search, Wikipedia, Twitter and many other websites?"
    canvas.itemconfigure(canvas_text, text=fake_text)
    # print(canvas_text.winfo_width())
    # print(canvas_text.winfo_height())
    size = canvas.bbox(canvas_text)
    canvas.coords(canvas_text_bg, size)
    pass

def yyyyy():
    # size = random.choice(["400x400", "500x500", "600x600"])
    # root.geometry(size)
    global cty
    cty = cty + 1
    canvas.moveto(canvas_text, x=ctx, y=cty)
    pass

def zzzzz():
    # new_width = random.choice([10, 20, 30, 40, 50])
    # new_bg = random.choice(["red", "blue", "green"])
    # button1.config(width=new_width)
    # button1.config(bg=new_bg)
    global cty
    cty = cty - 1
    canvas.moveto(canvas_text, x=ctx, y=cty)
    pass

# Create Buttons
button1 = Button( root, text = "Exit", command=zzzzz, width=50)
button3 = Button( root, text = "Start", command=yyyyy)
button2 = Button( root, text = "Reset", command=xxxxx)
text1 = Text( root)
label1 = Label(root, text="This is a label...")



# Display Buttons
button1_canvas = canvas.create_window( 100, 10, 
                                       anchor = "nw",
                                       window = button1)
  
button2_canvas = canvas.create_window( 100, 40,
                                       anchor = "nw",
                                       window = button2)
  
button3_canvas = canvas.create_window( 100, 70, anchor = "nw",
                                       window = button3)

text_canvas = canvas.create_window( 100, 100, anchor = "nw",
                                       window = text1)

label_canvas = canvas.create_window( 40, 130, anchor = "nw",
                                       window = label1)


# Execute tkinter
root.mainloop()

print("after mainloop()")

