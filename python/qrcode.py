# coding:utf-8

import os
from MyQR import myqr
words = '''
https://qr.alipay.com/bax03807pz9bvst5kxf60001
'''.strip()
version, level, qr_name = myqr.run(
    words,
    version=1,
    level='H',
    picture=None,
    colorized=False,
    contrast=1.0,
    brightness=1.0,
    save_name=None,
    save_dir='C:\\Users\\Administrator\\Desktop'
)