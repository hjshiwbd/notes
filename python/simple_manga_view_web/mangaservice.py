import logging
import os

from flask import jsonify, request

import tools
from resp import Response

folder_root = r'G:\!fin-e\[韩漫]2022年新整理大合集[224本][36.5G]\resources'


def get_all_folders():
    """
    所有2级目录,即漫画目录
    """
    folders = []
    for root, dirs, files in os.walk(folder_root):
        # 当前路径相对root的层级
        level = root.count(os.sep) - folder_root.count(os.sep)
        # logging.info('{}|{}'.format('-' * 4 * level, root))
        if level == 2:
            obj = {
                "name": root.split('\\')[-1],  # root的名字
                "path": root,
            }
            folders.append(obj)
    r = Response(data={
        "rows": folders,
        "total": len(folders)
    })
    return jsonify(r.__dict__)


def manga_detail():
    """
    漫画详情
    """
    # 漫画磁盘路径
    path = request.form.get('path')
    # logging.info('path: %s' % path)

    files = os.listdir(path)
    count = 0
    for f in files:
        file = os.path.join(path, f)
        if os.path.isfile(file) and tools.is_img(file):
            count = count + 1
    # path = d:\a\b\c\d, 截取"c和d",并用"\"链接
    img_parent_path = "/".join(path.split('\\')[-2:])
    r = Response(data={
        "total": count,
        "imgParentPath": img_parent_path
    })
    return jsonify(r.__dict__)
