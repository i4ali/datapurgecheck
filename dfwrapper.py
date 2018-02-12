import logging
import subprocess


# create logger
logger = logging.getLogger('main.dfwrapper')


def get_available_space(partition, use_mounted_on=False):
    """
    :param partition:
    :return available space for the filesystem argument:
    """
    logger.info("getting available space for {0} using 'mount on' {1} ".format(partition, use_mounted_on))
    df = subprocess.Popen(["df", "-h", "--block-size=GB"], stdout=subprocess.PIPE)
    for line in df.stdout:
        splitline = line.decode().split()
        if use_mounted_on:
            if splitline[5] == partition:
                return int(splitline[3][:-2])
        else:
            if splitline[0] == partition:
                return int(splitline[3][:-2])


if __name__ == '__main__':
    threshold = 250
    prod_partition = '/media/ubuntu/USB'
    dev_partition = '/dev/sda1'
    print(get_available_space(dev_partition))