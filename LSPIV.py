# -*- coding: utf-8 -*-
"""
Complete LSPIV script

@author: SSchurer
"""

import os 
import numpy as np
import matplotlib
import matplotlib.pyplot as plt
import pandas as pd
import pylab
import tensorflow as tf

from tqdm import tqdm # the progress bar
from openpiv import tools, process, scaling, pyprocess, validation, filters

#------------------------------------------------------------------------------

def remove_outliers(u, v, mask):
    """
    Removal of outliers. Points are indicated as outlier if u or v
    is off two times the standard deviation from the median.
    
    This function is placed after validation.sig2noise_val()
    
    Input:
    ------
    u, v, mask prefereably as output of validation.sig2noise_val()
    
    Output:
    -------
    u, v, mask without outliers
    """

    u_nonan = u.copy()
    v_nonan = v.copy()

    u_no_outliers = u.copy()
    v_no_outliers = v.copy()
    mask_no_outliers = mask.copy()

    u_nonan = u_nonan[~np.isnan(u_nonan)]
    v_nonan = v_nonan[~np.isnan(v_nonan)]

    u_median = np.median(u_nonan)
    u_std = np.std(u_nonan)

    v_median = np.median(v_nonan)
    v_std = np.std(v_nonan)

    for i in range(len(u)):
        for j in range(len(u[i])):
            if u[i,j] > u_median + 2*u_std or u[i,j] < u_median - 2*u_std:
                mask_no_outliers[i,j] = True
                u_no_outliers[i,j] = np.nan
                v_no_outliers[i,j] = np.nan

            if v[i,j] > v_median + 2*v_std or v[i,j] < v_median - 2*v_std:
                mask_no_outliers[i,j] = True
                u_no_outliers[i,j] = np.nan
                v_no_outliers[i,j] = np.nan

    return u_no_outliers, v_no_outliers, mask_no_outliers

#------------------------------------------------------------------------------

# Import images
path_data= r'C:/Users/SSchurer/Documents/TU_Delft/Thesis/LSPIV/Edited/After rain/Images_OSGGC_10sec'

# Returns a list containing the names of the entries in the directory given
images = os.listdir(path_data)

# set-up parameters
winsize        = 100            # Pixels, size of the interrogation window in image A
searchsize     = winsize        # Pixels, size of the search area in image B
overlap        = 50             # Pixels, overlap between adjacent windows
frame_rate     = 30             # Frequence of the video(frames per second)
dt             = 1./frame_rate  # Time interval

#1080p          = 1980 x 1080 pixels
#4K             = 3840 x 2160 pixels
#after rain     = 2704 x 1520 pixels (21.62 pix/m)
#before rain    = 3840 x 2160 pixels (4k) (36.36 pix/m)
#tracers        = 4096 x 2160 pixels (29.72 pix/m)
scaling_factor = 21.62     # Pixels / metre

#------------------------------------------------------------------------------

# Function that processes the images
def PIV(image_0, image_1, winsize, searchsize, overlap, frame_rate, scaling_factor):
     
    frame_0 = image_0
#     [0:600, :]
    frame_1 = image_1
#     [0:600, :]
    
    # Processing the images with interrogation area and search area / cross correlation algortihm
    u, v, sig2noise = pyprocess.extended_search_area_piv(frame_0,
                                                         frame_1,
                                                         window_size=winsize,
                                                         overlap=overlap,
                                                         dt=dt,
                                                         search_area_size=searchsize,
                                                         sig2noise_method='peak2peak')
    
    # Compute the coordinates of the centers of the interrogation windows
    x, y = pyprocess.get_coordinates(image_size=frame_0.shape,
                                     window_size=winsize,
                                     overlap=overlap)
    
    # This function actually sets to NaN all those vector for 
    # which the signal to noise ratio is below 1.3.
    # mask is a True/False array, where elements corresponding to invalid vectors have been replace by Nan.
    u, v, mask = validation.sig2noise_val(u,
                                          v,
                                          sig2noise,
                                          threshold=1.5)
    
    # Function as described above, removing outliers deviating with more 
    # than twice the standard deviation
    u, v, mask = remove_outliers(u, v, mask)
    
    # Replacing the outliers with interpolation 
#    u, v = filters.replace_outliers(u,
#                                    v,
#                                    method='nan',
#                                    max_iter=50,
#                                    kernel_size=3)
                                   
    # Apply an uniform scaling to the flow field to get dimensional units
    x, y, u, v = scaling.uniform(x,
                                 y,
                                 u,
                                 v,
                                 scaling_factor=scaling_factor)
    
    return x, y, u, v, mask

#------------------------------------------------------------------------------

# with tqdm(total=i_max) as pbar:
# N = 2
N = len(images)-1

u_sum = 0
v_sum = 0 
values_u = 0
values_v = 0

# Reading the images from the file and run them through the PIV function
# Save the vectors in a .txt file
with tqdm(total=N) as pbar: # use the progress bar
    for n in range(N): # loop through all images
        image_0 = tools.imread('C:/Users/SSchurer/Documents/TU_Delft/Thesis/LSPIV/Edited/After rain/Images_OSGGC_10sec/'+str(images[n]))
        image_1 = tools.imread('C:/Users/SSchurer/Documents/TU_Delft/Thesis/LSPIV/Edited/After rain/Images_OSGGC_10sec/'+str(images[n+1]))

        x, y, u, v, mask = PIV(image_0, image_1, winsize, searchsize, overlap, frame_rate, scaling_factor)

        tools.save(x,
                   y,
                   u,
                   v,
                   mask,
                   'C:/Users/SSchurer/Documents/TU_Delft/Thesis/LSPIV/Edited/After rain/OSGGC/Output' +str(n)+ '.txt')
        tools.save(x,
                   y,
                   u,
                   u,
                   v,
                   'C:/Users/SSchurer/Documents/TU_Delft/Thesis/LSPIV/Edited/After rain/OSGGC/STDV/stdv' +str(n)+ '.txt')
        
        #Making the nan cells into 0 cells for the summation. Otherwise cells with 1 missing value end up with nan
        num_u = np.nan_to_num(u)
        num_v = np.nan_to_num(v)
        
        # sum the vector values of all images 
        u_sum += num_u
        v_sum += num_v
        
        # returns a grid with 0 and 1. 1 for when the cell has a number
        v_u = np.isfinite(u)
        val_u = v_u.astype(int)
        v_v = np.isfinite(v)
        val_v = v_v.astype(int)
        
        #Sums the zeros and ones
        values_u += val_u
        values_v += val_v
        
        #print(values_u)
        pbar.update(1)

shape = u_sum.shape
print(shape)

#Only keep the values > N/2 in the u_values column
arr_u = np.array(values_u.ravel())
arr_u[arr_u < (N/2)] = 0
u_values = arr_u.reshape(shape)

arr_v = np.array(values_v.ravel())
arr_v[arr_v < (N/2)] = 0
v_values = arr_v.reshape(shape)

# Determine averages of the cells > N/2 due to the use of u_values
u_avg = u_sum/u_values
v_avg = v_sum/v_values

# Getting the inf and -inf values out
u_avg[u_avg > 100] = np.nan
u_avg[u_avg < -100] = np.nan

v_avg[v_avg > 100] = np.nan
v_avg[v_avg < -100] = np.nan
mask_avg = np.zeros_like(mask)

tools.save(values_u,
           u_values,
           u_avg,
           v_avg,
           mask,
           'C:/Users/SSchurer/Documents/TU_Delft/Thesis/LSPIV/Edited/After rain/OSGGC/amount_of_values.txt')

# save the average vectors in a .txt file
tools.save(x,
           y,
           u_avg,
           v_avg,
           mask_avg,
           'C:/Users/SSchurer/Documents/TU_Delft/Thesis/LSPIV/Edited/After rain/OSGGC/average.txt')

# display the vector field that is saved (blue field)
tools.display_vector_field('C:/Users/SSchurer/Documents/TU_Delft/Thesis/LSPIV/Edited/After rain/OSGGC/average.txt',
                           scale=6,
                           width=0.0035,
                          )
plt.savefig('C:/Users/SSchurer/Documents/TU_Delft/Thesis/LSPIV/Edited/After rain/OSGGC/average.jpg')

plt.axis('scaled')

plt.plot(u_values, v_values,'ko', ms=1)
plt.axis('scaled')
plt.xlabel('u')
plt.ylabel('v')
plt.savefig('C:/Users/SSchurer/Documents/TU_Delft/Thesis/LSPIV/Edited/After rain/OSGGC/deviation_U_V_adjusted')

fig=plt.figure(figsize=(9,4))
BackG = plt.imread(r'C:/Users/SSchurer/Documents/TU_Delft/Thesis/Report/Images/Background_LSPIV_40Transparent.JPG')
plt.imshow(BackG, extent=[0, 130, 0, 70])
# norm = matplotlib.colors.Normalize(vmin=0,vmax=1.,clip=False)
color=np.sqrt(v_avg**2 + u_avg**2)

plt.quiver(x, y, u_avg, v_avg, color)
plt.axis('scaled')
plt.colorbar();

plt.savefig('C:/Users/SSchurer/Documents/TU_Delft/Thesis/LSPIV/Edited/After rain/OSGGC/Vector_field_Background.jpg')