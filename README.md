# FluoPi

Hardware design files, code and teaching materials for a low cost and open source fluorescent image registration station.

## Overview

FluoPi is composed of a blue-light transilluminator, an amber acrylic filter and a raspberry camera contained in a black acrylic mainframe. All the hardware is controlled with a Raspberry pi small computer.
With this equipment you are able to:  

* Take images of fluorescent samples ranges from um to cm.
* Perform timelapse assays of up to 3 fluorescent proteins simultaneously
* See electrophoresis gel stained with blue excitable chemicals (such as GelRed or SYBR Safe).

## Getting Started

You can see the full project at [OSF](https://osf.io/dy6p2/)
and a pre-print manuscript at [Biorxiv](https://www.biorxiv.org/content/early/2017/09/27/194324)

### Prerequisites

To assemble this device you need access to a laser cutter and a 3D printer. You also need a mouse, keyboard and a screen
with HDMI (or hdmi to VGA adaptor) to connect the Raspberry pi (although you can manage the equipment through SSH or using programs such as [teamviewer](https://pages.teamviewer.com/published/raspberrypi/))


### Installing

All the installation instructions are available on the [wiki page][wiki]


### Running the equipment

The equipment has a manual switch and the camera can be controlled with [_camera module commands_](https://www.raspberrypi.org/documentation/usage/camera/raspicam/README.md).
The project includes some python codes (based on [camera python module](https://www.raspberrypi.org/documentation/usage/camera/python/)) to control the hardware:  
* _timelapse.py_ --> to perform timelapse experiments
* _turnON.py_ --> to turn ON the transilluminator
* _turnOFF.py_ --> to turn OFF the transilluminator

### Running the notebooks

To test the jupyter notebooks you only need to download the data from the [OSF page project](https://osf.io/dy6p2/) or linked Google Drive:FluoPi_Data/Manuscript_data/Raw_data_figures_manuscript. You will find two folders with example data:  
* fig 4_fig 5_S4 movie
* fig 6_S5_S6_S7_S8movies

Download the data and put the path folder in the proper code block inside the jupyter notebook.

```
fname =  "D:\myFolder\TLE_G_7_3_17\image_%04d.jpg"
```

for further information please see the [wiki page][wiki]

## Authors

**Universidad Catolica de Chile**
* Isaac Nu�ez - [Prosimio](https://github.com/Prosimio)
* Tamara Matute - [tfmatute](https://github.com/tfmatute)
* Juan Keymner - [Keymer Lab](http://keymerlab.nl/www/?page_id=26)
* Tim Rudge - [timrudge](https://github.com/timrudge)
* Fernan Federici - [FernanFederici](https://github.com/FernanFederici)

[**Backyard Brains Chile**](http://www.backyardbrains.cl/)
* Roberto Pellizzari - [RoHPellizzari](https://github.com/RoHPellizzari)
* Tim Marzullo


## License

This project is licensed under the MIT License - see the [LICENSE.txt](LICENSE.txt) file for details

## Acknowledgments

* _Toby Wenzel_ for guidance on Docubricks documentation
* _Tom Baden_  and _Andre Chagas_ for feedback and advice on camera
* _Bernardo Pollak_ for helping out with sequences
* _Douglas Densmore_ for the CIDAR MoClo Parts Kit

* _OpenPlant Fund_ and _Fondecyt_ for providing financial support


[wiki]: https://github.com/SynBioUC/FluoPi/wiki
