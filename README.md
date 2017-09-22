# FluoPi

Hardware design files, code and teaching materials for SynBio_UC/BackyardBrains raspberry pi fluorescent image registration station.

## Overview

FluoPi is composed of a blue-ligh transilluminator toghether a black box and a raspberry camera.  All the hadware is controlled with a Raspberry pi small computer.
With this equipment you are able to:  
* See electrophoresis gel stained with blue excitable chemicals (such as GelRed or SYBR Safe).
* Take images of fluorescent samples
* Perform timelapse images series of fluorescent samples

## Getting Started

You can see the full project at [OSF](https://osf.io/dy6p2/)

### Prerequisites

To hardware assembly you need access to a laser cutter and also a 3D printer. The other materials are general stuff like screwdrivers, wrench or pliers.
Also you will need a HDMI screen where to connect the Raspberry pi (although  you can manage the equipment through SSH or using programs such as [teamviewer](https://pages.teamviewer.com/published/raspberrypi/))


### Installing

All the installation instructions are available on the [wiki page][wiki]


### Running the equipment

The equipment has a manual swith and also you can control the camera with [_camera module commands_](https://www.raspberrypi.org/documentation/usage/camera/raspicam/README.md). 
To perform further experimentation and process automation the project include some python codes (based on [camera python module](https://www.raspberrypi.org/documentation/usage/camera/python/) to control the hardarware:  
* _timelapse.py_ --> to perform timelapse experiments
* _turnON.py_ --> to turn ON the transilluminator
* _turnOFF.py_ --> to turn OFF the transilluminator

### Running the notebooks

To test the jupyter notebooks you only need to download the data from the [OSF page project](https://osf.io/dy6p2/) on the inside folder Google Drive:FluoPi_Data/Manuscript_data/Raw_data_figures_manuscript. There you will find two folder with example data:  
* fig 4_fig 5_S4 movie
* fig 6_S5_S6_S7_S8movies

Download the data and put the path folder in the proper code block inside the jupyter notebook.

```
fname =  "D:\myFolder\TLE_G_7_3_17\image_%04d.jpg"
```

for further information see the [wiki page][wiki]

## Authors

Universidad Catolica de Chile: 
* Isaac Nuñez [Prosimio](https://github.com/Prosimio)
* Tamara Matute [tfmatute](https://github.com/tfmatute)
* Juan Keymner
* Tim Rudge [timrudge](https://github.com/timrudge)
* Fernan Federici [FernanFederici](https://github.com/FernanFederici)

Backyard Brains Chile
* Roberto Pellizzari [RoHPellizzari](https://github.com/RoHPellizzari)
* Tim Marzullo 


## License

This project is licensed under the MIT License - see the [LICENSE.txt](LICENSE.txt) file for details

## Acknowledgments

* Toby Wenzel for guidance on Docubricks documentation
* Tom Baden for feedback and advice on camera
* Bernardo Pollak for helping with sequences
* Douglas Densmore for the CIDAR MoClo Parts Kit


[wiki]: https://github.com/SynBioUC/FluoPi/wiki
