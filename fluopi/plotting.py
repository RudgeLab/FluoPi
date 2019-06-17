
import matplotlib
import matplotlib.pyplot as plt
import numpy as np

# Define the image channels
CHANNELS = ['R','G','B']

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


def row_transect(data, row, data_frame=-1, show_im = True):
    """
    Plot the value of a transect (row of pixels) in a frame and plot it

    Parameters
    ----------
    data : dictionary or numpy array
        dictionary with the R G B data of all images
        bi dimentional numpy array.

    row : int
        row where you want to see the transect

    data_frame: int
        frame number of the image of interest, default = last one
    
    show_im: boolean
        if True, the image frame is ploted

    """  
    row = int(row)  #just in case a non integer number is given
     
    if type(data) == dict:
                            
        plt.figure(figsize=(15,3))
        plt.subplot(131)
        plt.plot(data[CHANNELS[0]][row,:,data_frame])
        plt.xlabel('pixels')
        plt.ylabel('value')
        plt.title('Red channel')

        plt.subplot(132)
        plt.plot(data[CHANNELS[1]][row,:,data_frame])
        plt.xlabel('pixels')
        plt.title('Green channel')

        plt.subplot(133)
        plt.plot(data[CHANNELS[2]][row,:,data_frame])
        plt.xlabel('pixels')
        plt.title('Blue channel')

        
        if show_im == True:
        #Rebuild the image
        
            n,m,l = data[CHANNELS[0]].shape
            image = np.zeros((n,m,len(CHANNELS)))
            for i in range(len(CHANNELS)):
                image[:,:,i] = data[CHANNELS[i]][:,:,data_frame]
                
            image = image.astype('uint8')   #change the data type to show the image properly

            #plot selected line transect on the image        

            plt.figure(figsize=(6,6))
            fig = plt.gcf()
            ax = fig.gca()
            ax.imshow(image)
            rect = matplotlib.patches.Rectangle((0,row), m, 0, linewidth=1, edgecolor='r', facecolor='none')
            ax.add_patch(rect)
            
    if type(data) == np.ndarray:
        
        plt.figure()
        plt.plot(data[row,:])
        plt.xlabel('pixels')
        plt.ylabel('value')
        plt.title('Fused Channels')



        if show_im == True:

            #image = data.astype('uint8')   #change the data type to show the image properly
            #plot selected line transect on the image        

            plt.figure(figsize=(6,6))
            
            plt.title('All channels')
            #fig.colorbar()
            fig = plt.gcf()
            ax = fig.gca()
            im = ax.imshow(data,cmap='viridis')
            fig.colorbar(im, fraction =0.035)
            #ax.colorbar()
            rect = matplotlib.patches.Rectangle((0,row), data.shape[1], 0, linewidth=1, edgecolor='r', facecolor='none')
            ax.add_patch(rect)

def im_zoom(x_lims, y_lims, imagen):
    """
    Make a zoom of a region of interest in an image

    Parameters
    ----------
        xlims: list
            x-axis limits of the zoomed section. 
            e.g. [x_min, x_max]

        ylims: list
            y-axis limits of the zoomed section. 
            e.g. [y_min, y_max]

        imagen: numpy array
            the imagen array to be display

    """
    
    X2R = x_lims[1]-x_lims[0] #convert on steps because the rectangle patch definition
    Y2R = y_lims[1]-y_lims[0]
    
    plt.figure(figsize=(15,5))
    
    plt.subplot(121)
    plt.imshow(imagen)
    fig = plt.gcf()
    ax = fig.gca()
    rect = matplotlib.patches.Rectangle((y_lims[0],x_lims[0]), Y2R, X2R, linewidth=1, edgecolor='r', facecolor='none')
    ax.add_patch(rect)
    
    plt.subplot(122)
    plt.imshow(imagen[x_lims[0]:x_lims[1],y_lims[0]:y_lims[1]])
    plt.colorbar()

    
def rois_plt_fluo_dynam(rois, time_v, cv, filename='null'):
    """
    Plot the total fluorescence of each colony over time

    Parameters
    ----------
        rois: dictionary
            the ROI image array data (is better to use circular ROIS, obtained with obtain_rois() function)

        time_v: vector
            the vector of real time values

        cv: vector
            contain the ID of the of colonies analysed
        
        filename: string
            filename with whom save the output image with fluorescence dynamics
    """

    plt.figure(figsize=(17,3))
    POS_VECT = [131,132,133]
    count = 0
    for c in CHANNELS:
        plt.subplot(POS_VECT[count])
        for i in cv:
            plt.plot(time_v,rois[c][i].sum(axis=(0,1)))   #sum the value
            #plt.hold(True)

        plt.xlabel('Time [h]')
        plt.ylabel('Fluorescence intensity')
        plt.title(c+' channel')
        count += 1
        
    if filename != 'null':
        #plt.savefig("FluorIntRGB.pdf", transparent=True)
        plt.savefig(str(filename) + ".pdf", transparent=True)

#plt.legend(['Colony %d'%i for i in range(len(A))])


def tl_roi(rois, times, idx, frames, fname = 'null', radius='null', chan_sum=False, 
           same_bar = True, gridsize=[0,0]):
    """
    Save images of selected time steps on "times" vector, for a selected ROI (idx).
    This images can be used to make timelapse videos of isolated colonies.
    
    If you specify a gridsize of a proper size, then it display the ROI frames on the notebook

    Parameters
    ----------
    rois: dictionary
            RGB time-lapse image data of each rois, from obtain_rois()
    
    times: vector
        contain the experimental time vector
    
    idx: intr
            contain the ID of the of the selected colony
         
    frames: vector
        conitains the selected time frames
    
    fname: string
        the complete filename to save the images of ROIs
        e.g. fname=('rois/Col'+str(idx)+'_ROI_step%d.png')
    
    chan_sum: boolean
        True to perfom the sum of the three channels of the ROI.
        False to show the image original colors.
    
    gridsize: vector
        size of the subplot grid. if gridsize=[0,0] the figure will not be shown on the notebook.

    Returns
    -------
    Save the images of the selected frames of a ROI.
    
    """
    from fluopi.analysis import channels_sum
    
    if type(idx) == int:      #Check that ID is only one colony
        if len(frames)>0:        #Check time vector have some value
            
            w1 = rois[CHANNELS[0]][idx].shape[0]
            h1 = rois[CHANNELS[0]][idx].shape[1]
            
            if chan_sum == True:
                ROIa = channels_sum(rois,[idx])  # sum the three channels 
                ROI = ROIa[idx][:,:,:]
                mx = np.max(ROI[:,:,:])
            else:  
                #Reconstruct an image file for each time
                ROI = np.zeros((w1,h1,3))
           
            
        # make the plot of each frame and save it
            roi = {}
            for i in frames:
    
                plt.figure(figsize=(8,8))        
                                
                if chan_sum == True:   #Plot the ROI os sum with a colorbar
                    roi = ROI[:,:,i]
                    if same_bar == True:
                        plt.imshow(roi, interpolation='none',vmin=0, vmax=mx)
                    else:
                        plt.imshow(roi)
                    plt.colorbar()
                    plt.xticks([])
                    plt.yticks([])
                    
                        
                else:                #Plot the ROI original image
                    ROI[:,:,0] = rois[CHANNELS[0]][idx][:,:,i]      #RED layer
                    ROI[:,:,1] = rois[CHANNELS[1]][idx][:,:,i]      #GREEN layer
                    ROI[:,:,2] = rois[CHANNELS[2]][idx][:,:,i]      #BlUE layer
                    roi[i] = ROI.astype('uint8')
                    plt.imshow(roi[i])
                    plt.xticks([])
                    plt.yticks([])
                
                if radius != 'null':
                    
                    circle = plt.Circle((round((w1-1)/2), round((h1-1)/2)), radius[i], color='r', fill=False , lw=2)
                    fig = plt.gcf()
                    ax = fig.gca()
                    ax.add_artist(circle)
                    #ax.axes.get_xaxis().set_visible(False)
                    #ax.axes.get_yaxis().set_visible(False)
                
                if fname != 'null':
                    plt.savefig(fname%(times[i]), transparent=True)
                
                plt.close()
            
            # display the plots in the notebook
            n = gridsize[0]
            m = gridsize[1]
            if n and m >0:              # make n or m equal to zero to not display the figure in the notebook.
                if (n*m)<(len(frames)):
                    print('the subplot grid is smaller than the number of plots. Increase x or y, and try again')
                else:
                    plt.figure(figsize=(4*m,4*n))
                    count = 1
                    for i in frames :
                        plt.subplot(n, m, count)

                        if chan_sum == True:
                            roi = ROI[:,:,i]
                            if same_bar == True:
                                plt.imshow(roi, interpolation='none',vmin=0, vmax=mx)
                            else:
                                plt.imshow(roi)
                            plt.colorbar()
                        
                        else:
                            
                            plt.imshow(roi[i])
                            
                        if radius != 'null':
                    
                            circle = plt.Circle((round((w1-1)/2), round((h1-1)/2)), radius[i], color='r', fill=False , lw=2)
                            fig = plt.gcf()
                            ax = fig.gca()
                            ax.add_artist(circle)
                        
                        plt.title(str(times[i])+' Hours')
                        count += 1
        else:
            print('ERROR: Time vector have to be of lenght higher than zero')
    else:
        print('ERROR: use an integer value for the colony ID') 
        

def logplot_radius(r, cv, t, filename='null'):
    """
    Plot the log of the square of the radius for each colony
    
    Parameters
    ----------
        r: dictionary
            colony radius at each time step of each colony at each time step (obtained with frame_colony_size() function) 
                
        cv: vector
            colonies ID vector to plot
        
        T: vector
            the vector of real time values
        filename: string
            filename to save the plot generated
    """
    for i in cv:
        R = r[i]
        plt.plot(t, np.log(R*R), '.')
        #plt.hold(True)
        plt.xlabel('Time [h]')
        plt.ylabel('log(Radius^2) [pixels]')
        plt.title('Colony radius')
     
    if filename != 'null':    
        #plt.savefig("Radius.pdf", transparent=True)
        plt.savefig(str(filename)+".pdf", transparent=True)

def plot_radius(r, cv, t, col_label=True, filename='null'):
    """
    Plot the radius for each colony at each time step
    
    Parameters
    ----------
        r: dictionary
            colony radius at each time step of each colony (obtained with frame_colony_size() function) 
        
        cv: vector
            colonies ID vector to plot
            
        t: vector
            the vector of real time values
        
        col_label: boolen
            to define if include or not the colony labels in the plot
            
        filename: string
            filename to save the plot generated
    """
    for i in cv:
        R = r[i]
        
        if col_label == True:
            plt.plot(t,R, '.',label='colony '+str(i))
            plt.legend(loc='best')
        else:
            plt.plot(t,R, '.')
            
        plt.xlabel('Time [h]')
        plt.ylabel('Radius [pixels]')
        plt.title('Colony radius')     
     
    if filename != 'null':    
        #plt.savefig("Radius.pdf", transparent=True)
        plt.savefig(str(filename)+".pdf", transparent=True)


def ROI_radius(rois, idx, frame= -1, r='null', filename='null', transect = False, plt_circle = False):
    """
    Plot the colony radius estimate overlayed on an kymograph image slice
    
    Parameters
    ----------      
        r:
            colony radius at each time step of the selected colony 
            (obtained with frame_colony_radius() function) 
        
        rois: dictionary
            ROI image of each colony (obtained with obtain_rois() function)
        
        idx: int
            id of the colony to check
            
        frame: int
            the frame to see
        
        filename: string
            filename to save the plot generated
            
        transect: boolean
            To indicate of include or not the middle transect line
            
        plt_circle: boolean
            To indicate of include or not the circle line
    """
    rw,cl,_ = rois[idx].shape
    
    plt.figure()
    fig = plt.gcf()
    ax = fig.gca()
    ax.imshow(rois[idx][:,:,frame], interpolation='none', cmap='gray')
    
    if transect == True:
        rect = matplotlib.patches.Rectangle((0,int((rw-1)/2)), cl, 0, linewidth=1, edgecolor='r', facecolor='none')
        ax.add_patch(rect)
        
    if plt_circle == True:
        circle = plt.Circle((int((cl-1)/2), int((rw-1)/2)), r[idx][frame], color='w', fill=False , lw=0.5)
        ax.add_artist(circle)
    
    if filename != 'null':    
        plt.savefig(str(filename)+".pdf", transparent=True)


def check_radius(rois, idx, t, r_fit='null', r_dots='null', filename='null', transect = False):
    """
    Plot the colony radius estimate overlayed on an kymograph image slice
    
    Parameters
    ----------
        r_fit: vector
            colony fited radius at each time step of the selected colony 
            (obtained from a model) 
        
        r_dots:
            colony radius at each time step of the selected colony 
            (obtained with frame_colony_radius() function) 
        
        rois: dictionary
            ROI image of each colony (obtained with obtain_rois() function)
        
        idx: int
            id of the colony to check
            
        t: vector
            the vector of real time values
        
        filename: string
            filename to save the plot generated
            
        transect: boolean
            To indicate of include or not the middle transect line
    """
    plt.figure(figsize=(18,7))
    fig = plt.gcf()
    ax = fig.gca()
    
    w,h,_ = rois[idx].shape
    
    # use the x-middle transect (--> (w-1)/2)
    im = ax.imshow(rois[idx][int(round((w-1)/2)),:,:], interpolation='none')#,cmap='gray') 
    fig.colorbar(im, fraction =0.03)

    if transect == True:
        rect2 = matplotlib.patches.Rectangle((0,int((h-1)/2)), len(t)-1, 0, linewidth=1, edgecolor='r', facecolor='none')
        ax.add_patch(rect2)
    
    if r_fit != 'null':

        plt.plot(-r_fit+(h-1)/2, 'r-')
        plt.plot(r_fit+(h-1)/2, 'r-')
    
    if r_dots != 'null':

        plt.plot(-r_dots+(h-1)/2, 'rx', ms=9)
        plt.plot(r_dots+(h-1)/2, 'rx', ms=9)             
    
    step = int(len(t)*0.1)
    plt.xticks(range(0,len(t),step),t[0:-1:step].astype(int))
    plt.xlabel('Time')
    plt.ylabel('y-axis position')
    plt.title('Colony '+str(idx))
    
    if filename != 'null':    
        #plt.savefig("KymoGraph.pdf", transparent=True) 
        plt.savefig(str(filename)+".pdf", transparent=True)
        
def rois_last_frame_2chan_plt(rois_data, channel_x, channel_y, serie_name):
    """
    Sum all the pixel values for channel_x and channel_y (e.g.channel G and 
    channel R) separately for the last frame of each ROI and make a plot where 
    channel_x sum value is on the X axis and channel_y sum value is on the Y 
    axis.
    Each dot correspond to one ROI values and represent the ratio of the two
    channels for that colony.    
    
    Parameters
    ----------
        rois_data : dictionary
            RGB time-lapse image data of each ROI, obtained with obtain_rois()
        
        channel_x: string
            channel name (e.g. 'G') to be on the x axis
        
        channel_y: string
            channel name (e.g. 'R') to be on the y axis

        serie_name: string
            name of the the data serie in analysis (used as title of the plot)
    """
      
    # variable inicialization
    chanx = np.zeros((len(rois_data[channel_x]),1))
    chany = np.zeros((len(rois_data[channel_x]),1))
    
    # perform the sum of selected channels for the last frame of each ROI
    for i in range(len(rois_data[channel_x])):
        chanx[i] = rois_data[channel_x][i][:,:,-1].sum(axis=(0,1))
        chany[i] = rois_data[channel_y][i][:,:,-1].sum(axis=(0,1))
    
    # size the plot dimentions
    axisMax = np.max([np.max(chanx), np.max(chany)])
    axisMin = np.min([np.min(chanx), np.min(chany)])
    #print(axisMax,axisMin)
    
    #plt.figure(figsize=(8,8))
    plt.plot(chanx,chany,'bo')
    plt.title(serie_name)
    plt.xlabel(channel_x+' Channel')
    plt.ylabel(channel_y+' Channel')
    plt.axis([axisMin, axisMax, axisMin, axisMax])
    return(chanx,chany)

def plt_lin_fit(x_min, x_max, l_fit, color):
    """
    Make a plot of an already linear fit, being posible to define the function
    evaluation limits (x independient variable limits) and the color of the 
    dots and fitted line.
    
    Parameters
    ----------
        x_min : int
            RGB time-lapse image data of each ROI, obtained with obtain_rois()
        
        x_max: int
            channel name (e.g. 'G') to be on the x axis
        
        l_fit: vector
            linear fitted parameters. Obtained with linear_fit function

        color: char
            char of the color to be used on the dots and line (e.g. 'r')
    """ 
    p = np.poly1d(l_fit)
    xp = np.linspace(x_min, x_max, 2)
    plt.plot(xp, p(xp), color +'-')
# End

