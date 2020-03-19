# -*- coding: utf-8 -*-
"""
Created on Wed Nov 27 17:19:38 2019

@author: Mico
"""

import cv2
import glob

#folder_path = 'C:\\Users\\Mico\\Desktop\\marcha\\territoria2\\num\\*.png'
#folder_path = 'C:\\Users\\Mico\\Desktop\\odd\\dataset_tools\\storage\\batch 0\\*.jpg'
#folder_path = 'C:\\Users\\Mico\\Desktop\\New folder\\*.jpg'
#folder_path = 'C:\\Users\\Mico\\Desktop\\odd\\workers\\bbox\\Batch 2019-10-11_2\\*.jpg'
#folder_path = 'C:\\Users\\Mico\\Desktop\\marcha\\test_SFCN\\heatmap\\*.png'

#folder_path = 'C:\\Users\\Mico\\Desktop\\marcha\\territoria2_SFCN\\heatmap\\*.png'
folder_path = 'C:\\Users\\Mico\\Desktop\\blender-python\\scripting\\workers\\poc\\renders\\test\\*.jpg'
#folder_path = 'C:\\Users\\Mico\\Desktop\\marcha\\territoria2_SFCN\\original\\*.jpg'
img_array = []
contador = 0

for filename in glob.glob(folder_path):
    contador = contador + 1
    if contador%1 == 0:
        img = cv2.imread(filename)
        scale_percent = 100
        width = int(img.shape[1] * scale_percent / 100)
        height = int(img.shape[0] * scale_percent / 100)
        dim = (width, height)
        img = cv2.resize(img, dim, interpolation = cv2.INTER_AREA)
        height, width, layers = img.shape
        size = (width,height)
        img_array.append(img)

out_filename = 'worker_helmet_colorchange'
#out_filename = 'territoria2_org'
#out = cv2.VideoWriter(out_filename+'.avi',cv2.VideoWriter_fourcc(*'DIVX'), 15, size)
out = cv2.VideoWriter(out_filename+'.mp4',cv2.VideoWriter_fourcc(*'MP4V'), 15, size)

for i in range(len(img_array)):
    out.write(img_array[i])
out.release()