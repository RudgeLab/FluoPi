/*
    With this code you can make a camera holder for RPI camera from waveshare (http://www.waveshare.com/product/mini-pc/raspberry-pi/cameras/rpi-camera-b.htm) or for V2 RPI camera (https://www.raspberrypi.org/products/camera-module-v2/)
    
    The code was modified from Fernán Federici 2017 version.
    
    This is licensed under the Creative Commons - Attribution license (CC BY 4.0)
    Isaac Núñez 2020.
 
*/

///////////////////////
// Fluopi parameters

holder_x=54;//acrylic bed width to fit into holder
holder_z=3*1.1;//acrylic bed thickness to fit into holder, normally 3 mm acrylic. 1.1 correction factor applied to surpass acrylic manufacture variations.

////////////////////////
// Defined by the user

// Base holder parameters

sca_thick_up = 3; // holder scafold thickness
sca_thick_side = 3; // holder scafold thickness
sca_thick_down = 2; // holder scafold thickness
sca_deep = 10;  // holder scafold back deep, it have to be shorter than the distance to the screws in the camera PCB (14 mm aprox)
sca_arms_width = 11; // holder scafold arms width

sca_arms_space = 1;  // space attach relaxation


sca_trans = (sca_thick_up - sca_thick_down)/2; // translate the holder space to achieve the desired up and down thicknes

scafold_x = holder_x + 2*sca_thick_side;
scafold_y = 33.5; // depth
scafold_z = holder_z + sca_thick_up + sca_thick_down;


//camera holder parameters

side_thick = 2; //side support thickness
bottom_thick = 1; // bottom support thickness
back_thick = 2; // back support thickness

/////////////////////
//  Camera details:

////////////////////////////////
// Waveshare Chinesse camera //
///////////////////////////////
waveshare_cam_x=32.2 + 1; // 1mm of error
waveshare_cam_y=32.2; 
waveshare_cam_z=1.5*1.1;//thickness
WS_hold_x = 5.1 - 0.3;    // space between border and cable conector. 0.3 the security factor
WS_hold_y = 4.5 - 0.3;  // space between border and resistor. 0.3 the security factor

///////////////////
// RPI V2 camera //
///////////////////

RPIV2_cam_x = 25 + 1 ; // 1mm of error
RPIV2_cam_y = 24; 
RPIV2_cam_z = 1 + 0.1; // PCB thickness, 0.1 mm of error
RPIV2_connec_x = 22; // cable conector length
RPIV2_connec_z = 2.7+ 0.1; // cable conector thikness, 0.1 mm error

RPIV2_sensor_x = 16 + 0.5; // sensor base length (8.5 mm) or adaptor lenght + 0.5 mm error

V2_hold_x =(RPIV2_cam_x - RPIV2_sensor_x)/2 - 0.3;    // space between camera border and sensor base. 0.3 the security factor
V2_hold_y = 7 - 0.2;  // space between border and PCB first obstacle (sensor base or electronic componentes). 0.2 security value.


module cam_holder_base() {
    
    difference(){
    cube([scafold_x,scafold_y,scafold_z], center=true);
     translate([0,0,sca_trans])cube([holder_x,scafold_y*1.1,holder_z], center=true);
     translate([0,sca_deep/2,0])cube([scafold_x - 2*sca_arms_width,scafold_y - sca_deep,scafold_z], center=true);
     translate([holder_x/2-sca_arms_space/2,sca_deep/2,scafold_z/2])cube([sca_arms_space,scafold_y - sca_deep,scafold_z], center=true);
     translate([-holder_x/2+sca_arms_space/2,sca_deep/2,scafold_z/2])cube([sca_arms_space,scafold_y - sca_deep,scafold_z], center=true);
        
        }      
}

module camera_mount(camera){

    if(camera == "waveshare"){
            cam_x = waveshare_cam_x;
            cam_y = waveshare_cam_y;
            cam_z = waveshare_cam_z;
            hold_x = WS_hold_x;
            hold_y = WS_hold_y;
    
        support_z = cam_z+bottom_thick;
        support_y = hold_y + back_thick;
        translate([0,-scafold_y/2 + support_y/2,scafold_z/2+support_z/2])difference(){cube([cam_x+2*side_thick,support_y,support_z], center=true);
            translate([0,back_thick/2,-bottom_thick/2])cube([cam_x,hold_y,cam_z], center=true);
            translate([0,0,0])cube([cam_x - 2*hold_x,support_y,support_z], center=true);
    }
    }
    
    else if(camera == "RPIV2"){
            cam_x = RPIV2_cam_x;
            cam_y = RPIV2_cam_y;
            cam_z = RPIV2_cam_z;
            hold_x = V2_hold_x;
            hold_y = V2_hold_y;
            base_space = RPIV2_connec_x+0.2;
         
    support_z = cam_z+bottom_thick + RPIV2_connec_z;
    support_y = hold_y + back_thick;
    translate([0,-scafold_y/2 + support_y/2,scafold_z/2+support_z/2])difference(){cube([cam_x+2*side_thick,support_y,support_z], center=true);
        translate([0,back_thick/2,-bottom_thick/2 + RPIV2_connec_z/2])cube([cam_x,hold_y,cam_z], center=true); // camera PCB hole
        translate([0,0,-bottom_thick/2])cube([base_space,support_y,support_z-bottom_thick], center=true); // base hole
                translate([0,0,(support_z-bottom_thick)/2])cube([RPIV2_sensor_x,support_y,bottom_thick], center=true); // camera hole
    }
    }
    
}


cam_holder_base();

//uncomment the one you pretend to use

camera_mount("RPIV2");
//camera_mount("waveshare");