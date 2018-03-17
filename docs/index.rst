.. datapurgecheck documentation master file, created by
   sphinx-quickstart on Wed Mar  7 15:10:52 2018.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.

Welcome to datapurgecheck documentation
==========================================

Introduction
************

Data purge check is an in-house developed utility that helps to validate the data purging functionality for Coban products.


Documentation
*************

.. automodule:: datapurgecheck

Installation
************

Download the latest datapurgecheck utility from the utilities folder in X->SWQA->Utilities and copy the .tar file
into the test unit.

Untar the utility using the following commands

    ::

     tar -xvf datapurgecheck.tar


Usage
*****

Sample usage(s) are shown below:

     ::

      python3 datapurgecheck -p '/vagrant/development/datapurgecheck/datapurgecheck/data' -t 249 -d 5 -f '/vagrant' -m 'Mounted on'

if you want to see all available arguments and supported features
    ::

      usage: datapurgecheck [-h] [-p COBANVIDEOSPATH] [-f PENDRIVEFILESYSTEM]
                      [-d DATAPURGEWAITTIME] [-m {Filesystem,Mounted on}]
                      [-t THRESHOLD] [-o FILE] [-e EXTENSION] [-s]

       optional arguments:
      -h, --help            show this help message and exit
      -p COBANVIDEOSPATH, --cobanvideospath COBANVIDEOSPATH
                            Path to cobanvideos folder (default:
                            /media/ubuntu/USB/cobanvideos)
      -f PENDRIVEFILESYSTEM, --pendrivefilesystem PENDRIVEFILESYSTEM
                            Pen drive file system (default: /dev/sdb1)
      -d DATAPURGEWAITTIME, --datapurgewaittime DATAPURGEWAITTIME
                            Time to wait for data purging to complete (default:
                            300)
      -m {Filesystem,Mounted on}, --mount {Filesystem,Mounted on}
                            Use filesystem device path or mounted on path
                            (default: Filesystem), run'df -h to identify the field
                            to use'
      -t THRESHOLD, --threshold THRESHOLD
                            MHDD Space Threshold (default: 25)
      -o FILE, --csvfile FILE
                            Filename for the results file(including ext (default:
                            datapurgeresult.csv))
      -e EXTENSION, --extension EXTENSION
                            Extension of the junk file to be added
      -s, --splitfile       Split the junk data file into multiple 1GB files


.. toctree::
   :maxdepth: 2
   :caption: Contents:



Indices and tables
==================

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`
