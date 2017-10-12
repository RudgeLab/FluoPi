# [<img src="https://github.com/SynBioUC/FluoPi/blob/master/Images_wiki/fluopi23_logo.jpg" width="200">][website] 

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
with HDMI (or hdmi to VGA adaptor) to connect with the Raspberry pi (you can also manage the equipment through SSH or using programs such as [teamviewer](https://pages.teamviewer.com/published/raspberrypi/))


### Installing

All the installation instructions are available on the [wiki page][wiki]

Full documentation and assembly instructions can be found at [Docubricks](http://docubricks.com/viewer.jsp?id=701517893260717056)


### Running the equipment

The equipment has a manual switch and the camera can be controlled with [_camera module commands_](https://www.raspberrypi.org/documentation/usage/camera/raspicam/README.md).
The project includes some python codes (based on [camera python module](https://www.raspberrypi.org/documentation/usage/camera/python/)) to control the hardware:  
* _timelapse.py_ --> to perform timelapse experiments
* _turnON.py_ --> to turn ON the transilluminator
* _turnOFF.py_ --> to turn OFF the transilluminator

### Running the notebooks

Jupyter notebooks are included (Examples/ and Tutorials/) to demonstrate the analysis principles and the use of the fluopi module to analyse time-lapse image data. Sample image data is included in the relevant folders. You can start from these examples, switching the file paths to your data.

## Authors

**Universidad Catolica de Chile**
* Isaac Nuñez - [Prosimio](https://github.com/Prosimio)
* Tamara Matute - [tfmatute](https://github.com/tfmatute)
* Juan Keymner - [Keymer Lab](http://keymerlab.nl/www/?page_id=26)
* Tim Rudge - [timrudge](http://rudge-lab.org)
* Fernan Federici - [Fernan´s labpage ](https://federicilab.org)

[**Backyard Brains Chile**](http://www.backyardbrains.cl/)
* Roberto Pellizzari - [RoHPellizzari](https://github.com/RoHPellizzari)
* Tim Marzullo - 


## License

This project is licensed under the MIT License - see the [LICENSE.txt](LICENSE.txt) file for details. Hardware is lincesed under the CERN license.

## Acknowledgments

* _Toby Wenzel_ for guidance on Docubricks documentation
* _Tom Baden_  and _Andre Chagas_ for feedback and advice on camera
* _Bernardo Pollak_ for helping out with sequences
* _Douglas Densmore_ for the CIDAR MoClo Parts Kit

* _OpenPlant Fund_ and _Fondecyt_ for providing financial support


[wiki]: https://github.com/SynBioUC/FluoPi/wiki
[website]: https://osf.io/dy6p2/
