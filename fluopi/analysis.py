
import matplotlib
import matplotlib.pyplot as plt
import numpy as np
import glob

from skimage.filters import gaussian
import skimage.feature as skfeat
from math import pi

from scipy.optimize import curve_fit

# Define the image channels
CHANNELS = ['R','G','B']


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
# red,_,blue=get_im_data(xframes,imagecount)  ---> this only takes the red and blue channels


def time_vector(data, x_frames, dt):
    """
    Get the vector of times for the image sequence loaded

    Parameters
    ----------
    data : dictionary
        dictionary with the R G B data of all images

    xframes : int
        step frames used on the analysis (e.g 10 means you are using one every ten to ten images)
    
    dt : double
        time step of the frames in hour units. It can be obtained from the file used to perform the timelapse.
        
    Returns
    -------
    T: array_like
        Time vector for the used data (hour units)
    """

    _,_,LT = data[CHANNELS[0]].shape     # Length of time vector
    T = np.zeros((LT))
    for i in range(0,LT):
        T[i] = (i)*x_frames*dt
    
    return(T)


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

    X2R = x2-x1 #convert on steps because the rectangle patch definition
    Y2R = y2-y1

    #plot the defined area
    plt.figure(figsize=(8,8))
    fig = plt.gcf()
    ax = fig.gca()
    Im = plt.imread(data['Im']%(im_count-1))
    ax.imshow(Im)
    rect = matplotlib.patches.Rectangle((y1,x1), Y2R, X2R, linewidth=1, edgecolor='r', facecolor='none')
    ax.add_patch(rect)


    #get the mean background value at each time for each channel and plot it
    BG = {}
    LColors = ['r','g','b']    # each color will be for each line in the plot
    count = 0
    
    plt.figure()
    for chan in CHANNELS:
        BG[chan] = data[chan][x1:x2,y1:y2,:].mean(axis=(0,1))
        plt.plot(BG[chan][:],LColors[count])
        count += 1

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

    L = bg[CHANNELS[0]].shape[0]
    S1,S2,_ = data[CHANNELS[0]].shape

    for c in CHANNELS:
        for i in range(0,L):
            BGM = np.ones((S1,S2))
            BGM =  BGM*bg[c][i]         #create a matrix with bg to substract it to the frame

            Data = data[c][:,:,i]

            Data = Data-BGM         #perform the substraction

            Data[Data<0] = 0        # values < 0 are not allowed --> transform it to 0

            data[c][:,:,i] = Data   #actualize Data


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
    SData = data[CHANNELS[0]][:,:,:].sum(axis=(2))+data[CHANNELS[1]][:,:,:].sum(axis=(2))+data[CHANNELS[2]][:,:,:].sum(axis=(2))
    plt.imshow(SData)
    plt.colorbar()
    plt.title('All channels')

    return(SData)
    
def smooth_data(data,sigma):

    """
    Apply gaussian filter to smooth each frame data

    Parameters
    ----------
    data: dictionary
        4 dimensional (R,G,B, and Time) matrix with the data 
    sigma: double
        Filter parameter (standard deviation)

    Returns
    -------
    NSIms: dictionary
        Sum over time of Smoothed data per channel (call it nsims[channel][r,c])

    NSImsAll: array_like
        Matrix with sum of nsims over the channels (call it nsimsAll[r,c])
    
    SImsT: dictionary
        Smoothed data per channel per frame (call it as simsT[channel][r,c,f])

    """

    NSIms = {}
    NSIms_All = np.zeros((data[CHANNELS[0]].shape[0],
                          data[CHANNELS[0]].shape[1]))
    SImsT = {}
    
    plt.figure(figsize=(17,3))
    POS_VECT = [131,132,133]           # figure position vector
    count = 0

    for c in CHANNELS:
        # apply filter
        Data_Sum = data[c].sum(axis=2)
        SIms = gaussian(Data_Sum, sigma)
        NSIms [c] = (SIms-SIms.min())/(SIms.max()-SIms.min())

        NSIms_All += NSIms[c]
        
        Maux = np.zeros((data[CHANNELS[0]].shape))
        for fr in range(data[c].shape[-1]):
            Maux[:,:,fr] = gaussian(data[c][:,:,fr], sigma) 
            
        SImsT[c] = Maux
        # make plot of the sum over time of smoothed data per channel
    
        plt.subplot(POS_VECT[count])
        plt.imshow(NSIms[c])
        plt.colorbar()
        plt.title(c+' channel')
    
        count += 1
    
    return(NSIms,NSIms_All,SImsT)


def colony_blobs_id(data, thresh, im_name, filename='null'):
    """
    Use skimage to identify the position of each colony and define the circular region
    used by each of them

    Parameters
    ----------
    data: array of single channel image data

    thresh:
        Pixel values > thresh are included in the analysis, range (0,1)
        
    im_name:
        Name of an image on which to overlay colony positions and sizes
    
    filename: string
        filename with whom save the output image+blobs+ID

    Returns
    -------
    A: array (Nx3)
        Contains the (x,y) position and size of each blob for each of N colonies detected
    """

    A = skfeat.blob_log(data, min_sigma=1.0, max_sigma=10.0, num_sigma=100, 
                        threshold=thresh, overlap=0.8)

    plt.figure(figsize=(8,8))
    plt.imshow(data, cmap='gray')
    #plt.hold(True)
    plt.title('Sumarized Image')
    for i in range(len(A)):
        circle = plt.Circle((A[i,1], A[i,0]), 2*A[i,2], color='r', fill=False , 
                            lw=0.5)
        fig = plt.gcf()
        ax = fig.gca()
        ax.add_artist(circle)

    plt.figure(figsize=(8,8))
    plt.imshow(plt.imread(im_name))
    #plt.hold(True)
    plt.title('Over '+ im_name)
    for i in range(len(A)):
        # plot the circle area identified for each colony
        circle = plt.Circle((A[i,1], A[i,0]), 2*A[i,2], color='w', fill=False , lw=0.5)
        fig = plt.gcf()
        ax = fig.gca()
        ax.add_artist(circle)
        ax.axes.get_xaxis().set_visible(False)
        ax.axes.get_yaxis().set_visible(False)
        
        # attach the ID label to each colony
        plt.annotate(i, xy=(A[i,1], A[i,0]), xytext=(-2, 2),
                     textcoords='offset points', ha='right', va='bottom',
                     color='white')
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
    nc = len(blobs)

    for char in CHANNELS:
        rois = {}
        rois_circle = {}

        for i in range(nc):
            x = blobs[i,0]
            y = blobs[i,1]
            r = 2*blobs[i,2] # blobs[i,2] is the std deviation of the radius 
                             #  --> r=2*std implies 95% confidence

####### this lines are to eliminate the out of image bounds error
            x1 = round(x-r)
            x2 = round(x+r+1)  #plus 1 because slice working
            y1 = round(y-r)
            y2 = round(y+r+1)  #plus 1 because slice working

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
            xr = int((rois[i].shape[0]+1)/2)
            yr = int((rois[i].shape[1]+1)/2)
            rois_circle[i] = np.zeros((rois[i].shape))
            for n in range(rois[i].shape[0]):
                for m in range(rois[i].shape[1]):
                    if ((n-xr)**2+(m-yr)**2) <= (r**2):
                        rois_circle[i][n,m,:] = rois[i][n,m,:]
        all_rois[char] = rois
        all_rois_circle[char] = rois_circle

    return(all_rois,all_rois_circle,nc)

# rois contains a square arund the colony
# rois_circle makes the values outside the colony boundaries equals to zero


def channels_sum(rois_data, cv):
    """
    Compute the sum over the RGB channels for each image

    Parameters
    ----------
    rois_data: dictionary
            RGB time-lapse image data of each ROIS, from obtain_rois()
    
    cv: vector
            contain the ID of the of colonies analysed

    Returns:
    ----------
        sum_chan_rois: dictionary
            Sum of channels for each time step and ROI
    """
    sum_chan_rois = {}
    for i in cv:
            sum_chan_rois[i] = np.zeros((rois_data[CHANNELS[0]][i].shape))

    for c in CHANNELS:
        for i in cv:
            sum_chan_rois[i] += rois_data[c][i][:,:,:]

    return(sum_chan_rois)


def frame_colony_radius(rois, cv, thr, min_sig=0.5, max_sig=10, num_sig=200):
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
        
        min_sig: double
            minimum value of sigma used on skfeat.blob_log
        
        max_sig: double
            maximum value of sigma used on skfeat.blob_log
        
        num_sig: int
            number of sigma values used between min_sig and max_sig on skfeat.blob_log

    Returns:
    ----------
        R: dictionary
            The time series of colony size, indexed by colony id number
    """
    R = {}
    nt = rois[cv[0]].shape[2]
    for k in cv:
        R[k] = np.zeros((nt,))
        for i in range(nt):
            troi = rois[k][:,:,i].astype(np.float32)
            if len(troi):
                nt_roi = (troi-troi.min())/(troi.max()-troi.min())
                AA = skfeat.blob_log(nt_roi, min_sigma=min_sig, 
                                     max_sigma=max_sig, num_sigma=num_sig, 
                                     threshold=thr, overlap=0.8)
                #AA = skfeat.blob_log(nt_roi, min_sigma=0.1, max_sigma=6.0, num_sigma=150, threshold=thr, overlap=0.8)
                if len(AA)>0:
                    R[k][i] = AA[0,2]
    return(R)


def area(r, cv, T, filename='null'):
    """
    Compute and plot the colonies area over time as a perfect circle (using 
    the input radius value) around the colony position value 
    
    Parameters
    ----------
        r: dictionary
            colony radius at each time step of the selected colony (obtained with frame_colony_size() function) 
        
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
        R = r[i]
        A[i] = pi*R*R
        plt.plot(T,A[i],'.',label='colony '+str(i))  

    if filename != 'null':    
        #plt.savefig("KymoGraph.pdf", transparent=True) 
        plt.savefig(str(filename)+".pdf", transparent=True)
    
    return(A)

def f_sigma(t, a, b, c):
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


def function_fit(xdata, ydata, init, end, cv, func=f_sigma, 
                 param_bounds=([1,-np.inf,0.1],[np.inf,-1,1])):
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
        
        func: function
            function to be fitted
        
        param_bounds: array of vectors
            lower and upper bounds of each parameters
            para_bounds=([lower bounds],[upper bounds])
        
    Return
    ----------
        Y_fit: dictionay
            contain the fitting result for each colony in the dictionary. 
            It is:
            
            Y_fit[col ID][evalF z]:
                
                evalF: vector
                    result vector of the fitted function:  
                    evalF=func(xdata, optimal_parameters)
                    
                z: vector
                    fitted parameters
    
    """
    
    Y_fit = {}
    for i in cv:
        z,_ = curve_fit(func, xdata[init:end], ydata[i][init:end], 
                        bounds=param_bounds)
        print(z)
        evalF = func(xdata,z[0],z[1],z[2])
        plt.plot(xdata, ydata[i], '.',xdata, evalF, '-')
        plt.title('Colony '+str(i))
        plt.show()
        Y_fit[i] = evalF,z
    return(Y_fit)


def croi_mean_int_frames(data, blobs, radii, cv):
    """
    compute the mean intensity values for each time and channels for each CROI 
    (circular ROI), redefining the ROIS based on radii values 
    It takes the fit radius value at each time (radii), with it defines a 
    circular ROI, sum all the pixel values inside them and divide this value  
    for the number of pixel considered. --> obtain the intensity mean value 
    inside the colony limits on each time.
    
    Parameters
    ----------
        data: dictionary
             RGB dictionary with the images data
        
        blobs: array like
            contains the information of identified blobs
        
        radii: dictionary
            contains the radius for each colony on each time step
        
        cv: vector
            contain the ID of the colonies to analyse
        
    Return
    ----------
        AllC_CRois_mean_val: dictionary
            contain the mean pixel value of each channel for each time step of each colony.
            call it as: AllC_CRois_mean_val['channel_name'][blob_number][timepoint]

    
    """
    AllC_CRois_mean_val = {}
    
    for char in CHANNELS:
        CRois_mean_val = {}
        
        for i in cv:
            #x and y are the colony center pixel stored on blobs
            x = blobs[i,0]
            y = blobs[i,1]
            CRoi_int = 0
            count = 0
            meanInt = np.zeros((len(radii[i])))
            
            for j in range(len(radii[i])): 
####### this lines is to eliminate the out of image bounds error
                r = radii[i][j]
    
                x1 = round(x-r)
                x2 = round(x+r+1)
                y1 = round(y-r)
                y2 = round(y+r+1)

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
                xr = int((SRoi.shape[0]+1)/2)
                yr = int((SRoi.shape[1]+1)/2)
                
                for n in range(SRoi.shape[0]):
                    for m in range(SRoi.shape[1]):
                        if ((n-xr)**2+(m-yr)**2) <= (r**2):
                            CRoi_int += SRoi[n,m]
                            count += 1
                if count != 0:
                    meanInt[j] = CRoi_int/count
            CRois_mean_val[i] = meanInt
        AllC_CRois_mean_val[char] = CRois_mean_val
    
    return(AllC_CRois_mean_val)

def f_mu (t, b, d):
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
        evaluated "mu" fucntion with the given parameters

    
    """
    return((d /(np.exp(d*(t+b))+1)))


# End

