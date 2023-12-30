/*
    
    With this code you can make a filter holder to attach it to the lens focus wheel used for the camera in the FluoPi project.
    
    Isaac Núñez 2020 (CC BY 4.0; https://creativecommons.org/licenses/by/4.0/) 
 
*/

////////////////
// Parameters //


ri = 12.6;   //filter radius
side_thick = 1 ;
filter_thick = 3;
filter_free_space = 0.5;
bottom_thick = 0.8;
sheet = 1; // sheet tickness to support the filter

rb = ri-sheet; // internal hole radius
re = ri +side_thick; // External radius

h_fs = filter_thick +filter_free_space + bottom_thick; //base filter support heigh

// HQ camera
r_hq = 15; // HQ camera radius
h_ring = 3; // Height of the ring attached to the camera

// RPI V2 camera


// Clamp support system for waveshare camera
h_clam = 2;
free_clam_space = 10;
angles1 = [0,120,240];
angles2 = [15,135,255];

h_WS = h_fs + h_clam; // for waveshare

////////////////////////////////////

module clam_space(length, wide, thickness, angles){

    for(ang = angles){
       rotate([0,0,ang])
       translate([length/2, 0, 0])
       cube([length, wide, thickness], center = true);
    }
}



////////////////////////
// Create the holder //

module filter_support(h){
    difference(){
    linear_extrude(height = h, center = true, convexity = 10, twist = 0,$fn = 100)
    circle(re);
    
    translate([0,0,bottom_thick])
    linear_extrude(height = h, center = true, convexity = 10, twist = 0,$fn = 100)
    circle(ri);
        
    translate([0,0,-bottom_thick])          linear_extrude(height = h, center = true, convexity = 10, twist = 0,$fn = 100)
    circle(rb);
    }
}

module fsup_WS_clamp(h){
    difference(){
        
        filter_support(h);
        
        // Clamp system
        translate([0,0,h/2-h_clam/2 - h_clam/4]) 
        clam_space(re*1.5, free_clam_space ,h_clam/2, angles1);

        translate([0,0,h/2-0.8*h_clam/2.1])  
        intersection() {

            clam_space(re*1.5, free_clam_space ,h_clam*0.8, angles1);

            clam_space(re*1.5, free_clam_space ,h_clam*0.8, angles2);
        }
    }
}

module fsup_HQ(h){
    h_total = h + bottom_thick + h_ring;
    
    difference(){
        union(){
            filter_support(h);
            
            //union ring
            translate([0,0,(h-bottom_thick)/2])
            cylinder(h=bottom_thick, r=r_hq+side_thick, $fn=100, center =true);
            
            //ring attached to HQ camera
            translate([0,0,(h+h_ring)/2])
            difference(){
                cylinder(h=h_ring, r=r_hq+side_thick, $fn=100, center =true);
                cylinder(h=h_ring, r=r_hq, $fn=100, center =true);
            }
            }
    translate([0,0,bottom_thick+h/2])          
    cylinder(h=h_total, r=ri, $fn=100, center =true);  
    }

}

module fsup_rpiv2(h){
    union(){
        filter_support(h);
    
    }
}

// Uncomment the module you wanna generate
//fsup_WS_clamp(h_WS);
//filter_support(h_WS);
fsup_HQ(h_fs);

