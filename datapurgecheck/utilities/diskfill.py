import logging
import os
from argparse import ArgumentParser

# create logger
logger = logging.getLogger('main.diskfill')


class DiskFill:
    thousandKB = 1000000  # bytes

    def __init__(self, sizeinGB, filename, splitfile=False):
        self.sizeinGB = sizeinGB
        self.count = 0
        # self.filename = filename
        self.file, self.filext = os.path.splitext(filename)
        self.splitfile = splitfile

    def diskfill(self):
        logger.info("writing to disk - size:{0}GB, filename:{1}".format(self.sizeinGB, self.file+self.filext))
        counter = 1
        dfile = self.file+self.filext
        if self.splitfile and (self.count > 0):
            dfile = self.file+str(self.count)+self.filext
        with open(dfile, 'ab') as fout:
            while counter < (self.sizeinGB * 1000):
                fout.write(os.urandom(self.thousandKB))
                counter = counter + 1
        self.count += 1
        return

    def getsizewritten(self):
        logger.info("size written to disk {0}GB".format(self.count*self.sizeinGB))
        return self.count*self.sizeinGB


if __name__ == '__main__':
    parser = ArgumentParser(description='Disk Filling Program')
    parser.add_argument("-s", "--size", help="GB to write", type=int, action="store")
    parser.add_argument("-f", "--file", help="File to write(with path)", type=str, action="store")
    args = parser.parse_args()

    GBtowrite = args.size
    file = args.file

    df = DiskFill(GBtowrite, file)
    df.diskfill()
    df.getsizewritten()
