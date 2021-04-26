import pydicom
import os
import numpy as np
from PIL import Image
from matplotlib import pyplot
import cv2
import bs4

save_path_nodule = r"H:\dicomTest\dataset\nodule_frames"
save_path_non_nodule = r"H:\dicomTest\dataset\non_nodule_frames"



def convert_dicom_png(folder_path,type):
    '''
    :param folder_path: lidc文件夹根目录    LIDC dataset root dir
    :param type: 转换结节还是非结节CT文件
    :return:
    '''

    dataset_size = 1000  # 生成的数据集大小,并非缺数，因为每次是输出一个文件夹的所有CT文件
    dicm_files_list = []
    dir_list=[]
    for root, dirs, files in os.walk(folder_path):
        if (len(files) > 10 and dataset_size*3 > 0):  # 10是根据数据集特点写的，因为一个病患有两种ct文件，一个是胸部横截面，一个是正面CT，正面的只有两张
            dataset_size -= len(files)
            dicm_files_list.append(files)
            dir_list.append(root)


    if(type=="nodule"):
        for dir in dir_list:
            uids = find_nodule_frame(dir)
            # print(dir)
            # print(uids)
            file_list = os.listdir(dir)
            count = 0
            for file in file_list:
                if file.endswith("xml"):
                    continue
                file_path = os.path.join(dir, file)
                ds = pydicom.dcmread(file_path)
                # print(ds[0x0008,0x0018].value)
                if (ds[0x0008, 0x0018].value in uids):  # 这里的0x0008,0x0018是SOP_Instance_UID
                    data = np.array(ds.pixel_array)
                    cv2.imwrite(save_path_nodule + '\\' + file + '_' + str(count) + '.png', data)
                    count += 1
                #print(count)


    if(type=="non-nodule"):
        for dir in dir_list:
            uids = find_nodule_frame(dir)
            file_list = os.listdir(dir)
            count = 0
            num=0
            around_nodule=5
            for file in file_list:
                if file.endswith("xml"):
                    continue
                file_path = os.path.join(dir, file)
                ds = pydicom.dcmread(file_path)
                if (ds[0x0008, 0x0018].value in uids):  # 这里的0x0008,0x0018是SOP_Instance_UID
                    for i in range(around_nodule):
                        if((num+i)>=len(file_list) or (num-i)<=0):
                            break
                        file_path = os.path.join(dir, file_list[num+i])
                        ds = pydicom.dcmread(file_path)
                        if(ds[0x0008, 0x0018].value not in uids):
                            data = np.array(ds.pixel_array)
                            cv2.imwrite(save_path_non_nodule + '\\' + file_list[num+i] + '_' + str(count) + '.png', data)
                            count += 1

                        file_path = os.path.join(dir, file_list[num - i])
                        ds = pydicom.dcmread(file_path)
                        if (ds[0x0008, 0x0018].value not in uids):
                            data = np.array(ds.pixel_array)
                            cv2.imwrite(save_path_non_nodule + '\\' + file_list[num - i] + '_' + str(count) + '.png', data)
                            count += 1

                num+=1
                #print(num)


'''
# 原 找非结节CT，存在的问题是有很多空白图，没有肺部造影
    if (type == "non-nodule"):
        for dir in dir_list:
            uids = find_nodule_frame(dir)
            file_list = os.listdir(dir)
            count = 0
            for file in file_list:
                if file.endswith("xml"):
                    continue
                file_path = os.path.join(dir, file)
                ds = pydicom.dcmread(file_path)
                data = np.array(ds.pixel_array)
                cv2.imwrite(save_path_non_nodule + '\\' + file + '_' + str(count) + '.png', data)
                count += 1
                print(count)
'''






# 找出所有有结节的frame的UID
def find_nodule_frame(folder_path):

    file_list = os.listdir(folder_path)
    for file in file_list:
        if file.endswith("xml"):
            file_path = os.path.join(folder_path, file)
            xml_path = file_path
    if(not xml_path):
        return

    uids = []
    with open(xml_path, 'r') as xml_file:
        markup = xml_file.read()
    xml = bs4.BeautifulSoup(markup, features="xml")
    reading_session = xml.LidcReadMessage.find_all("readingSession")

    for readingSession in reading_session:
        nodule_info = readingSession.find_all("unblindedReadNodule")
        for nodule_info in nodule_info:
            nodule_roi = nodule_info.find_all("roi")
            for nodule_roi in nodule_roi:
                frame_uid = nodule_roi.find_all("imageSOP_UID")
                if(frame_uid[0].string in uids):                      # 因为有多个医生的诊断信息  所以会出现重复UID
                    continue
                uids.append(frame_uid[0].string)
    return uids



#path = r"H:\manifest-1600709154662\LIDC-IDRI\LIDC-IDRI-0008\01-01-2000-30141\3000549.000000-21954"

path=r"H:\manifest-1600709154662\LIDC-IDRI"
convert_dicom_png(path,"nodule")
convert_dicom_png(path,"non-nodule")






