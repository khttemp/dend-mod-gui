import tkinter
import program.textSetting as textSetting
import program.appearance.ttkCustomWidget as ttkCustomWidget
from tkinter import simpledialog as sd


class CustomSimpleDialog(sd.Dialog):
    def __init__(self, master, title, bgColor):
        self.bgColor = bgColor
        self.box = None
        self.buttonList = []
        super().__init__(parent=master, title=title)

    def body(self, master):
        for child in self.children.values():
            child["bg"] = self.bgColor
        self["bg"] = self.bgColor

    def buttonbox(self, styleName=None):
        super().buttonbox()
        for idx, frame in enumerate(self.children.values()):
            frame["bg"] = self.bgColor
            if idx == 1:
                self.box = frame

        for idx, child in enumerate(self.box.winfo_children()):
            child.destroy()

        w = ttkCustomWidget.CustomTtkButton(self.box, text="OK", width=10, command=self.ok, default=tkinter.ACTIVE)
        w.pack(side=tkinter.LEFT, padx=5, pady=5)
        if styleName is not None:
            w.configure(style=styleName)
        w = ttkCustomWidget.CustomTtkButton(self.box, text="Cancel", width=10, command=self.cancel)
        w.pack(side=tkinter.LEFT, padx=5, pady=5)
        if styleName is not None:
            w.configure(style=styleName)
        self.buttonList = self.box.winfo_children()


class CustomAskstring(CustomSimpleDialog):
    def __init__(self, master, title, prompt, initialvalue, bgColor):
        self.prompt = prompt
        self.initialvalue = initialvalue
        super().__init__(master, title, bgColor)

    def body(self, master):
        w = ttkCustomWidget.CustomTtkLabel(master, text=self.prompt, justify=tkinter.LEFT, font=textSetting.textList["font2"])
        w.grid(row=0, padx=5, sticky=tkinter.W)

        self.entry = ttkCustomWidget.CustomTtkEntry(master, font=textSetting.textList["font2"])
        self.entry.grid(row=1, padx=5, sticky=tkinter.W+tkinter.E)

        if self.initialvalue is not None:
            self.entry.insert(0, self.initialvalue)
            self.entry.select_range(0, tkinter.END)
        super().body(master)

    def validate(self):
        self.result = self.entry.get()
        return True
