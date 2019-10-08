#coding=utf-8

import json
import glob
import os
from PIL import Image


def make_json(dir):

    # 获取指定目录下所有jpg文件
    path = "../media/"+ dir + "/thumb/*.jpg"
    list = glob.glob(path)
    print(len(list))
    data_num = 100
    page_num = int(len(list)/data_num) + 1

    cnt = 0
    page = 0
    # 建立字典
    dict = {"data":[], "num":page_num}

    for i in list:
        # 读取图片信息
        img = Image.open(i)
        w, h = img.size
        h = int(h*440/w)
        w = 440

        # 获取文件名
        name = os.path.join(i[21:])
        # 添加键值对并写入字典
        temp = {"name":name, "width":w, "height":h}
        dict["data"].append(temp)

        cnt += 1
        if (cnt >= data_num):
            cnt = 0
            page += 1

            # 创建json文件
            file_name = "../json/" + dir + "_thumb_mb" + str(page) + ".json"
            with open(file_name, "w") as file:
                # 把字典按照json样式可视化显示
                json_str = json.dumps(dict, indent=1)
                file.write(json_str)
                file.close()
                dict = {"data":[], "num":page_num}

    if (cnt > 0):
        page += 1
        # 创建json文件
        file_name = "../json/" + dir + "_thumb_mb" + str(page) + ".json"
        with open(file_name, "w") as file:
            # 把字典按照json样式可视化显示
            json_str = json.dumps(dict, indent=1)
            file.write(json_str)
            file.close()         

    print("finish")

if __name__=='__main__':
    # make_json("video")
    make_json("photo")
