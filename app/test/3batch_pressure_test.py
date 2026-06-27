# -*- coding: utf-8 -*-

import requests
import time
from PIL import Image
from io import BytesIO
import base64
import os
import json
from datetime import datetime
import shutil
import PIL
from PIL import ImageFile
from tqdm import tqdm
import traceback

from concurrent.futures import ThreadPoolExecutor



def appendTxt(txtStr,txtpath):    
    f = open(txtpath,'a', encoding="utf-8")
    f.write(txtStr+'\n')
    f.close()    
    
    
def rewrite(txtStr,txtpath):    
    f = open(txtpath,'w', encoding="utf-8")
    f.write(txtStr+'\n')
    f.close()

# url = 'http://192.168.10.47:20067/query'
#url = 'http://192.168.10.51:20072/query'
#url = 'http://192.168.10.56:20093/query'
url = 'http://192.168.10.166:20096/query'

# file_scan_path=r"D:\01项目测试数据\待OCR识别+统计字数\20241125 59种_to"
error_file_path=r"F:\Python37\py_file\wenzhou-20250715-to_error2.txt"
file_scan_path= r"F:\大数据中心\33 - 明代别集数据库\5-待OCR识别+统计字数\20260420_to"


def compress_image_wh(infile,outfile,_width,_height, isratio):
    Image.MAX_IMAGE_PIXELS = 2300000000
    #print("==>压缩到固定高宽 ", _height, "->", _width)
    
    with  Image.open(infile) as my_image:
            
        #print("The original size is: ", round(len(my_image.fp.read())/1024,2), "KB")
        #Image.NEAREST ：低质量 
        #Image.BILINEAR：双线性 
        #Image.BICUBIC ：三次样条插值 
        #Image.ANTIALIAS：高质量
        #compressed the image
        if isratio is not True:
            my_image = my_image.resize((int(_width), int(_height)),PIL.Image.LANCZOS)
                         
        else:
            # the original width and height of the image
            image_height = my_image.height
            image_width = my_image.width      
                 
            radio = image_height/image_width
            width = _height / radio
            width_radio = int(width)
            #print("==>计算后的宽度：", width_radio)
            my_image = my_image.resize((int(width_radio), int(_height)),PIL.Image.LANCZOS)
            #my_image = my_image.resize((int(image_width / 2), int(image_height / 2)),PIL.Image.LANCZOS)
        
        my_image = my_image.convert("RGB")
        #save the image
        my_image.save(outfile)

        #open the compressed image
        picsize=0
        with Image.open(outfile) as compresed_image:
            picsize = round(len(compresed_image.fp.read())/1024,2) 
            #print("The size of compressed image is: ", picsize, 'kb')
            #print("topath=",topath)
            return picsize

def GetFileByDirList(dirpath, fileList):
    newDir = dirpath
    if os.path.isfile(dirpath):
        basename=os.path.splitext(dirpath)[1]
        #402881e85e702e13015e707f387413691577350412694_CatalogFile
        if basename== ".jpg":
            filename=os.path.basename(dirpath)
            #if filename == 'tabel-6.jpg':
                #print(dirpath)
            fileList.append(dirpath)
                
    elif os.path.isdir(dirpath):  
        #dirlist.append(dirpath)
        for s in os.listdir(dirpath):
            newDir = os.path.join(dirpath,s)
            GetFileByDirList(newDir, fileList)  
    return fileList


#import numpy as np
def run():
    
    if os.path.exists(error_file_path):
        os.remove(error_file_path)
        print("==>删除"+error_file_path+"成功！")
        
    createtime=datetime.now().strftime("%Y-%m-%d")
    print(createtime)
    
    bookdirs=os.listdir(file_scan_path)
    bookbar = tqdm(bookdirs)
    for _bookdir in bookbar:
        #print(bookdir)
        bookdir = os.path.join(file_scan_path,_bookdir)
        #if _bookdir != "64a4828219854913a77ed45c1677279d":
        #    continue
        bookname=os.path.basename(_bookdir)
        if bookname == 'ZSK92494 少石集十三卷':
            continue
            
        bookbar.set_description("解析图书 %s" % _bookdir)
        
        jsondirpath=bookdir+"\\json\\"
               
        if os.path.exists(jsondirpath) is False:
            os.mkdir(jsondirpath)
        #else:
        #    shutil.rmtree(jsondirpath)
        #    os.mkdir(jsondirpath)
            
        # fp = open(file_path, 'rb')
        # files = {"img": fp}
        jpglist=GetFileByDirList(bookdir+"\\pageimages_old", [])
        
        newpicdirpath=bookdir+"\\pageimages\\"
        if os.path.exists(newpicdirpath) is False:
            os.mkdir(newpicdirpath)
        #else:
        #    shutil.rmtree(newpicdirpath)
        #    os.mkdir(newpicdirpath)
                    
        #bar = tqdm(jpglist)
        print("文件总数：", len(jpglist))
        for file_path in jpglist:
                   
            #print("图片先压缩处理", file_path)
            fname=os.path.basename(file_path)
            #bar.set_description("Processing %s" % fname)
            
            fp = os.path.dirname(file_path)
            basename, ext = os.path.splitext(fname)           
                       
            newpicpath=newpicdirpath + fname
            topath = newpicpath
                        
            #print(createtime, "==>输出的文件是：",topath)
            basename, ext = os.path.splitext(fname)
                
            jsonpath=bookdir+"\\json\\"+basename+".json"
            if os.path.exists(jsonpath):
                continue
            
            _width = 300
            _height = 1000
            picsize=compress_image_wh(file_path,topath,_width,_height,True)
            #print(topath)
            with open(topath, 'rb') as f:
                image = f.read()
                image_base64 = str(base64.b64encode(image), encoding='utf-8')
        
            fname=os.path.basename(file_path)
            #print(fname)
            
            files = {'image': image_base64,
                     'imgName': fname,
                     'layout': 'single_column'
                    }
            
            
            
            files = json.dumps(files)
        
            session = requests.Session()
            start_time = time.time()
            try:
                response = session.post(url=url, data=files)
                  
                respJson = response.content.decode('utf-8')
                json_data = json.loads(respJson)
                code = json_data['code']
                if code == 200:
                    images = json_data['Images']
                    rewrite(response.content.decode('utf-8'),jsonpath)
                    #appendTxt(json.dumps(images), jsonpath)
                else:
                    appendTxt("null",jsonpath)
            except:
                # 发生错误时回滚
                traceback.print_exc()
                appendTxt("path="+file_path,error_file_path)
                
        
    print("==>全部处理完毕<==")       

run()
