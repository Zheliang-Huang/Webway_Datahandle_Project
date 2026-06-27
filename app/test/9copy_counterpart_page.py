import os
def traverse_dir(file_path, path_read, ext):
    import os

    # '''
    # 该方法可以递归遍历路径下的子文件，可指定格式
    # file_path: 待遍历路径
    # path_read: 子文件列表
    # ext：格式为列表，可写入指定格式后缀
    # 例：
    # src = r'D:\黄哲良\Python-dataHandle\爬数据\刘思汐_语料清洗（MNBVC）20230706\dst'
    # dst = r'D:\黄哲良\Python-dataHandle\爬数据\刘思汐_语料清洗（MNBVC）20230706\txt'
    # json_paths =[]
    # traverse_dir(src,json_paths,['.jsonl'])
    # '''
    # put file name from file_path in temp_list
    temp_list = os.listdir(file_path)
    for temp_list_nor in temp_list:
        if os.path.isfile(os.path.join(file_path, temp_list_nor)):
            # temp_path = file_path + file_sep + temp_list_nor
            temp_path = os.path.join(file_path, temp_list_nor)
            if len(ext) == 0:
                path_read.append(temp_path)
            else:
                ext_dic = {key: 1 for key in ext}
                if (os.path.splitext(temp_path)[-1]).lower() in ext_dic:
                    path_read.append(temp_path)
                else:
                    continue
        else:
            traverse_dir(os.path.join(file_path, temp_list_nor),
                         path_read, ext)  # loop traversal


def copy_file(srcfile, dstfile):
    import os
    import shutil
    if not os.path.isfile(srcfile):
        print("%s not exist!" % (srcfile))
    if os.path.isfile(dstfile):
        print("%s already exist!" % (srcfile))
    else:
        shutil.copy(srcfile, dstfile)  # 移动文件
        print("copy %s -> %s" % (srcfile, dstfile))


if __name__ == '__main__':
    pic_dir = r"F:\大数据中心\33 - 明代别集数据库\5-待OCR识别+统计字数\20260420_to"
    source = r'F:\大数据中心\33 - 明代别集数据库\5-待OCR识别+统计字数\20260420_to-json提取'
    
    json_list = []
    traverse_dir(source, json_list, ['.json'])
    json_names = [os.path.splitext(os.path.basename(jsonpath))[0] for jsonpath in json_list]
    
    for book in os.listdir(pic_dir):
        print(book)
        book_dir = os.path.join(pic_dir,book)
        if os.path.isdir(book_dir):
            pic_list = []
            traverse_dir(book_dir, pic_list, ['.jpg', '.tif', '.jpeg'])
            for pic in pic_list:
                picname = os.path.splitext(os.path.basename(pic))[0] 
                if picname in json_names:
                    new_pic = os.path.join(source, os.path.basename(pic))
                    copy_file(pic, new_pic)
