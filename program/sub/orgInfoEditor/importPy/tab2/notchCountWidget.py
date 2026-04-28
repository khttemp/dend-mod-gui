import tkinter
from tkinter import messagebox as mb
import program.textSetting as textSetting
import program.appearance.ttkCustomWidget as ttkCustomWidget
from program.appearance.customSimpleDialog import CustomSimpleDialog, CustomAskstring


class NotchCountWidget:
    def __init__(self, root, trainIndex, notchNum, decryptFile, reloadWidget):
        self.trainIndex = trainIndex
        self.notchNum = notchNum
        self.decryptFile = decryptFile
        self.reloadWidget = reloadWidget
        fixedWidth = 86
        fixedHeight = 32
        self.font2 = QFont(textSetting.textList["font2"][0], textSetting.textList["font2"][1])

        # mainLayout
        mainLayout = QGridLayout(self)
        mainLayout.setContentsMargins(0, 0, 0, 0)
        mainLayout.setSpacing(0)
        # notchNameLabel
        notchNameLabel = QLabel(textSetting.textList["orgInfoEditor"]["notchLabel"], font=self.font2)
        notchNameLabel.setFrameStyle(QFrame.Shape.Box | QFrame.Shadow.Plain)
        notchNameLabel.setAlignment(Qt.AlignmentFlag.AlignCenter)
        notchNameLabel.setFixedSize(fixedWidth, fixedHeight)
        mainLayout.addWidget(notchNameLabel, 0, 0)
        # notchLabel
        notchLabel = QLabel("{0}".format(notchNum), font=self.font2)
        notchLabel.setFrameStyle(QFrame.Shape.Box | QFrame.Shadow.Plain)
        notchLabel.setAlignment(Qt.AlignmentFlag.AlignCenter)
        notchLabel.setFixedSize(fixedWidth, fixedHeight)
        mainLayout.addWidget(notchLabel, 0, 1)
        # notchButton
        notchButton = QPushButton(textSetting.textList["orgInfoEditor"]["modifyBtnLabel"], font=self.font2)
        notchButton.clicked.connect(self.editNotchCount)
        mainLayout.addWidget(notchButton, 0, 2)

    def editNotchCount(self):
        if self.notchNum not in [4, 5, 12]:
            mb.showerror(title=textSetting.textList["error"], message=textSetting.textList["errorList"]["E23"].format(self.notchNum))
            return

        editNotchCountDialog = EditNotchCountDialog(self, textSetting.textList["orgInfoEditor"]["editNotchLabel"], self.trainIndex, self.notchNum, self.decryptFile)
        if editNotchCountDialog.exec() == QDialog.Accepted:
            self.reloadWidget()


class EditNotchCountDialog(QDialog):
    def __init__(self, parent, title, trainIndex, notchNum, decryptFile):
        super().__init__(parent)
        self.setWindowTitle(title)
        self.trainIndex = trainIndex
        self.notchNum = notchNum
        self.decryptFile = decryptFile
        font2 = QFont(textSetting.textList["font2"][0], textSetting.textList["font2"][1])

        if notchNum == 4:
            notchIdx = 0
        elif notchNum == 5:
            notchIdx = 1
        elif notchNum == 12:
            notchIdx = 2

        # layout
        layout = QVBoxLayout(self)
        # notchNameLabel
        notchNameLabel = QLabel(textSetting.textList["infoList"]["I57"], font=font2)
        layout.addWidget(notchNameLabel)
        notchList = textSetting.textList["orgInfoEditor"]["editNotchList"]
        self.notchCombo = QComboBox(font=font2)
        self.notchCombo.addItems(notchList)
        self.notchCombo.setCurrentIndex(notchIdx)
        layout.addWidget(self.notchCombo)
        # layout - QDialogButtonBox
        buttonBox = QDialogButtonBox(QDialogButtonBox.Ok | QDialogButtonBox.Cancel)
        buttonBox.accepted.connect(self.accept)
        buttonBox.rejected.connect(self.reject)
        layout.addWidget(buttonBox)

    def validate(self):
        if self.decryptFile.game in ["LS", "BS"]:
            if self.notchCombo.currentIndex() == 2:
                mb.showerror(title=textSetting.textList["error"], message=textSetting.textList["errorList"]["E23"].format(12))
                return False

        newNotchNum = -1
        notchIdx = self.notchCombo.currentIndex()
        if notchIdx == 0:
            newNotchNum = 4
        elif notchIdx == 1:
            newNotchNum = 5
        elif notchIdx == 2:
            newNotchNum = 12

        if not self.decryptFile.saveNotchInfo(self.trainIndex, newNotchNum):
            self.decryptFile.printError()
            mb.showerror(title=textSetting.textList["saveError"], message=textSetting.textList["errorList"]["E4"])
            return False
        return True

    def accept(self):
        result = mb.askokcancel(title=textSetting.textList["confirm"], message=textSetting.textList["infoList"]["I58"])
        if result != mb.OK:
            return

        if not self.validate():
            return
        super().accept()
        mb.showinfo(title=textSetting.textList["success"], message=textSetting.textList["infoList"]["I59"])
