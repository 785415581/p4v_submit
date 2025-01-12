#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Author: 785415581@qq.com
Date: 2021/12/28 15:44
"""
import os
import sys
import re
package = 'R:/ProjectX/Scripts/Python/tools/toolset/SubstanceDesigner/Tools/combineGraph/widget'
if package not in sys.path:
    sys.path.insert(0, package)

from PySide2 import QtWidgets
from PySide2 import QtGui
from Tools.unreal_tools import ConfigTools
from referenceWidget.studiolibraryWidget.item import Item
from referenceWidget.studiolibraryWidget.itemswidget import ItemsWidget
import imp
imp.reload(ConfigTools)
from Tools.unreal_tools import checkChangeList
imp.reload(checkChangeList)


class View(QtWidgets.QMainWindow):
    def __init__(self):
        super(View, self).__init__()
        self.resize(490, 630)
        self.setStyleSheet("""
        QMainWindow{background-color: #242424;}
        QWidget{background-color: #242424;
        color: (36, 36, 36);
        }
        """)
        self._itemsWidget = ItemsWidget(self)
        self._itemsWidget._setViewMode('icon')
        self._textColor = QtGui.QColor(255, 255, 255)
        self._backgroundColor = QtGui.QColor(30, 30, 30, 200)
        self._backgroundHoverColor = QtGui.QColor(26, 26, 26, 35)
        self._backgroundSelectedColor = QtGui.QColor(38, 187, 255)
        self._itemsWidget.setTextColor(self._textColor)
        self._itemsWidget.setBackgroundColor(self._backgroundColor)
        self._itemsWidget.setBackgroundHoverColor(self._backgroundHoverColor)
        self._itemsWidget.setBackgroundSelectedColor(self._backgroundSelectedColor)

        self.setCentralWidget(self._itemsWidget)
        self.loadPreview()
        self._itemsWidget.itemDoubleClicked.connect(self.showTool)

    def loadPreview(self):
        for toolName, toolInfo in ConfigTools.Tools.items():
            item = Item()
            icon = QtGui.QIcon(toolInfo.get("icon"))
            item.setIcon(0, icon)
            item.setName(toolName)
            item.setItemData(toolInfo)
            self._itemsWidget.addItem(item)

    def showTool(self, item):
        import imp
        imp.reload(ConfigTools)
        self._itemsWidget.clear()
        self.loadPreview()

        ToolInfo = item.itemData()
        if ToolInfo.get("type") == "window":
            function = ToolInfo.get("function")
            if not QtWidgets.QApplication.instance():
                app = QtWidgets.QApplication(sys.argv)
            global window
            window = function()
            window.setWindowTitle(ToolInfo.get("name"))
            window.show()
        elif ToolInfo.get("type") == "run":
            if ToolInfo.get("args"):
                function = ToolInfo.get("function")
                function(ToolInfo.get("args"))
            else:
                function = ToolInfo.get("function")
                function()


if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    win = View()
    win.show()
    app.exec_()