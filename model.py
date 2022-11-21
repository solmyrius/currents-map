import math
import json
from netCDF4 import Dataset

def get_model(file_name):

    if(file_name.find('.u.') > 0):
        model_id = 'u'
    if(file_name.find('.v.') > 0):
        model_id = 'v'
    if(file_name.find('.temp.') > 0):
        model_id = 'temp'
    if(file_name.find('.salt.') > 0):
        model_id = 'salt'
    if(file_name.find('.eta.') > 0):
        model_id = 'eta'

    if(model_id == 'u'):
        return {
            'id':'u',
            'name':'current U',
            'lng':'xu_ocean',
            'lat':'yu_ocean',
            'var':'u',
            'type':'vector',
            'dimension':'st_ocean',
            'dimension_name':'depth',
        }
    if(model_id == 'v'):
        return {
            'id':'v',
            'name':'current V',
            'lng':'xu_ocean',
            'lat':'yu_ocean',
            'var':'v',
            'type':'vector',
            'dimension':'st_ocean',
            'dimension_name':'depth',
        }
    if(model_id == 'temp'):
        return {
            'id':'temp',
            'name':'Temperature',
            'lng':'xt_ocean',
            'lat':'yt_ocean',
            'var':'temp',
            'type':'scalar',
            'dimension':'st_ocean',
            'dimension_name':'depth',
        }
    if(model_id == 'salt'):
        return {
            'id':'salt',
            'name':'Practical Salinity',
            'lng':'xt_ocean',
            'lat':'yt_ocean',
            'var':'salt',
            'type':'scalar',
            'dimension':'st_ocean',
            'dimension_name':'depth',
        }
    if(model_id == 'eta'):
        return {
            'id':'eta',
            'name':'surface height on T cells',
            'lng':'xt_ocean',
            'lat':'yt_ocean',
            'var':'eta_t',
            'type':'scalar',
        }