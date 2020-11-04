#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Jan 24 15:47:05 2020

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


path='/scratch/snx3000/jvergara/Files_for_EUCP_ERA/'
path='/scratch/snx3000/jvergara/Files_for_Silje/'

variables=glob.glob(path+'*')
variables=[var.split('/')[-1] for var in variables]

dom='ALP-3'
#driving='MPI'
driving='ECMWF-ERAINT'
model='COSMO-pompa'
version='5.0_2019.1'


transfer=False
uploading_server='jvergara@lab.eucp-project.eu'
uploading_server='jvergara@jsc-cordex.fz-juelich.de'

naming_dict={}
naming_dict['TOT_PREC']='pr'
naming_dict['PS']='ps'
naming_dict['T_2M']='tas'
naming_dict['rsds']='rsds'
naming_dict['QV_2M']='huss'
#%%


set_of_years=[[1996,2005,'historical'],[2041,2050,'rcp85'],[2090,2099,'rcp85']]
set_of_years=[[2000,2009,'evaluation'],[2092,2101,'PGW-MPI-rcp85']]
set_of_years=[[2000,2009,'evaluation']]




for var in variables:
    if not var in naming_dict.keys():continue
    print (var)
    
    files=np.sort(glob.glob(path+var+'/lffd????_*nc')).tolist()
    os.makedirs(path+var+'/prepare',exist_ok=1)
    os.makedirs(path+var+'/upload',exist_ok=1)
    print(files)

    for file in files:
        print(file)
        new_name=path+var+'/prepare/'+file.split('/')[-1]
        print(new_name)
        cmd=f'cdo chname,{var},{naming_dict[var]} {file} {new_name}'    
        print(cmd)
        a=os.system(cmd)
    times=int(Dataset(files[3]).variables['time'].shape[0])
    freq=str(int(365/times*24))
    for set_y in set_of_years:
        years=np.arange(set_y[0],set_y[1]+1)
        for year in years:
            cmd='mv  '
            cmd=cmd+path+var+'/prepare/'+'lffd'+str(year)+'_'+var+'.nc '
            str_ini=f'{year}01010030'
            str_end=f'{year}12312330'
        #final_name=f'{path}/{var}/upload/{naming_dict[var]}_{dom}_{driving}_{set_y[2]}_r1i1p1_{model}_{version}_{freq}hr_{set_y[0]}_{set_y[1]}.nc'
            final_name=f'{path}/{var}/upload/{naming_dict[var]}_{dom}_{driving}_{set_y[2]}_r1i1p1_{model}_{version}_{freq}hr_{str_ini}_{str_end}.nc'
            cmd=cmd+final_name
            if os.path.exists(final_name):
                print(f'FILE EXISTS \n {final_name} \n SKIPING!!!')
                continue
            print(cmd)
            a=os.system(cmd)
    ###UPLOAD
            if transfer:
                dir_in_juelich=f'~/fpscpcm/cordex-fpsc/output/{dom}/ETHZ-2/{driving}/{set_y[2]}/r1i1p1/{model}/{version}/{freq}hr/{naming_dict[var]}/'
#        dir_in_juelich=f'/mnt/data/data1/cp-rcm/ETHZ-COSMO-ALP/{dom}/ETHZ-2/{driving}/{set_y[2]}/r1i1p1/{model}/{version}/{freq}hr/{naming_dict[var]}/'
                mkdir_cmd=f'ssh -t {uploading_server} "mkdir -p {dir_in_juelich}"'
                a=os.system(mkdir_cmd)
                cmd=f'scp {final_name} {uploading_server}:{dir_in_juelich}'
                print(cmd)
#            a=os.system(cmd)
'''
cdo cat pr_EU_MPI_011EU_rcp85_COSMO_1hr_2090-2099.nc

_historical_r1i1p1_CLMcom-KIT-CCLM5-0-15_x2yn2v1_1hr_200501010030-200512312330.nc
pr_ALP-3_MPI-M-MPI-ESM-LR_historical_r1i1p1_CLMcom-KIT-CCLM5-0-15_x2yn2v1_1hr_200501010030-200512312330.nc
'''
