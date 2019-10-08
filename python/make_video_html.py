#coding=utf-8

import os
import glob
from PIL import Image


html_head_str = """
<!DOCTYPE html>
<html>
<head>
<meta charset=\"utf-8\">
<title>media</title>
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

html_end_str = """
</body>
</html>"""



class make_html(object):
    """docstring for ClassName"""
    row_cnt = 0
    page_cnt = 0
    img_arr = None
    html_path = None
    html_file = None
    screen_width = 0
    screen_row = 0
    button_size = 0
    font_size = 0
    device = None
    dir = None
    format = None

    def __init__(self, dev, dir):
        self.device = dev
        self.dir = dir

        if (self.dir == "video"):
            self.format = ".mp4"
        elif (self.dir == "photo"):
            self.format = ".jpg"

        if (dev == "pc"):
            self.screen_width = 1880
            self.screen_row = 10
            self.html_path = "../html/"+self.dir+"_pc_page.html"
            self.button_size = 50
            self.font_size = 20

        elif (dev == "mb"):
            self.screen_width = 960
            self.screen_row = 20
            self.html_path = "../html/"+self.dir+"_mb_page.html"
            self.button_size = 100
            self.font_size = 40


    def get_img_info(self):
        self.img_arr = []
        # 将图片名称、长、宽保存到数组
        file_list = glob.glob(r"../media/"+self.dir+"/thumb/*.jpg")
        for i in file_list:
            img = Image.open(i)
            w, h = img.size
            info = {}
            info['name'] = i[21:]
            info['width'] = w
            info['hight'] = h
            self.img_arr.append(info)


    def html_start(self):
        # 建立新网页
        self.page_cnt += 1
        print(self.page_cnt)
        self.html_file = open(self.html_path[:21]+str(self.page_cnt)+self.html_path[21:], 'w')
        self.html_file.write(html_head_str)             


    def html_end(self, page):
        # 添加页面选择按钮
        self.html_file.write("<p>\r\n")
        self.html_file.write("  <br>\r\n")

        self.html_file.write("    <a href=\"http://192.168.0.42\"><input type=\"button\" value=\"<\"\
                             style=\"width:"+str(self.button_size)+"px;height:"+str(self.button_size)+"px;font-size:"\
                             +str(self.font_size)+"px;background:"+"white"+";border:none;\" /></a>\r\n")

        for i in range(1, self.page_cnt):
            if (i == page):
                self.html_file.write("    <a href=\"http://192.168.0.42/html/"+self.dir+"_"+self.device+"_page"+str(i)\
                                      +".html\"><input type=\"button\" value=\""+str(i)\
                                      +"\" style=\"width:"+str(self.button_size)+"px;height:"+str(self.button_size)+"px;font-size:"\
                                      +str(self.font_size)+"px;background:"+"lightblue"+";border:none;\" /></a>\r\n")      
            else:
                self.html_file.write("    <a href=\"http://192.168.0.42/html/"+self.dir+"_"+self.device+"_page"+str(i)\
                                      +".html\"><input type=\"button\" value=\""+str(i)\
                                      +"\" style=\"width:"+str(self.button_size)+"px;height:"+str(self.button_size)+"px;font-size:"\
                                      +str(self.font_size)+"px;background:"+"white"+";border:none;\" /></a>\r\n")  
                    
        self.html_file.write("  </br>\r\n")
        self.html_file.write("  <br>\r\n")
        self.html_file.write("  </br>\r\n")
        self.html_file.write("</p>\r\n")                
        self.html_file.write(html_end_str)
        self.html_file.close()      


    def html_row(self, arr, zoom):
        self.html_file.write("<div class=\"flex-container\">\r\n")
        for i in arr:
            # 添加图片信息
            self.html_file.write("  <div class=\"img\">\r\n")
            self.html_file.write("    <a target=\"_blank\" href=\""+"../media/"+self.dir+"/"+i[:-4]+self.format+"\">\r\n")
            self.html_file.write("      <img src=\""+"../media/"+self.dir+"/thumb/"+i+"\" alt=\"Mountains\" height=\""+str(zoom)+"\">\r\n")
            self.html_file.write("    </a>\r\n")
            self.html_file.write("  </div>\r\n\r\n")
        self.html_file.write("</div>\r\n\r\n")        


    def html_finish(self):
        self.page_cnt += 1
        for i in range(1, self.page_cnt):
            self.html_file = open(self.html_path[:21]+str(i)+self.html_path[21:], 'a+')
            self.html_end(i)


    def separate(self):
        
        sum_width = 0
        sum_cnt = 0
        tmp_arr = []

        self.get_img_info()
        self.html_start()

        for i in self.img_arr:
            tmp = i['width']
            name = i['name']

            # 加上图片宽度一半就超过屏幕宽度,则把当前图片放下下一行
            if ((self.screen_width-sum_width) < tmp/2):
                zoom = int((self.screen_width-10*sum_cnt)*200/sum_width)
                print (sum_width, sum_cnt, zoom)
                # 一行图片
                self.html_row(tmp_arr, zoom)

                self.row_cnt += 1
                # 一个页面包含十行图片
                if self.row_cnt > self.screen_row:
                    self.row_cnt = 0
                    self.html_file.close()
                    self.html_start()      

                tmp_arr = []
                sum_cnt = 1
                tmp_arr.append(name)
                sum_width = tmp
                
            else:
                sum_width += tmp
                sum_cnt += 1
                tmp_arr.append(name)

        # 最后一行图片
        self.html_row(tmp_arr, 200)
        self.html_file.close()

        self.html_finish()


if __name__=='__main__':
    '''
    a = make_html("mb", "photo")
    a.separate()
    del a

    b = make_html("pc", "photo")
    b.separate()
    del b
    '''

    c = make_html("mb", "video")
    c.separate()
    del c

    d = make_html("pc", "video")
    d.separate()
    del d

