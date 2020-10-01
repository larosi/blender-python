# -*- coding: utf-8 -*-
"""
Created on Fri Mar 27 15:28:10 2020

@author: Mico
"""
import pandas as pd
import os
from skimage import io

def make_folder(folder_path):
    if not os.path.exists(folder_path):
        os.mkdir(folder_path)
        
df_filename = 'metadata.xls'
df = pd.read_excel(df_filename)

color_cascos = df['color_casco'].unique()

base_folder = 'cropped_images'
make_folder(base_folder)
for folder in color_cascos:
    make_folder(os.path.join(base_folder,folder))

for index, row in df.iterrows():
    xmin = row['xmin']
    ymin = row['ymin']
    xmax = row['xmax']
    ymax = row['ymax']
    color_casco = row['color_casco']
    filename = row['filename']
    filepath = os.path.join('images',color_casco,filename)
    im = io.imread(filepath)
    im_crop = im[ymin:ymax,xmin:xmax,:]
    out_filepath = os.path.join(base_folder,color_casco,filename)
    io.imsave(out_filepath,im_crop)