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

if (len(sys.argv) < 2):
  print 'Error: missing arguments!'
  print 'e.g. python images2MaxProjPNG_tn.py image1.nrrd imageN.nrrd ...'
else:
  for x in range(1,(len(sys.argv))):
    print 'creating tumbnail of image ', sys.argv[x]
    readdata, options = nrrd.read(str(sys.argv[x]))
    flat = np.transpose(np.max(readdata,axis=2))
    rfile = os.path.basename(sys.argv[x]).replace('.nrrd','.png')
    png.from_array(flat,'L').save(rfile)
    print np.shape(flat)
    if np.shape(flat)[0] < np.shape(flat)[1]:
      thumbnail(rfile, size=(120,60))
    else:
      thumbnail(rfile, size=(60,120))
    del flat

print 'Done.'
