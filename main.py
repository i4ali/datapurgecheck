#!/usr/bin/python3
import os
import time
import datetime
import dfwrapper
from argparse import ArgumentParser
import logging
import sys


def get_uploaded_files(directory):
    """
    scans the directory and returns a list of files that are uploaded to the server
    this is checked by using .ok extension for a given filename
    :param directory:
    :return list of uploaded files:
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
    # test
    # dev_dir = '/vagrant/development/datapurgecheck/data'

    # defaults
    coban_video_path = '/media/ubuntu/USB/cobanvideos'  # default cobanvideos path
    pen_drive_fsystem = '/dev/sdb1'  # default pen drive file system
    print_loop_delay = 5  # default loop delay
    threshold = 25

    # command line arguments parser
    parser = ArgumentParser(description='Data Purge Checking Program')
    parser.add_argument("-p", "--cobanvideospath", help="Path to cobanvideos folder", type=str, action="store")
    parser.add_argument("-d", "--loopdelay", help="Delay between loops", type=int, action="store")
    parser.add_argument("-t", "--threshold", help="MHDD Space Threshold", type=int, action="store")
    parser.add_argument("-o", "--logfile",
                        help='Filename for the log file(including ext)',
                        metavar="FILE", action="store")
    args = parser.parse_args()

    # logging
    sys.stdout = logging.Logger(args.logfile if args.logfile else 'datapurge.log')

    os.chdir(coban_video_path)
    uploadedfilestatus = []
    coban_video_path = args.cobanvideospath if args.cobanvideospath else coban_video_path
    uploadedfiles = get_uploaded_files(coban_video_path)
    while True:
        print('*'*20)
        print('{:%Y-%m-%d %H:%M:%S}'.format(datetime.datetime.today()))
        print('available space on {0}: {1}GB'.format(pen_drive_fsystem, dfwrapper.get_available_space(pen_drive_fsystem)))
        print('*'*20)
        for upfile in uploadedfiles:
            if os.path.isfile(upfile['file']):
                upfile['exists'] = 'not-deleted'
            else:
                upfile['exists'] = 'deleted'
            print('{0:<30}{1:<30}'.format(upfile['file'], upfile['exists']))
        time.sleep(args.loopdelay if args.loopdelay else print_loop_delay)

















