from program.sub.tkinterScrollbarTreeviewClass import ScrollbarTreeview


class ScrollbarTreeviewComicscript(ScrollbarTreeview):
    def __init__(self, parent, v_select, btnList):
        super().__init__(parent, v_select)
        self.v_select = v_select
        self.btnList = btnList

    def treeSelect(self, event):
        super().treeSelect(event)
        editLineBtn = self.btnList[0]
        insertLineBtn = self.btnList[1]
        deleteLineBtn = self.btnList[2]
        copyLineBtn = self.btnList[3]

        editLineBtn["state"] = "normal"
        insertLineBtn["state"] = "normal"
        deleteLineBtn["state"] = "normal"
        copyLineBtn["state"] = "normal"
