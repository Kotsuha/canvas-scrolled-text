from tkinter import *
from inspector_widget import *


class MyColor:  # https://colorhunt.co/palette/eb5353f9d92336ae7c187498
    R = "#EB5353"
    Y = "#F9D923"
    G = "#36AE7C"
    B = "#187498"


lorem = "Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua. Ut enim ad minim veniam, quis nostrud exercitation ullamco laboris nisi ut aliquip ex ea commodo consequat. Duis aute irure dolor in reprehenderit in voluptate velit esse cillum dolore eu fugiat nulla pariatur. Excepteur sint occaecat cupidatat non proident, sunt in culpa qui officia deserunt mollit anim id est laborum."


root = Tk()
root.geometry("1080x760")
root.configure(background=MyColor.B)
root.configure(padx=4, pady=4)
Label(root, text="Canvas 座標測試 (記得把 Windows DPI Scale 調成 100%)", font=("bold", 12), bg=MyColor.B, fg="white").pack()

canvas = Canvas(root, width=400, height=200, bg=MyColor.R)
canvas.pack(pady=4)
rect = canvas.create_rectangle(0, 0, 40, 40, fill=MyColor.Y, outline="black")


def create_inspectors():
    container = Frame(root)
    container.pack()
    inspectors: list[WidgetOptionInspector] = [
        WidgetOptionInspector(container, f"Canvas {OPTION.WIDTH}", canvas, OPTION.WIDTH),
        WidgetOptionInspector(container, f"Canvas {OPTION.HEIGHT}", canvas, OPTION.HEIGHT),
        WidgetOptionInspector(container, f"Canvas {OPTION.HIGHLIGHT_THICKNESS}", canvas, OPTION.HIGHLIGHT_THICKNESS),
        WidgetOptionInspector(container, f"Canvas {OPTION.BORDER_WIDTH}", canvas, OPTION.BORDER_WIDTH),
        CanvasItemOptionInspector(container, f"Rect border {OPTION.WIDTH}", canvas, rect, OPTION.WIDTH),
        CanvasItemOptionInspector(container, f"Rect {OPTION.COORDS}", canvas, rect, OPTION.COORDS),
        CanvasItemOptionInspector(container, f"Rect {OPTION.BBOX}", canvas, rect, OPTION.BBOX),
        CanvasItemOptionInspector(container, f"Rect {OPTION.MOVE}", canvas, rect, OPTION.MOVE),
        CanvasItemOptionInspector(container, f"Rect {OPTION.MOVETO}", canvas, rect, OPTION.MOVETO),
    ]
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
• moveto 0 0 總是會讓 bbox 變成 0 0，受 border width 影響
• 結論，爲了單純些，建議 Canvas 不要設 border highlightthickness。Rect border width 設不設大概無所謂。不要用 moveto 用 coords 就好。
"""
Label(root, text=conclusion_text, font=("normal", 12), bg=MyColor.B, fg="white", justify=LEFT).pack()

root.mainloop()
