import pydicom
import os
import numpy as np
from PIL import Image
from matplotlib import pyplot
import cv2
import bs4
# 调用本地的 dicom file
folder_path = r"H:\dicomTest\LIDC-IDRI-0006\01-01-2000-92500\3000556.000000-20957"
file_name = "1-063.dcm"
file_path = os.path.join(folder_path,file_name)
ds = pydicom.dcmread(file_path)
ds2=pydicom.read_file(file_path)

#print(ds.PatientID,ds.StudyDate,ds.Modality)
#访问一个frame的UID
print(ds2)




data_img = Image.fromarray(ds.pixel_array)
data_img_rotated = data_img.rotate(angle=45,resample=Image.BICUBIC,fillcolor=data_img.getpixel((0,0)))


#将dicom格式保存为png
data = np.array(ds.pixel_array)
cv2.imwrite('a.png',data)


pyplot.imshow(ds.pixel_array,cmap=pyplot.cm.bone)


#img=cv2.imread('H:\dicomTest\3000566.000000-03192\1-001.dcm')
#cv2.threshold(img,0,255,cv2.THRESH_BINARY)

pyplot.show()


#解析xml文件，找到结点frame
xml_path= r"H:\dicomTest\LIDC-IDRI-0006\01-01-2000-92500\3000556.000000-20957\078.xml"
with open(xml_path, 'r') as xml_file:
    markup=xml_file.read()
xml=bs4.BeautifulSoup(markup, features="xml")

readingSession=xml.LidcReadMessage.find_all("readingSession")
nodule_info=readingSession[0].find_all("unblindedReadNodule")
nodule_roi=nodule_info[0].find_all("roi")
zPosition=nodule_roi[0].find_all("imageZposition")
nodule_shape=nodule_roi[0].find_all("edgeMap")
frame_uid=nodule_roi[0].find_all("imageSOP_UID")
#print(nodule_roi)
#print(zPosition)
#print(nodule_shape)
#print(frame_uid)


