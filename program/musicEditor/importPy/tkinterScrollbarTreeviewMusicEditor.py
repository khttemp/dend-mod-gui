from program.tkinterScrollbarTreeviewClass import ScrollbarTreeview


class ScrollbarTreeviewMusicEditor(ScrollbarTreeview):
    def __init__(self, parent, content, btnList):
        super().__init__(parent, None)
        self.content = content
        self.btnList = btnList

    def treeSelect(self, event):
        selectId = self.tree.selection()[0]
        self.tree.set(selectId)

        editButton = self.btnList[0]
        swapButton = self.btnList[1]

        editButton['state'] = 'normal'
        swapButton['state'] = 'normal'
