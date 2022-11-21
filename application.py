import json
import os
import io
import math

from dotenv import load_dotenv
from flask import Flask, Response, render_template
from netCDF4 import Dataset

from model import get_model
from model_vector import build_vector_model
from model_scalar import build_scalar_model_temp, build_scalar_model_salt, build_scalar_model_eta
from ftp_util import get_listing, get_nwp_file, get_file_info
from ncd_util import grp_min_max_4, grp_min_max_3

load_dotenv()

def prepare_vector_model(src, dimension):
    if src.find('.v.')>0:
        v_file = src
        u_file = src.replace('.v.','.u.')
    if src.find('.u.')>0:
        u_file = src
        v_file = src.replace('.u.','.v.')

    get_nwp_file(u_file)
    get_nwp_file(v_file)

    build_vector_model(src+'-'+str(dimension)+'.json', u_file, v_file, dimension)

def prepare_scalar_model(src, dimension, model):
    get_nwp_file(src)

    if model['id'] == 'temp':
        build_scalar_model_temp(src+'-'+str(dimension)+'.json', src, dimension, model)
    if model['id'] == 'salt':
        build_scalar_model_salt(src+'-'+str(dimension)+'.json', src, dimension, model)
    if model['id'] == 'eta':
        build_scalar_model_eta(src+'-'+str(dimension)+'.json', src, model)

def get_all_models(model_name):
    models = {}
    if model_name.find('.v.')>0:
        models['model_name_u'] = model_name.replace('.v.','.u.')
        models['model_name_temp'] = model_name.replace('.v.','.temp.')
        models['model_name_eta'] = model_name.replace('.v.','.eta.')
        models['model_name_salt'] = model_name.replace('.v.','.salt.')
    if model_name.find('.u.')>0:
        models['model_name_u'] = model_name
        models['model_name_temp'] = model_name.replace('.u.','.temp.')
        models['model_name_eta'] = model_name.replace('.u.','.eta.')
        models['model_name_salt'] = model_name.replace('.u.','.salt.')
    if model_name.find('.temp.')>0:
        models['model_name_u'] = model_name.replace('.temp.','.u.')
        models['model_name_temp'] = model_name
        models['model_name_eta'] = model_name.replace('.temp.','.eta.')
        models['model_name_salt'] = model_name.replace('.temp.','.salt.')
    if model_name.find('.salt.')>0:
        models['model_name_u'] = model_name.replace('.salt.','.u.')
        models['model_name_temp'] = model_name.replace('.salt.','.temp.')
        models['model_name_eta'] = model_name.replace('.salt.','.eta.')
        models['model_name_salt'] = model_name
    if model_name.find('.eta.')>0:
        models['model_name_u'] = model_name.replace('.eta.','.u.')
        models['model_name_temp'] = model_name.replace('.eta.','.temp.')
        models['model_name_eta'] = model_name
        models['model_name_salt'] = model_name.replace('.eta.','.salt.')
    return models

application = Flask(__name__)

@application.route('/')
def home():
    return page_listing()

@application.route('/file/<file_name>')
def page_file_info(file_name):
    html = ''
    html = html + '<div>File name: '+file_name+'</div>'

    info = get_file_info(file_name)

    html = html + '<div>File size: '+str(info['size'])+'</div>'

    if(info['size'] > 4000000):
        html = html + '<div>This file is too big and will not be processed on demo AWS instance but you still can process it on your own AWS</div>'
    else:
        get_nwp_file(file_name)

        model_id = ''
        rootgrp = Dataset(f"./bom_file/{file_name}", "r", format="NETCDF4")

        model = get_model(file_name)
        html = html + '<div>'+model['name']+'</div>'

        rootgrp = Dataset(f"./bom_file/{file_name}", "r", format="NETCDF4")
        lat_set = rootgrp[model['lat']][:]
        lng_set = rootgrp[model['lng']][:]

        lat1 = lat_set[0]
        lat2 = lat_set[len(lat_set)-1]

        lng1 = lng_set[0]
        lng2 = lng_set[len(lng_set)-1]

        html = html + f'<div>Lat from:{lat1} to:{lat2} total points:{len(lat_set)}'+'</div>'
        html = html + f'<div>Lng from:{lng1} to:{lng2} total points:{len(lng_set)}'+'</div>'

        if 'dimension' in model:

            dim_set = rootgrp[model['dimension']][:]
            dim_len = len(dim_set)
            dim_name = model['dimension_name']
            
            html = html + f"<div>Dimension: {dim_name} from:{dim_set[0]} to:{dim_set[len(dim_set)-1]} total points:{len(dim_set)}"+'</div>'
            html = html + f'<div>Available maps from this file:</div>'
            for i in range(dim_len):
                d = dim_set[i]
                min_max = grp_min_max_4(rootgrp, model, i)
                if model['id']=='u' or model['id']=='v':
                    html = html + f'<div><a href="/map_vector/{file_name}/{i}?lat1={lat1}&lat2={lat2}&lng1={lng1}&lng2={lng2}">{dim_name} {d}</a></div>'
                else:
                    html = html + f'<div><a href="/map_scalar/{file_name}/{i}?lat1={lat1}&lat2={lat2}&lng1={lng1}&lng2={lng2}">{dim_name} {d}</a> min:{min_max["min"]} max:{min_max["max"]}</div>'

        else:
            html = html + f'<div><a href="/map_scalar/{file_name}/0?lat1={lat1}&lat2={lat2}&lng1={lng1}&lng2={lng2}">This file contains only one map</a></div>'

    return html

@application.route('/map_vector/<file_name>/<dimension>')
def page_map_vector(file_name, dimension):
    models = get_all_models(file_name)
    return render_template('index.html', model_name = file_name, dimension=dimension, models=models)

@application.route('/map_scalar/<file_name>/<dimension>')
def page_map_scalar(file_name, dimension):
    models = get_all_models(file_name)
    return render_template('index.html', model_name = file_name, dimension=dimension, models=models)

@application.route('/bom_data/<file_name>')
def bom_data(file_name):
    if file_name.find('.json') > 0:
        if not os.path.exists(f"./bom_data/{file_name}"):
            name = file_name.replace('.json','')
            name_parts = name.split('-')
            src = name_parts[0]
            dimension = int(name_parts[1])
            model = get_model(src)
            if model['type'] == 'vector':
                prepare_vector_model(src, dimension)
            if model['type'] == 'scalar':
                prepare_scalar_model(src, dimension, model)

        f = open(f"./bom_data/{file_name}", 'r')
        str = f.read()
        return Response(str, mimetype='application/json')

def page_listing():
    html = ''
    d = get_listing()
    for f in d:
        fp = f.split('/')
        if fp[1][:8] != 'IDYOC703':
            html = html + '<div><a href="/file/'+fp[1]+'">'+fp[1]+'</div>'
    return html

if __name__ == "__main__":
    application.debug = True
    application.run()