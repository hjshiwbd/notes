"""
所有子文件夹穷举
文件夹结构
├─app.py
├─other.py
├─index.html
├─manga_category1_folder
│  └─managa_folder1-1
│      ├─manga_images_1~9999.jpg
│  └─managa_folder1-2
│      ├─manga_images_1~9999.jpg
├─manga_category2_folder
│  └─managa_folder2-1
│      ├─manga_images_1~9999.jpg
│  └─managa_folder2-2
│      ├─manga_images_1~9999.jpg
"""

import os
import sys
import json


def is_has_index(file_list):
    has_index = False
    for f in file_list:
        if f == "~index.html":
            has_index = True
            break
    return has_index


def gen_mklink_script():
    """
    为2级文件夹的~index.html文件,生成mklink脚本
    此代码不会实际影响文件
    需要cmd管理员权限手动运行, 才能生成软链接
    """
    p = sys.path[0]

    for parent_folder, folder_list, file_list in os.walk(p):
        # 获取parent_folder的目录层级
        level = parent_folder.count(os.sep) - p.count(os.sep)
        if level == 2:
            # 判断当前路径下是否已有~index.html文件
            if is_has_index(file_list):
                continue

            s = f"""
    mklink /h "{parent_folder}\\~index.html" "g:\\!fin-e\\[韩漫]2022年新整理大合集[224本][36.5g]\\~index.html"
    """.strip()
            print(s)


def gen_image_file_count_json():
    """
    读取2级文件夹下的所有图片文件数量, 生成json文件
    """
    p = sys.path[0]
    result = {}
    for parent_folder, folder_list, file_list in os.walk(p):
        # dirpath相对盘符的层级 - root相对盘符的层级 = 2, 说明是第一层子文件夹
        level = parent_folder.count(os.sep) - p.count(os.sep)
        if level == 2:
            # parent_folder是全路径, 取最后一级文件夹名
            folder_name = parent_folder.split("\\")[-1]
            # file_list里图片文件的数量
            n = 0
            for f in file_list:
                if os.path.splitext(f)[1].lower() in ['.jpg', '.png', '.jpeg']:
                    n = n + 1
            result[folder_name] = n
        pass
    str = json.dumps(result, indent=4, ensure_ascii=False)
    str = "var imageCount = " + str
    io = open('image_count.js', 'w', encoding='utf8')
    io.write(str)
    io.close()
    print('image_count.js generate ok')


if __name__ == '__main__':
    gen_mklink_script()
    gen_image_file_count_json()
