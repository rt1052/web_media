#coding=utf-8

import os
import glob
from PIL import Image

def thumbnail_pic():
    a = glob.glob(r'../media/photo/*.jpg')

    cnt = 0
    for i in a:
        cnt += 1
        if (cnt > 99):
            break
        name = os.path.join("../media/photo/thumb_mb", i[15:])
        # 本来就存在缩略图不会重复操作
        if False == os.path.exists(name):
            img = Image.open(i)
            w, h = img.size
            # 按比例把图片高度调整为200
            height = int(h*440/w)
            # width = int(w*200/h)
            out = img.resize((440, height))
            print(name, out.format, out.size, out.mode)
            out.save(name, 'JPEG')
            img.close()
    print('Done!')


if __name__=='__main__':
    path='.'
    thumbnail_pic()


