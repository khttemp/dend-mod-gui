from program.tkinterScrollbarTreeviewClass import ScrollbarTreeview


class ScrollbarTreeviewSmf(ScrollbarTreeview):
    def __init__(self, parent, btnList):
        super().__init__(parent, None)
        self.btnList = btnList

    def treeSelect(self, event):
        super().treeSelect(event)
        selectId = self.tree.selection()[0]
        if selectId == "item0":
            for btn in self.btnList:
                btn["state"] = "disabled"
        else:
            for btn in self.btnList:
                btn["state"] = "normal"
