# -*- coding: utf-8 -*-
"""
Created on Wed Mar 18 20:51:14 2020

@author: Mico
"""

import os
import pandas as pd
import parse as str_parser

format_string = 'worker-{}-{}-sample_{}_act_{}_time_{}.{}'

dataset_folder = 'workers_blender'
folders = os.listdir(dataset_folder)

df_header = ['filename',
             'color_casco',
             'traje_blanco',
             'color_traje',
             'sample',
             'animation',
             'frame']

rows = []
for folder in folders:
    folder_path = os.path.join(dataset_folder,folder)
    im_filenames = os.listdir(folder_path)
    for im_filename in im_filenames:
        res = str_parser.parse(format_string,im_filename)
        color_casco, color_traje, sample, animation, frame, extension = list(res)
        traje_blanco = color_traje.split('_')[0] == 'blanco'
        row = [im_filename,
               color_casco,
               traje_blanco,
               color_traje,
               sample,
               animation,
               frame]          
        rows.append(row)

df = pd.DataFrame(rows,col=df_header)

df.to_excel('workers_blender_metadata.xls')
