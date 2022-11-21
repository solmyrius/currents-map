import math
from netCDF4 import Dataset

def to_float(val):
    try:
        x = float(val)
        if math.isnan(x):
            return 0
        else:
            return x
    except:
        return 0

def grp_min_max_4(grp, model, dim):
    lat_set = grp[model['lat']][:]
    lng_set = grp[model['lng']][:]
    data_set = grp[model['var']][:]
    min = 1000
    max = -1000
    for i in range(len(lat_set)):
        for j in range(len(lng_set)):
            x = float(data_set[0, dim, i, j])
            if not math.isnan(x):
                if x<min:
                    min = x
                if x>max:
                    max = x
    return {'min':min,'max':max}

def grp_min_max_3(grp, model):
    lat_set = grp[model['lat']][:]
    lng_set = grp[model['lng']][:]
    data_set = grp[model['var']][:]
    min = 1000
    max = -1000
    for i in range(len(lat_set)):
        for j in range(len(lng_set)):
            x = float(data_set[0, i, j])
            if not math.isnan(x):
                if x<min:
                    min = x
                if x>max:
                    max = x
    return {'min':min,'max':max}
