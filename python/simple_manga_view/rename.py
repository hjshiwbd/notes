"""
批量重命名img文件
将文件夋下的所有图片文件重命名为Image00001.jpg, Image00002.jpg, ...
"""

import os

folder = r'G:\!fin-e\[韩漫]2022年新整理大合集[224本][36.5G]\2024\[韩漫] 亲子餐厅的妈妈们 50-105话 完结 中文无水印'
prefix = 'Image'
left_padd_len = 5


def is_img(f):
    """
    判断是否为图片文件
    """
    return os.path.splitext(f)[1].lower() in ['.jpg', '.png', '.jpeg']


n = 1
for f in os.listdir(folder):
    if is_img(f):
        newname = f'{prefix}{str(n).zfill(left_padd_len)}{os.path.splitext(f)[1]}'
        n = n + 1
        os.rename(os.path.join(folder, f), os.path.join(folder, newname))
    pass
