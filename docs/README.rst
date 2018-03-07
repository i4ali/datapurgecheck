.. datapurgecheck documentation master file, created by
   sphinx-quickstart on Wed Mar  7 15:10:52 2018.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.

Welcome to datapurgecheck's documentation
==========================================

Introduction
************

Data purge check is an in-house developed utility that helps validate the data purging functionality for Coban products.


Documentation
*************

.. automodule:: datapurgecheck


Usage
*****

    ::

     usage: __main__.py [-h] [-p COBANVIDEOSPATH] [-f PENDRIVEFILESYSTEM]
                   [-d DATAPURGEWAITTIME] [-m {Filesystem,Mounted on}]
                   [-t THRESHOLD] [-o FILE]

     optional arguments:
     -h, --help            show this help message and exit
     -p COBANVIDEOSPATH, --cobanvideospath COBANVIDEOSPATH
                        Path to cobanvideos folder (default:
                        /media/ubuntu/USB/cobanvideos)
     -f PENDRIVEFILESYSTEM, --pendrivefilesystem PENDRIVEFILESYSTEM
                        Pen drive file system (default: /dev/sdb1)
     -d DATAPURGEWAITTIME, --datapurgewaittime DATAPURGEWAITTIME
                        Time to wait for data purging (default: 300)
     -m {Filesystem,Mounted on}, --mount {Filesystem,Mounted on}
                        Use filesystem device path or mounted on path
                        (default: Filesystem)
     -t THRESHOLD, --threshold THRESHOLD
                        MHDD Space Threshold (default: 25)
     -o FILE, --csvfile FILE
                        Filename for the results file(including ext (default:
                        datapurgeresult.csv))


Sample usage(s) are shown below:

     ::

      python3 datapurgecheck -p '/vagrant/development/datapurgecheck/datapurgecheck/data' -t 249 -d 5 -f '/vagrant' -m 'Mounted on'
      python3 datapurgecheck -h


.. toctree::
   :maxdepth: 2
   :caption: Contents:



Indices and tables
==================

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`
