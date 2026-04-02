from program.tkinterScrollbarTreeviewClass import ScrollbarTreeview


class ScrollbarTreeviewSSUnity(ScrollbarTreeview):
    def __init__(self, parent, v_select, btnList):
        super().__init__(parent, v_select)
        self.btnList = btnList

    def treeSelect(self, event):
        super().treeSelect(event)

        if len(self.tree.selection()) > 0:
            for btn in self.btnList:
                btn["state"] = "normal"
        else:
            for btn in self.btnList:
                btn["state"] = "disabled"
