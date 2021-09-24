import ctypes
import os
import sys
from functools import partial

from PySide2 import QtCore
from PySide2 import QtGui
from PySide2 import QtWidgets
from AssetBrowser import publishInterface
from AssetBrowser.control.controller import Controller
from AssetBrowser.modules.ui_main import Ui_MainWindow
from AssetBrowser.view.baseWidget import ListWidgetItem

widgets = None


class MainWindow(QtWidgets.QMainWindow):
    def __init__(self, parent=None, *args):
        super(MainWindow, self).__init__(parent)
        self.setWindowTitle('Publish for P4V')
        self.currentPathList = list()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        global widgets
        widgets = self.ui
        self.control = Controller()
        self.control.view = widgets
        self.control.init()
        self.control.initSignal()
        self.control.appFunction.initValue()
        widgets.currentPathCombox.currentIndexChanged.connect(self.changeCurrentPath)
        widgets.workTree.itemClicked.connect(self.listPath)
        widgets.connectBtn.clicked.connect(self.buttonClick)
        widgets.publishBtn.clicked.connect(self.buttonClick)
        widgets.listWidget.setAcceptDrops(True)
        widgets.listWidget.setDefaultDropAction(QtCore.Qt.MoveAction)
        widgets.listWidget.setDragDropMode(QtWidgets.QAbstractItemView.InternalMove)
        widgets.listWidget.setSelectionMode(QtWidgets.QAbstractItemView.ContiguousSelection)
        widgets.listWidget.installEventFilter(self)
        widgets.assetNameComboBox.installEventFilter(self)

    def eventFilter(self, watched, event):
        if event.type() == QtCore.QEvent.DragEnter:
            if watched is self.ui.listWidget:
                event.accept()
                return True
        elif event.type() == QtCore.QEvent.Drop:
            if watched is self.ui.listWidget:
                data = event.mimeData()
                urls = data.urls()
                for url in urls:
                    filePath = url.toLocalFile()
                    item = ListWidgetItem(self.ui.listWidget)
                    item.filePath = filePath
                    item.setCurrentEnterFile(os.path.basename(filePath))
                    widgets.listWidget.addItem(item)
                    item.exportCheck.clicked.connect(partial(self.control.appFunction.checkedExportItem, item))
                    item.exportPath.clicked.connect(partial(self.control.appFunction.selectExportPath, item))

        elif event.type() == QtCore.QEvent.KeyPress:
            if watched is self.ui.assetNameComboBox:
                key = event.key()
                if key == QtCore.Qt.Key_Enter or key == QtCore.Qt.Key_Return:
                    self.control.createAsset(self.control)
            elif watched is self.ui.submitStepCom:
                print('222')
        return QtCore.QObject.eventFilter(self, watched, event)

    def changeCurrentPath(self, index):
        treeWidgetItem = widgets.currentPathCombox.itemData(index, QtCore.Qt.UserRole)
        widgets.workTree.setCurrentItem(treeWidgetItem)

    def listPath(self, item, column):
        res = self.getCurrentPath(item).replace('\\', '/')
        print(res)
        if self.control.appFunction.clientRoot and res not in self.currentPathList:
            widgets.currentPathCombox.addItem(res.replace('\\', '/'))
            self.currentPathList.append(res)
            index = widgets.currentPathCombox.count()
            widgets.currentPathCombox.setItemData(index - 1, item, QtCore.Qt.UserRole)
        widgets.currentPathCombox.setCurrentText(res.replace('\\', '/'))

    def getCurrentPath(self, item, strPath=''):
        if item.parent():
            parentWidget = item.parent()
            currentFolderName = item.text(0)
            if strPath:
                strPath = currentFolderName + '/' + strPath
            else:
                strPath = currentFolderName
            return self.getCurrentPath(parentWidget, strPath)
        else:
            currentType = widgets.typeComboBox.currentText()
            currentAsset = widgets.assetNameComboBox.currentText()
            currentStep = widgets.submitStepCom.currentText()
            currentPath = os.path.join(self.control.appFunction.clientStream,
                                       currentType,
                                       currentAsset,
                                       currentStep,
                                       strPath)
            return currentPath

    def buttonClick(self):
        btn = self.sender()
        btnName = btn.objectName()
        if btnName == "connectBtn":
            self.control.p4Model.user = self.ui.userLn.currentText()
            self.control.p4Model.client = self.ui.workLn.currentText()
            self.control.p4Model.serverPort = self.ui.serverLn.currentText()
            self.control.p4Model.password = self.ui.passwordLn.text()
            self.control.p4Model.validation()
            self.control.p4Model.initClient()
            clientRoot = self.control.p4Model.getRoot()
            print("clientRoot = {}".format(clientRoot))
            clientStream = self.control.p4Model.getStreamName()
            print("clientStream = {}".format(clientStream))
            if clientStream:
                self.control.appFunction.validation = self.control.p4Model.validation
                self.control.appFunction.clientRoot = clientRoot
                self.control.appFunction.clientStream = clientStream
                self.control.appFunction.initWindow()
            else:
                print('error')
        elif btnName == "publishBtn":
            step = self.control.appFunction.submitStepComText
            if step:
                stepClass = publishInterface.get_step_interface_class(stepName=step)
                Interface = stepClass()
                Interface.control = self.control
                Interface.publish()
            print('publishBtn')

    def closeEvent(self, event):
        event.accept()
        self.control.appFunction.callBack()


if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    app.setWindowIcon(QtGui.QIcon("icon.png"))
    ctypes.windll.shell32.SetCurrentProcessExplicitAppUserModelID('Hero_Publish')
    window = MainWindow()
    window.show()
    app.exec_()