#coding=utf-8

import os
import glob
from PIL import Image

img_arr = []
screen_width = 1880

html_head = """
<!DOCTYPE html>
<html>
<head>
<meta charset=\"utf-8\">
<title>photo</title>
<style>

.flex-container {
    display: -webkit-flex;
    display: flex;
    width: 100%;
    height: auto;
    background-color: white;
}

.flex-item {
    background-color: cornflowerblue;
    width: auto;
    height: auto;
    margin: 10px;
}

img {
    border: 1px solid #ddd;
    border-radius: 4px;
    padding: 5px;
}

</style>
</head>
<body>

"""

html_end = """
</body>
</html>
"""

def get_img_info():
    # 将图片名称、长、宽保存到数组
    a = glob.glob(r'../media/video/thumb/*.jpg')
    for i in a:
        img = Image.open(i)
        w, h = img.size
        info = {}
        info['name'] = i[21:]
        info['width'] = w
        info['hight'] = h
        img_arr.append(info)


def separate():
    # 建立网页
    f = open("../html/video.html",'w')

    row_cnt = 0
    sum_width = 0
    sum_cnt = 0
    tmp_arr = []
    f.write(html_head)

    for i in img_arr:
        tmp = i['width']
        name = i['name']

        # 加上图片宽度一半就超过屏幕宽度,则把当前图片放下下一行
        if ((screen_width-sum_width) < tmp/2):
            zoom = int((screen_width-10*sum_cnt)*200/sum_width)
            print (sum_width, sum_cnt, zoom)
            # 建立新容器
            f.write("<div class=\"flex-container\">\r\n")
            for i in tmp_arr:
                # 添加图片信息
                f.write("  <div class=\"img\">\r\n")
                f.write("    <a target=\"_blank\" href=\""+"../media/video/"+i[:-4]+".mp4\">\r\n")
                f.write("      <img src=\""+"../media/video/thumb/"+i+"\" alt=\"Mountains\" height=\""+str(zoom)+"\">\r\n")
                f.write("    </a>\r\n")
                f.write("  </div>\r\n\r\n")
            f.write("</div>\r\n\r\n")

            row_cnt += 1
            if row_cnt > 10:
                break

            tmp_arr = []
            sum_cnt = 1
            tmp_arr.append(name)
            sum_width = tmp
            
        else:
            sum_width += tmp
            sum_cnt += 1
            tmp_arr.append(name)


    # 剩余的图片
    f.write("<div class=\"flex-container\">\r\n")
    for i in tmp_arr:
        # 添加图片信息
        f.write("  <div class=\"img\">\r\n")
        f.write("    <a target=\"_blank\" href=\""+"../media/video/"+i[:-4]+".mp4\">\r\n")
        f.write("      <img src=\""+"../media/video/thumb/"+i+"\" alt=\"Mountains\" height=\""+str(200)+"\">\r\n")
        f.write("    </a>\r\n")
        f.write("  </div>\r\n\r\n")
    f.write("</div>\r\n\r\n\r\n")

    f.write(html_end)
    f.close()


if __name__=='__main__':
    path='.'
    get_img_info()
    separate()

