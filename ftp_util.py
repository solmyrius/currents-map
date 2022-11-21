from ftplib import FTP
import io
import os
import json

from dotenv import load_dotenv

load_dotenv()

def get_ftp():
    uname = os.getenv('BOM_USER_NAME', '')
    upass = os.getenv('BOM_USER_PASSWORD', '')

    ftp_client = FTP('ftp.bom.gov.au')
    ftp_client.login(uname,upass)

    return ftp_client


def get_nwp_file(fname):

    uname = os.getenv('BOM_USER_NAME', '')

    if os.path.exists(f"./bom_file/{fname}"):
        return

    ftp = get_ftp()

    ftp.cwd(f'/register/{uname}/nwp')

    f = open(f"./bom_file/{fname}", 'wb')

    ftp.retrbinary('RETR ' + fname, f.write)

    ftp.close()
    f.close()

def get_listing():

    ftp = get_ftp()
    d = ftp.nlst('nwp')

    ftp.close()

    return d

def get_file_info(fname):

    info = {}
    ftp = get_ftp()
    info['size'] = ftp.size(f'nwp/{fname}')

    ftp.close()

    return info