#!/usr/bin/python3
import logging
import os
import time
import dfwrapper
from argparse import ArgumentParser
import sys
import diskfill

logger = logging.getLogger('main')


def check_file_exist(files, directory):
    logger.info("checking if files {0} exist in {1}".format(files, directory))
    logger.info("changing working directory to {0}".format(directory))
    os.chdir(directory)
    for f in files:
        if os.path.isfile(f['file']):
            f['exists'] = 'not-deleted'
        else:
            f['exists'] = 'deleted'
    return files


def get_uploaded_files(directory):
    """
    scans the directory and returns a list of files that are uploaded to the server
    this is checked by using .ok extension for a given filename
    :param directory:
    :return list of uploaded files:
    """
    # get filename(without ext) of the files that are uploaded
    logger.info("getting uploaded files from {0}".format(directory))
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
    logger.info("getting not uploaded files from {0}".format(directory))
    _notuploadedfiles = []
    for f in os.listdir(directory):
        if os.path.isdir(f):
            continue
        if f not in uploaded_files:
            _notuploadedfiles.append({'file': f, 'uploadstat': 'not-uploaded'})
    return _notuploadedfiles


if __name__ == '__main__':
    logger.setLevel(logging.DEBUG)
    # create file handler which logs even debug messages
    fh = logging.FileHandler('datapurge.log')
    fh.setLevel(logging.DEBUG)
    # create console handler with a higher log level
    ch = logging.StreamHandler()
    ch.setLevel(logging.ERROR)
    # create formatter and add it to the handlers
    formatter = logging.Formatter('%(asctime)s - %(name)s,%(lineno)d - %(levelname)s - %(message)s')
    fh.setFormatter(formatter)
    ch.setFormatter(formatter)
    # add the handlers to the logger
    logger.addHandler(fh)
    logger.addHandler(ch)
    # command line arguments parser
    parser = ArgumentParser(description='Data Purge Checking Program')
    parser.add_argument("-p", "--cobanvideospath", help="Path to cobanvideos folder", type=str, action="store")
    parser.add_argument("-f", "--pendrivefilesystem", help="Pen drive file system", type=str, action="store")
    parser.add_argument("-d", "--datapurgewaittime", help="Time to wait for data purging", type=int, action="store")
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
    data_purge_wait_time = args.datapurgewaittime if args.datapurgewaittime else 300  # default loop delay
    # TODO pick up this value from config.zip instead
    threshold = args.threshold if args.threshold else 25

    # if the available space on pen drive is less than the defined threshold
    # quit the program
    if dfwrapper.get_available_space(pen_drive_fsystem, True) <= threshold:
        logger.error("Test cannot start as the available space is already less than the threshold!")
        raise ValueError

    uploadedfiles = get_uploaded_files(coban_video_path)
    notuploadedfiles = get_notuploaded_files(coban_video_path, uploadedfiles)
    allfiles = uploadedfiles + notuploadedfiles

    while dfwrapper.get_available_space(pen_drive_fsystem, True) > threshold:
        diskfill.diskfill(1)

    # TODO make this configurable
    logger.info("waiting for {0}secs to complete data purge".format(data_purge_wait_time))
    time.sleep(data_purge_wait_time)  # wait for clean up to finish
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

    allfiles = check_file_exist(allfiles, coban_video_path)

    with open('datapurgeresult.log', 'a') as res:
        logger.info("writing results to file")
        for file in allfiles:
            res.write(str(file)+'\n')

















