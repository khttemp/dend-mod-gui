import tkinter


class ScrollbarFrame():
    def __init__(self, parent, bar_x=False, bar_y=True):
        self.canvas = tkinter.Canvas(parent)
        self.frame = tkinter.Frame(self.canvas, width=parent.winfo_width() - 8, height=parent.winfo_height())
        self.frame.bind("<Configure>", lambda e: self.canvas.configure(scrollregion=self.canvas.bbox("all")))
        self.frame.pack()

        self.canvas.create_window((0, 0), window=self.frame, anchor="nw")

        if bar_x:
            self.scrollbar_x = tkinter.Scrollbar(parent, orient=tkinter.HORIZONTAL, command=self.canvas.xview)
            self.scrollbar_x.pack(side=tkinter.BOTTOM, fill=tkinter.X)
            self.canvas.configure(xscrollcommand=self.scrollbar_x.set)

        if bar_y:
            self.scrollbar_y = tkinter.Scrollbar(parent, orient=tkinter.VERTICAL, command=self.canvas.yview)
            self.scrollbar_y.pack(side=tkinter.RIGHT, fill=tkinter.Y)
            self.canvas.configure(yscrollcommand=self.scrollbar_y.set)

        self.canvas.pack(fill="both", expand=True)
        self.canvas.bind("<MouseWheel>", self._on_mousewheel)

    def _on_mousewheel(self, event):
        self.canvas.yview_scroll(int(-1 * (event.delta / 120)), "units")
