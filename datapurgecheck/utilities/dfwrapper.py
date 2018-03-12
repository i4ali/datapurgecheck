import logging
import subprocess


# create logger
logger = logging.getLogger('main.dfwrapper')


def get_available_space(partition, dev_path):
    """
    :param partition:
    :return available space for the filesystem argument:
    """
    logger.info("getting available space for {0} using mount on {1} ".format(partition, dev_path))
    df = subprocess.Popen(["df", "-h", "--block-size=GB"], stdout=subprocess.PIPE)
    for line in df.stdout:
        splitline = line.decode().split()
        if dev_path == 'Mounted on':
            if splitline[5] == partition:
                available_space = int(splitline[3][:-2])
                logger.info("Available space is {0}GB".format(available_space))
                return available_space
        elif dev_path == 'Filesystem':
            if splitline[0] == partition:
                available_space = int(splitline[3][:-2])
                logger.info("Available space is {0}GB".format(available_space))
                return available_space
        else:
            raise ValueError("Unsupported device path")


if __name__ == '__main__':
    threshold = 250
    prod_partition = '/media/ubuntu/USB'
    dev_partition = '/dev/sda1'
    print(get_available_space(dev_partition))