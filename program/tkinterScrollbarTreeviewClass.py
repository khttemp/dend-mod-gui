import tkinter
from tkinter import ttk


class ScrollbarTreeview():
    def __init__(self, parent, v_select):
        self.v_select = v_select

        self.frame = ttk.Frame(parent)
        self.frame.pack(expand=True, fill=tkinter.BOTH)

        self.tree = ttk.Treeview(self.frame, selectmode="browse")

        self.scrollbar_x = ttk.Scrollbar(self.frame, orient=tkinter.HORIZONTAL, command=self.tree.xview)
        self.tree.configure(xscrollcommand=lambda first, last: self.scrollbar_x.set(first, last))
        self.scrollbar_x.pack(side=tkinter.BOTTOM, fill=tkinter.X)

        self.scrollbar_y = ttk.Scrollbar(self.frame, orient=tkinter.VERTICAL, command=self.tree.yview)
        self.tree.configure(yscrollcommand=lambda first, last: self.scrollbar_y.set(first, last))
        self.scrollbar_y.pack(side=tkinter.RIGHT, fill=tkinter.Y)

        self.tree.pack(expand=True, fill=tkinter.BOTH)
        self.tree.bind("<<TreeviewSelect>>", self.treeSelect)

    def treeSelect(self, event):
        if len(self.tree.selection()) > 0:
            selectId = self.tree.selection()[0]
            selectItem = self.tree.set(selectId)
            if self.v_select is not None:
                self.v_select.set(selectItem["treeNum"])
