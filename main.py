#!/usr/bin/python3
import os
import time
import datetime
import dfwrapper
from argparse import ArgumentParser
import logging
import sys
import diskfill


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
    for f in os.listdir(directory):
        filename, file_extension = os.path.splitext(f)
        if file_extension == '.ok':
            _uploadedfilenames.append(filename)
    # get all files(with ext) that have the same filename AND if they were uploaded
    for f in os.listdir(directory):
        filename, file_extension = os.path.splitext(f)
        if filename in _uploadedfilenames:
            _uploadedfiles.append({'file': f, 'uploadstat': 'uploaded'})
    return _uploadedfiles


def get_notuploaded_files(directory, uploaded_files):
    _notuploadedfiles = []
    for f in os.listdir(directory):
        if os.path.isdir(f):
            continue
        if f not in uploaded_files:
            _notuploadedfiles.append({'file': f, 'uploadstat': 'not-uploaded'})
    return _notuploadedfiles


if __name__ == '__main__':

    # command line arguments parser
    parser = ArgumentParser(description='Data Purge Checking Program')
    parser.add_argument("-p", "--cobanvideospath", help="Path to cobanvideos folder", type=str, action="store")
    parser.add_argument("-f", "--pendrivefilesystem", help="Pen drive file system", type=str, action="store")
    parser.add_argument("-d", "--loopdelay", help="Delay between loops", type=int, action="store")
    parser.add_argument("-dev", "--development", help="Development Mode", action="store_true")
    parser.add_argument("-t", "--threshold", help="MHDD Space Threshold", type=int, action="store")
    parser.add_argument("-o", "--logfile",
                        help='Filename for the log file(including ext)',
                        metavar="FILE", action="store")
    args = parser.parse_args()

    # development directories
    dev_dir = '/vagrant/development/datapurgecheck'

    coban_video_path = dev_dir if args.development else (args.cobanvideospath if args.cobanvideospath else '/media/ubuntu/USB/cobanvideos')   # default cobanvideos path
    pen_drive_fsystem = args.pendrivefilesystem if args.pendrivefilesystem else '/dev/sdb1'  # default pen drive file system
    print_loop_delay = args.loopdelay if args.loopdelay else 5  # default loop delay
    #TODO pick up this value from config.zip instead
    threshold = args.threshold if args.threshold else 25

    # logging
    # TODO define a better logging structure
    sys.stdout = logging.Logger(args.logfile if args.logfile else 'datapurge.log')

    os.chdir(coban_video_path)

    # if the available space on pen drive is less than the defined threshold
    # quit the program
    if dfwrapper.get_available_space(pen_drive_fsystem) < threshold:
        print("Test cannot start as the available space is already less than the threshold")
        sys.exit(1)

    uploadedfiles = get_uploaded_files(coban_video_path)
    notuploadedfiles = get_notuploaded_files(coban_video_path, uploadedfiles)
    allfiles = uploadedfiles + notuploadedfiles

    while dfwrapper.get_available_space(pen_drive_fsystem) > threshold:
        diskfill.diskfill(1)

    # TODO make this configurable
    time.sleep(300)  # wait for clean up to finish
    # while True:
    #     print('*'*20)
    #     print('{:%Y-%m-%d %H:%M:%S}'.format(datetime.datetime.today()))
    #     print('available space on {0}: {1}GB'.format(pen_drive_fsystem, dfwrapper.get_available_space(pen_drive_fsystem)))
    #     print('*'*20)
    #     for file in allfiles:
    #         if os.path.isfile(file['file']):
    #             file['exists'] = 'not-deleted'
    #         else:
    #             file['exists'] = 'deleted'
    #         print('{0:<30}{1:<30}{2:<30}'.format(file['file'], file['uploadstat'], file['exists']))
    #     time.sleep(args.loopdelay if args.loopdelay else print_loop_delay)

    for file in allfiles:
        if os.path.isfile(file['file']):
            file['exists'] = 'not-deleted'
        else:
            file['exists'] = 'deleted'
    print(allfiles)

















