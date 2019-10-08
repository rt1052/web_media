from flask import Flask, render_template, request
import sqlite3 as sql

import json
import glob
import os
from PIL import Image

app = Flask(__name__)
 

@app.route('/')
def home():
   return render_template('index.html')


@app.route('/photo_pc')
def photo_pc():
   return render_template('photo_pc.html')


@app.route('/photo_mb')
def photo_mb():
   return render_template('photo_mb.html')


@app.route('/photo_view_mb')
def photo_view_mb():
   return render_template('photo_view_mb.html')


@app.route('/video_pc')
def video_pc():
   return render_template('video_pc.html')


@app.route('/video_play_pc')
def video_play_pc():
   return render_template('video_play_pc.html')


@app.route('/video_mb')
def video_mb():
   return render_template('video_mb.html')


@app.route('/video_play_mb')
def video_play_mb():
   return render_template('video_play_mb.html')

 
@app.route('/list')
def list():
   dir = request.args.get("dir")
   dev = request.args.get('dev')
   page = int(request.args.get('page'))
   print(dir, dev, page)

   con = sql.connect("media.db")
   con.row_factory = sql.Row
 
   cur = con.cursor()


   cur.execute("select count(*) from " + dir + ";")
   print("##########")
   #print(cur.fetchone()["count"])

   sql_start = (page-1)*100
   sql_end = page*100
   sql_str = "select * from " + dir + " where num > " + str(sql_start) + " and num < " + str(sql_end) + ";"
   print(sql_str)
   cur.execute(sql_str)
 
   rows = cur.fetchall()

   dict = {"data":[], "num":11}
   for i in rows:
      if (dev == "mb"):
         height = int(i["height"]*440/i["width"])
         width = 440
      elif (dev == "pc"):
         height = i["height"]
         width = i["width"]

      temp = {"name":i["name"], "width":width, "height":height}
      dict["data"].append(temp)

   json_str = json.dumps(dict, indent=1)
   # print(json_str)

   return json_str
 

@app.route('/refresh')
def refresh():
   dir = request.args.get('dir')

   # 获取指定目录下所有jpg文件
   path = "static/media/"+ dir + "/thumb/*.jpg"
   print(path)
   # #加上r让字符串不转义
   # r'../media/photo/thumb/*.jpg'
   list = glob.glob(path)
   print(len(list))


   con = sql.connect("media.db")
   cur = con.cursor()
   # 删除表
   cur.execute("DROP TABLE " + dir) 
   # 建立照片表
   cur.execute("CREATE TABLE " + dir + " (num INT NOT NULL, name TEXT NOT NULL, width INT NOT NULL, height INT NOT NULL);")

   num = 0
   for i in list:
      # 读取图片信息
      img = Image.open(i)
      width, height = img.size
      # 获取文件名
      name = os.path.join(i[25:])
      num += 1

      print(num, name, width, height)

      cur.execute("INSERT INTO "+ dir + " (num, name, width, height) VALUES (?,?,?,?)", (num, name, width, height))
      con.commit()

   con.close()

   return render_template('test.html')


if __name__ == '__main__':
   app.run(debug=True, host='0.0.0.0', port=80)

