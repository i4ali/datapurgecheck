#!/usr/bin/python3
import os
import time
import datetime
import dfwrapper

dev_dir = '/vagrant/development/datapurgecheck/data'
prod_dir = '/media/ubuntu/USB/cobanvideos'
pen_drive = '/dev/sdb1'


def get_uploaded_files(directory):
    """
    scans the directory and returns a list of files that are uploaded to the server
    this is checked by using .ok extension for a given filename
    :param directory:
    :return list of uploaded files
    """
    # get filename(without ext) of the files that are uploaded
    _uploadedfilenames = []
    _uploadedfiles = []
    for file in os.listdir(directory):
        filename, file_extension = os.path.splitext(file)
        if file_extension == '.ok':
            _uploadedfilenames.append(filename)
    # get all files(with ext) that have the same filename AND if they were uploaded
    for file in os.listdir(directory):
        filename, file_extension = os.path.splitext(file)
        if filename in _uploadedfilenames:
            _uploadedfiles.append({'file': file})
    return _uploadedfiles


if __name__ == '__main__':
    os.chdir(prod_dir)
    uploadedfilestatus = []
    uploadedfiles = get_uploaded_files(prod_dir)
    while True:
        print('*'*20)
        print('{:%Y-%m-%d %H:%M:%S}'.format(datetime.datetime.today()))
        print('available space: {0}GB'.format(dfwrapper.get_available_space(pen_drive)))
        print('*'*20)
        for upfile in uploadedfiles:
            if os.path.isfile(upfile['file']):
                upfile['exists'] = 'not-deleted'
            else:
                upfile['exists'] = 'deleted'
            print('{0:<30}{1:<30}'.format(upfile['file'], upfile['exists']))
        time.sleep(5)

















