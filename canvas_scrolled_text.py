import uuid
from tkinter import HIDDEN, NORMAL, Canvas, Event
from typing import Tuple, Union


class CanvasScrolledText:
    def __init__(self, canvas: Canvas, canvas_size: Tuple[int, int], text_width=0, padx=8, pady=8, scrollx=False, scrolly=True, text="", tag: Union[str, None] = None) -> None:
        """Construct a CanvasScrolledText.

        Parameters
        ----------
        canvas : Canvas
            The master canvas. It is recommended that you set its 'borderwidth' and 'highlightthickness' to 0.
        canvas_size : Tuple[int, int]
            Tell me the canvas's width and height.

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

        # 要動態得到準確的 canvas_size 有困難
        # 一是必須等到 root.mainloop() 開始以後才能取得非 0 值，這點辦得到
        # 二是得到的值會受 highlightthickness (已驗證) 和 borderwidth (沒驗證) 影響
        # 我暫時不知道怎麼取得這兩個值，也不知道有沒有其他值也會影響
        # 決定讓使用者自己傳 canvas size 進來了

        # 若沒有 tag 產生一個隨機 tag
        if not tag:
            tag = uuid.uuid4().hex

        # 創建 text object
        options = {
            "anchor": "nw",
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

        # Create a vertical progress bar
        id_line_y = canvas.create_line(canvas_size[0] - 2, 0, canvas_size[0] - 2, canvas_size[1], fill="#f0f0f0", width=4)

        # 創建 rect object (for debug)
        id_rect = canvas.create_rectangle(
            canvas.bbox(id_text), tags=(tag,), fill="gray")
        canvas.tag_lower(id_rect, id_text)
        canvas.itemconfigure(id_rect, state="hidden")

        # 無腦把變數保存至 instance
        self.canvas = canvas
        self.canvas_size = canvas_size
        self.text_width = text_width
        self.padx = padx
        self.pady = pady
        self.scrollx = scrollx
        self.scrolly = scrolly
        self.tag = tag
        self.id_text = id_text
        self.id_line_y = id_line_y
        self.id_rect = id_rect
        self.debug = False

        # 監聽事件
        self.canvas.bind("<B1-Motion>", self._on_drag)
        self.canvas.bind("<ButtonRelease-1>", self._on_release)
        self.canvas.bind("<MouseWheel>", self._on_mousewheel)
        self._last_drag = None

        # Something can only be done until members vars set
        self._update_progress_y()

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

    def _update_progress_y(self):
        CAN_SIZE = self.canvas_size
        bb = self.canvas.bbox(self.id_text)
        h = bb[3] - bb[1]
        ratio = CAN_SIZE[1] / h
        if ratio >= 1:
            self.canvas.itemconfigure(self.id_line_y, state=HIDDEN)
            return
        else:
            self.canvas.itemconfigure(self.id_line_y, state=NORMAL)
        x0 = CAN_SIZE[0] - 2
        y0 = int((bb[1] * -1) * ratio)
        x1 = x0
        y1 = y0 + int(CAN_SIZE[1] * ratio)
        self.canvas.coords(self.id_line_y, x0, y0, x1, y1)

    def scroll(self, x, y):
        txt_box = self.canvas.bbox(self.id_text)
        txt_width = txt_box[2] - txt_box[0]
        txt_height = txt_box[3] - txt_box[1]
        can_width = self.canvas_size[0]
        can_height = self.canvas_size[1]
        txt_box_limit = [
            self.padx + 1,
            self.pady + 1,
            can_width - self.padx - 1,
            can_height - self.pady - 1
        ]
        if self.debug:
            print(f"txt_box: {txt_box}")
            print(f"txt_box_limit: {txt_box_limit}")
        if self.scrollx:
            if txt_width <= can_width - self.padx * 2:
                x = (self.padx + 1) - txt_box[0]
            else:
                if txt_box[0] + x > txt_box_limit[0]:
                    x = txt_box_limit[0] - txt_box[0]
                elif txt_box[2] + x < txt_box_limit[2]:
                    x = txt_box_limit[2] - txt_box[2]
        else:
            x = 0
        if self.scrolly:
            if txt_height <= can_height - self.pady * 2:
                y = (self.pady + 1) - txt_box[1]
            else:
                if txt_box[1] + y > txt_box_limit[1]:
                    y = txt_box_limit[1] - txt_box[1]
                elif txt_box[3] + y < txt_box_limit[3]:
                    y = txt_box_limit[3] - txt_box[3]
        else:
            y = 0

        if self.debug:
            print(f"x: {x}")
        self.canvas.move(self.tag, x, y)
        # Test
        self._update_progress_y()

    def update_scroll(self):
        self.scroll(0, 0)

    def set_debug(self, value: bool):
        """Set debug mode. 啓用時會印 log 及顯示 text 的 bbox。
        """
        self.debug = value
        if value:
            self.canvas.itemconfigure(self.id_rect, state=NORMAL)
        else:
            self.canvas.itemconfigure(self.id_rect, state=HIDDEN)

    def update_debug_rect(self):
        self.canvas.coords(self.id_rect, self.canvas.bbox(self.id_text))

    def _on_drag(self, e: Event):
        if self.debug:
            print(e)
        if self._last_drag is None:
            if self.debug:
                print("drag began")
            self._last_drag = e
        else:
            if self.debug:
                print("dragging")
            dx, dy = (e.x - self._last_drag.x), (e.y - self._last_drag.y)
            self.scroll(dx, dy)
            self._last_drag = e

    def _on_release(self, e: Event):
        if self.debug:
            print(e)
            print("drag ended")
        self._last_drag = None

    def _on_mousewheel(self, e: Event):
        if self.debug:
            print(e)
        self.scroll(0, e.delta)
