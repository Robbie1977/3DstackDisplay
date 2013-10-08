import numpy as np
import os
import sys
import nrrd

if (len(sys.argv) < 5):
    print 'Error: missing arguments!' 
    print 'e.g. python GrowIndex.py template.nrrd indexfile.nrrd EXP newindex.nrrd unindexed.nrrd'
    print 'EXP = voxel expantion radius (int) e.g. 3'
else:
    print 'Loading images...' 
    #for x in range(2,(len(sys.argv))):
    #print 'adding data from file', sys.argv[x]
    readdata, options = nrrd.read(str(sys.argv[1]))
    readdata1, options1 = nrrd.read(str(sys.argv[2]))
    exp = int(sys.argv[3])
    bg = readdata
    ind = np.copy(readdata1)
    
    ind[ind==23]=0 #remove Cerebrum
    ind[ind==22]=0 #remove NG tract
    ind[ind==21]=0 #remove NG tract
    ind[ind>5]=0 #remove All but Neuromeres
    
    i = int(exp)
    tmpind = np.copy(ind)
    unlab = readdata
    unlab[readdata1>0]=np.uint8(0)
    print 'expanding to radius of', str(i)
    itindx=np.where(unlab>0)
    for j in range(len(itindx[0])-1,-1,-1):
        x=itindx[0][j]
        y=itindx[1][j]
        z=itindx[2][j]
        if x-i >= 0:
            x1=x-i
        else:
            x1=0
        if y-i >= 0:
            y1=y-i
        else:
            y1=0     
        if z-i >= 0:
            z1=z-i
        else:
            z1=0
        if x+i < np.size(unlab,0):
            x2=x+i
        else:
            x2=np.size(unlab,0)
        if y+i < np.size(unlab,1):
            y2=y+i
        else:
            y2=np.size(unlab,1)
        if z+i < np.size(unlab,2):
            z2=z+i
        else:
            z2=np.size(unlab,2)
        if np.sum(tmpind[x1:x2,y1:y2,z1:z2])>0:    
            ind[x,y,z]=np.uint8(np.argmax(np.histogram(tmpind[x1:x2,y1:y2,z1:z2], bins=range(0,255))[0][1:])+1)
            print 'updating point', str(j), '(', str(x), ',', str(y), ',', str(z), ') to index', str(ind[x,y,z])
        
    print 'Saving results...'
    nrrd.write(str(sys.argv[4]), np.uint8(ind))
    ind[readdata1>0]=0
    ind=np.add(ind,readdata1)
    
    unlab = readdata
    unlab[ind>0]=np.uint8(0)
    nrrd.write(str(sys.argv[5]), np.uint8(unlab))
    
    
print 'Done.'