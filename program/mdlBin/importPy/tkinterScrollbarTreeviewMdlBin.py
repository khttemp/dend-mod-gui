from program.tkinterScrollbarTreeviewClass import ScrollbarTreeview


class ScrollbarTreeviewMdlBin(ScrollbarTreeview):
    def __init__(self, parent, v_select, btnList):
        super().__init__(parent, v_select)
        self.btnList = btnList

    def treeSelect(self, event):
        super().treeSelect(event)

        selectId = self.tree.selection()[0]
        selectItem = self.tree.set(selectId)

        editLineBtn = self.btnList[0]
        insertLineBtn = self.btnList[1]
        deleteLineBtn = self.btnList[2]
        copyLineBtn = self.btnList[3]
        listNumModifyBtn = self.btnList[4]
        listHeadeModifyBtn = self.btnList[5]
        numModifyBtn = self.btnList[6]

        editLineBtn["state"] = "normal"
        insertLineBtn["state"] = "normal"
        deleteLineBtn["state"] = "normal"
        copyLineBtn["state"] = "normal"

        if "#" in selectItem["treeName"]:
            listNumModifyBtn["state"] = "normal"
            listHeadeModifyBtn["state"] = "normal"
            numModifyBtn["state"] = "normal"

            editLineBtn["state"] = "disabled"
            deleteLineBtn["state"] = "disabled"
            copyLineBtn["state"] = "disabled"
        else:
            listNumModifyBtn["state"] = "disabled"
            listHeadeModifyBtn["state"] = "disabled"
            numModifyBtn["state"] = "disabled"

            editLineBtn["state"] = "normal"
