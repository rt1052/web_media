#coding=utf-8

import os
import glob
from PIL import Image


html_head_str = """
<!DOCTYPE html>
<html>
<head>
<meta charset="utf-8">
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

.img-m {
    border: 1px solid #ddd;
    border-radius: 4px;
    padding: 5px;
}


#imgModule{
  display:none;
}

.mask{
  background:black;
  position:fixed;
  left:0;
  top:0;
  width:100%;
  height:100%;
}

.lightBoxContent{
  width:90%;
  height:90%;
  position:fixed;
  left:5%;
  top:5%;
  background:black;
  text-align:center
}

#imgLoader{
  width:60px;
  height:60px;
  position:fixed;
  left:50%;
  top:50%;
  margin:-16px 0 0 -16px;
  display:none;
}

#imgLight{
  width:auto;
  height:100%;
  -webkit-animation:change 1s;
  animation:change 1s;
  transform:rotate(0deg);  
}

.btn{
  width:40px;
  height:50px;
  position:fixed;
  top:50%;
  margin-top:-25px;
  cursor:pointer;
}

.lightBoxSprite{
  background-image:url(imgIcons.png);
  background-repeat:no-repeat;
}

#lightBoxPrev{
  left:150px;
  background-position:2px center;
}

#lightBoxNext{
  right:150px;
  background-position:-42px center;
}

#lightBoxClose{
  right:150px;
  top:10%;
  background-position:-100px center;
}

</style>
</head>
<body>

<div id="main">
"""

html_end_str = """
</body>
</html>
"""

html_script_str = """
<script>
(function(){
    var LightBox = function(options){
        this.idx = 0;
        this.angle = 0;
        this.init();
    };

    LightBox.prototype.init = function(){
        this.renderDOM();
        this.imgListClick();
        this.nextBtnClick();
        this.prevBtnClick();
        this.closeBtnClick();
        this.imgClick();
    };

    LightBox.prototype.renderDOM = function(){
        var imgModule = document.createElement("div");
        imgModule.id = "imgModule";

        var oHtml = "";
        oHtml += '<div class="mask"></div>';
        oHtml +=    '<div class="lightBox">';
        oHtml +=        '<div class="lightBoxContent">';
        oHtml +=            '<img src="loading.gif" alt="" id="imgLoader">';
        oHtml +=            '<img alt="" id="imgLight">';
        oHtml +=        '</div>';
        oHtml +=        '<span class="btn lightBoxSprite" id="lightBoxPrev"></span>';
        oHtml +=        '<span class="btn lightBoxSprite" id="lightBoxNext"></span>';
        oHtml +=        '<span class="btn lightBoxSprite" id="lightBoxClose"></span>';         
        oHtml +=    '</div>';

        imgModule.innerHTML = oHtml;
        document.body.appendChild(imgModule);
    };

    LightBox.prototype.imgListClick = function(){
        var imgList = document.getElementsByClassName("img-m");
        var imgModule = document.getElementById("imgModule");
        var self = this;

        for(var i = 0; i < imgList.length; i++){
            imgList[i].index = i;

            imgList[i].onclick = function(){
                imgModule.style.display = "block";
                var src = this.getAttribute("data-src");
                self.idx = this.index;

                self.imgLoad(src);
            }
        }
    };

    LightBox.prototype.prevBtnClick = function(){
        var prevBtn = document.getElementById("lightBoxPrev");
        var self = this;

        prevBtn.onclick = function(){
            var imgList = document.getElementsByClassName("img-m");
            
            self.idx--;

            if(self.idx < 0){  
                self.idx = imgList.length - 1;  
            }

            var src = imgList[self.idx].getAttribute("data-src");
            self.imgLoad(src);
        }
    };

    LightBox.prototype.nextBtnClick = function(){
        var nextBtn = document.getElementById("lightBoxNext");
        var self = this;
        
        nextBtn.onclick = function(){
            var imgList = document.getElementsByClassName("img-m");

            self.idx++;            

            if(self.idx >= imgList.length){  
                self.idx = 0;  
            }

            var src = imgList[self.idx].getAttribute("data-src");
            self.imgLoad(src);
        }
    };

    LightBox.prototype.closeBtnClick = function(){
        var closeBtn = document.getElementById("lightBoxClose");
        var imgLight = document.getElementById("imgLight");
        var imgModule = document.getElementById("imgModule");        
        
        closeBtn.onclick = function(){
            imgModule.style.display = "none";
            imgLight.src = "";
        }    
    };    

    LightBox.prototype.imgClick = function(){
        var imgLight = document.getElementById("imgLight");
        var imgModule = document.getElementById("imgModule");
        
        imgLight.onclick = function(){
            self.angle = (self.angle+90)%360;
            this.style.transform = "rotate("+self.angle+"deg)";
        }     
    };    

    LightBox.prototype.imgLoad = function(src, callback){
        var imgLight = document.getElementById("imgLight");
        var loader = document.getElementById("imgLoader");
        loader.style.display = "block";
        // imgLight.src = "";

        var img = new Image();
        img.onload = function(){
            loader.style.display = "none";
            self.angle = 0;
            imgLight.style.transform = "rotate("+self.angle+"deg)";            
            imgLight.src = src;
        };
        img.src = src;
    };

    window.LightBox = LightBox;
})();

new LightBox();
</script>
"""


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

        self.html_file.write(html_script_str)                    
        self.html_file.write(html_end_str)
        self.html_file.close()      


    def html_row(self, arr, zoom):
        self.html_file.write("<div class=\"flex-container\">\r\n")
        for i in arr:
            # 添加图片信息
            # self.html_file.write("  <div class=\"img\">\r\n")
            self.html_file.write("  <div>\r\n")
            self.html_file.write("      <img class=\"img-m\" \
                                             src=\""+"../media/"+self.dir+"/thumb/"+i+"\" \
                                             data-src=\""+"../media/"+self.dir+"/"+i[:-4]+self.format+"\" \
                                             alt=\""+i+"\" height=\""+str(zoom)+"\">\r\n")
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
        # div-main的结束
        self.html_file.write("</div>\r\n\r\n") 
        self.html_file.close()

        self.html_finish()


if __name__=='__main__':
    '''
    a = make_html("mb", "photo")
    a.separate()
    del a
    '''

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
    '''
