import sys
import logging
import os
import re
from logging.handlers import TimedRotatingFileHandler


def setup_logger(log_name, log_path=sys.path[0]):
    """
    创建日志.依赖于全局有个cst.py文件,且存在cst.env
    :param log_name: 日志名称
    :return:
    """
    log = logging.getLogger()
    log.setLevel(logging.INFO)

    log_formatter = logging.Formatter(
        "%(asctime)s|%(levelname)s|%(process)d|%(filename)s.%(lineno)d|%(message)s"
    )

    os.makedirs(os.path.join(log_path, "logs"), exist_ok=True)
    log_path = os.path.join(log_path, "logs", log_name + ".log")
    # interval 滚动周期，
    # when="MIDNIGHT", interval=1 表示每天0点为更新点，每天生成一个文件
    # backupCount  表示日志保存个数
    file_handler = TimedRotatingFileHandler(
        filename=log_path, when="MIDNIGHT", interval=1, backupCount=30
    )
    # filename="mylog" suffix设置，会生成文件名为mylog.2020-02-25.log
    file_handler.suffix = "%Y-%m-%d"
    # extMatch是编译好正则表达式，用于匹配日志文件名后缀
    # 需要注意的是suffix和extMatch一定要匹配的上，如果不匹配，过期日志不会被删除。
    file_handler.extMatch = re.compile(r"^\d{4}-\d{2}-\d{2}.log$")
    file_handler.setFormatter(log_formatter)
    log.addHandler(file_handler)

    # streaHandler
    stream_handler = logging.StreamHandler()
    stream_handler.setLevel(logging.DEBUG)
    stream_handler.setFormatter(log_formatter)
    log.addHandler(stream_handler)

    return log


def exception_handler(func):
    """
    修饰器, 捕获异常
    :param func:
    :return:
    """

    def wrapper(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except Exception as e:
            print(e)
            traceback.print_exc()
            qw.QMessageBox.warning(None, "系统异常", str(e))

    return wrapper
