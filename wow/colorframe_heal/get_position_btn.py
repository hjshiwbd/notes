from threading import Thread

import PyQt6.QtWidgets as qw
from pynput import mouse

from tools import exception_handler


class GetPositionButton(qw.QPushButton):
    # 是否在获取位置, 1是0否
    get_position_state = 0
    on_get_position = None

    def __init__(self, parent_widget, x, y, on_get_position):
        super().__init__()
        self.setText("获取")
        self.setParent(parent_widget)
        self.resize(130, 30)
        self.move(x, y)
        self.clicked.connect(self.on_get_position)
        self.on_get_position = on_get_position

    @exception_handler
    def on_get_position(self, v):
        """
        获取框体位置
        :return:
        """
        self.setText("请点击坐标位置")
        if self.get_position_state == 0:
            self.get_position_state = 1
            # 线程创建监听器,以免阻塞主线程
            self.listener_thread = Thread(target=self.start_listener)
            self.listener_thread.start()

    def start_listener(self):
        with mouse.Listener(on_click=self.on_click) as listener:
            listener.join()
            # self.listener_thread线程关闭
            self.listener_thread = None

    @exception_handler
    def on_click(self, x, y, btn, pressed):
        if pressed and self.get_position_state == 1:
            self.get_position_state = 0
            if self.on_get_position:
                info = {
                    "x": x,
                    "y": y
                }
                self.on_get_position(info)
            # self.color_frame_position_input.setText(f"{x},{y}")
            self.setText("已获取.可再点击获取")
            return False
