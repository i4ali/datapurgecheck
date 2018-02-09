import os
from argparse import ArgumentParser


def diskfill(sizeinGB=1, filename='largefile'):
    thousandKB = 1000000  # bytes
    counter = 1
    with open(filename, 'ab') as fout:
        while counter < (sizeinGB*1000):
            fout.write(os.urandom(thousandKB))
            counter = counter+1
    return


if __name__ == '__main__':
    parser = ArgumentParser(description='Disk Filling Program')
    parser.add_argument("-s", "--size", help="GB to write", type=int, action="store")
    parser.add_argument("-f", "--file", help="File to write(with path)", type=str, action="store")
    args = parser.parse_args()

    GBtowrite = args.size
    file = args.file

    diskfill(GBtowrite, file)