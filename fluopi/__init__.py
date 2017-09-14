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
from math import pi

from scipy.optimize import curve_fit

# Define the image channels
channels=['R','G','B']

def plot_im_frame(f_path,frame):

    """
    To perform separated plots of each channel of image frame

    Parameters
    ----------
    f_path : string_like
        path directory where the images are stored
    frame : int
        frame number to plot

    """
    plt.figure()
    Im = plt.imread(f_path%frame)
    plt.imshow(Im)
    plt.title('frame '+str(frame)+' image')
    
def plt_im_frame_channels(f_path,frame):

    """
    To perform separated plots of each channel of an image frame

    Parameters
    ----------
    f_path : string_like
        folder name where the images are stored
    frame : int
        Frame number to plot

    """
    Im = plt.imread(f_path%frame)

    plt.figure(figsize=(15,3))
    plt.subplot(131)
    plt.imshow(Im[:,:,0])
    plt.colorbar()
    plt.title('Red channel')

    plt.subplot(132)
    plt.imshow(Im[:,:,1])
    plt.colorbar()
    plt.title('Green channel')

    plt.subplot(133)
    plt.imshow(Im[:,:,2])
    plt.colorbar()
    plt.title('Blue channel')


def count_files(path,file_type):
    """
    To count the number of files of a defined extension (filetype on a certain folder (path)

    Parameters
    ----------
    path : string
        folder name where the images are stored

    file_type : string
        extension of the files to count (e.g. tif, png, jpg)

    Returns
    -------
    ImageCount : int
        number of defined filetype files on the path folder

    """

    ImageCount = len(glob.glob1(path,"*."+file_type))
    print(path.split('\\')[-1]+' = '+str(ImageCount) + ' files')
    return(ImageCount)


def get_im_data(x_frames,image_count,f_name):
    """
    Load image data from a sequence of files

    Parameters
    ----------
    x_frames : int
        step frames (e.g 10 to use only ten to ten images)

    image_count : int
        total number of files on the folder (can be obtained with count_files function)

    f_name : string
        file name pattern including full path where images are stored, e.g. "/folder/image-%04d"

    Returns
    -------
    ImsR,ImsG,ImsB: array_like
        data per channel of each image (ImsR -> matrix size = (W,H,image_count/x_frames))

    """
    
    W,H,_ = plt.imread(f_name%1).shape      # Measure the image size based on the first image on the folder
    NT = int(image_count/x_frames)
    ImsR = np.zeros((W,H,NT))
    ImsG = np.zeros((W,H,NT))
    ImsB = np.zeros((W,H,NT))
    for i in range(0,NT):
        im = plt.imread(f_name%(i*x_frames))
        ImsR[:,:,i] = im[:,:,0]              # Last number code the channel: 0=red, 1=green, 2=blue
        ImsG[:,:,i] = im[:,:,1]
        ImsB[:,:,i] = im[:,:,2]
    return(ImsR,ImsG,ImsB)

# at call you can take only the channels you are interested in (e.g.):
# red,_,blue=get_im_data(xframes,imageCount)  ---> this only takes the red and blue channels


def time_vector(data, x_frames, dT):
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

    _,_,LT=data[channels[0]].shape     # Length of time vector
    T=np.zeros((LT))
    for i in range(0,LT):
        T[i]=(i)*x_frames*dT
    
    return(T)

def row_transect(data, row, x_frames, data_frame = -1):
    """
    Plot the value of a transect (row of pixels) in a frame and plot it

    Parameters
    ----------
    data : dictionary
        dictionary with the R G B data of all images, and his names on Data['Im']

    row : int
        row where you want to see the transect

    x_frames : int
        step frames used on the analysis (e.g 10 means you are using one every ten to ten images)
    
    data_frame: int
        frame number of the image of interest, default = last one

    """
    
    row=int(row)  #just in case a non integer number is given
    
    plt.figure(figsize=(15,3))
    plt.subplot(131)
    plt.plot(data[channels[0]][row,:,data_frame])
    plt.xlabel('pixels')
    plt.ylabel('value')
    plt.title('Red channel')

    plt.subplot(132)
    plt.plot(data[channels[1]][row,:,data_frame])
    plt.xlabel('pixels')
    plt.title('Green channel')

    plt.subplot(133)
    plt.plot(data[channels[2]][row,:,data_frame])
    plt.xlabel('pixels')
    plt.title('Blue channel')

    #plot selected line transect on the image
    if data_frame > 0:
        ImFrame = x_frames*(data_frame)   # The corresponding image on the path
    else:
        _,_,ST=data[channels[0]].shape
        ImFrame=(ST-1)*x_frames
        
    
    Im = plt.imread(data['Im']%(ImFrame))
    S1,S2,_=Im.shape
    plt.figure(figsize=(6,6))
    fig = plt.gcf()
    ax = fig.gca()
    ax.imshow(Im)
    rect = matplotlib.patches.Rectangle((0,row),S2,0,linewidth=1,edgecolor='r',facecolor='none')
    ax.add_patch(rect)
    
def bg_value(x1, x2, y1, y2, data, im_count):
    """
    compute the background mean value for each channel and frame based on a rectagle
    defined by the user. Plot the rectangle over the image and makes plots of each channel
    mean background value over time

    Parameters
    ----------
    x1,x2,x1,x2: int values
        rectangle area limits: (x1,y1) = left-up corner. (x2,y2) = rigth-bottom corner
    
    data : dictionary
        R G B images data to get the background, and his names on data['Im']
    
    im_count : int
        total number of files on the folder (can be obtained with count_files function)

    Returns
    -------
    bg: dictionary
        Background mean value of each channel for every time frame

    """

    X2R=x2-x1 #convert on steps because the rectangle patch definition
    Y2R=y2-y1

    #plot the defined area
    plt.figure(figsize=(8,8))
    fig = plt.gcf()
    ax = fig.gca()
    Im = plt.imread(data['Im']%(im_count-1))
    ax.imshow(Im)
    rect = matplotlib.patches.Rectangle((y1,x1),Y2R,X2R,linewidth=1,edgecolor='r',facecolor='none')
    ax.add_patch(rect)


    #get the mean background value at each time for each channel and plot it
    BG={}
    LColors=['r','g','b']    # each color will be for each line in the plot
    count=0
    
    plt.figure()
    for chan in channels:
        BG[chan]= data[chan][x1:x2,y1:y2,:].mean(axis=(0,1))
        plt.plot(BG[chan][:],LColors[count])
        count+=1

    plt.xlabel('Time step')
    plt.ylabel('Fluorescence intensity')

    return(BG)

def bg_subst(data, bg):
    """
    Substract the mean background value for each channel and frame obtained with BG_Val function.
    
    data: dictionary
        R G B images data
    bg : array
        ackground mean value of each channel for every time frame (can be obtained with BG_Val function)


    Returns
    -------
    Data: dictionary
        R G B images data with the background substracted

    """

    L=bg[channels[0]].shape[0]
    S1,S2,_=data[channels[0]].shape

    for c in channels:
        for i in range(0,L):
            BGM=np.ones((S1,S2))
            BGM= BGM*bg[c][i]         #create a matrix with bg to substract it to the frame

            Data=data[c][:,:,i]

            Data=Data-BGM         #perform the substraction

            Data[Data<0]=0        # values < 0 are not allowed --> transform it to 0

            data[c][:,:,i]=Data   #actualize Data


    return(data)

def data_sum_time(data):
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
    SData=data[channels[0]][:,:,:].sum(axis=(2))+data[channels[1]][:,:,:].sum(axis=(2))+data[channels[2]][:,:,:].sum(axis=(2))
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
    nsimsAll=np.zeros((data[channels[0]].shape[0],data[channels[0]].shape[1]))
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
        
        Maux=np.zeros((data[channels[0]].shape))
        for fr in range(data[c].shape[-1]):
            Maux[:,:,fr]=gaussian(data[c][:,:,fr], sigma) 
            
        simsT[c]=Maux
        # make plot of the sum over time of smoothed data per channel
    
        plt.subplot(pvect[count])
        plt.imshow(nsims[c])
        plt.colorbar()
        plt.title(c+' channel')
    
        count+=1
    
    return(nsims,nsimsAll,simsT)

def colonyBlob(data,thresh,ImName,filename='null'):
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
    
    filename: string
        filename with whom save the output image+blobs+ID

    Returns
    -------
    A: array (Nx3)
        Contains the (x,y) position and size of each blob for each of N colonies detected
        """

    A = skfeat.blob_log(data, min_sigma=1.0, max_sigma=10.0, num_sigma=100, threshold=thresh, overlap=0.8)

    plt.figure(figsize=(8,8))
    plt.imshow(data, cmap='gray')
    #plt.hold(True)
    plt.title('Sumarized Image')
    for i in range(len(A)):
        circle = plt.Circle((A[i,1], A[i,0]), 2*A[i,2], color='r', fill=False , lw=0.5)
        fig = plt.gcf()
        ax = fig.gca()
        ax.add_artist(circle)

    plt.figure(figsize=(8,8))
    plt.imshow(plt.imread(ImName))
    #plt.hold(True)
    plt.title('Over '+ ImName)
    for i in range(len(A)):
        # plot the circle area identified for each colony
        circle = plt.Circle((A[i,1], A[i,0]), 2*A[i,2], color='w', fill=False , lw=0.5)
        fig = plt.gcf()
        ax = fig.gca()
        ax.add_artist(circle)
        ax.axes.get_xaxis().set_visible(False)
        ax.axes.get_yaxis().set_visible(False)
        
        # attach the ID label to each colony
        plt.annotate(
        i,
        xy=(A[i,1], A[i,0]), xytext=(-2, 2),
        textcoords='offset points', ha='right', va='bottom',color='white')
    if filename != 'null':
        plt.savefig(str(filename) + ".pdf", transparent=True)

    return(A)

def obtain_rois(data,blobs):
    """
    Based on the information of each identified colony, create arrays to contain
    the regions of interest (ROI) around each one.
    
    
    Parameters
    ----------
    data: dictionary
        R G B image data per frame

    blobs: array like
        Array of colony positions and sizes given by skimage in colonyBlob()

    Returns
    -------
    all_rois:
        The ROI array image data for square region around colony position of side 2*(colony size)
        to call it: all_rois['channel_name'][blob_number][y,x,timepoint]
    
    all_rois_circle:
        The ROI array image data only within circle (radius = width/2), with the data outside the circle equal to zero.
        The size of the array is equal to square ROIS (all_rois) size.
        to call it: all_rois_circle['channel_name'][blob_number][y,x,timepoint]

    nc:
        Number of colonies analysed (length of returned arrays)
    """

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

####### this lines are to eliminate the out of image bounds error
            x1=round(x-r)
            x2=round(x+r+1)  #plus 1 because slice working
            y1=round(y-r)
            y2=round(y+r+1)  #plus 1 because slice working

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
# rois_circle makes the values outside the colony boundaries equals to zero


def rois_plt_Fdynam(rois,T,cv,filename='null'):
    """
    Plot the total fluorescence of each colony over time

    Parameters
    ----------
        rois: dictionary
            the ROI image array data (is better to use circular ROIS, obtained with obtain_rois() function)

        T: vector
            the vector of real time values

        cv: vector
            contain the ID of the of colonies analysed
        
        filename: string
            filename with whom save the output image with fluorescence dynamics
    """

    plt.figure(figsize=(17,3))
    pvect = [131,132,133]
    count=0
    for c in channels:
        plt.subplot(pvect[count])
        for i in cv:
            plt.plot(T,rois[c][i].sum(axis=(0,1)))   #sum the value
            #plt.hold(True)

        plt.xlabel('Time [h]')
        plt.ylabel('Fluorescence intensity')
        plt.title(c+' channel')
        count+=1
        
    if filename != 'null':
        #plt.savefig("FluorIntRGB.pdf", transparent=True)
        plt.savefig(str(filename) + ".pdf", transparent=True)

#plt.legend(['Colony %d'%i for i in range(len(A))])

def channelSum(RData,cv):
    """
    Compute the sum over the RGB channels for each image

    Parameters
    ----------
    RData: dictionary
            RGB time-lapse image data of each ROIS, from obtain_rois()
    
    cv: vector
            contain the ID of the of colonies analysed

    Returns:
    ----------
        ACrois: dictionary
            Sum of channels for each time step and ROI
    """
    ACrois = {}
    for i in cv:
            ACrois[i]=np.zeros((RData[channels[0]][i].shape))

    for c in channels:
        for i in cv:
            ACrois[i]+=RData[c][i][:,:,:]

    return(ACrois)


def TL_ROI(ROIs,idx,Times,fname,radius='null',ChanSum=False,gridsize=[0,0]):
    """
    Save images of selected time steps on "Times" vector, for a selected ROI (idx).
    This images can be used to make timelapse videos of isolated colonies.
    
    If you specify a gridsize of a proper size, then it display the ROI frames on the notebook

    Parameters
    ----------
    ROIs: dictionary
            RGB time-lapse image data of each ROIS, from obtain_rois()
    
    idx: intr
            contain the ID of the of the selected colony
    Times: vector
        conitains the selected frames times
    
    fname: string
        the complete filename to save the images of ROIs
        e.g. fname=('ROIs/Col'+str(idx)+'_ROI_step%d.png')
    
    ChanSum: boolean
        True to perfom the sum of the three channels of the ROI.
        False to show the image original colors.
    
    gridsize: vector
        size of the subplot grid. if gridsize=[0,0] the figure will not be shown on the notebook.

    Returns:
    ----------
    Save the images of the selected frames of a ROI.
    
    """
    
    if type(idx)==int:      #Check that ID is only one colony
        if len(Times)>0:        #Check time vector have some value
            
            w1=ROIs[channels[0]][idx].shape[0]      #cambiar todas las n y m por w y h
            h1=ROIs[channels[0]][idx].shape[1]
            
            if ChanSum == True:
                ROIa=channelSum(ROIs,[idx])  # sum the three channels 
                ROI=ROIa[idx][:,:,:]
                mx=np.max(ROI[:,:,:])
            else:  #Reconstruct an image file for each time
                ROI=np.zeros((w1,h1,3))
           
            
        # make the plot of each frame and save it
            for i in Times :
    
                plt.figure(figsize=(8,8))        
                                
                if ChanSum == True:   #Plot the ROI os sum with a colorbar
                    roi = ROI[:,:,i]
                    plt.imshow(roi, interpolation='none',vmin=0, vmax=mx)
                    plt.colorbar()
                    plt.xticks([])
                    plt.yticks([])
                    
                    if radius != 'null':
                        circle = plt.Circle((round((w1-1)/2), round((h1-1)/2)), 2*radius[i], color='r', fill=False , lw=2)
                        fig = plt.gcf()
                        ax = fig.gca()
                        ax.add_artist(circle)
                        #ax.axes.get_xaxis().set_visible(False)
                        #ax.axes.get_yaxis().set_visible(False)
                        
                else:                #Plot the ROI original image
                    ROI[:,:,0]=ROIs[channels[0]][idx][:,:,i]      #RED layer
                    ROI[:,:,1]=ROIs[channels[1]][idx][:,:,i]      #GREEN layer
                    ROI[:,:,2]=ROIs[channels[2]][idx][:,:,i]      #BlUE layer
                    roi=ROI.astype('uint8')
                    plt.imshow(roi)
                    plt.xticks([])
                    plt.yticks([])
                
                plt.savefig(fname%(i+1), transparent=True)
                plt.close()
            
            # display the plots in the notebook
            n=gridsize[0]
            m=gridsize[1]
            if n and m >0:              # make n or m equal to zero to not display the figure in the notebook.
                if (n*m)<(len(Times)):
                    print('the subplot grid is smaller than the number of plots. Increase x or y, and try again')
                else:
                    plt.figure(figsize=(4*m,4*n))
                    count=1
                    for i in Times :
                        plt.subplot(int(str(n)+str(m)+str(count)))
                        if ChanSum == True:
                            roi = ROI[:,:,i]
                            plt.imshow(roi, interpolation='none',vmin=0, vmax=mx)
                            plt.colorbar()
                        else:
                            plt.imshow(roi)
                        plt.title(str(i+1)+' Hours')
                        count+=1
        else:
            print('ERROR: Time vector have to be of lenght higher than zero')
    else:
        print('ERROR: use an integer value for the colony ID') 
        
        

def frame_colony_radius(rois,cv,thr, minS=0.5, maxS=10,numS=200):
    """
    Get the colony radius at each time step
    
    Parameters:
    ----------
        rois: dictionary
            ROI image data from obtain_rois()

        cv: vector
            contain the ID of the of colonies analysed

        thr: double
            Threshold for skfeat.blob_log 
        
        minS: double
            minimum value of sigma used on skfeat.blob_log
        
        maxS: double
            maximum value of sigma used on skfeat.blob_log
        
        numS: int
            number of sigma values used between minS and maxS on skfeat.blob_log

    Returns:
    ----------
        R: dictionary
            The time series of colony size, indexed by colony id number
    """
    R = {}
    nt= rois[cv[0]].shape[2]
    for k in cv:
        R[k] = np.zeros((nt,))
        for i in range(nt):
            troi = rois[k][:,:,i].astype(np.float32)
            if len(troi):
                ntroi = (troi-troi.min())/(troi.max()-troi.min())
                AA = skfeat.blob_log(ntroi, min_sigma=minS, max_sigma=maxS, num_sigma=numS, threshold=thr, overlap=0.8)
                #AA = skfeat.blob_log(ntroi, min_sigma=0.1, max_sigma=6.0, num_sigma=150, threshold=thr, overlap=0.8)
                if len(AA)>0:
                    R[k][i] = AA[0,2]
    return(R)

def logplot_radius(R,cv,t,filename='null'):
    """
    Plot the log of the square of the radious for each colony
    
    Parameters
    ----------
        R: dictionary
            colony radio at each time step of each colony at each time step (obtained with frame_colony_size() function) 
                
        cv: vector
            colonies ID vector to plot
        
        T: vector
            the vector of real time values
        filename: string
            filename to save the plot generated
    """
    for i in cv:
        r = R[i]
        plt.plot(t,np.log(r*r), '.')
        #plt.hold(True)
        plt.xlabel('Time [h]')
        plt.ylabel('log(Radius^2) [pixels]')
        plt.title('Colony radio')
     
    if filename != 'null':    
        #plt.savefig("Radio.pdf", transparent=True)
        plt.savefig(str(filename)+".pdf", transparent=True)

def plot_radius(R,cv,t,filename='null'):
    """
    Plot the radious for each colony at each time step
    
    Parameters
    ----------
        R: dictionary
            colony radio at each time step of each colony (obtained with frame_colony_size() function) 
        
        cv: vector
            colonies ID vector to plot
            
        t: vector
            the vector of real time values
            
        filename: string
            filename to save the plot generated
    """
    for i in cv:
        r = R[i]
        plt.plot(t,r, '.')
        #plt.hold(True)

        plt.xlabel('Time [h]')
        plt.ylabel('Radius [pixels]')
        plt.title('Colony radius')

     
    if filename != 'null':    
        #plt.savefig("Radio.pdf", transparent=True)
        plt.savefig(str(filename)+".pdf", transparent=True)

def checkR(rois,idx,t,Rfit='null',Rdots='null', filename='null'):
    """
    Plot the colony radius estimate overlayed on an kymograph image slice
    
    Parameters
    ----------
        Rfit: vector
            colony fited radius at each time step of the selected colony (obtained from a model) 
        Rdots:
            colony radius at each time step of the selected colony (obtained with frame_colony_size() function) 
        rois: dictionary
            ROI image of each colony (obtained with obtain_rois() function)
        
        idx: int
            id of the colony to check
            
        t: vector
            the vector of real time values
        
        filename: string
            filename to save the plot generated
    """
    plt.figure(figsize=(18,7))
    w,h,_ = rois[idx].shape
    #plt.imshow(rois[idx][round(w/2),:,:], interpolation='none', cmap='gray') # use the x-middle transect (--> w/2)
    plt.imshow(rois[idx][round((w-1)/2),:,:], interpolation='none') 
    plt.colorbar()
    if Rfit != 'null':
        plt.plot(t,-Rfit*2+(h-1)/2,'r-')
        plt.plot(t,Rfit*2+(h-1)/2,'r-')
    if Rdots != 'null':
        plt.plot(t,-Rdots*2+(h-1)/2,'rx',ms=9)
        plt.plot(t,Rdots*2+(h-1)/2,'rx',ms=9)             
    
    plt.xlabel('Time')
    plt.ylabel('y-axis position')
    plt.title('Colony '+str(idx))
    
    if filename != 'null':    
        #plt.savefig("KymoGraph.pdf", transparent=True) 
        plt.savefig(str(filename)+".pdf", transparent=True)

def Area(R,cv,T,filename='null'):
    """
    Compute and plot the colonies area over time as a perfect circle using the input radius value
    
    Parameters
    ----------
        R: dictionary
            colony radio at each time step of the selected colony (obtained with frame_colony_size() function) 
        
        cv: vector
            colonies ID vector to plot

            
        T: vector
            the vector of real time values
        
        filename: string
            filename to save the plot generated
    
    Return
    ----------
        A: dictionary
         colony area at each time step of the selected colony. call as: A[colonyID][time step]
    """
    plt.figure()
    A = {}
    for i in cv:
        r=R[i]
        A[i] = pi*r*r
        plt.plot(T,A[i],'.',label='colony '+str(i))  

    if filename != 'null':    
        #plt.savefig("KymoGraph.pdf", transparent=True) 
        plt.savefig(str(filename)+".pdf", transparent=True)
    
    return(A)
    
def F_sigma(t, a, b, c):
    """
    Compute the sigmoide function value using the given input values
    
    Parameters
    ----------
        t: vector
            independent variable ( "x axis", suposed to be time) 
        
        a: double
            maximum value parameter
        
        b: double
            function parameter
            
        c: double
            delay parameter
        
    Return
    ----------
    function evaluation
    
    """
    return((a /(1+np.exp(-(t+b)*c))))
    #return((a /(1+np.exp(-(t+b)*c)))+d)    

def Function_fit(xdata,ydata,init,end,cv,func=F_sigma,ParamBounds=([1,-np.inf,0.1],[np.inf,-1,1])):
    """
    Fit a given function to given data
    
    Parameters
    ----------
        xdata: vector
            independent variable ( "x axis", suposed to be time vector) 
        
        ydict: array like
            array of dependent variable vectors 
        
        init: double
            point on the time vector to init the fitting
            
        end: double
            point on the time vector to end the fitting
        
        cv: vector
            contain the ID of the colonies to analyse
        
    Return
    ----------
        Y_fit: dictionay
            contain the fitting result for each colony in the dictionary. Contains:
            
            Y_fit[col ID][evalF z]:
                
                evalF: vector
                    result vector of the fitted function:  evalF=FittedFunction(xdata)
                z: vector
                    fitted parameters
    
    """
    
    Y_fit={}
    for i in cv:
        z,_=curve_fit(func,xdata[init:end], ydata[i][init:end],bounds=ParamBounds)
        print(z)
        evalF=func(xdata,z[0],z[1],z[2])
        plt.plot(xdata, ydata[i], '.',xdata, evalF, '-')
        plt.title('Colony '+str(i))
        plt.show()
        Y_fit[i]=evalF,z
    return(Y_fit)



def CRoiMeanInt_frames(data,blobs,R,cv):
    """
    compute the mean intensity values for each time and channels for each CROI (circular ROI), redefining the ROIS based on Rdata values
    it takes the fit r value at each time (Rdata), with it defines a circular ROI, sum all the pixel values inside them and 
    divide this value  for the number of pixel considered. --> obtain the intensity mean value inside the colony limits on each time.
    
    Parameters
    ----------
        data: dictionary
             RGB dictionary with the ianges data
        
        blobs: array like
            contains the information of identified blobs
        
        R: dictionary
            contains the radio for each colony on each time step
        
        cv: vector
            contain the ID of the colonies to analyse
        
    Return
    ----------
        AllC_CRois_meanVal: dictionary
            contain the mean pixel value of each channel for each time step of each colony.
            call it as: AllC_CRois_meanVal['channel_name'][blob_number][timepoint]

    
    """
    AllC_CRois_meanVal = {}
    
    for char in channels:
        CRois_meanVal = {}
        
        for i in cv:
            #x and y are the colony center pixel stored on blobs
            x = blobs[i,0]
            y = blobs[i,1]
            CRoiInt=0
            count=0
            meanInt=np.zeros((len(R[i])))
            
            for j in range(len(R[i])): 
####### this lines is to eliminate the out of image bounds error
                r=R[i][j]
    
                x1=round(x-r)
                x2=round(x+r+1)
                y1=round(y-r)
                y2=round(y+r+1)

                if x1 <= 0:
                    x1 = 0
                if x2 >= data[char].shape[0]:
                    x2 = data[char].shape[0]
                if y1 <= 0:
                    y1 = 0
                if y2 >= data[char].shape[1]:
                    y2 = data[char].shape[1]

                SRoi = data[char][x1:x2,y1:y2,j]

#######            
                xr=int((SRoi.shape[0]+1)/2)
                yr=int((SRoi.shape[1]+1)/2)
                
                for n in range(SRoi.shape[0]):
                    for m in range(SRoi.shape[1]):
                        if ((n-xr)**2+(m-yr)**2) <= (r**2):
                            CRoiInt += SRoi[n,m]
                            count+=1
                if count != 0:
                    meanInt[j]=CRoiInt/count
            CRois_meanVal[i]=meanInt
        AllC_CRois_meanVal[char] = CRois_meanVal
    
    return(AllC_CRois_meanVal)

def F_mu (t,b,d):
    """
    compute the grwoth rate (mu) function value
    
    Parameters
    ----------
        t: int or vector
             independent variable values (suposed to be time vector)
        
        b: double
            functon parameter
        
        c: double
           function parameter
        
        
    Return
    ----------
        evaluated "mu" fucntion with the givven parameters

    
    """
    return((d /(np.exp(d*(t+b))+1)))


# End
