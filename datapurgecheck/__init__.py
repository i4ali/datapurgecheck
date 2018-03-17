
"""

A utility that scans the coban video path directory to determine the *uploaded* and *not-uploaded* files, tracks both
for deletion(purge). Also, provides functionality to fill up disk space to
trigger purging activity when the specified threshold is exceeded. The result is a list of status'es of each file in
coban video path of *uploaded/not-uploaded* and *deletion* as shown in table below

+-----------------------+-------------------------+----------------------+
| File                  | Uploaded/Not-uploaded   | Deleted/Not-deleted  |
+=======================+============+============+======================+
| 2@20180212133324-1.mp4| uploaded                | deleted              |
+-----------------------+-------------------------+----------------------+
| 2@20180212133324-1.ok | uploaded                | deleted              |
+-----------------------+-------------------------+----------------------+
| 2@20180212150925.c    | not-uploaded            | not-deleted          |
+-----------------------+-------------------------+----------------------+

Validation of purging functionality can be done using the above output which is made available
in a csv file

"""