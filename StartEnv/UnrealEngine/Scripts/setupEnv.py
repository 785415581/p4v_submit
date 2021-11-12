#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Author: 785415581@qq.com
Date: 2021/11/10 16:29
"""
import sys
import unreal
ToolsLib = r'R:\ProjectX\Scripts\Python\tools\publish'
site_package = r'R:\ProjectX\Scripts\Python37\Lib\site-packages'
for libPath in [ToolsLib, site_package]:
    if libPath not in sys.path:
        sys.path.append(libPath)


def main():
    menus = unreal.ToolMenus.get()
    main_menu = menus.find_menu("LevelEditor.MainMenu")

    my_menu = main_menu.add_sub_menu("[My.Menu](http://My.Menu)", "Python", "My Menu", "Assets Library")

    for name in ["Open Assets Library Window"]:
        menuEntry = unreal.ToolMenuEntry(
            name=name,
            type=unreal.MultiBlockType.MENU_ENTRY,
        )
        menuEntry.set_label(name)
        commandType = unreal.ToolMenuStringCommandType.PYTHON
        menuEntry.set_string_command(commandType, "", 'from StartEnv.UnrealEngine.Scripts.buildEnv import mainFunc\nmainFunc()')
        my_menu.add_menu_entry("Items", menuEntry)

    menus.refresh_all_widgets()


if __name__ == '__main__':
    main()
