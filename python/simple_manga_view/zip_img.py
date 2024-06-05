import os

import tools
from PIL import Image

folder = r'G:\!fin-e\[韩漫]2022年新整理大合集[224本][36.5G]\2024\美麗新世界1-216'
# kb
target_size = 400

for f in os.listdir(folder):
    if tools.is_img(f):
        # 获取图片的大小
        imgfile = os.path.join(folder, f)
        size = os.path.getsize(imgfile)
        quality = 100
        # size > 300k
        while size > target_size * 1024:
            # 使用第三方库pillow, 压缩图片: 名称不变,大小200k以下,图片分辨率不变
            zip_imgfile = os.path.join(folder, f"zip_{f}")
            img = Image.open(imgfile)
            quality = quality * 0.8
            img.save(zip_imgfile, quality=int(quality))
            size = os.path.getsize(zip_imgfile)
            # size convert to mb str
            size2 = f"{size / 1024:.2f}kb"
            print(f"zip {quality}: {imgfile} to {zip_imgfile} size: {size2}")
