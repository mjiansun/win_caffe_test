#coding:utf-8
import sys
import numpy as np
import os
from scipy import misc
import copy
import cv2
import shutil
if sys.version_info[0] == 2:
    import xml.etree.cElementTree as ET
else:
    import xml.etree.ElementTree as ET

def get_coordi(xml_path, w, h):
    tree = ET.parse(xml_path)
    root = tree.getroot()

    # count记录这个xml中检测框的数量
    count = 0
    coordi = [0,0,0,0]
    for obj in root.iter('object'):
        count += 1
        name = obj.find('name').text.lower().strip()

        obj.find('pose').text = "Left"

        bbox = obj.find('bndbox')
        coordi = [int(bbox.find('xmin').text) * 1. / w,
                  int(bbox.find('ymin').text) * 1. / h,
                  int(bbox.find('xmax').text) * 1. / w,
                  int(bbox.find('ymax').text) * 1. / h]
    # assert len(coordi) == 1
    return coordi

root_image_path = r"E:\data\pic\sun"
root_xml_path = r"E:\data\pic\Annotation\sun"
root_image_save_path = r"E:\data\slide_pic\sun_save"
f_train = open(r"D:\myproject\caffe_win\20190410\regression\data"+ "\\" + 'trainval.txt', 'a')
for image_name in os.listdir(root_image_path):
    image_path = root_image_path + "\\" + image_name
    image_save_path = root_image_save_path + "\\" + image_name
    image = misc.imread(image_path)
    h,w,c = image.shape

    # new_image = misc.imresize(image, (400,400))
    # misc.imsave(image_save_path, new_image)

    xml_path = root_xml_path + "\\" + image_name.replace(".png", ".xml")
    if os.path.exists(xml_path):
        coordi_lists = np.array(get_coordi(xml_path, w, h))
    else:
        coordi_lists = np.array([0,0,0,0])
    print(coordi_lists)
    f_train.write(image_name + " " + str(coordi_lists[0]) + " " + str(coordi_lists[1]) + " " + str(coordi_lists[2]) + " " + str(coordi_lists[3]) + "\n")
f_train.close()