from program.sub.tkinterScrollbarTreeviewClass import ScrollbarTreeview


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
        listHeadeModifyBtn = self.btnList[4]
        listNumModifyBtn = self.btnList[5]
        numModifyBtn = self.btnList[6]

        insertLineBtn["state"] = "normal"
        if "#" in selectItem["treeName"]:
            editLineBtn["state"] = "disabled"
            deleteLineBtn["state"] = "disabled"
            copyLineBtn["state"] = "disabled"

            listHeadeModifyBtn["state"] = "normal"
            listNumModifyBtn["state"] = "normal"
            numModifyBtn["state"] = "normal"
        else:
            editLineBtn["state"] = "normal"
            deleteLineBtn["state"] = "normal"
            copyLineBtn["state"] = "normal"

            listHeadeModifyBtn["state"] = "disabled"
            listNumModifyBtn["state"] = "disabled"
            numModifyBtn["state"] = "disabled"
