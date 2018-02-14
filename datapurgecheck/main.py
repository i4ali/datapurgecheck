#!/usr/bin/python3
import logging
import os
import time
from utilities import dfwrapper, diskfill
from argparse import ArgumentParser
import sys
from utilities.helperutil import ChDir

# TODO write unit tests
logger = logging.getLogger('main')

validextensions = ['.ok', '.l', '.v', '.log', '.mp4', '.jpg', '.c', '.d', '.ts', '.a']


def check_file_exist(files, directory):
    """

    :param files: a list of dictionaries with filename, uploadstat info
    :param directory: directory to scan
    :return files: a list of dictionaries with filename, exists, uploadedstat info
    """
    logger.info("checking if files {0} exist in {1}".format(files, directory))
    with ChDir(directory):
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
    :param directory: directory to scan
    :return list of uploaded files:
    """

    logger.info("getting uploaded files from {0}".format(directory))
    with ChDir(directory):
        _uploadedfilenames = []
        uploadedfiles = []
        # get filename(without ext) of the files that are uploaded
        for f in os.listdir(directory):
            if os.path.isdir(f):
                continue
            filename, file_extension = os.path.splitext(f)
            if file_extension == '.ok':
                _uploadedfilenames.append(filename)
        # get all files(with ext) that have the same filename AND if they were uploaded
        for f in os.listdir(directory):
            if os.path.isdir(f):
                continue
            filename, file_extension = os.path.splitext(f)
            if file_extension not in validextensions:
                filename = f
            if filename in _uploadedfilenames:
                uploadedfiles.append(f)
    return uploadedfiles


def get_notuploaded_files(directory, uploaded_files):
    """

    :param directory: directory to scan
    :param uploaded_files: list of uploaded files
    :return notuploadedfiles: list of not uploaded files
    """
    logger.info("getting not uploaded files from {0}".format(directory))
    with ChDir(directory):
        notuploadedfiles = []
        for f in os.listdir(directory):
            if os.path.isdir(f):
                continue
            if f not in uploaded_files:
                notuploadedfiles.append(f)
    return notuploadedfiles


if __name__ == '__main__':
    """
    example run options
    main.py -t 243 -dev -d 5 -f '/vagrant' -m
    main.py -t 25 -d 1000
    """
    # TODO rethink if filehandler is required
    logger.setLevel(logging.DEBUG)
    # create file handler which logs even debug messages
    # fh = logging.FileHandler('datapurge.log')
    # fh.setLevel(logging.DEBUG)
    # create console handler with a higher log level
    ch = logging.StreamHandler()
    ch.setLevel(logging.DEBUG)
    # create formatter and add it to the handlers
    formatter = logging.Formatter('%(asctime)s - %(name)s,%(lineno)d - %(levelname)s - %(message)s')
    # fh.setFormatter(formatter)
    ch.setFormatter(formatter)
    # add the handlers to the logger
    # logger.addHandler(fh)
    logger.addHandler(ch)
    # command line arguments parser
    # TODO show default values when -h is called
    parser = ArgumentParser(description='Data Purge Checking Program')
    parser.add_argument("-p", "--cobanvideospath", help="Path to cobanvideos folder", type=str, action="store")
    parser.add_argument("-f", "--pendrivefilesystem", help="Pen drive file system", type=str, action="store")
    parser.add_argument("-d", "--datapurgewaittime", help="Time to wait for data purging", type=int, action="store")
    parser.add_argument("-dev", "--development", help="Development Mode", action="store_true")
    parser.add_argument("-m", "--mount", help="Use Mounted on", action="store_true", default=False)
    parser.add_argument("-t", "--threshold", help="MHDD Space Threshold", type=int, action="store")
    parser.add_argument("-o", "--csvfile",
                        help='Filename for the results file(including ext)',
                        metavar="FILE", action="store")
    # TODO rethink the Use mounted on option and how to handle that properly
    args = parser.parse_args()

    # development directories
    dev_dir = '/vagrant/development/datapurgecheck/data'

    coban_video_path = dev_dir if args.development else (args.cobanvideospath if args.cobanvideospath else '/media/ubuntu/USB/cobanvideos')   # default cobanvideos path
    pen_drive_fsystem = args.pendrivefilesystem if args.pendrivefilesystem else '/dev/sdb1'  # default pen drive file system
    data_purge_wait_time = args.datapurgewaittime if args.datapurgewaittime else 300  # default loop delay
    # TODO pick up this value from config.zip instead
    threshold = args.threshold if args.threshold else 25
    csv_file = args.csvfile if args.csvfile else 'datapurgeresult.csv'

    logger.debug("arguments provided - {0} ".format(sys.argv))

    # if the available space on pen drive is less than the defined threshold
    # quit the program
    if dfwrapper.get_available_space(pen_drive_fsystem, args.mount) <= threshold:
        logger.error("Test cannot start as the available space is already less than the threshold!")
        raise ValueError

    uploadedfiles = get_uploaded_files(coban_video_path)
    logger.debug("uploaded files - {0}".format(uploadedfiles))
    notuploadedfiles = get_notuploaded_files(coban_video_path, uploadedfiles)
    logger.debug("notuploaded files - {0}".format(notuploadedfiles))

    common_files = [x for x in uploadedfiles if x in notuploadedfiles]
    assert not common_files   # make sure no common files in uploaded and not-uploaded files exist
    allfileswstatus = []
    for f in uploadedfiles:
        allfileswstatus.append({'file': f, 'uploadstat': 'uploaded'})
    for f in notuploadedfiles:
        allfileswstatus.append({'file': f, 'uploadstat': 'not-uploaded'})

    while dfwrapper.get_available_space(pen_drive_fsystem, args.mount) > threshold:
        diskfill.diskfill(1, os.path.join(coban_video_path, 'largefile'))

    logger.info("waiting for {0}secs to complete data purge".format(data_purge_wait_time))
    time.sleep(data_purge_wait_time)  # wait for clean up to finish

    allfileswstatus = check_file_exist(allfileswstatus, coban_video_path)

    allfileswstatus = sorted(allfileswstatus, key=lambda k: k['file'])    # sort the list by filenames for easier read

    with open(csv_file, 'a') as res:
        logger.info("writing results to file {0}".format(csv_file))
        for file in allfileswstatus:
            res.write(str(file['file'])+',')
            res.write(str(file['uploadstat'])+',')
            res.write(str(file['exists'])+'\n')

















