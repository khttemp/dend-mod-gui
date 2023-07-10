from program.tkinterScrollbarTreeviewClass import ScrollbarTreeview


class ScrollbarTreeviewComicscript(ScrollbarTreeview):
    def __init__(self, parent, v_select, btnList):
        super().__init__(parent, v_select)
        self.v_select = v_select
        self.btnList = btnList

        csvExtractBtn = self.btnList[4]
        csvLoadAndSaveBtn = self.btnList[5]
        headerFileEditBtn = self.btnList[6]

        csvExtractBtn["state"] = "normal"
        csvLoadAndSaveBtn["state"] = "normal"
        headerFileEditBtn["state"] = "normal"

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
