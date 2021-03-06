import numpy as np
import sys
import nrrd
import gc

colourL=np.array([[0,0,255],[255,0,0],[0,255,0],[255,26,185],[255,211,0],[0,132,246],[0,141,70],[167,97,62],[79,0,106],[0,255,246],[62,123,141],[237,167,255],[211,255,149],[185,79,255],[229,26,88],[132,132,0],[0,255,149],[97,0,44],[246,132,18],[202,255,0],[44,62,0],[0,53,193],[255,202,132],[0,44,97],[158,114,141],[79,185,18],[158,193,255],[149,158,123],[255,123,176],[158,9,0],[255,185,185],[132,97,202],[158,0,114],[132,220,167],[255,0,246],[0,211,255],[255,114,88],[88,62,53],[0,62,53],[220,97,220],[97,114,176],[185,202,44],[18,176,167],[97,18,0],[44,0,44],[88,0,202],[149,193,202],[211,158,35],[132,176,88],[229,237,185],[246,211,255],[185,79,97],[141,9,167],[106,79,0],[0,62,158],[123,62,123],[62,123,97],[167,255,97],[0,149,211],[62,114,0],[176,88,0],[220,0,123],[158,158,255],[79,70,97],[167,255,246],[229,0,44],[114,220,114],[255,237,123],[176,141,70],[97,114,255],[220,70,0],[0,0,114],[9,0,70],[53,237,79],[44,0,0],[167,0,255],[0,246,193],[158,0,44],[0,62,255],[246,158,123],[106,114,53],[255,255,70],[193,176,176],[114,114,114],[193,106,167],[0,88,35],[255,132,141],[176,132,114],[0,70,97],[141,255,18],[176,141,202],[114,79,246],[114,158,0],[211,9,193],[158,0,79],[193,123,255],[141,149,185],[246,167,211],[35,35,9],[255,106,202],[0,141,18],[255,167,88],[229,193,158],[0,18,44],[193,185,88],[0,193,123],[70,44,0],[123,62,88],[158,70,167],[79,88,62],[106,53,185],[114,176,149],[255,176,0],[79,53,132],[185,70,53],[97,167,255],[211,132,149],[123,97,62],[106,0,79],[237,88,255],[149,211,0],[53,167,193],[0,0,158],[123,53,53],[220,255,106],[149,211,79],[132,255,176],[132,53,0],[79,220,229],[70,35,53],[0,44,9],[185,220,193],[88,141,79],[158,114,0],[202,70,132],[0,193,70],[202,9,237],[202,220,255],[0,88,167],[44,167,123],[141,220,255],[35,44,53],[193,255,185],[0,106,158],[0,88,255],[246,88,132],[220,123,70],[202,53,167],[167,202,141],[79,220,193],[97,114,211],[106,35,255],[141,9,202],[220,193,44],[193,185,123],[62,35,88],[123,97,149],[185,123,220],[255,220,211],[237,88,97],[202,185,255],[62,88,88],[114,149,149],[123,255,123],[149,53,106],[202,158,185],[114,62,26],[149,9,141],[246,141,220],[97,176,62],[255,202,97],[211,123,114],[255,237,158],[202,246,255],[88,193,255],[141,97,237],[97,185,114],[141,97,97],[70,70,123],[0,88,211],[88,220,9],[0,26,114],[211,62,44],[149,149,70],[202,123,0],[79,106,141],[149,132,255],[70,35,141],[0,132,132],[246,114,53],[158,220,132],[202,220,106],[176,79,220],[79,9,18],[255,26,123],[123,176,211],[26,0,26],[141,53,246],[88,0,167],[237,141,255]],np.uint8)

if (len(sys.argv) < 3):
    print 'Error: I need at least one image to work with!'
    print 'e.g. python CreateRGBstack.py outputImages.nrrd firstImage.nrrd [NthImage.nrrd ....]'
else:

    print 'Creating RGB stacks:', str(sys.argv[1]).replace('.nrrd','_R|G|B.nrrd')
    print 'Loading image:', str(sys.argv[2])

    refFile = str(sys.argv[1]).replace('.nrrd','_Key.rtf')
    refSS = '{\\rtf1\\ansi\\deff0 \n{\\colortbl;'
    refSE = '}'
    refFE = '\n}'

    readdata, options = nrrd.read(str(sys.argv[2]))

    im1 = readdata

    Ishape=im1.shape

    Tsize=im1.size

    mi=np.max(im1)

    if (mi > 255):
        mi=np.divide(mi,255.0)
        im1=np.uint8(np.floor(np.divide(im1,mi)))

    print 'Calculating final image volume..'

    imN = np.zeros(Ishape,np.uint16)

    print 'Creating transverse plane slices..'
    imT=np.array(np.reshape(np.repeat(im1,3),[Ishape[0],Ishape[1],Ishape[2],3]),np.uint16)
    Tshape=imT.shape
    print 'Colouring transverse plane and adding to final image..'
    imN=np.multiply(imT,np.reshape(np.tile((colourL[0]/255.0),Tsize),Tshape))

    imT=None

    refFN = '\n\\cf1 \n' + str(sys.argv[2]) + '\\line'
    refSS = refSS + '\\red' + str(colourL[0][0]) + '\\green' + str(colourL[0][1]) +'\\blue' + str(colourL[0][2]) + ';'
    gc.collect()

    print 'Finalising colour merge..'
    imN[imN>255]=np.uint16(255)

    for i in range(3,len(sys.argv)):
        print 'Adding data from ', str(sys.argv[i])
        readdata, options = nrrd.read(str(sys.argv[i]))
        im1 = readdata
        mi=np.max(im1)
        if (mi > 180):
            mi=np.divide(mi,180.0)
            im1=np.uint8(np.floor(np.divide(im1,mi)))
        if (Tsize <> im1.size):
            print '\n\nError: Images must be the same size!'
            print 'Skipping: ', str(sys.argv[i])
        else:

            print 'Creating transverse plane slices..'
            imT=np.array(np.reshape(np.repeat(im1,3),[Ishape[0],Ishape[1],Ishape[2],3]),np.uint16)
            print 'Colouring transverse plane and adding to final image..'
            imN=np.add(np.uint16(np.multiply(imT,np.reshape(np.tile((colourL[(i-2)]/255.0),Tsize),Tshape))),imN)
            imT=None
            refFN = refFN + '\n\\cf' + str((i-1)) + ' \n' + str(sys.argv[i]) + '\\line'
            refSS = refSS + '\\red' + str(colourL[(i-2)][0]) + '\\green' + str(colourL[(i-2)][1]) +'\\blue' + str(colourL[(i-2)][2]) + ';'
            gc.collect()

#            print 'Finalising colour merge..'
#            imN[imN>255]=np.uint16(255)
#            gc.collect()

    print 'converting to 8-bit..'
    imN[imN>255] = np.uint16(255)
    mi=np.divide(np.max(imN),255.0)
    imN=np.uint8(np.floor(np.divide(imN,mi)))
    gc.collect()


    print 'saving NRRD copy as R,G & B images:'
    print 'Saving red image..'
    nrrd.write(str(sys.argv[1]).replace('.nrrd','_R.nrrd'),imN[:,:,:,0])
    print 'Saving green image..'
    nrrd.write(str(sys.argv[1]).replace('.nrrd','_G.nrrd'),imN[:,:,:,1])
    print 'Saving blue image..'
    nrrd.write(str(sys.argv[1]).replace('.nrrd','_B.nrrd'),imN[:,:,:,2])



    print 'Saving colour key data to...'
    print refFile
    with open(refFile, "w") as text_file:
        text_file.write("%s%s%s%s" % (refSS, refSE, refFN, refFE))


print 'Done.'
