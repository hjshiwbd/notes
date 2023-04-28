# coding=utf-8
"""
修改git地址的域名部分
git -C D:\\git\\yuzhi\\318-portal remote -v
git -C D:\\git\\yuzhi\\318-portal remote set-url origin http://git.wedemo.cn:82/ems/318-portal.git
"""

import logging
import os
import re
import traceback

logging.basicConfig(level=logging.INFO,
                    format='%(asctime)s|%(levelname)s|%(process)d|%(filename)s.%(lineno)d|%(message)s',
                    datefmt='%y-%m-%d %H:%M:%S')


def git_set_url(path):
    cmd = f'git -C {path} remote -v'

    url = ""
    try:
        r = os.popen(cmd)
        for x in r.readlines():
            if "origin" in x:
                ss = re.findall(r'http://\S*', x)
                if len(ss) > 0:
                    url = ss[0]
                break
    except Exception as e:
        logging.info(e)
        traceback.print_exc()

    if url != "" and ":82" in url:
        # url = url.replace("at4", "wedemo")
        url = url.replace(":82", "")
        set_cmd = f'git -C "{path}" remote set-url origin {url}'
        logging.info(set_cmd)
        os.popen(set_cmd)
    else:
        logging.info(f"{path} url invalid:{url}")


def run():
    # path = "D:\\git\\yuzhi\\apartment-mpw"
    # git_set_url(path)

    root = "D:\\git\\yuzhi"
    dirlist = os.listdir(root)

    ignore = ['!new folder']

    for d in dirlist:
        if os.path.isdir(os.path.join(root, d)):
            if not d.startswith("!"):
                p = os.path.join(root, d)
                logging.info(p)
                git_set_url(p)
            # else:
            #     if d not in ignore:
            #         # d=!xx d+child1+child1-1=!xx/[ver]/prjname
            #         prefix_emark = os.path.join(root, d)  # "!"开头
            #         children1 = os.listdir(prefix_emark)  # ver
            #         for child1 in children1:
            #             c1 = os.listdir(os.path.join(root, d, child1))  # prjname
            #             pp = os.path.join(prefix_emark, child1, c1[0])
            #             logging.info(pp)
            #             git_set_url(pp)


if __name__ == '__main__':
    run()
