#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Oct 25 08:27:02 2019

@author: jvergara
"""

import numpy as np
import glob
import sys
from netCDF4 import Dataset
import os
import sys
sys.path.append('/users/jvergara/python_code')
import Jesuslib_eth as jle
import cdo
#substract and move fields from model runs

#define files to move
if len(sys.argv)==1:
    sys.argv.append('/store/c2sm/pr04/jvergara/RUNS_IN_SCRATCH/MPI_present/lm_c')
    sys.argv.append('test_key')
    sys.argv.append('TOT_PREC,T_2M')

path=str(sys.argv[1])+'/'
print('path: \n',path)
tranfer_key=str(sys.argv[2])


variables=str(sys.argv[3])
var_list=[var for var in variables.split(',')]

name=f'Files_for_{tranfer_key}/'

sc_path=os.environ['SCRATCH']+'/'+name

os.makedirs(sc_path,exist_ok=1)

#%%
storage_format='folders'
if len(glob.glob(path+'1h/????'))>3:
    storage_format='years'
    years=glob.glob(path+'1h/*')
#    files=[]
#
#    for year in years: 
#        print(year)
##    if not '1999' in year: continue
#        year_files=glob.glob(year+'/lffd*')
#    files=files+year_files
    years_str=[path.split('/')[-1] for path in years]

if storage_format=='folders':
    files=glob.glob(path+'1h/lf*0.nc')

#    print(files)
    years=[f.split('lffd')[-1][:4] for f in files]
    years_str=np.sort(list(set(years)))
print('storage_format: ', storage_format)
print(years_str)
print(tranfer_key)
print(var_list)
#%%

def get_file_path(var):
    var_folder=''
    
    if var[-2:]=='_p':
        var= var[:-2]
        add='p'
    else: 
        add=''
    if storage_format=='folders':
        folders=glob.glob(path+'*/')
    if storage_format=='years': 
        folders=glob.glob(path+f'*/{years_str[3]}')
    folders=[f for f in folders if not '_mm' in f]
    folders=[f for f in folders if not 'job' in f]
    folders=[f for f in folders if not 'rest' in f]
    folders=[f for f in folders if not 'per' in f]
    folders=[f for f in folders if not '6min' in f]
        
    folders=np.sort(folders).tolist()
    for folder in folders:
        sample_files=glob.glob(folder+f'lffd*{add}.nc')
        if len(sample_files)==0:continue
        variables=Dataset(sample_files[0]).variables.keys()
        if var in variables:
            var_folder=folder
            break
    if storage_format=='folders':
        files=glob.glob(var_folder+f'lffd*{add}.nc')
    if storage_format=='years': 
       files=[]
       for year in years_str: 
           print(year)
           year_files=glob.glob(var_folder+year+'/'+f'lffd*{add}.nc')
           files=files+year_files
    files=np.sort(files).tolist()
    return files
    
#%%

   
def get_adds(file):
    fmt=len(file.split('/')[-1])
#    print(fmt)
    if fmt==21 or fmt==22:
        add='??????????'
        add_0='0000'
    else:
        add='??????'
        add_0=''

    if file[-4]=='p':
        add=add+'p'
        add_0=add_0+'p'
    return add, add_0
#%%
#Create folder in scratch and move files there
a=0

import time
time.sleep(1)
for var in var_list:
    print('moving files' , var)
    files=get_file_path(var)
#    continue
    sample_file=files[0]
    var_path=sc_path+var+'/'
    os.makedirs(var_path,exist_ok=1)
    time.sleep(1)
    for file in files:
        print(file)
        new_file=var_path+file.split('/')[-1][:-3]+'_'+var+'.nc'
        if os.path.exists(new_file):continue
        cmd=f'echo o|ncks -v {var} {file} {new_file}'
        print(cmd)
        a=os.system(cmd)
        if a:
            print(a)
            break
    print('concatenating files', var)
    for y in years_str:
        print(y)
        print(len(files))
        os.makedirs(sc_path+var+'/'+y,exist_ok=1)
        add,add_0=get_adds(sample_file)
        files=np.sort(glob.glob(sc_path+var+'/lffd'+y+add+'_'+var+'.nc')).tolist()
        if len(files)<2:continue        
        files.append(sc_path+var+'/lffd'+str(int(y)+1)+'010100'+add_0+'_'+var+'.nc')
        if files[0]==sc_path+var+'/lffd'+y+'010100'+add_0+'_'+var+'.nc':
            files=files[1:]
        for f in files:
            cmd='mv '+f+' '+sc_path+var+'/'+y
            print(cmd)
            a=os.system(cmd)
        cdo.Cdo().cat(input=sc_path+var+'/'+y+'/lffd*_'+var+'.nc',output=sc_path+var+'/lffd'+y+'_'+var+'.nc')

