from dataclasses import dataclass
from functools import partial
from tkinter import *


class MyColor:  # https://colorhunt.co/palette/eb5353f9d92336ae7c187498
    R = "#EB5353"
    Y = "#F9D923"
    G = "#36AE7C"
    B = "#187498"


lorem = "Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua. Ut enim ad minim veniam, quis nostrud exercitation ullamco laboris nisi ut aliquip ex ea commodo consequat. Duis aute irure dolor in reprehenderit in voluptate velit esse cillum dolore eu fugiat nulla pariatur. Excepteur sint occaecat cupidatat non proident, sunt in culpa qui officia deserunt mollit anim id est laborum."


class OPTION:
    """option 名稱常數 (不一定是 Tkinter 真正的 option)
    """
    WIDTH = "width"
    HEIGHT = "height"
    HIGHLIGHT_THICKNESS = "highlightthickness"
    BORDER_WIDTH = "borderwidth"
    # Fake options
    COORDS = "coords"
    BBOX = "bbox"
    MOVE = "move"
    MOVETO = "moveto"


@dataclass
class OptionInfo:
    name: str
    gettable: bool
    settable: bool
    fake: bool


OptionTable = {
    OPTION.WIDTH: OptionInfo(
        name=OPTION.WIDTH,
        gettable=True,
        settable=True,
        fake=False
    ),
    OPTION.HEIGHT: OptionInfo(
        name=OPTION.HEIGHT,
        gettable=True,
        settable=True,
        fake=False
    ),
    OPTION.HIGHLIGHT_THICKNESS: OptionInfo(
        name=OPTION.HIGHLIGHT_THICKNESS,
        gettable=True,
        settable=True,
        fake=False
    ),
    OPTION.BORDER_WIDTH: OptionInfo(
        OPTION.BORDER_WIDTH,
        True,
        True,
        False
    ),
    OPTION.COORDS: OptionInfo(
        name=OPTION.COORDS,
        gettable=True,
        settable=True,
        fake=True
    ),
    OPTION.BBOX: OptionInfo(
        name=OPTION.BBOX,
        gettable=True,
        settable=False,
        fake=True
    ),
    OPTION.MOVE: OptionInfo(
        name=OPTION.MOVE,
        gettable=False,
        settable=True,
        fake=True
    ),
    OPTION.MOVETO: OptionInfo(
        name=OPTION.MOVETO,
        gettable=False,
        settable=True,
        fake=True
    ),
}


root = Tk()
root.geometry("1080x760")
root.configure(background=MyColor.B)
root.configure(padx=4, pady=4)
Label(root, text="Canvas 座標測試 (記得把 Windows DPI Scale 調成 100%)", font=("bold", 12), bg=MyColor.B, fg="white").pack()

canvas = Canvas(root, width=400, height=200, bg=MyColor.R)
canvas.pack(pady=4)
rect = canvas.create_rectangle(0, 0, 40, 40, fill=MyColor.Y, outline="black")


class WidgetOptionValInspector:
    def __init__(self, master: Widget, label_text: str, target_widget: Widget, option: str) -> None:
        frame = Frame(master)
        label = Label(frame, text=label_text, width=32, anchor=W)
        label2_var = StringVar()
        label2 = Label(frame, textvariable=label2_var, text="?", width=16, justify=CENTER, relief=SUNKEN, bd=1)
        entry_var = StringVar()
        entry = Entry(frame, textvariable=entry_var, width=16, justify=CENTER)
        button = Button(frame, text="Set", command=self.onclick)
        entry.bind("<Return>", lambda _: self.onclick())

        if not OptionTable[option].gettable:
            label2.configure(state=DISABLED)

        if not OptionTable[option].settable:
            entry.configure(state=DISABLED)
            button.configure(state=DISABLED)
            
        self.target_widget = target_widget
        self.option = option
        self.frame = frame
        self.label = label
        self.label2 = label2
        self.entry = entry
        self.button = button
        self.entry_var = entry_var
        self.label2_var = label2_var

        self.keep_update_curval()

    def pack(self):
        self.frame.pack()
        self.label.pack(side=LEFT)
        self.label2.pack(side=LEFT)
        self.entry.pack(side=LEFT)
        self.button.pack(side=LEFT)

    def onclick(self):
        val = self.entry_var.get()
        self._set(val)

    def keep_update_curval(self):
        curval = self._get()
        self.label2_var.set(curval)
        canvas.after(1000, self.keep_update_curval)

    def _get(self):
        if not OptionTable[self.option].gettable:
            return None
        val = self.target_widget.cget(self.option)
        return val

    def _set(self, val):
        if not OptionTable[self.option].settable:
            return
        self.target_widget.configure({self.option: val})


class CanvasItemOptionValInspector(WidgetOptionValInspector):
    def __init__(self, master: Widget, label: str, target_widget: Widget, item_id: str, option: str) -> None:
        self.item_id = item_id
        super().__init__(master, label, target_widget, option)

    @property
    def canvas(self) -> Canvas:
        return self.target_widget

    def _get(self):
        if not OptionTable[self.option].gettable:
            return None
        if self.option == OPTION.WIDTH:
            val = self.canvas.itemcget(self.item_id, self.option)
            return val
        if self.option == OPTION.COORDS:
            val = self.canvas.coords(self.item_id)
            return val
        elif self.option == OPTION.BBOX:
            val = self.canvas.bbox(self.item_id)
            return val

    def _set(self, val):
        if not OptionTable[self.option].settable:
            return
        if self.option == OPTION.WIDTH:
            self.canvas.itemconfigure(self.item_id, {self.option: val})
        if self.option == OPTION.COORDS:
            coords = [float(x) for x in val.split(" ")]
            self.canvas.coords(self.item_id, coords)
        elif self.option == OPTION.MOVE:
            pos = [float(x) for x in val.split(" ")]
            self.canvas.move(self.item_id, pos[0], pos[1])
        elif self.option == OPTION.MOVETO:
            pos = [float(x) for x in val.split(" ")]
            self.canvas.moveto(self.item_id, pos[0], pos[1])


def create_inspectors():
    container = Frame(root)
    container.pack()
    inspectors: list[WidgetOptionValInspector] = []
    inspectors.append(WidgetOptionValInspector(container, f"Canvas {OPTION.WIDTH}", canvas, OPTION.WIDTH))
    inspectors.append(WidgetOptionValInspector(container, f"Canvas {OPTION.HEIGHT}", canvas, OPTION.HEIGHT))
    inspectors.append(WidgetOptionValInspector(container, f"Canvas {OPTION.HIGHLIGHT_THICKNESS}", canvas, OPTION.HIGHLIGHT_THICKNESS))
    inspectors.append(WidgetOptionValInspector(container, f"Canvas {OPTION.BORDER_WIDTH}", canvas, OPTION.BORDER_WIDTH))
    inspectors.append(CanvasItemOptionValInspector(container, f"Rect border {OPTION.WIDTH}", canvas, rect, OPTION.WIDTH))
    inspectors.append(CanvasItemOptionValInspector(container, f"Rect {OPTION.COORDS}", canvas, rect, OPTION.COORDS))
    inspectors.append(CanvasItemOptionValInspector(container, f"Rect {OPTION.BBOX}", canvas, rect, OPTION.BBOX))
    inspectors.append(CanvasItemOptionValInspector(container, f"Rect {OPTION.MOVE}", canvas, rect, OPTION.MOVE))
    inspectors.append(CanvasItemOptionValInspector(container, f"Rect {OPTION.MOVETO}", canvas, rect, OPTION.MOVETO))
    for x in inspectors:
        x.pack()


create_inspectors()
conclusion_text = """
結論：
• Canvas width border highlightthickness 三個值互相獨立
• Canvas 總共的寬等於 width + border * 2 + highlightthickness * 2
• Canvas 總共的高類推
• Canvas Space 座標原點 (0, 0) 從「總共的寬高」左上角開始算
• create_rectangle 時填的 x0 y0 x1 y1 會變成 coords
• rect coords x0 y0 爲左上座標，x1 y1 爲右下座標外擴 1px (要在 rect border width 爲 0 時才能正確觀察到，否則會被 border 誤導)
• coords 0 0 10 10 則寬爲 10，但預設值 rect border width 爲 1，容易誤以爲 coords 0 0 10 10 則寬爲 11
• rect border 的位置類似 Photoshop 的 Selection -> Stroke -> Location: Center (而不是 Inside 或 Outside)
• coords 和 rect border width 互相獨立
• 如果 Rect x0 y0 爲 0 0，且 Canvas border 或 highlightthickness 大於 0，Rect 會被蓋住一部分
• 若 Rect border width 爲 0，則 bbox 會是 coords 外擴 1px。例如 coords 0 0 9 9，bbox -1 -1 10 10
• rect bbox 會受 rect border width 影響
• 結論，爲了單純些，建議 Canvas 不要設 border highlightthickness。Rect border width 設不設大概無所謂。
"""
Label(root, text=conclusion_text, font=("normal", 12), bg=MyColor.B, fg="white", justify=LEFT).pack()

root.mainloop()
