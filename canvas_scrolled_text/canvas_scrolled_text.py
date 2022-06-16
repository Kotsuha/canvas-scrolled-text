import uuid
from tkinter import HIDDEN, NORMAL, NW, Canvas, Event
from typing import Tuple, Union


class DRAG_STATE:
    NONE = "None"
    CONTENT = "Content"
    VSB = "VSB"


class CanvasScrolledText:
    def __init__(self, canvas: Canvas, text_width=0, padx=8, pady=8, scrollx=False, scrolly=True, text="", tag: Union[str, None] = None) -> None:
        """Construct a CanvasScrolledText.

        Parameters
        ----------
        canvas : Canvas
            The master canvas. It is strongly recommended that you set its 'borderwidth' and 'highlightthickness' to 0.

        Optional Parameters
        ----------
        text_width : int, optional
            Your desired text width. (Positive) Would set as it is. (Zero) Would fill the canvas horizontally. (Negative) Would not set.
        padx : int, optional

        pady : int, optional

        scrollx : bool, optional
            Whether to allow horizontal scrolling.
        scrolly : bool, optional
            Whether to allow vertical scrolling.
        text : str, optional

        tag : Union[str, None], optional

        """

        canvas_size = [int(canvas.cget("width")), int(canvas.cget("height"))]

        # Create a random tag if not specified
        if not tag:
            tag = uuid.uuid4().hex

        # Create a text object
        options = {
            "anchor": NW,
            "tags": (tag,),
            "text": text
        }
        if text_width > 0:
            options["width"] = text_width
        elif text_width == 0:
            text_width = canvas_size[0] - (padx * 2)
            options["width"] = text_width
        # 爲什麼要 +2 +1 我也不知道，它不按照我給的數字排
        id_text = canvas.create_text(padx + 2, pady + 1, **options)
        # b = canvas.bbox(id_text)  # 你可以把 +2 +1 拿掉，用中斷點停在這行就知道意思了，會看到一個偏移 2px 一個偏移 1px (記得把 Window DPI Scaling 設成 100%)
        # c = canvas.coords(id_text)
        # 後日談：Tkinter Canvas 有多個座標相關的 method，每個計算方式不太一樣。很混亂。
        # 這裏 bbox 的回傳也不符合我預期。不過反正可以用。

        # Create a fake vertical scrollbar
        id_vsb = canvas.create_line(canvas_size[0] - 2, 0, canvas_size[0] - 2,
                                    canvas_size[1], width=4, fill="black", activefill="cyan")

        # Create a rect object (for debug)
        id_rect = canvas.create_rectangle(canvas.bbox(id_text), tags=(tag,), fill="gray", width=0)
        canvas.tag_lower(id_rect, id_text)
        canvas.itemconfigure(id_rect, state=HIDDEN)

        # Store info into instance
        self.canvas = canvas
        self.canvas_size = canvas_size
        self.text_width = text_width
        self.padx = padx
        self.pady = pady
        self.scrollx = scrollx
        self.scrolly = scrolly
        self.tag = tag
        self.id_text = id_text
        self.id_vsb = id_vsb
        self.id_rect = id_rect
        self.debug = False

        # Private vars
        self._hover_vsb = False
        self._drag_state = DRAG_STATE.NONE
        self._last_drag_e = None

        # Something cannot be done until members set
        self._update_vsb()

        # Bind events
        def on_vsb_enter(e: Event):
            self._hover_vsb = True

        def on_vsb_leave(e: Event):
            self._hover_vsb = False

        canvas.tag_bind(id_vsb, "<Enter>", on_vsb_enter)
        canvas.tag_bind(id_vsb, "<Leave>", on_vsb_leave)
        canvas.bind("<B1-Motion>", self._on_mousedrag)
        canvas.bind("<ButtonRelease-1>", self._on_mouserelease)
        canvas.bind("<MouseWheel>", self._on_mousewheel)

    def get_text(self):
        return self.canvas.itemcget(self.id_text, "text")

    def set_text(self, text):
        self.canvas.itemconfigure(self.id_text, text=text)
        self.update_scroll()
        self.update_debug_rect()

    def append_text(self, text):
        old_text = self.get_text()
        new_text = old_text + text
        self.set_text(new_text)

    def get_text_bbox_limit(self):
        bblimit = [
            self.padx + 1,
            self.pady + 1,
            self.canvas_size[0] - self.padx - 1,
            self.canvas_size[1] - self.pady - 1
        ]
        return bblimit

    def scroll(self, x, y):
        text_bbox = self.canvas.bbox(self.id_text)
        text_bbox_limit = self.get_text_bbox_limit()

        text_bbox_size = [
            text_bbox[2] - text_bbox[0],
            text_bbox[3] - text_bbox[1]
        ]

        if self.scrollx:
            if text_bbox_size[0] <= self.canvas_size[0] - self.padx * 2:
                x = text_bbox_limit[0] - text_bbox[0]
            if text_bbox[0] + x > text_bbox_limit[0]:
                x = text_bbox_limit[0] - text_bbox[0]
            elif text_bbox[2] + x < text_bbox_limit[2]:
                x = text_bbox_limit[2] - text_bbox[2]
        else:
            x = 0

        if self.scrolly:
            if text_bbox_size[1] <= self.canvas_size[1] - self.pady * 2:
                y = text_bbox_limit[1] - text_bbox[1]
            elif text_bbox[1] + y > text_bbox_limit[1]:
                y = text_bbox_limit[1] - text_bbox[1]
            elif text_bbox[3] + y < text_bbox_limit[3]:
                y = text_bbox_limit[3] - text_bbox[3]
        else:
            y = 0

        if x != 0 or y != 0:
            self.canvas.move(self.tag, x, y)
        self._update_vsb()

    def update_scroll(self):
        self.scroll(0, 0)

    def _update_vsb(self):
        visible, *coords = self._calc_vsb()
        self.canvas.coords(self.id_vsb, coords)
        self.canvas.itemconfigure(self.id_vsb, state=(NORMAL if visible else HIDDEN))

    def _calc_vsb(self):
        # 不是很懂，反正就是這樣
        CANSIZE = self.canvas_size
        text_bbox = self.canvas.bbox(self.id_text)
        content_bbox = tuple(map(sum, zip(text_bbox, (-self.padx, -self.pady, self.padx, self.pady))))
        content_bbox_h = content_bbox[3] - content_bbox[1]
        ratio = CANSIZE[1] / content_bbox_h
        x0 = x1 = CANSIZE[0] - 2
        if ratio >= 1:
            visible = False
            y0 = 0
            y1 = CANSIZE[1]
        else:
            visible = True
            y0 = int(-(text_bbox[1] - (self.pady + 1)) * ratio)
            y1 = y0 + int(CANSIZE[1] * ratio)
        return (visible, x0, y0, x1, y1)

    def set_debug(self, value: bool):
        """Set debug mode. 啓用時會印 log 及顯示 text 的 bbox。
        """
        self.debug = value
        self.canvas.itemconfigure(self.id_rect, state=(NORMAL if value else HIDDEN))

    def update_debug_rect(self):
        self.canvas.coords(self.id_rect, self.canvas.bbox(self.id_text))

    def _on_mousedrag(self, e: Event):
        if self._last_drag_e is None:
            if self.debug:
                print(f"drag began: {e}")
            self._last_drag_e = e
            if self._hover_vsb:
                self._drag_state = DRAG_STATE.VSB
            else:
                self._drag_state = DRAG_STATE.CONTENT
        else:
            if self.debug:
                print(f"dragging: {e}")
            dx, dy = 0, 0
            if self._drag_state == DRAG_STATE.CONTENT:
                dx, dy = (e.x - self._last_drag_e.x), (e.y - self._last_drag_e.y)
            elif self._drag_state == DRAG_STATE.VSB:
                text_bbox = self.canvas.bbox(self.id_text)
                content_bbox = tuple(map(sum, zip(text_bbox, (-self.padx, -self.pady, self.padx, self.pady))))
                content_bbox_h = content_bbox[3] - content_bbox[1]
                ratio = content_bbox_h / self.canvas_size[1]
                dy = (e.y - self._last_drag_e.y) * ratio * -1
            self.scroll(dx, dy)
            self._last_drag_e = e

    def _on_mouserelease(self, e: Event):
        if self.debug:
            print(f"drag ended: {e}")
        self._last_drag_e = None
        self._drag_state = DRAG_STATE.NONE

    def _on_mousewheel(self, e: Event):
        if self.debug:
            print(f"wheel: {e}")
        self.scroll(0, e.delta)
