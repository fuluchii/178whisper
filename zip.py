#encoding:utf-8
import re
import os
import os.path
import zipfile
import sys

folder = sys.argv[1]
url = folder
root_z = url+"zip"
print "%s %s" % (url,root_z)
os.mkdir(root_z)
for root,dirs,files in os.walk(url):
    print root
    for d in dirs:
        with zipfile.ZipFile(os.path.join(root_z,d+".zip"),'w') as z:
            for r,ds,fs in os.walk(os.path.join(root,d)):
                for f in fs:
                    print os.path.join(root,d,f)
                    z.write(os.path.join(root,d,f),f,zipfile.ZIP_STORED)
        print d+" zipde."           
print "ziped."