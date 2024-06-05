import os

def is_img(f):
    """
    判断是否为图片文件
    """
    return os.path.splitext(f)[1].lower() in ['.jpg', '.png', '.jpeg']
