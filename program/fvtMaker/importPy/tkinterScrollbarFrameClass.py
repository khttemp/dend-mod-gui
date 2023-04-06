import tkinter


class ScrollbarFrame():
    def __init__(self, parent):
        self.canvas = tkinter.Canvas(parent, width=parent.winfo_width(), height=parent.winfo_height())
        self.frame = tkinter.Frame(self.canvas)
        self.frame.bind("<Configure>", lambda e: self.canvas.configure(scrollregion=self.canvas.bbox("all")))

        self.scrollbar = tkinter.Scrollbar(parent, orient=tkinter.HORIZONTAL, command=self.canvas.xview)
        self.scrollbar.pack(side=tkinter.BOTTOM, fill=tkinter.X)

        self.canvas.create_window((0, 0), window=self.frame, anchor="nw")
        self.canvas.configure(xscrollcommand=self.scrollbar.set)
        self.canvas.pack()

        self.canvas.bind("<MouseWheel>", self._on_mousewheel)

    def _on_mousewheel(self, event):
        self.canvas.yview_scroll(int(-1*(event.delta/120)), "units")
