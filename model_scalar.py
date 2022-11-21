import numpy as np
import os
import math
import json
import pandas as pd
from netCDF4 import Dataset

from ncd_util import to_float, grp_min_max_3, grp_min_max_4

def build_scalar_model_temp(dst_j, src, dim, model):

    grp = Dataset(f"./bom_file/{src}", "r", format="NETCDF4")

    data = []

    lat_set = grp[model['lat']][:]
    lng_set = grp[model['lng']][:]
    temp_set = grp[model['var']][:]
    min_max = grp_min_max_4(grp, model, dim)

    i=0

    # Sampling rate for data. 1 - means include all data, 10 means include 1/10 part along each dimension (1/100 of whole data)
    divisor = 10

    for i in range(len(lat_set)):
        if i % divisor == 0:
            for j in range(len(lng_set)):
                if j % divisor == 0:
                    t = temp_set[0,dim,i,j]
                    tn = (t-min_max['min'])/(min_max['max']-min_max['min'])
                    if(t>0):
                        data.append([lat_set[i], lng_set[j], tn])

    f = open(f"./bom_data/{dst_j}", "w")
    f.write(json.dumps(data))
    f.close()

def build_scalar_model_salt(dst_j, src, dim, model):

    grp = Dataset(f"./bom_file/{src}", "r", format="NETCDF4")

    data = []

    lat_set = grp[model['lat']][:]
    lng_set = grp[model['lng']][:]
    temp_set = grp[model['var']][:]
    min_max = grp_min_max_4(grp, model, dim)

    i=0

    # Sampling rate for data. 1 - means include all data, 10 means include 1/10 part along each dimension (1/100 of whole data)
    divisor = 10

    for i in range(len(lat_set)):
        if i % divisor == 0:
            for j in range(len(lng_set)):
                if j % divisor == 0:
                    t = temp_set[0,dim,i,j]
                    tn = (t-min_max['min'])/(min_max['max']-min_max['min'])
                    if(t>0):
                        data.append([lat_set[i], lng_set[j], tn])

    f = open(f"./bom_data/{dst_j}", "w")
    f.write(json.dumps(data))
    f.close()

def build_scalar_model_eta(dst_j, src, model):

    grp = Dataset(f"./bom_file/{src}", "r", format="NETCDF4")

    data = []

    lat_set = grp[model['lat']][:]
    lng_set = grp[model['lng']][:]
    temp_set = grp[model['var']][:]
    min_max = grp_min_max_3(grp, model)

    i=0

    # Sampling rate for data. 1 - means include all data, 10 means include 1/10 part along each dimension (1/100 of whole data)
    divisor = 10

    for i in range(len(lat_set)):
        if i % divisor == 0:
            for j in range(len(lng_set)):
                if j % divisor == 0:
                    t = temp_set[0,i,j]
                    tn = (t-min_max['min'])/(min_max['max']-min_max['min'])
                    if(t>0):
                        data.append([lat_set[i], lng_set[j], tn])

    f = open(f"./bom_data/{dst_j}", "w")
    f.write(json.dumps(data))
    f.close()
