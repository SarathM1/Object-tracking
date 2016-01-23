import os,re

def deleteFiles():
    for f in os.listdir('./'):
        if re.search('Detected.*', f):
            os.remove(f)
