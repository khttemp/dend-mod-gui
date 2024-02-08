import tkinter
from tkinter import ttk


class ScrollbarFrame(ttk.Frame):
    def __init__(self, parent, bar_x=False, *args, **kw):
        ttk.Frame.__init__(self, parent, *args, **kw)

        # Create a canvas object and a vertical scrollbar for scrolling it.
        vscrollbar = ttk.Scrollbar(self, orient=tkinter.VERTICAL)
        vscrollbar.pack(fill=tkinter.Y, side=tkinter.RIGHT, expand=False)

        if bar_x:
            hscrollbar = ttk.Scrollbar(self, orient=tkinter.HORIZONTAL)
            hscrollbar.pack(fill=tkinter.X, side=tkinter.BOTTOM, expand=False)


        self.canvas = tkinter.Canvas(self, bd=0, highlightthickness=0, width = 200, height = 300, yscrollcommand=vscrollbar.set)
        self.canvas.pack(fill=tkinter.BOTH, expand=True)
        vscrollbar.config(command = self.canvas.yview)

        if bar_x:
            hscrollbar.config(command = self.canvas.xview)
            self.canvas.config(xscrollcommand=hscrollbar.set)

        # Reset the view
        self.canvas.xview_moveto(0)
        self.canvas.yview_moveto(0)

        # Create a frame inside the canvas which will be scrolled with it.
        self.interior = ttk.Frame(self.canvas)
        self.interior.bind("<Configure>", self._configure_interior)
        self.canvas.bind("<Configure>", self._configure_canvas)
        self.interior_id = self.canvas.create_window(0, 0, window=self.interior, anchor=tkinter.NW)

        self.interior.bind("<MouseWheel>", self._on_mousewheel)

    def _configure_interior(self, event):
        # Update the scrollbars to match the size of the inner frame.
        size = (self.interior.winfo_reqwidth(), self.interior.winfo_reqheight())
        self.canvas.config(scrollregion=(0, 0, size[0], size[1]))
        if self.interior.winfo_reqwidth() != self.canvas.winfo_width():
            # Update the canvas's width to fit the inner frame.
            self.canvas.config(width = self.interior.winfo_reqwidth())

    def _configure_canvas(self, event):
        if self.interior.winfo_reqwidth() < self.canvas.winfo_width():
            # Update the inner frame's width to fill the canvas.
            self.canvas.itemconfigure(self.interior_id, width=self.canvas.winfo_width())

    def _on_mousewheel(self, event):
        self.canvas.yview_scroll(int(-1 * (event.delta / 120)), "units")
