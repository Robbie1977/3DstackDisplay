import numpy as np
import os
import sys
import nrrd, png
from PIL import Image


def thumbnail(im, size=(25,25)):
    im = im.resize(size, Image.ANTIALIAS)
    return im

if (len(sys.argv) < 2):
    print 'Error: missing arguments!'
    print 'e.g. python images2MaxProjPNG_tn.py image1.nrrd imageN.nrrd ...'
else:
    for x in range(1,(len(sys.argv))):
        print 'creating tumbnail of image ', sys.argv[x]
        readdata, options = nrrd.read(str(sys.argv[x]))
        flat = np.transpose(np.max(domain,axis=2))
        tnfile = os.path.basename(sys.argv[x]).replace('.nrrd','_tn.png')
        thumbnail(png.from_array(flat,'L'), size=(120,60)).save(tnfile)
        del flat

print 'Done.'
