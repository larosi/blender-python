# -*- coding: utf-8 -*-
"""
Created on Wed Mar 18 20:51:14 2020

@author: Mico
"""

import os
import pandas as pd
from tqdm import tqdm
import parse as str_parser
from skimage import io, measure

def bbox_from_mask(mask_filepath):
    mask_image = io.imread(mask_filepath,as_gray=True)
    mask_label = measure.label(mask_image)
    mask_props = measure.regionprops(mask_label)

    xmins = []
    ymins = []
    xmaxs = []
    ymaxs = []

    for props in mask_props:
        # (min_row, min_col, max_row, max_col)
        minr, minc, maxr, maxc = props.bbox
        ymins.append(minr)   
        xmins.append(minc)
        ymaxs.append(maxr)
        xmaxs.append(maxc)

    xmin = min(xmins)
    ymin = min(ymins)
    xmax = max(xmaxs)
    ymax = max(ymaxs)

    return [xmin,ymin,xmax,ymax]

format_string = 'worker-{}-{}-sample_{}_act_{}_frame_{}.{}'


folders = os.listdir('images')

df_header = ['filename',
             'color_casco',
             'traje_blanco',
             'xmin','ymin','xmax','ymax',
             'color_traje',
             'sample',
             'animation',
             'frame']

rows = []
for folder in tqdm(folders):
    images_basepath = os.path.join('images',folder)
    masks_basepath = os.path.join('masks',folder)
    im_filenames = os.listdir(images_basepath)
    for im_filename in tqdm(im_filenames):
        mask_filepath = os.path.join(masks_basepath, im_filename)

        [xmin,ymin,xmax,ymax] = bbox_from_mask(mask_filepath)
        res = str_parser.parse(format_string,im_filename)
        color_casco, color_traje, sample, animation, frame, extension = list(res)
        traje_blanco = color_traje.split('_')[0] == 'blanco'
        row = [im_filename,
               color_casco,
               traje_blanco,
               xmin,ymin,xmax,ymax,
               color_traje,
               sample,
               animation,
               frame]          
        rows.append(row)

df = pd.DataFrame(rows,columns=df_header)

df.to_excel('metadata.xls')


