# -*- coding: utf-8 -*-
"""
Created on Tue Jan 28 11:09:59 2020

Convert latitude and longitude to metres and vice versa

@author: SSchurer
"""

from pyproj import Proj
import pandas as pd
import numpy as np
import re
import os
import pickle

# def make_list(excel_file):
#     print(excel_file)
#     df = pd.read_excel(os.path.join(r'C:\Thesis_Sten\RTK', excel_file))
#     geom = df['Geometry']
#     full_list = []
    
#     for i in range(len(geom)):
#         first = geom.iloc[i]
        
#         to_use = re.findall('\((.*)\)', first)[0]
        
#         rows =  to_use.split(',')
#         x = [row.strip().split(' ') for row in rows]
        
        
#         full_list += x 
        
#     x_list = []
#     y_list = []
#     z_list = []
    
#     for row in full_list:
#         x, y, z = row
#         x_list.append(float(x))
#         y_list.append(float(y))
#         z_list.append(float(z))
#     return x_list, y_list, z_list

# print(os.path.join(r'C:\Thesis_Sten\RTK'))

# files = [file for file in os.listdir(r'C:\Thesis_Sten\RTK') if file.endswith('.xls')]

# x_list = []
# y_list = []
# z_list = []

# for file in files:
# #    x_list.append([''])
# #    y_list.append([''])
# #    z_list.append([''])
#     x, y, z = make_list(file)
#     x_list += x
#     y_list += y
#     z_list += z

# a  = pd.DataFrame([x_list])

# b = pd.DataFrame([y_list])

# orig = pd.concat([a, b], axis=0, sort=False)
# orig.index  = np.arange(orig.shape[0])
# c = orig.T


# #p = Proj(proj="utm", zone=36, ellps="WGS84", south=True)
# #
# #a = []
# #for i in range (len(x_list)):
# #    try:
# #        
# #        out= p(x_list[i], y_list[i])
# #        out = [*out, z_list[i]]
# #    except TypeError:
# #        out = [0, 0, 0]
# #    a.append(out)
# #
# ##print(a)


# np.savetxt('Total_coordinates_original.csv', c, delimiter = ',')

#------------------------------------------------------------------------------

#Coordinates of the 5 flow velocity values used in the 3D model. 
one   = (30.216830286730765)
two   = (-14.993960037142855)
three = (30.217068568076918)
four  = (-14.993857437857141)
five  = (30.216651479807688)
six   = (-14.993924869999999)
seven = (30.216908463269231)
eight = (-14.993753985000000)
nine  = (30.216894635576907)
ten   = (-14.994360191428569)

#land boundary
LeftNorth1 = 199145.497
LeftNorth2 = 8345005.807
LeftMiddleHigh1 = 200324.494
LeftMiddleHigh2 = 8340803.182
LeftMiddleLow1 = 200371.2
LeftMiddleLow2 = 8340303.9
LeftSouth1 = 201532.430
LeftSouth2 = 8336097.78

#width grid
Left1  = 200300.83
Left2  = 8340452.76
Right1 = 200830.34
Right2 = 8340556.07

#Length grid
# north1 = 199516.29
# north2 = 8345092.23
# south1 = 201528.69
# south2 = 8336098.67

#obs
obs1  = -14.99378915
obs12 = 30.21708727
obs2  = -14.99388339
obs21 = 30.21700348
obs3  = -14.99400118
obs31 = 30.21689874
obs4  = -14.99406349
obs41 = 30.21699039
obs5  = -14.99400476
obs51 = 30.21683253

#length obs grid
# one = 200654.609
# two = 8340478.696
# three = 200656.283
# four = 8340471.765

#RTK track
north1 =  200498.3942024240096 
north2 =  8340837.957817549817
south1 =  200653.7816712190106
south2 =  8340427.568922979757

#length upper/lower boundary step
s1 = 200338.0
s2 = 8340325.0
s3 = 200346.0
s4 = 8340289.0

#length extension from rtk track south
k1 = 200653.78
k2 = 8340428
k3 = 201582.04
k4 = 8336113.66

#length extension from rtk track south

myproj = Proj(proj="utm", zone=36, ellps="WGS84", south=True, units= 'm')
print(myproj(k1, k2, inverse=True))
