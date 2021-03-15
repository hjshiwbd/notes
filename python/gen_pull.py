import sys
import os

"""
对root文件夹下所有git仓库执行git pull
约定:
  默认root下每个文件夹都是一个仓库,执行git pull
  root下以"!"开头的文件夹表示下一个仓库的多个分支,会对每个仓库都git pull
  全局变量excludes表示不是仓库的文件夹,不处理
  
eg:
  root=D:\\git\\yuzhi
  root下有子文件夹"wechat-parent", "!admin", "!new folder"
  "wechat-parent"是普通仓库,
  "!admin"是包含多个分支的仓库,目录结构为:D:\\git\\yuzhi\\!admin\\1.2.0\\yuzhi-app-admin (root\\二级仓库简称\\三级分支版本名\\四级仓库名)
  "!new folder"是不处理的文件夹

调用脚本
@echo off
python gen_pull.py
pull.bat
"""

# 指定的不pull
excludes = ["!new folder"]
# !开头的要搜索其二级目录,并pull
# !开头的!new folder不pull

root = sys.path[0]


def is_exclude(name):
    flag1 = name in excludes
    return flag1


def get_folers(root_folder):
    result = []
    a = os.listdir(root_folder)
    for file_name in a:
        if is_exclude(file_name):
            continue
        p = os.path.join(root_folder, file_name)
        if not os.path.isfile(p):
            # if not is_exclude(file_name):
            if file_name.startswith("!"):
                # !开头的文件夹,其下每个文件夹都是一个仓库
                # D:\git\yuzhi\!admin\4.0.0\yuzhi-app-admin
                lv2_folder = os.path.join(root_folder, file_name)
                lv3_name_list = os.listdir(lv2_folder)
                for lv3_name in lv3_name_list:
                    lv3_folder = os.path.join(lv2_folder, lv3_name)
                    lv4_name = os.listdir(lv3_folder)[0]
                    result.append(os.path.join(lv3_folder, lv4_name))
            else:
                p = os.path.join(root_folder, file_name)
                result.append(p)
    return result


def list_to_bat(list):
    total = len(list)
    count = 0
    result = []
    for p in list:
        count = count + 1
        result.append("echo %s, %s/%s" % (p, str(count), str(total)))
        result.append("git -C \"" + p + "\" pull")
    result.append("pause")
    txt = "\n".join([x for x in result])
    return txt


def run():
    list1 = get_folers(root)
    txt = list_to_bat(list1)
    # print(txt)
    io = open('pull.bat', "w+")
    io.write(txt)
    io.close()


if __name__ == '__main__':
    run()
