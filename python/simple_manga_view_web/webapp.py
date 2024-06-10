import logging
import os
import sys

from flask import Flask, render_template, send_from_directory

app = Flask('mangaview')

import mangaservice
import utils

run_path = ''


def run():
    """
    app初始化
    """
    app.template_folder = 'web/pages'
    app.static_folder = 'web/assets'
    app.run(host='0.0.0.0', port=3002, debug=False)


@app.route('/')
def index():
    """
    首页
    """
    return render_template('/index.html')


@app.route('/view')
def view():
    """
    首页
    """
    return render_template('/view.html')


@app.route('/api/getAllFolders', methods=['POST'])
def get_all_folders():
    """
    列出满足条件的文件夹
    """
    return mangaservice.get_all_folders()


@app.route('/api/mangaDetail', methods=['POST'])
def manga_detail():
    """
    漫画详情
    """
    return mangaservice.manga_detail()


@app.route('/imgs/<folder1>/<folder2>/<img_name>')
def get_img(folder1, folder2, img_name):
    folder = os.path.join(run_path, 'resources', folder1, folder2)
    return send_from_directory(folder, img_name)


if __name__ == '__main__':
    utils.setup_logger('manga')
    # 获得运行路径
    run_path = os.path.dirname(os.path.abspath(__file__))
    run()
