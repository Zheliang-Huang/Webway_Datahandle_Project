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
import time
from datetime import datetime
import cv2 as cv
from tqdm import tqdm



def appendTxt(txtStr,txtpath):    
    f = open(txtpath,'a', encoding="utf-8")
    f.write(txtStr+'\n')
    f.close()    
    
    


file_scan_path = r"F:\大数据中心\33 - 明代别集数据库\5-待OCR识别+统计字数\20260420_to"



#import numpy as np
def run():
    
    createtime=datetime.now().strftime("%Y-%m-%d")
    print(createtime)
    
   
    bookdirs=os.listdir(file_scan_path)
    bookbar = tqdm(bookdirs)
    for _bookdir in bookbar:
        #print(bookdir)
        bookdir = os.path.join(file_scan_path, _bookdir)
        
        bookbar.set_description("解析图书 %s" % _bookdir)
        
       
        picdirpath = bookdir+"\\pageimages_old\\"
               
        if os.path.exists(picdirpath) is True:
           
            shutil.rmtree(picdirpath)
            
                 

    print("==>全部处理完毕<==")
    
    
run()
