# -*- coding: utf-8 -*-
"""
Created on Wed Jan 29 08:32:08 2020

Extract the coordinate data of the RTK GPS in batch from the .xls files.
Convert the coorinates from lat/lon to metres. 

@author: SSchurer
"""
from pyproj import Proj
import pandas as pd
import numpy as np
import os
import re

df = pd.read_excel(os.path.join(r'C:/Users/SSchurer/Documents/TU_Delft/Thesis/RTK/17-12', '17_12_transect9.xls'))

geom = df['Geometry']

for i in range(len(geom)):
    first = geom.iloc[i]
    to_use = re.findall('\((.*)\)', first)[0]

print(to_use)

full_list = []

for i in range(len(geom)):
    first = geom.iloc[i]
        
    to_use = re.findall('\((.*)\)', first)[0]
        
    rows =  to_use.split(',')
    x = [row.strip().split(' ') for row in rows]
        
        
    full_list += x

#print(full_list)


    x_list = []
    y_list = []
    z_list = []
    
    for row in full_list:
        x, y, z = row
        x_list.append(float(x))
        y_list.append(float(y))
        z_list.append(float(z))
    

p = Proj(proj="utm", zone=36, ellps="WGS84", south=True)

a = []
for i in range (len(x_list)):
      out= p(x_list[i], y_list[i])
      out = [*out, z_list[i]]
      a.append(out)

# np.savetxt('Waterline_track_metres.csv', a, delimiter=',')