#!/usr/bin/env python3

import logging
import os
import time
from datapurgecheck.utilities import dfwrapper
from datapurgecheck.utilities.diskfill import DiskFill
from argparse import ArgumentParser
import sys
from datapurgecheck.utilities.helperutil import ChDir

# TODO write unit tests
logger = logging.getLogger('main')

validextensions = ['.ok', '.l', '.v', '.log', '.mp4', '.jpg', '.c', '.d', '.ts', '.a']



def check_file_exist(file, directory):
    """
    scans the directory for the file and provides the status of its existence
    :param file: file to be checked for existence
    :param directory: directory to be scanned
    :return boolean: True of False
    """
    logger.debug("checking if file {0} exists in {1} directory".format(file, directory))
    with ChDir(directory):
        if os.path.isfile(file):
            return True
        else:
            return False


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
    scans the directory and returns a list of files that are not-uploaded to the server
    this is checked by using .ok extension for a given filename
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

    logger.setLevel(logging.DEBUG)
    # create file handler which logs even debug messages
    fh = logging.FileHandler('datapurge.log')
    fh.setLevel(logging.DEBUG)
    # create console handler with a higher log level
    ch = logging.StreamHandler()
    ch.setLevel(logging.DEBUG)
    # create formatter and add it to the handlers
    formatter = logging.Formatter('%(asctime)s - %(name)s,%(lineno)d - %(levelname)s - %(message)s')
    # fh.setFormatter(formatter)
    ch.setFormatter(formatter)
    # add the handlers to the logger
    logger.addHandler(fh)
    logger.addHandler(ch)
    # command line arguments parser
    parser = ArgumentParser(description=__doc__)
    parser.add_argument("-p", "--cobanvideospath", help="Path to cobanvideos folder (default: %(default)s)", type=str, action="store",
                        default='/media/ubuntu/USB/cobanvideos')
    parser.add_argument("-f", "--pendrivefilesystem", help="Pen drive file system (default: %(default)s)", type=str, action="store",
                        default='/dev/sdb1')
    parser.add_argument("-d", "--datapurgewaittime", help="Time to wait for data purging (default: %(default)s)", type=int, action="store",
                        default=300)
    parser.add_argument("-m", "--mount", help="Use filesystem device path or mounted on path (default: %(default)s)", action="store", type=str,
                        choices=['Filesystem', 'Mounted on'], default='Filesystem')
    parser.add_argument("-t", "--threshold", help="MHDD Space Threshold (default: %(default)s)", type=int, action="store",
                        default=25)
    parser.add_argument("-o", "--csvfile",
                        help='Filename for the results file(including ext (default: %(default)s))',
                        metavar="FILE", action="store", default='datapurgeresult.csv')
    parser.add_argument("-e", "--extension", help="Extension of the file to be added",
                        type=str, action="store", default='')
    args = parser.parse_args()

    logger.debug("arguments provided - {0} ".format(sys.argv))

    # if the available space on pen drive is less than the defined threshold
    # quit the program
    if dfwrapper.get_available_space(args.pendrivefilesystem, args.mount) <= args.threshold:
        #TODO rethink if this error message is needed
        logger.error("Test cannot start as the available space is already less than the threshold!")
        raise ValueError("Available space is less than the defined threshold")

    uploadedfiles = get_uploaded_files(args.cobanvideospath)
    logger.debug("uploaded files - {0}".format(uploadedfiles))
    notuploadedfiles = get_notuploaded_files(args.cobanvideospath, uploadedfiles)
    logger.debug("notuploaded files - {0}".format(notuploadedfiles))

    common_files = [x for x in uploadedfiles if x in notuploadedfiles]
    assert not common_files   # make sure no common files in uploaded and not-uploaded files exist
    allfileswstatus = []
    for f in uploadedfiles:
        allfileswstatus.append({'file': f, 'uploadstat': 'uploaded'})
    for f in notuploadedfiles:
        allfileswstatus.append({'file': f, 'uploadstat': 'not-uploaded'})

    DiskFill(1, os.path.join(args.cobanvideospath, ('largefile'+args.extension)))

    while dfwrapper.get_available_space(args.pendrivefilesystem, args.mount) > args.threshold:
        DiskFill.diskfill()
        DiskFill.sizewritten()
        # diskfill.diskfill(1, os.path.join(args.cobanvideospath, ('largefile'+args.extension)))

    logger.info("waiting for {0}secs to complete data purge".format(args.datapurgewaittime))
    time.sleep(args.datapurgewaittime)  # wait for purging to finish

    for file in allfileswstatus:
        if check_file_exist(file['file'], args.cobanvideospath):
            file['exists'] = 'not-deleted'
        else:
            file['exists'] = 'deleted'

    allfileswstatus = sorted(allfileswstatus, key=lambda k: k['file'])    # sort the list by filenames for easier read

    with open(args.csvfile, 'a') as res:
        logger.info("writing results to file {0}".format(args.csvfile))
        for file in allfileswstatus:
            res.write(str(file['file'])+',')
            res.write(str(file['uploadstat'])+',')
            res.write(str(file['exists'])+'\n')

















