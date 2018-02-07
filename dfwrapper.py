import subprocess


def get_available_space(partition):
    """
    :param partition:
    :return available space for the filesystem argument:
    """
    df = subprocess.Popen(["df", "-h", "--block-size=GB"], stdout=subprocess.PIPE)
    for line in df.stdout:
        splitline = line.decode().split()
        if splitline[0] == partition:
            return int(splitline[3][:-2])


if __name__ == '__main__':
    threshold = 250
    prod_partition = '/media/ubuntu/USB'
    dev_partition = '/dev/sda1'
    print(get_available_space(dev_partition))