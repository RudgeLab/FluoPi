
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


def row_transect(data, row, x_frames, data_frame=-1):
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
    
    row = int(row)  #just in case a non integer number is given
    
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

    #plot selected line transect on the image
    if data_frame > 0:
        ImFrame = x_frames*(data_frame)   # The corresponding image on the path
    else:
        _,_,ST = data[CHANNELS[0]].shape
        ImFrame = (ST-1)*x_frames
        
    
    Im = plt.imread(data['Im']%(ImFrame))
    S1,S2,_ = Im.shape
    plt.figure(figsize=(6,6))
    fig = plt.gcf()
    ax = fig.gca()
    ax.imshow(Im)
    rect = matplotlib.patches.Rectangle((0,row), S2, 0, linewidth=1, edgecolor='r', facecolor='none')
    ax.add_patch(rect)
    
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


def tl_roi(rois, idx, times, fname, radius='null', chan_sum=False, 
           gridsize=[0,0]):
    """
    Save images of selected time steps on "times" vector, for a selected ROI (idx).
    This images can be used to make timelapse videos of isolated colonies.
    
    If you specify a gridsize of a proper size, then it display the ROI frames on the notebook

    Parameters
    ----------
    rois: dictionary
            RGB time-lapse image data of each rois, from obtain_rois()
    
    idx: intr
            contain the ID of the of the selected colony
    times: vector
        conitains the selected frames times
    
    fname: string
        the complete filename to save the images of ROIs
        e.g. fname=('rois/Col'+str(idx)+'_ROI_step%d.png')
    
    chan_sum: boolean
        True to perfom the sum of the three channels of the ROI.
        False to show the image original colors.
    
    gridsize: vector
        size of the subplot grid. if gridsize=[0,0] the figure will not be shown on the notebook.

    Returns:
    ----------
    Save the images of the selected frames of a ROI.
    
    """
    
    if type(idx) == int:      #Check that ID is only one colony
        if len(times)>0:        #Check time vector have some value
            
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
            for i in times :
    
                plt.figure(figsize=(8,8))        
                                
                if chan_sum == True:   #Plot the ROI os sum with a colorbar
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
                    ROI[:,:,0] = rois[CHANNELS[0]][idx][:,:,i]      #RED layer
                    ROI[:,:,1] = rois[CHANNELS[1]][idx][:,:,i]      #GREEN layer
                    ROI[:,:,2] = rois[CHANNELS[2]][idx][:,:,i]      #BlUE layer
                    roi = ROI.astype('uint8')
                    plt.imshow(roi)
                    plt.xticks([])
                    plt.yticks([])
                
                plt.savefig(fname%(i+1), transparent=True)
                plt.close()
            
            # display the plots in the notebook
            n = gridsize[0]
            m = gridsize[1]
            if n and m >0:              # make n or m equal to zero to not display the figure in the notebook.
                if (n*m)<(len(times)):
                    print('the subplot grid is smaller than the number of plots. Increase x or y, and try again')
                else:
                    plt.figure(figsize=(4*m,4*n))
                    count = 1
                    for i in times :
                        plt.subplot(int(str(n)+str(m)+str(count)))
                        if chan_sum == True:
                            roi = ROI[:,:,i]
                            plt.imshow(roi, interpolation='none',vmin=0, vmax=mx)
                            plt.colorbar()
                        else:
                            plt.imshow(roi)
                        plt.title(str(i+1)+' Hours')
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

def plot_radius(r, cv, t, filename='null'):
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
            
        filename: string
            filename to save the plot generated
    """
    for i in cv:
        R = r[i]
        plt.plot(t,R, '.')
        #plt.hold(True)

        plt.xlabel('Time [h]')
        plt.ylabel('Radius [pixels]')
        plt.title('Colony radius')

     
    if filename != 'null':    
        #plt.savefig("Radius.pdf", transparent=True)
        plt.savefig(str(filename)+".pdf", transparent=True)


def check_radius(rois, idx, t, r_fit='null', r_dots='null', filename='null'):
    """
    Plot the colony radius estimate overlayed on an kymograph image slice
    
    Parameters
    ----------
        r_fit: vector
            colony fited radius at each time step of the selected colony 
            (obtained from a model) 
        
        r_dots:
            colony radius at each time step of the selected colony 
            (obtained with frame_colony_size() function) 
        
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
    # use the x-middle transect (--> (w-1)/2)
    plt.imshow(rois[idx][round((w-1)/2),:,:], interpolation='none')
    # plt.imshow(rois[idx][round(w/2),:,:], interpolation='none', cmap='gray') 
    plt.colorbar()
    if r_fit != 'null':
        plt.plot(t, -r_fit*2+(h-1)/2, 'r-')
        plt.plot(t, r_fit*2+(h-1)/2, 'r-')
    if r_dots != 'null':
        plt.plot(t, -r_dots*2+(h-1)/2, 'rx', ms=9)
        plt.plot(t, r_dots*2+(h-1)/2,'rx', ms=9)             
    
    plt.xlabel('Time')
    plt.ylabel('y-axis position')
    plt.title('Colony '+str(idx))
    
    if filename != 'null':    
        #plt.savefig("KymoGraph.pdf", transparent=True) 
        plt.savefig(str(filename)+".pdf", transparent=True)

# End

