import tkinter
from tkinter import ttk


class CustomTtkLabel(ttk.Label):
    def __init__(self, master, **kw):
        ttk.Label.__init__(self, master=master, **kw)
        self.configure(style="custom.TLabel")
        self.configure(**kw)

    def setFgColor(self, color):
        if color == "red":
            self.configure(style="custom.red.TLabel")
        elif color == "blue":
            self.configure(style="custom.blue.TLabel")
        elif color == "green":
            self.configure(style="custom.green.TLabel")
        elif color == "#444444":
            self.configure(style="custom.444444.TLabel")
        else:
            self.configure(style="custom.TLabel")


class CustomTtkEntry(ttk.Entry):
    def __init__(self, master, **kw):
        ttk.Entry.__init__(self, master=master, **kw)
        self.configure(style="custom.TEntry")
        self.configure(**kw)


class CustomTtkButton(ttk.Button):
    def __init__(self, master, **kw):
        ttk.Button.__init__(self, master=master, **kw)
        self.configure(style="custom.TButton")
        self.configure(**kw)


class CustomTtkCheckbutton(ttk.Checkbutton):
    def __init__(self, master, **kw):
        ttk.Checkbutton.__init__(self, master=master, **kw)
        self.configure(style="custom.TCheckbutton")
        self.configure(**kw)


class CustomTtkRadiobutton(ttk.Radiobutton):
    def __init__(self, master, **kw):
        ttk.Radiobutton.__init__(self, master=master, **kw)
        self.configure(style="custom.TRadiobutton")
        self.configure(**kw)


class CustomTtkLabelFrame(ttk.LabelFrame):
    def __init__(self, master, **kw):
        ttk.LabelFrame.__init__(self, master=master, **kw)
        self.configure(style="custom.TLabelframe")
        self.configure(**kw)


class CustomTtkCombobox(ttk.Combobox):
    def __init__(self, master, **kw):
        ttk.Combobox.__init__(self, master=master, **kw)
        self.configure(style="custom.TCombobox")
        self.configure(**kw)


class CustomTtkFrame(ttk.Frame):
    def __init__(self, master, **kw):
        ttk.Frame.__init__(self, master=master, **kw)
        self.configure(style="custom.TFrame")
        self.configure(**kw)


class CustomTtkScrollbar(ttk.Scrollbar):
    def __init__(self, master, **kw):
        ttk.Scrollbar.__init__(self, master=master, **kw)
        if kw["orient"] == tkinter.VERTICAL:
            self.configure(style="custom.Vertical.TScrollbar")
        elif kw["orient"] == tkinter.HORIZONTAL:
            self.configure(style="custom.Horizontal.TScrollbar")
        self.configure(**kw)


class CustomTtkSeparator(ttk.Separator):
    def __init__(self, master, **kw):
        ttk.Separator.__init__(self, master=master, **kw)
        self.configure(style="custom.TSeparator")
        self.configure(**kw)


class CustomTtkTreeview(ttk.Treeview):
    def __init__(self, master, **kw):
        ttk.Treeview.__init__(self, master=master, **kw)
        self.configure(style="custom.Treeview")
        self.configure(**kw)


class CustomTtkMenubutton(ttk.Menubutton):
    def __init__(self, master, **kw):
        ttk.Menubutton.__init__(self, master=master, **kw)
        self.configure(style="custom.TMenubutton")
        self.configure(**kw)


class CustomTtkSpinbox(ttk.Spinbox):
    def __init__(self, master, **kw):
        ttk.Spinbox.__init__(self, master=master, **kw)
        self.configure(style="custom.TSpinbox")
        self.configure(**kw)
