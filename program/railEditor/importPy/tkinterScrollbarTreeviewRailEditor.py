from program.tkinterScrollbarTreeviewClass import ScrollbarTreeview


class ScrollbarTreeviewRailEditor(ScrollbarTreeview):
    def __init__(self, parent, v_select, btnList, selectFunc=None):
        super().__init__(parent, v_select)
        self.btnList = btnList
        self.selectFunc = selectFunc

    def treeSelect(self, event):
        super().treeSelect(event)

        for btn in self.btnList:
            btn["state"] = "normal"
        if self.selectFunc is not None:
            self.selectFunc()
