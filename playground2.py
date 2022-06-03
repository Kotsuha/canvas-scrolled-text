from tkinter import *
root=Tk()
root.geometry("800x600")
frame=Frame(root,width=300,height=300)
# frame.pack(expand=True, fill=BOTH) #.grid(row=0,column=0)
frame.pack()
canvas=Canvas(frame,bg='#FFFFFF',width=300,height=300,scrollregion=(0,0,500,500))
# hbar=Scrollbar(frame,orient=HORIZONTAL)
# hbar.pack(side=BOTTOM,fill=X)
# hbar.config(command=canvas.xview)
vbar=Scrollbar(frame,orient=VERTICAL)
vbar.pack(side=RIGHT,fill=Y)
vbar.config(command=canvas.yview)
canvas.config(width=300,height=300)
# canvas.config(xscrollcommand=hbar.set, yscrollcommand=vbar.set)
canvas.config(yscrollcommand=vbar.set)
canvas.pack(side=LEFT,expand=True,fill=BOTH)

# Add background
img = PhotoImage(file="img/myLogo2_1.png")
canvas.create_image(8, 8, anchor=NW, image=img)

# Add text
lorem = "Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua. Ut enim ad minim veniam, quis nostrud exercitation ullamco laboris nisi ut aliquip ex ea commodo consequat. Duis aute irure dolor in reprehenderit in voluptate velit esse cillum dolore eu fugiat nulla pariatur. Excepteur sint occaecat cupidatat non proident, sunt in culpa qui officia deserunt mollit anim id est laborum."
article = " ".join([lorem] * 2)
canvas.create_text(0, 0, anchor=NW, text=article, width=300)

root.mainloop()

# 參考 https://stackoverflow.com/questions/7727804/tkinter-using-scrollbars-on-a-canvas
