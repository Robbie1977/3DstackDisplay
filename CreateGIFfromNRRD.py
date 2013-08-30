import numpy as np
import sys
import nrrd

colourL=[[0,0,255],[255,0,0],[0,255,0],[255,26,185],[255,211,0],[0,132,246],[0,141,70],[167,97,62],[79,0,106],[0,255,246],[62,123,141],[237,167,255],[211,255,149],[185,79,255],[229,26,88],[132,132,0],[0,255,149],[97,0,44],[246,132,18],[202,255,0],[44,62,0],[0,53,193],[255,202,132],[0,44,97],[158,114,141],[79,185,18],[158,193,255],[149,158,123],[255,123,176],[158,9,0],[255,185,185],[132,97,202],[158,0,114],[132,220,167],[255,0,246],[0,211,255],[255,114,88],[88,62,53],[0,62,53],[220,97,220],[97,114,176],[185,202,44],[18,176,167],[97,18,0],[44,0,44],[88,0,202],[149,193,202],[211,158,35],[132,176,88],[229,237,185],[246,211,255],[185,79,97],[141,9,167],[106,79,0],[0,62,158],[123,62,123],[62,123,97],[167,255,97],[0,149,211],[62,114,0],[176,88,0],[220,0,123],[158,158,255],[79,70,97],[167,255,246],[229,0,44],[114,220,114],[255,237,123],[176,141,70],[97,114,255],[220,70,0],[0,0,114],[9,0,70],[53,237,79],[44,0,0],[167,0,255],[0,246,193],[158,0,44],[0,62,255],[246,158,123],[106,114,53],[255,255,70],[193,176,176],[114,114,114],[193,106,167],[0,88,35],[255,132,141],[176,132,114],[0,70,97],[141,255,18],[176,141,202],[114,79,246],[114,158,0],[211,9,193],[158,0,79],[193,123,255],[141,149,185],[246,167,211],[35,35,9],[255,106,202],[0,141,18],[255,167,88],[229,193,158],[0,18,44],[193,185,88],[0,193,123],[70,44,0],[123,62,88],[158,70,167],[79,88,62],[106,53,185],[114,176,149],[255,176,0],[79,53,132],[185,70,53],[97,167,255],[211,132,149],[123,97,62],[106,0,79],[237,88,255],[149,211,0],[53,167,193],[0,0,158],[123,53,53],[220,255,106],[149,211,79],[132,255,176],[132,53,0],[79,220,229],[70,35,53],[0,44,9],[185,220,193],[88,141,79],[158,114,0],[202,70,132],[0,193,70],[202,9,237],[202,220,255],[0,88,167],[44,167,123],[141,220,255],[35,44,53],[193,255,185],[0,106,158],[0,88,255],[246,88,132],[220,123,70],[202,53,167],[167,202,141],[79,220,193],[97,114,211],[106,35,255],[141,9,202],[220,193,44],[193,185,123],[62,35,88],[123,97,149],[185,123,220],[255,220,211],[237,88,97],[202,185,255],[62,88,88],[114,149,149],[123,255,123],[149,53,106],[202,158,185],[114,62,26],[149,9,141],[246,141,220],[97,176,62],[255,202,97],[211,123,114],[255,237,158],[202,246,255],[88,193,255],[141,97,237],[97,185,114],[141,97,97],[70,70,123],[0,88,211],[88,220,9],[0,26,114],[211,62,44],[149,149,70],[202,123,0],[79,106,141],[149,132,255],[70,35,141],[0,132,132],[246,114,53],[158,220,132],[202,220,106],[176,79,220],[79,9,18],[255,26,123],[123,176,211],[26,0,26],[141,53,246],[88,0,167],[237,141,255]]

if (len(sys.argv) < 2):
    print 'Error: I need at least one image to work with!'
    print 'e.g. python CreateGIFfromNRRD.py firstImage.nrrd [NthImage.nrrd ....]'
else:

    print 'Creating animated GIF...'
    print 'Loading image:', str(sys.argv[1])
    
    readdata, options = nrrd.read(str(sys.argv[1]))
    
    im1 = readdata
    
    Tsize=im1.size
    
    print 'Calculating final image volume..'
    
    imN = np.zeros([im1.shape[0]+im1.shape[2],im1.shape[1]+im1.shape[2],im1.shape[1],3],np.uint8)
    
    print 'Calculating coronal plane area..'
    imC=imN[im1.shape[2]:,0:im1.shape[2],:,:]
    print 'Calculating sagittal plane area..'
    imS=imN[0:im1.shape[2],im1.shape[2]:,:,:]
    print 'Calculating transverse plane area..'
    imT=imN[im1.shape[2]:,im1.shape[2]:,:,:]
    print 'Creating coronal plane slices..'
    imC=np.array(np.reshape(np.repeat(np.transpose(im1,(0,2,1)),3),imC.shape))
    print 'Creating transverse plane slices..'
    imT=np.array(np.repeat(np.reshape(np.repeat(im1[:,:,::-1],3),[imT.shape[0],imT.shape[1],im1.shape[2],imT.shape[3]]),np.int(np.floor(float(im1.shape[1])/float(im1.shape[2]))),2))
    print 'Creating sagittal plane slices..'
    imS=np.array(np.repeat(np.reshape(np.repeat(np.transpose(im1,(2,1,0)),3),[imS.shape[0],imS.shape[1],im1.shape[0],imS.shape[3]]),np.int(np.floor(float(im1.shape[1])/float(im1.shape[0]))),2))
    
    #multiply intensity with channel colour levels and add to existing signals
    print 'Colouring coronal plane and adding to final image..'
    imN[im1.shape[2]:,0:im1.shape[2],:,:]=np.add(np.uint8(np.multiply((imC/255.0),np.reshape(np.tile(colourL[0],imC.size/3),imC.shape))),imN[im1.shape[2]:,0:im1.shape[2],:,:])
    print 'Colouring sagittal plane and adding to final image..'
    imN[0:im1.shape[2],im1.shape[2]:,:imS.shape[2],:]=np.add(np.uint8(np.multiply((imS/255.0),np.reshape(np.tile(colourL[0],imS.size/3),imS.shape))),imN[0:im1.shape[2],im1.shape[2]:,:imS.shape[2],:])
    print 'Colouring transverse plane and adding to final image..'
    imN[im1.shape[2]:,im1.shape[2]:,:imT.shape[2],:]=np.add(np.uint8(np.multiply((imT/255.0),np.reshape(np.tile(colourL[0],imT.size/3),imT.shape))),imN[im1.shape[2]:,im1.shape[2]:,:imT.shape[2],:])
    print 'Finalising colour merge..'
    imN[imN>255]=np.uint8(255)
    print 'Saving image..'
    nrrd.write('test.nrrd',imN[:,:,:,2])
    
#    readdata, options = nrrd.read(str(sys.argv[1])) 
#    im1 = readdata
#      
#    if (Tsize <> im1.size):
#        print '\n\nError: Images must be the same size!!'
#    else:
#    
#       
#        
#        r=np.zeros([255,253])
#        for j in range(1,255):
#            print 'Checking index %s...'% str(j)
#            i = np.where(im1 == j)
#            d=np.zeros(np.size(i[0],0))
#            for c in range(0, np.size(i[0],0)):
#                d[c] = im2[i[0][c]][i[1][c]][i[2][c]] 
#            r[j]=np.histogram(d, bins=range(0,255))[0][1:]
#        
#        st1='['  
#        st2='['  
#        dv = '' 
#        for c in range(1,255):
#            if (r[c].argmax() > 1):
#                print '%s -> %s' % (str(c), str((r[c].argmax())+1))
#                st1 = st1 + dv + str(c)
#                st2 = st2 + dv + str((r[c].argmax())+1)
#                dv= ','
#            else:
#                print '%s -> %s' % (str(c), str(r[c].argmax()))
#                
#        st1 = st1 + ']'
#        st2 = st2 + ']'
#        
#        print st1
#        print st2
#
#    
#        #print 'The alignment has a RMS Diff value of:', r1, ' (0=perfect)'
#        #
#        #print 'Outputing results to ', str(sys.argv[3])
#        #
#        #with open(str(sys.argv[3]), "a") as myfile: 
#        #    myfile.write(str(r1) + ', RMS Diff, ' + str(sys.argv[1]) + ', ' + str(sys.argv[2]) + '\n')
#        
#        print 'Done.'
        
  

