import numpy as np
import os
import math
import json
import pandas as pd
from netCDF4 import Dataset

from ncd_util import to_float

def build_vector_model(dst_j, src_u, src_v, dim):

    u_grp = Dataset(f"./bom_file/{src_u}", "r", format="NETCDF4")
    v_grp = Dataset(f"./bom_file/{src_v}", "r", format="NETCDF4")

    lat_set = u_grp['yu_ocean'][:]
    lng_set = u_grp['xu_ocean'][:]
    u_set = u_grp['u'][:]
    v_set = v_grp['v'][:]

    lat_start = lat_set[0]
    lat_end = lat_set[len(lat_set)-1]
    lat_diff = (lat_end - lat_start)/(len(lat_set)-1)

    lng_start = lng_set[0]
    lng_end = lng_set[len(lng_set)-1]
    lng_diff = (lng_end - lng_start)/(len(lng_set)-1)

    u_filtered = []
    v_filtered = []

    # Sampling rate for data. 1 - means include all data, 10 means include 1/10 part along each dimension (1/100 of whole data)
    divisor = 1

    i=0
    nx=0
    ny=0

    for i in range(len(lat_set)):
        if i % divisor == 0:
            ny=ny+1
            for j in range(len(lng_set)):
                if j % divisor == 0:
                    if ny==1:
                        nx=nx+1
                    u = to_float(u_set[0,dim,len(lat_set)-i-1,j])
                    v = to_float(v_set[0,dim,len(lat_set)-i-1,j])
                    u_filtered.append(u)
                    v_filtered.append(v)

    d1 = {}
    d1['header'] = {
          "dx": lng_diff*divisor,
          "dy": lat_diff*divisor,
          "la1": lat_end,
          "la2": lat_start,
          "lo1": lng_start,
          "lo2": lng_end,
          "numberPoints": nx*ny,
          "nx": nx,
          "ny": ny,
          "parameterCategory": 2,
          "parameterNumber": 2,
          "parameterNumberName": "eastward_current",
          "parameterUnit": "ms",
          "refTime": "2022"
    }
    d1['data'] = u_filtered

    d2 = {}
    d2['header'] = {
          "dx": lng_diff*divisor,
          "dy": lat_diff*divisor,
          "la1": lat_end,
          "la2": lat_start,
          "lo1": lng_start,
          "lo2": lng_end,
          "numberPoints": nx*ny,
          "nx": nx,
          "ny": ny,
          "parameterCategory": 2,
          "parameterNumber": 3,
          "parameterNumberName": "northward_current",
          "parameterUnit": "ms",
          "refTime": "2022"
    }
    d2['data'] = v_filtered

    data=[d1,d2]

    f = open(f"./bom_data/{dst_j}", "w")
    f.write(json.dumps(data))
    f.close()