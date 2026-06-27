# -*- coding: utf-8 -*-

import time
from PIL import Image
from io import BytesIO
import base64
import os
import json
from datetime import datetime
import shutil
import time
from datetime import datetime
import cv2 as cv
from tqdm import tqdm



def appendTxt(txtStr,txtpath):    
    f = open(txtpath,'a', encoding="utf-8")
    f.write(txtStr+'\n')
    f.close()    
    
    



file_scan_path=r"F:\大数据中心\33 - 明代别集数据库\5-待OCR识别+统计字数\20260420"
file_scan_path_to=r"F:\大数据中心\33 - 明代别集数据库\5-待OCR识别+统计字数\20260420_to"

def GetFileByDirList(dirpath, fileList):
    newDir = dirpath
    if os.path.isfile(dirpath):
        basename=os.path.splitext(dirpath)[1]
        #402881e85e702e13015e707f387413691577350412694_CatalogFile
        if basename== ".jpg" or basename == ".tif":
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
    
    createtime=datetime.now().strftime("%Y-%m-%d")
    print(createtime)
    
    if os.path.exists(file_scan_path_to) is False:
        os.mkdir(file_scan_path_to)
    
    bookdirs=os.listdir(file_scan_path)
    bookbar = tqdm(bookdirs)
    for _bookdir in bookbar:
        #print(bookdir)
        bookdir = os.path.join(file_scan_path, _bookdir)
        
        bookbar.set_description("解析图书 %s" % _bookdir)
        
        jpglist=GetFileByDirList(bookdir, [])
        
        
        tobookdir = os.path.join(file_scan_path_to, _bookdir)
        
        if os.path.exists(tobookdir) is False:
            os.mkdir(tobookdir)
        
        picdirpath = tobookdir+"\\pageimages_old\\"
               
        if os.path.exists(picdirpath) is False:
            os.mkdir(picdirpath)
        else:
            shutil.rmtree(picdirpath)
            os.mkdir(picdirpath)
            
            
                    
        #bar = tqdm(jpglist)
        print("==>图片总数量：", len(jpglist))
        for file_path in jpglist:
                   
            #print("图片先压缩处理", file_path)
            fname=os.path.basename(file_path)
            #bar.set_description("Processing %s" % fname)
            
            fp = os.path.dirname(file_path)
            basename, ext = os.path.splitext(fname)           
                       
            newpicpath = picdirpath + fname
            topath = newpicpath
            if os.path.isfile(topath):
                continue
                       
            if ext == '.tif':
                #print(basename)
                outfile=bookdir+"\\"+basename+".jpg"
                #img=cv.imread(file_path,-1)
                #cv.imwrite(outfile,img)
                Image.MAX_IMAGE_PIXELS = 2300000000
                
                with  Image.open(file_path) as my_image:
                        
                    #print("The original size is: ", round(len(my_image.fp.read())/1024,2), "KB")
                    #Image.NEAREST ：低质量 
                    #Image.BILINEAR：双线性 
                    #Image.BICUBIC ：三次样条插值 
                    #Image.ANTIALIAS：高质量
                    #compressed the image
                    
                    my_image = my_image.convert("RGB")
                    #save the image
                    my_image.save(outfile)
                    #print("==>转换成功....",outfile)        
                file_path = outfile
                newpicpath = picdirpath + basename+".jpg"
                topath = newpicpath
                        
           
                
                shutil.copy(file_path, topath)
            
                os.remove(file_path)
            else:
                shutil.copy(file_path, topath)

    print("==>全部处理完毕<==")
    
    
run()
