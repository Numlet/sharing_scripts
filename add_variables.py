#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Jan 27 09:58:18 2020

@author: jvergara
"""


import Jesuslib_eth as jle

from netCDF4 import Dataset
import numpy as np
import os
import sys
import glob


path='/scratch/snx3000/jvergara/Files_for_EUCP_ERA/'

variables=glob.glob(path+'*')
variables=[var.split('/')[-1] for var in variables]

final_name='rsds'

var1='ASWDIFU_S'

var2='ASOB_S'


long_name='Surface Downwelling Shortwave Radiation'
standard_name='surface_downwelling_shortwave_flux_in_air'


files=np.sort(glob.glob(path+var1+'/lffd????_*nc')).tolist()

os.makedirs(path+'/'+final_name,exist_ok=1)
os.makedirs(path+'/'+final_name+'/calculate',exist_ok=1)

for filename1 in files:
    print(filename1)
    filename2=filename1.replace(var1,var2)
    print(filename2)
    final_file=filename1.replace(var1,final_name)
    calc_file=final_file.replace(final_name+'/',final_name+'/calculate/')
    print(final_file)
    print(calc_file)
    
    cmd=f'cdo merge {filename1} {filename2} {calc_file}'
    a=os.system(cmd)
    add_cmd=f' -expr,"{final_name}={var1}+{var2};" {calc_file} {final_file}'
    atr1=f'-setattribute,{final_name}@long_name="{long_name}" '
    atr2=f'-setattribute,{final_name}@standard_name="{standard_name}" '
    cmd=f'cdo {atr1} {atr2} {add_cmd}'
    a=os.system(cmd)
    if not a:
        b=os.system(f'rm {calc_file}')
    
    
