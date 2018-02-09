import os

oneGB = 1024*1024 # 1GB
counter = 1
with open('large_file', 'wb') as fout:
    while (counter < 1024):
        fout.write(os.urandom(oneGB)) 
        counter = counter+1  