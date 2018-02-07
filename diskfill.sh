#!/usr/bin/env bash

# to run this script
# ./diskfill.sh file size_in_GB
dd if=/dev/zero of=$1 count=1024000000000 bs=$2