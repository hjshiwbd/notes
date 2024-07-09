from threading import Thread

from confighandler import load_config, save_config
from get_position_btn import GetPositionButton
from tools import exception_handler
import assertion
import re
import PyQt6.QtWidgets as qw
from pynput import keyboard


class Color2Heal(qw.QMainWindow):
    app = None
    position_reg = r'^-?\d+,-?\d+$'
    info = None
    # 是否运行,1是0否
    is_running = 0
    # 用于保存当前按下的按键
    current_keys = set()
    # 键盘监听的线程
    start_key_listener = None
    # 键盘监听
    keyboard_listener = None
    # 键盘监听时, 键盘按下和释放的次数
    key_press_count = 0
    key_release_count = 0

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

        # 设置开始的快捷键的button
        x = 10
        y = y + 40
        self.setStartKeyLabel = qw.QLabel("设置开始快捷键:", self)
        self.setStartKeyLabel.move(x, y)
        self.setStartKeyButton = qw.QPushButton("ALT+F2", self)
        self.setStartKeyButton.move(x + self.setStartKeyLabel.width(), y)
        self.setStartKeyButton.clicked.connect(self.on_set_start_key)
        self.setStartKeyConfirmButton = qw.QPushButton("确定", self)
        self.setStartKeyConfirmButton.move(x + self.setStartKeyLabel.width() + self.setStartKeyButton.width() + 10, y)
        self.setStartKeyConfirmButton.clicked.connect(self.on_set_start_key_confirm)

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

    def closeEvent(self, event):
        super().closeEvent(event)
        if self.keyboard_listener:
            self.keyboard_listener.stop()

    def on_color_frame_position_change(self):
        """
        框体位置输入框值变化
        :return:
        """
        print(self.color_frame_position_input.text())

    @exception_handler
    def on_set_start_key(self, v):
        self.setStartKeyButton.setText("请设置")
        # 线程开启键盘监听
        self.start_key_listener = Thread(target=self.listen_key)
        self.start_key_listener.start()

    @exception_handler
    def listen_key(self):
        # 键盘监听
        self.current_keys = []
        self.keyboard_listener = keyboard.Listener(on_press=self.on_set_key_press, on_release=self.on_set_key_release)
        self.keyboard_listener.start()
        self.keyboard_listener.join()

    @exception_handler
    def on_set_key_press(self, key):
        self.key_press_count = self.key_press_count + 1

        control_char_map = {
            '\x01': 'a',
            '\x02': 'b',
            '\x03': 'c',
            '\x04': 'd',
            '\x05': 'e',
            '\x06': 'f',
            '\x07': 'g',
            '\x08': 'h',
            '\x09': 'i',
            '\x0A': 'j',
            '\x0B': 'k',
            '\x0C': 'l',
            '\x0D': 'm',
            '\x0E': 'n',
            '\x0F': 'o',
            '\x10': 'p',
            '\x11': 'q',
            '\x12': 'r',
            '\x13': 's',
            '\x14': 't',
            '\x15': 'u',
            '\x16': 'v',
            '\x17': 'w',
            '\x18': 'x',
            '\x19': 'y',
            '\x1A': 'z',
            '\x1B': 'ESC',
            '\x7F': 'DEL'
        }

        # 如果是一个字母或数字键/如果是一个特殊键（如 Ctrl, Alt 等）
        try:
            if isinstance(key, keyboard.Key):
                # 控制键, ctrl,alt,shift等
                print('key:', key.name)
            if isinstance(key, keyboard.KeyCode):
                # 字母数字等
                print('keycode:', key.char)
        except:
            pass
        v = key.char if hasattr(key, 'char') else str(key)
        if v not in self.current_keys:
            self.current_keys.append(v)
        print(f'当前按下的按键: {self.current_keys}')

    @exception_handler
    def on_set_key_release(self, key):
        self.key_release_count = self.key_release_count + 1
        print(f'释放后的按键: {self.current_keys}')
        # 停止监听1
        if key == keyboard.Key.esc:
            self.keyboard_listener.stop()
        # 停止监听2
        if self.key_press_count == self.key_release_count:
            def sss(k):
                if hasattr(k, 'char'):
                    return k.char
                else:
                    return str(k)

            # self.current_keys倒序
            s1 = map(sss, self.current_keys)

            self.setStartKeyButton.setText("+".join(s1))
            self.keyboard_listener.stop()

    @exception_handler
    def on_set_start_key_confirm(self, v):
        self.start_key_listener = None
        self.keyboard_listener.stop()

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
