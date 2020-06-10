# -*- coding: utf-8 -*-
"""
Created on Thu Feb  6 15:51:41 2020

Extract the waterline from the point clouds created with different calibration methods 
in WebODM.

@author: SSchurer
"""

import rasterio
import pandas as pd
import numpy as np
import os
import numpy

dataset = rasterio.open(r'C:/Thesis_Sten/CC/Calibrated/raster_29_2.tif')

track_xy = pd.read_excel(os.path.join(r'D:/Data/RTK_River/waterline_height_XY.xls'))

interested_values = np.array([x[0] for x in  rasterio.sample.sample_gen(dataset, track_xy.values, indexes=None)])

print(interested_values)

# numpy.savetxt('rtk_section_from_cloud_rasterio.xls', interested_values)