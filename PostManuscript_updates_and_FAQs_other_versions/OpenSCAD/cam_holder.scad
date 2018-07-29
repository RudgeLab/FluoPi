/*
    Fernán Federici 2017 (CC BY 4.0; https://creativecommons.org/licenses/by/4.0/) 
 
    With this code you can make a camera adapter for RPI camera from waveshare (http://www.waveshare.com/product/mini-pc/raspberry-pi/cameras/rpi-camera-b.htm) and for V2 RPI camera (https://www.raspberrypi.org/products/camera-module-v2/)
 
*/

/////This code needs a lot of clean up and reorganization but it works//////////edits would be very welcome :) ////////////
 
x=60;//frontal width
y=47;//height 33+9+5
z=33.5; // depth
filter_x=43.7;
filter_y=31.4;
filter_z=3;
bed_x=54;
bed_y=3;
bed_z=100;
arm=5;
focus_space=20; // enough distance for lens focus adjustment
holder_x=54;//acrylic bed width to fit into holder
holder_y=3;//acrylic bed thickness to fit into holder, normally 3mm acrylic
$fn=100;
fudge=0.1; // to fix error in rendering leaving thin wall...help me!
int_gap=17.5; 
camera_type=0; //0 for waveshare camera (32x32mm); 1 for V2 RPI camera (25x24x9)
china_spacex= 24.3;
V2_spacex= 18;
waveshare_cam_x=32.2;
waveshare_cam_y=1.5; //thickness
waveshare_cam_z=32.2;
RPIV2_cam_x=25;
RPIV2_cam_y=1.5; //thickness
RPIV2_cam_z=24;


module cam_holder_base() {
    difference(){
    cube([x,y,z], center=true);
           translate([0,(y/2)-arm/2,2]) rotate([90,0,0])  cube([filter_x,filter_y,filter_z], center=true);
           translate([0,0,8])  color("blue") cube([filter_x-4,y+fudge,z*0.9], center=true);
           translate([0,(y/2)-(focus_space/2+arm),0])  color("Red")  cube([(x-arm),focus_space,z+fudge], center=true);
           translate([0,-((y/2)-arm/1.5),0]) color ("pink") cube([holder_x+fudge,holder_y,z+fudge], center=true);
           translate([0,-arm,arm+fudge]) color ("purple")  cube([(x-arm)+fudge,focus_space,(z-arm*2)+fudge], center=true);
           translate([0,-arm*1.5,-arm/2+fudge]) color ("yellow")  cube([int_gap,y/2,(z-arm*2)+fudge], center=true);
           translate([0,-arm*2,-arm/2+fudge]) color ("black")  cube([filter_x-4,arm*2,(z-arm*2)+fudge], center=true);
    }
}
       
module waveshare_cam() {
           translate([0,-((y/2)-arm/.75),0]) color ("red")  cube([china_spacex,arm*1.5,z+fudge], center=true);
           translate([0,-((y/2)-arm/.75),arm/2+fudge]) color ("yellow")  cube([waveshare_cam_x,waveshare_cam_y,z+fudge], center=true);
 }
  
module RPIV2_cam() {
       //difference() {
           //cam_holder_base();
           translate([0,-((y/2)-arm/.75),0]) color ("red")  cube([V2_spacex,arm*1.5,z+fudge], center=true);
           translate([0,-((y/2)-arm/.75),arm/2+fudge]) color ("yellow")  cube([RPIV2_cam_x,RPIV2_cam_y,RPIV2_cam_z+fudge], center=true);
     }     
     
module cam_holder(camera_type) {

     if(camera_type==0)
           difference() {
           cam_holder_base();
               waveshare_cam() ;
           }          
     else 
           difference() {
           cam_holder_base();
               RPIV2_cam();
           }
       }     
cam_holder(1); 


