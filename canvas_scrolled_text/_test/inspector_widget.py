from dataclasses import dataclass
from tkinter import *


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
    OPTION.WIDTH: OptionInfo(name=OPTION.WIDTH, gettable=True, settable=True, fake=False),
    OPTION.HEIGHT: OptionInfo(name=OPTION.HEIGHT, gettable=True, settable=True, fake=False),
    OPTION.HIGHLIGHT_THICKNESS: OptionInfo(name=OPTION.HIGHLIGHT_THICKNESS, gettable=True, settable=True, fake=False),
    OPTION.BORDER_WIDTH: OptionInfo(OPTION.BORDER_WIDTH, True, True, False),
    OPTION.COORDS: OptionInfo(name=OPTION.COORDS, gettable=True, settable=True, fake=True),
    OPTION.BBOX: OptionInfo(name=OPTION.BBOX, gettable=True, settable=False, fake=True),
    OPTION.MOVE: OptionInfo(name=OPTION.MOVE, gettable=False, settable=True, fake=True),
    OPTION.MOVETO: OptionInfo(name=OPTION.MOVETO, gettable=False, settable=True, fake=True),
}


class WidgetOptionInspector:
    def __init__(self, master: Widget, label_text: str, widget: Widget, option: str) -> None:
        frame = Frame(master)
        label = Label(frame, text=label_text, width=32, anchor=W)
        label2_var = StringVar()
        label2 = Label(frame, textvariable=label2_var, text="?", width=16, justify=CENTER, relief=SUNKEN, bd=1)
        entry_var = StringVar()
        entry = Entry(frame, textvariable=entry_var, width=16, justify=CENTER)
        button = Button(frame, text="Set", command=self.set_value)
        entry.bind("<Return>", lambda _: self.set_value())

        if not OptionTable[option].gettable:
            label2.configure(state=DISABLED)

        if not OptionTable[option].settable:
            entry.configure(state=DISABLED)
            button.configure(state=DISABLED)

        self.widget = widget
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

    def keep_update_curval(self):
        curval = self._get()
        self.label2_var.set(curval)
        self.frame.after(1000, self.keep_update_curval)

    def set_value(self):
        val = self.entry_var.get()
        self._set(val)

    def _get(self):
        if not OptionTable[self.option].gettable:
            return None
        val = self.widget.cget(self.option)
        return val

    def _set(self, val):
        if not OptionTable[self.option].settable:
            return
        self.widget.configure({self.option: val})


class CanvasItemOptionInspector(WidgetOptionInspector):
    def __init__(self, master: Widget, label_text: str, canvas: Canvas, item_id: str, option: str) -> None:
        self.canvas = canvas
        self.item_id = item_id
        super().__init__(master, label_text, canvas, option)

    def set_value(self):
        # return super().set_value()
        val = self.entry_var.get()
        if self.option == OPTION.WIDTH:
            self._set(val)
        elif self.option == OPTION.COORDS:
            val = [float(x) for x in val.split(" ")]
            self._set(*val)
        elif self.option == OPTION.MOVE:
            val = [float(x) for x in val.split(" ")]
            self._set(*val)
        elif self.option == OPTION.MOVETO:
            val = [float(x) for x in val.split(" ")]
            self._set(*val)

    def _get(self):
        if not OptionTable[self.option].gettable:
            return None
        val = None
        if self.option == OPTION.WIDTH:
            val = self.canvas.itemcget(self.item_id, self.option)
        if self.option == OPTION.COORDS:
            val = self.canvas.coords(self.item_id)
        elif self.option == OPTION.BBOX:
            val = self.canvas.bbox(self.item_id)
        return val

    def _set(self, *args):
        if not OptionTable[self.option].settable:
            return
        if self.option == OPTION.WIDTH:
            self.canvas.itemconfigure(self.item_id, {self.option: args[0]})
        if self.option == OPTION.COORDS:
            self.canvas.coords(self.item_id, *args)
        elif self.option == OPTION.MOVE:
            self.canvas.move(self.item_id, *args)
        elif self.option == OPTION.MOVETO:
            self.canvas.moveto(self.item_id, *args)
