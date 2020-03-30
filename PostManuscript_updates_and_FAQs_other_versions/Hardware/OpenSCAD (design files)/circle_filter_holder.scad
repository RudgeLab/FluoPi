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
h_clam = 2;
free_clam_space = 10;
angles1 = [0,120,240];
angles2 = [15,135,255];

rb = ri-1;
re = ri +side_thick;
h_int = h_clam + filter_thick +filter_free_space; //internal h
h_ext = h_clam + filter_thick +filter_free_space + bottom_thick; //external h


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


    difference(){
linear_extrude(height = h_ext, center = true, convexity = 10, twist = 0,$fn = 100)
circle(re);
                translate([0,0,bottom_thick])
        linear_extrude(height = h_int*1.1, center = true, convexity = 10, twist = 0,$fn = 100)

circle(ri);
    translate([0,0,-bottom_thick])          linear_extrude(height = h_int*1.1, center = true, convexity = 10, twist = 0,$fn = 100)
circle(rb);
                    translate([0,0,h_ext/2-h_clam/2 - h_clam/4]) 
        clam_space(re*1.5, free_clam_space ,h_clam/2, angles1);

                               translate([0,0,h_ext/2-0.8*h_clam/2.1])  
intersection() {

        clam_space(re*1.5, free_clam_space ,h_clam*0.8, angles1);

        clam_space(re*1.5, free_clam_space ,h_clam*0.8, angles2);
}
        
    }


    
