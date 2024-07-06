import logging
from threading import Thread

import PyQt6.QtGui

from confighandler import load_config, save_config
from get_position_btn import GetPositionButton
from tools import exception_handler
import assertion
import re
import PyQt6.QtWidgets as qw
from PyQt6.QtGui import QIcon
from pynput import mouse


class Color2Heal(qw.QMainWindow):
    app = None
    position_reg = r'^-?\d+,-?\d+$'
    info = None
    # 是否运行,1是0否
    is_running = 0

    def __init__(self):
        super().__init__()

        self.info = load_config()

        x = 10
        y = 10
        self.setWindowTitle("治疗助手")
        width = 800
        height = 600
        self.resize(width, height)

        # 插件位置: label
        self.colorFramePositionLabel = qw.QLabel("插件坐标:", self)
        self.colorFramePositionLabel.move(x, y)
        # 输入框
        self.color_frame_position_input = qw.QLineEdit(self)
        x = x + self.colorFramePositionLabel.width()
        self.color_frame_position_input.move(x, y)
        self.color_frame_position_input.resize(300, 30)
        self.color_frame_position_input.setPlaceholderText("插件坐标, eg:100,200")
        self.color_frame_position_input.setText(self.info["color_frame_position"])
        # 获取按钮
        self.get_color_frame_position_button = GetPositionButton(self,
                                                                 x + self.color_frame_position_input.width() + 10,
                                                                 y,
                                                                 self.on_get_frame_position)

        # 第一个人的坐标: label
        x = 10
        y = y + 40
        self.firstPersonPositionLabel = qw.QLabel("第一个人坐标:", self)
        self.firstPersonPositionLabel.move(x, y)
        # 输入框
        self.firstPersonPositionInput = qw.QLineEdit(self)
        x = x + self.firstPersonPositionLabel.width()
        self.firstPersonPositionInput.move(x, y)
        self.firstPersonPositionInput.resize(300, 30)
        self.firstPersonPositionInput.setPlaceholderText("第一个人坐标, eg:100,200")
        self.firstPersonPositionInput.setText(self.info["first_person_position"])
        # 获取按钮
        self.get_first_person_position_button = GetPositionButton(self,
                                                                  x + self.firstPersonPositionInput.width() + 10,
                                                                  y,
                                                                  self.on_get_person_position)

        # 设置开始的快捷键的输入框
        x = 10
        y = y + 40
        self.startKeyLabel = qw.QLabel("开始快捷键:", self)
        self.startKeyLabel.move(x, y)
        self.startKeyInput = qw.QLineEdit(self)
        x = x + self.startKeyLabel.width()
        self.startKeyInput.move(x, y)
        self.startKeyInput.resize(300, 30)
        self.startKeyInput.setPlaceholderText("快捷键, eg:Ctrl+Shift+A")

        # 保存按钮
        x = 10
        y = y + 40
        self.saveButton = qw.QPushButton("保存", self)
        self.saveButton.move(x, y)
        self.saveButton.clicked.connect(self.on_save_change)
        # 开始按钮
        x = x + self.saveButton.width() + 10
        self.startButton = qw.QPushButton("开始", self)
        self.startButton.resize(60, 30)
        # 按钮上没有文字是一个图标, 播放按钮的图标
        # self.startButton.setIcon(QIcon("./images/play.png"))
        self.startButton.move(x, y)
        self.startButton.clicked.connect(self.on_start)

    def on_color_frame_position_change(self):
        """
        框体位置输入框值变化
        :return:
        """
        print(self.color_frame_position_input.text())

    @exception_handler
    def on_save_change(self, _):
        color_frame_position = self.color_frame_position_input.text()
        first_person_position = self.firstPersonPositionInput.text()

        self.info = {
            "color_frame_position": color_frame_position,
            "first_person_position": first_person_position
        }
        self.validate()

        save_config(self.info)

    def validate(self):
        """
        校验输入框的值
        :param info:
        :return:
        """
        assertion.state(re.match(self.position_reg, self.info["color_frame_position"]), "框体坐标格式错误")
        assertion.state(re.match(self.position_reg, self.info["first_person_position"]), "第一个人坐标格式错误")

    def on_get_frame_position(self, info):
        self.color_frame_position_input.setText(f"{info["x"]},{info["y"]}")

    def on_get_person_position(self, info):
        self.firstPersonPositionInput.setText(f"{info["x"]},{info["y"]}")

    def on_start(self, _):
        self.is_running = 1 - self.is_running
        if self.is_running:
            self.startButton.setText("停止")
        else:
            self.startButton.setText("开始")
