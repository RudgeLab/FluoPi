# -*- coding: utf-8 -*-
"""
Created on Mon May 29 17:31:17 2017

@author: Prosimio
"""

import matplotlib
import matplotlib.pyplot as plt
import numpy as np
import glob

import skimage
from skimage import io, filters
from skimage.filters import gaussian
import skimage.feature as skfeat

#Define the image channels
channels=['R','G','B']

def plotImFrame(Fname,Frame):
  #inputs:
    # Fname = Filename where the images are stored
    # Frame = frame number to plot

    plt.figure()
    im1 = plt.imread(Fname%Frame)
    plt.imshow(im1)
    plt.title('frame '+str(Frame)+' image')
    
def pltImFrameChannels(Fname,Frame):

    """
    To perform separated plots of each channel of image frame

    Parameters
    ----------
    Fname : string_like
        folder name where the images are stored
    Frame : int
        Frame number to plot

    """
    im1 = plt.imread(Fname%Frame)

    plt.figure(figsize=(15,3))
    plt.subplot(131)
    plt.imshow(im1[:,:,0])
    plt.colorbar()
    plt.title('Red channel')

    plt.subplot(132)
    plt.imshow(im1[:,:,1])
    plt.colorbar()
    plt.title('Green channel')

    plt.subplot(133)
    plt.imshow(im1[:,:,2])
    plt.colorbar()
    plt.title('Blue channel')


def count_files(path,filetype):
    """
    To count the number of files of a defined extension (filetype on a certain folder (path)

    Parameters
    ----------
    path : string
        folder name where the images are stored

    filetype : string
        extension of the files to count (e.g. tif, png, jpg)

    Returns
    -------
    imageCount : int
        number of defined filetype files on the path folder

    """

    imageCount = len(glob.glob1(path,"*."+filetype))
    print(path.split('\\')[-1]+' = '+str(imageCount) + ' files')
    return(imageCount)


def get_im_data(xframes,imageCount,fname):
    """
    Load image data from a sequence of files

    Parameters
    ----------
    xframes : int
        step frames (e.g 10 to use only ten to ten images)

    imageCount : int
        total number of files on the folder (can be obtained with count_files function)

    fname : string
        file name pattern including full path where images are stored, e.g. "/folder/image-%04d"

    Returns
    -------
    imsR,imsG,imsB: array_like
        data per channel of each image (imsR -> matrix size = (w,h,imagecount/xframes))

    """
 #inputs:
  #xframes = step frames (e.g. 10 to use only ten to ten images)
  #imageCount = total number of files
  #fname = folder name

 #outputs:
   #imsR,imsG,imsB: data per channel of each image (imsR=matrix size (w,h,imagecount/xframes))

    w,h,_ = plt.imread(fname%1).shape      #measure the image size based on the first image on the folder
    nt = int(imageCount/xframes)
    imsR = np.zeros((w,h,nt))
    imsG = np.zeros((w,h,nt))
    imsB = np.zeros((w,h,nt))
    for i in range(0,nt):
        im = plt.imread(fname%(i*xframes))
        imsR[:,:,i] = im[:,:,0]              #last number code the channel: 0=red, 1=green, 2=blue
        imsG[:,:,i] = im[:,:,1]
        imsB[:,:,i] = im[:,:,2]
    return(imsR,imsG,imsB)

# when call you can take only the channels you are interested in (e.g.):
# red,_,blue=get_im_data(xframes,imageCount)  ---> this only takes the red and blue channels

# get the background time value and plot it

def Time_vector(data, xframes, dT):
    """
    Get the vector of times for the image sequence loaded

    Parameters
    ----------
    data : dictionary
        dictionary with the R G B data of all images

    xframes : int
        step frames used on the analysis (e.g 10 means you are using one every ten to ten images)
    
    dT : double
        time step of the frames in hour units. It can be obtained from the file used to perform the timelapse.
        
    Returns
    -------
    T: array_like
        Time vector for the used data (hour units)
    """

    _,_,st=data['R'].shape
    T=np.zeros((st))
    for i in range(0,st):
        T[i]=(i)*xframes*dT
    
    return(T)

def row_transect(Data, row, xframes, dataframe = -1):
    """
    Plot the value of a transect (row of pixels) in a frame and plot it

    Parameters
    ----------
    Data : dictionary
        dictionary with the R G B data of all images

    row : int
        row where you want to see the transect

    frame : int
        frame number of the image of interest, default = last one

    """
    #input:
    # row = the row where you want to see the transect  (integer)
    # frame = image frame to use  (integer)
    
    row=int(row)  #just in case a non integer number is given
    
    plt.figure(figsize=(15,3))
    plt.subplot(131)
    plt.plot(Data['R'][row,:,dataframe])
    plt.xlabel('pixels')
    plt.ylabel('value')
    plt.title('Red channel')

    plt.subplot(132)
    plt.plot(Data['G'][row,:,dataframe])
    plt.xlabel('pixels')
    plt.title('Green channel')

    plt.subplot(133)
    plt.plot(Data['B'][row,:,dataframe])
    plt.xlabel('pixels')
    plt.title('Blue channel')

    #plot selected line transect on the image (allways show it on the last frame)
    if dataframe > 0:
        imFrame = xframes*(dataframe)
    else:
        _,_,st=Data['R'].shape
        imFrame=(st-1)*xframes
        
    
    im = plt.imread(Data['Im']%(imFrame))
    s1,s2,_=im.shape
    plt.figure(figsize=(6,6))
    fig = plt.gcf()
    ax = fig.gca()
    ax.imshow(im)
    rect = matplotlib.patches.Rectangle((0,row),s2,0,linewidth=1,edgecolor='r',facecolor='none')
    ax.add_patch(rect)
    
def BG_Val(X1,X2,Y1,Y2,data, imCount):
    """
    compute the background mean value for each channel and frame based on a rectagle
    defined by the user. Plot the rectangle over the image and makes plots of each channel
    mean background value over time

    Parameters
    ----------
    X1,X2,Y1,Y2: int values
        rectangle area limits: (X1,Y1) = left-up corner. (X2,Y2) = rigth-bottom corner

    Y1,Y2 : int
        total number of files on the folder (can be obtained with count_files function)

    data : dictionary
        R G B images data to get the background

    Returns
    -------
    bg: dictionary
        Background mean value of each channel for every time frame

    """

    X2R=X2-X1 #convert on steps because the rectangle patch definition
    Y2R=Y2-Y1

    #plot the defined area
    plt.figure(figsize=(8,8))
    fig = plt.gcf()
    ax = fig.gca()
    im = plt.imread(data['Im']%(imCount-1))
    ax.imshow(im)
    rect = matplotlib.patches.Rectangle((Y1,X1),Y2R,X2R,linewidth=1,edgecolor='r',facecolor='none')
    ax.add_patch(rect)


    #get the mean background value at each time for each channel and plot it
    bg={}

    for chan in channels:
        bg[chan]= data[chan][X1:X2,Y1:Y2,:].mean(axis=(0,1))

    plt.figure()
    plt.plot(bg['R'][:],'r')
    #plt.hold(True)
    plt.plot(bg['G'][:],'g')
    plt.plot(bg['B'][:],'b')

    plt.xlabel('Time step')
    plt.ylabel('Fluorescence intensity')



    return(bg)

def BG_subst(Data,bg):
    """
    Substract the mean background value for each channel and frame obtained with BG_Val function.
    
    Data: dictionary
        R G B images data
    bg : array
        ackground mean value of each channel for every time frame (can be obtained with BG_Val function)


    Returns
    -------
    Data: dictionary
        R G B images data with the background substracted

    """

    l=bg['R'].shape[0]
    s1=Data['R'].shape[0]
    s2=Data['R'].shape[1]
    for c in channels:
        for i in range(0,l):
            bgm=np.ones((s1,s2))
            bgm= bgm*bg[c][i]         #create a matrix with bg to substract it to the frame

            data=Data[c][:,:,i]

            data=data-bgm         #perform the substraction

            data[data<0]=0        # values < 0 are not allowed --> transform it to 0

            Data[c][:,:,i]=data   #actualize Data


    return(Data)

def dataOT(Data):
    """
    Sum the data for each pixel over time

    Parameters
    ----------
    Data: dictionary
        R G B images data

    Returns
    -------
    SData: array like
        Sum data over time and over channels for each pixel of the Data

    """
    SData=Data['R'][:,:,:].sum(axis=(2))+Data['G'][:,:,:].sum(axis=(2))+Data['B'][:,:,:].sum(axis=(2))
    plt.imshow(SData)
    plt.colorbar()
    plt.title('All channels')

    return(SData)
    


def smoothDat(data,sigma):

    """
    Apply gaussian filter to smooth the each frame data

    Parameters
    ----------
    Data: dictionary
        4 dimensional (R,G,B, and Time) matrix with the data 
    sigma: double
        Filter parameter (standard deviation)

    Returns
    -------
    nsims: dictionary
        Sum over time of Smoothed data per channel (call it nsims[channel][r,c])

    nsimsAll: array_like
        Matrix with sum of nsims over the channels (call it nsimsAll[r,c])
    
    simsT: dictionary
        Smoothed data per channel per frame (call it as simsT[channel][r,c,f])

    """

    nsims={}
    nsimsAll=np.zeros((data['R'].shape[0],data['R'].shape[1]))
    simsT={}
    
    plt.figure(figsize=(17,3))
    pvect = [131,132,133]           #figure position vector
    count=0

    for c in channels:
        # apply filter
        data_sum = data[c].sum(axis=2)
        sims= gaussian(data_sum, sigma)
        nsims [c]= (sims-sims.min())/(sims.max()-sims.min())

        nsimsAll += nsims[c]
        
        Maux=np.zeros((data['R'].shape))
        for fr in range(data[c].shape[-1]):
            Maux[:,:,fr]=gaussian(data[c][:,:,fr], sigma) 
            
        simsT[c]=Maux
        # make plot
    
        plt.subplot(pvect[count])
        plt.imshow(nsims[c])
        plt.colorbar()
        plt.title(c+' channel')
    
        count+=1
    
    return(nsims,nsimsAll,simsT)

def colonyBlob(data,thresh,ImName):
    """
    Use skimage to identify the position of each colony and define the circular region
    used by each of them

    Parameters
    ----------
    data: array of single channel image data

    thresh:
        Pixel values > thresh are included in the analysis, range (0,1)
    ImName:
        Name of an image on which to overlay colony positions and sizes

    Returns
    -------
    A: array (Nx3)
        Contains the (x,y) position and size of each blob for each of N colonies detected
        """

    A = skfeat.blob_log(data, min_sigma=1.0, max_sigma=10.0, num_sigma=100, threshold=thresh, overlap=0.8)

    plt.figure(figsize=(8,8))
    plt.imshow(data, cmap='gray')
    plt.hold(True)
    plt.title('Sumarized Image')
    for i in range(len(A)):
        circle = plt.Circle((A[i,1], A[i,0]), 2*A[i,2], color='r', fill=False , lw=0.5)
        fig = plt.gcf()
        ax = fig.gca()
        ax.add_artist(circle)

    plt.figure(figsize=(8,8))
    plt.imshow(plt.imread(ImName))
    plt.hold(True)
    plt.title('Original Image')
    for i in range(len(A)):
        circle = plt.Circle((A[i,1], A[i,0]), 2*A[i,2], color='w', fill=False , lw=0.5)
        fig = plt.gcf()
        ax = fig.gca()
        ax.add_artist(circle)

    return(A)

def obtain_rois(data,blobs):
    """
    Use skimage to identify the position of each colony and define the circular region
    used by each of them

    Parameters
    ----------
    data: array of single channel image data

    blobs:
        Array of colony positions and sizes given by skimage in colonyBlob()


    Returns
    -------
    all_rois:
        The ROI array image data for square region around colony position of side 2*(colony size)

    all_rois_circle:
        The ROI array image data only within circle (radius = width/2)

    nc:
        Number of colonies analysed (size of returned arrays)
    """

 #inputs
    # data = matrix with sum in channels and time of the images
    # blobs = matrix with all the information of the obtainesd blobls (output from colonyBlob function)
 #return
    # all_rois = array with the information of the region of interest (square arund the colony)
    # all_rois_circle = array with the information inside the area of the colony (makes the values outside the colony equals to zero)
    # nc = number of colonies ( equals to the length of rois vector)

    all_rois = {}
    all_rois_circle = {}
    nc= len(blobs)

    for char in channels:
        rois = {}
        rois_circle = {}

        for i in range(nc):
            x = blobs[i,0]
            y = blobs[i,1]
            r = 2*blobs[i,2] #blobs[i,2] is the std deviation of the radious --> r=2*std implies 95% confidence

####### this lines is to eliminate the out of image bounds error
            x1=x-r
            x2=x+r
            y1=y-r
            y2=y+r

            if x1 <= 0:
                x1 = 0
            if x2 >= data[char].shape[0]:
                x2 = data[char].shape[0]
            if y1 <= 0:
                y1 = 0
            if y2 >= data[char].shape[1]:
                y2 = data[char].shape[1]

            rois[i] = data[char][x1:x2,y1:y2,:]
#######
            xr=int((rois[i].shape[0]+1)/2)
            yr=int((rois[i].shape[1]+1)/2)
            rois_circle[i]=np.zeros((rois[i].shape))
            for n in range(rois[i].shape[0]):
                for m in range(rois[i].shape[1]):
                    if ((n-xr)**2+(m-yr)**2) <= (r**2):
                        rois_circle[i][n,m,:] = rois[i][n,m,:]
        all_rois[char] = rois
        all_rois_circle[char] = rois_circle

    return(all_rois,all_rois_circle,nc)

# rois contains a square arund the colony
# roisC makes the values outside the colony equals to zero

# to call it:
# roisC['channel_name'][blob_number][y,x,timepoint]

def rois_plt_Fdynam(rois,T,nc):
    """
    Plot the total fluorescence of each colony over time

    Parameters:
        rois: the ROI image array data

        T: the vector of real time values

        nc: the number of colonies
    """

    plt.figure(figsize=(17,3))
    pvect = [131,132,133]
    count=0
    for c in channels:
        plt.subplot(pvect[count])
        for i in range(nc):
            plt.plot(T,rois[c][i].sum(axis=(0,1)))   #sum the value
            plt.hold(True)

        plt.xlabel('Time [hrs]')
        plt.ylabel('Fluorescence intensity')
        plt.title(c+' channel')
        count+=1

#plt.legend(['Colony %d'%i for i in range(len(A))])

def channelSum(RData,nc):
    """
    Compute the sum over the RGB channels for each image

    Parameters:
        RData: RGB time-lapse image data of each ROIS, from obtain_rois()

    Returns:
        ACrois: dictionary
            Sum of channels for each time step
    """
    ACrois = {}
    for i in range(nc):
            ACrois[i]=np.zeros((RData['R'][i].shape))

    for c in channels:
        for i in range(nc):
            ACrois[i]+=RData[c][i][:,:,:]

    return(ACrois)

def frame_colony_size(rois,nc,thr):
    """
    Get the colony size at each time step
    
    Parameters:
        rois: ROI image data from obtain_rois()

        nc: Number of colonies

        thr: Threshold for skfeat.blob_log 

    Returns:
        R: dictionary
            The time series of colony size, indexed by colony id number
    """
    R = {}
    nt= rois[0].shape[2]
    for k in range(nc):
        R[k] = np.zeros((nt,))
        for i in range(nt):
            troi = rois[k][:,:,i].astype(np.float32)
            if len(troi):
                ntroi = (troi-troi.min())/(troi.max()-troi.min())
                AA = skfeat.blob_log(ntroi, min_sigma=1.0, max_sigma=10.0, num_sigma=200, threshold=thr, overlap=0.8)
                if len(AA)>0:
                    R[k][i] = AA[0,2]
    return(R)

def plot_growth(R,t):
    """
    Plot the colony size data returned by frame_colony_size
    """
    for i in range(len(R)):
        r = R[i]
        plt.plot(t,np.log(r*r), '.')
        plt.hold(True)
        plt.xlabel('Time [hrs]')
        plt.ylabel('log(Radius^2) [pixels]')
        plt.title('Colony size')


def checkR(R,rois,idx,t):
    """
    Plot the colony radius estimate overlayed on an kymograph image slice
    """
    plt.figure(figsize=(16,12))
    w,h,_ = rois[idx].shape
    plt.imshow(rois[idx][w/2+1,:,:], interpolation='none', cmap='gray') # use the x-middle transect (--> w/2+1)
    plt.colorbar()
    plt.hold(True)
    plt.plot(t,-R[idx]*2+h/2+1,'r')
    plt.plot(t,R[idx]*2+h/2+1,'r')
    plt.xlabel('Time')
    plt.ylabel('y-axis position')

# End
