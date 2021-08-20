# coding:utf-8

import os
from MyQR import myqr
words = '''
http://deccapay.fuioupay.com/native?token=20210820081127466007
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