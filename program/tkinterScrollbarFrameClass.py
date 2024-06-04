import tkinter
import program.appearance.ttkCustomWidget as ttkCustomWidget


class ScrollbarFrame(ttkCustomWidget.CustomTtkFrame):
    def __init__(self, parent, bar_x=False, bgColor="white", **kw):
        ttkCustomWidget.CustomTtkFrame.__init__(self, parent, **kw)
        self.bar_x = bar_x

        # Create a canvas object and a vertical scrollbar for scrolling it.
        vscrollbar = ttkCustomWidget.CustomTtkScrollbar(self, orient=tkinter.VERTICAL)
        vscrollbar.pack(fill=tkinter.Y, side=tkinter.RIGHT, expand=False)

        if bar_x:
            hscrollbar = ttkCustomWidget.CustomTtkScrollbar(self, orient=tkinter.HORIZONTAL)
            hscrollbar.pack(fill=tkinter.X, side=tkinter.BOTTOM, expand=False)

        self.canvas = tkinter.Canvas(self, bd=0, highlightthickness=0, width=1, height=1, yscrollcommand=vscrollbar.set, background=bgColor)
        self.canvas.pack(fill=tkinter.BOTH, expand=True, anchor=tkinter.NW)
        vscrollbar.config(command = self.canvas.yview)

        if bar_x:
            hscrollbar.config(command = self.canvas.xview)
            self.canvas.config(xscrollcommand=hscrollbar.set)

        # Reset the view
        self.canvas.xview_moveto(0)
        self.canvas.yview_moveto(0)

        # Create a frame inside the canvas which will be scrolled with it.
        self.interior = ttkCustomWidget.CustomTtkFrame(self.canvas)
        self.interior.bind("<Configure>", self._configure_interior)
        self.canvas.bind("<Configure>", self._configure_canvas)
        self.interior_id = self.canvas.create_window(0, 0, window=self.interior, anchor=tkinter.NW)

        self.interior.bind("<MouseWheel>", self._on_mousewheel)

    def _configure_interior(self, event):
        self.canvas.config(scrollregion=self.canvas.bbox("all"))

    def _configure_canvas(self, event):
        # Update the inner frame's width to fill the canvas.
        bounds = self.canvas.bbox(self.interior_id)
        width = bounds[2] - bounds[0]
        height = bounds[3] - bounds[1]
        if not self.bar_x:
            if width != self.canvas.winfo_width():
                self.canvas.itemconfigure(self.interior_id, width=self.canvas.winfo_width())
        if height == 1:
            self.canvas.itemconfigure(self.interior_id, height=self.canvas.winfo_height())

    def _on_mousewheel(self, event):
        self.canvas.yview_scroll(int(-1 * (event.delta / 120)), "units")
