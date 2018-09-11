.. datapurgecheck documentation master file, created by
   sphinx-quickstart on Wed Mar  7 15:10:52 2018.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.

datapurgecheck utility documentation
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

Requirements
************

Python 3


Products supported
******************

H1


Usage
*****

Sample usage(s) are shown below:

     ::

      python3 datapurgecheck -p '/vagrant/development/datapurgecheck/datapurgecheck/data' -t 249 -d 5 -f '/vagrant' -m 'Mounted on'

if you want to see all available arguments and supported features
    ::

      python3 datapurgecheck -h


.. toctree::
   :maxdepth: 2
   :caption: Contents:



