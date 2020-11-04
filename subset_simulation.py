#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Jun  2 17:17:30 2020

@author: jvergara
"""

import sys
sys.path.append('/users/jvergara/python_code')

import Jesuslib_eth as jle

from netCDF4 import Dataset
import numpy as np
import os
import sys
import glob



start_date='2010021500'
end_date='2010022500'
all_dates=jle.Hourly_time_list(start_date,end_date)
path='/store/c2sm/pr04/jvergara/RUNS_IN_SCRATCH/MAC1/lm_f/'
path_in_sc=os.environ['SCRATCH']+'/MAC1_subset_for_Lisbon/'
os.makedirs(path_in_sc,exist_ok=True)
folders=glob.glob(path+'*')

for folder in folders:
    print(folder)
    files=glob.glob(folder+'/*.nc')
    address_dict=jle.Create_address_dict(all_dates,files)
    copy_path=path_in_sc+folder.split('/')[-1]
    os.makedirs(copy_path,exist_ok=True)
    for file in address_dict:
#        print(address_dict[file])
        cmd=f'cp {address_dict[file]} {copy_path}'
#        print(cmd)
        a=os.system(cmd)
        