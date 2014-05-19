import numpy as np
import os
import sys
import nrrd, png
from PIL import Image


def thumbnail(file, size=(25,25)):
    im = Image.open(file)
    im = im.resize(size, Image.ANTIALIAS)
    tnFile = file.replace('.png','_tn.png')
    im.save(tnFile,"PNG")
    return True

if (len(sys.argv) < 4):
    print 'Error: missing arguments!'
    print 'e.g. python Index2MaxProjPNG.py template DomainPrefix indexfile1.nrrd indexfileN.nrrd ...'
else:
    print 'Loading template...'
    data1, header1 = nrrd.read(str(sys.argv[1]))
    template=np.array((np.max(data1,axis=2)*0.5),dtype=np.uint8)
    del data1, header1
    print 'Adding to domains', str(sys.argv[2]), '....'
    for x in range(3,(len(sys.argv))):
        print 'adding data from file', sys.argv[x]
        readdata, options = nrrd.read(str(sys.argv[x]))
        for i in np.unique(readdata[readdata>0]):
            if np.uint8(i) in readdata:
                print 'appending index', str(i)
                domfile = str(sys.argv[2]) + str(i).zfill(4) + '.png'
                domain = np.zeros(readdata.shape,dtype=np.uint8)
                domain[readdata==i]=np.uint8(255)
                png1=np.max((np.transpose((np.max(domain,axis=2))), template.T),axis=0)
                png.from_array(png1,'L').save(domfile)
                thumbnail(domfile, size=(120,60))
                del domain, png1


print 'Done.'
