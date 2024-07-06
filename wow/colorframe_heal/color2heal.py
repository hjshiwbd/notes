"""
获取屏幕上某个坐标的颜色
根据颜色执行对应的键鼠操作

简单设计:
设置:第一个人的框体位置(x,y). 由第一个人推算出其他人(5人组 or 40人组)的位置(x,y), 即颜色的RGB(E48E4C)->被治疗人框体的坐标位置
设置:游戏插件ColorFrame提供的颜色rgb, 由此决定被治疗的人及其策略
设置:到游戏里插件的位置信息, 用于获取框体的的颜色

"""
import json
import logging

import PyQt6.QtWidgets as qw
import sys

import tools

from gui import Color2Heal


def run():
    app = qw.QApplication(sys.argv)
    window = Color2Heal()
    window.show()
    sys.exit(app.exec())


if __name__ == '__main__':
    tools.setup_logger("color2heal")
    try:
        run()
    except Exception as e:
        # trace e
        print(e)
