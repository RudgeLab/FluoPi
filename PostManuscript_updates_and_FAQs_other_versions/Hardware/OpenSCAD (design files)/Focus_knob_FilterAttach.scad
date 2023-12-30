/*
    With this code you can make a focus wheel extension for the M12 lenses used in the FluoPi project.
    
    Isaac Núñez 2020 (CC BY 4.0; https://creativecommons.org/licenses/by/4.0/) 
 
*/


////////////////////////////////////
//  Parameters  //

// This values have to be the same as in the filter holder to be compatibles
ri = 12.6;
side_thick = 1*1.2 ; // 1.2 times to let enter the clamp
h_clam = 2;
h = h_clam * 2;
thick_frac = 0.4 ; // free space fraction of clam thickness
free_clam_space = 4.2;
angles1 = [0,120,240];
angles2 = [20,140,260]; // 2 more degree to let the clam enter
// until here

///////////////
//wheel values

re_wheel = 16; //wheel external radii
ri_wheel = 14; // wheel internal radii
w_thick = 3; // wheel height (z axis)
nt = 20; // number of thoot
//thoot_size = 5; //

/////////////////
// M12 aperture

M12_ri = 7.15 ;
M12_side_thick = 2.5;
aperture_h = w_thick + 2; 

angles_M12 = [0,180];
free_M12 = 10;

M12_re = M12_ri + side_thick;


rb = ri-1;
re = ri +side_thick;

//////////////
// Moldules //

module clam_space(length, wide, thickness, angles){

for(ang = angles){
   rotate([0,0,ang])
    translate([length/2, 0, 0])
   cube([length, wide, thickness], center = true);
}
}

module wheel(){
    // to create the wheel
    tooth_ang = 360/nt; //angle per each gear tooth
    end_ang = 360 - tooth_ang;
    
    tw = sin(tooth_ang/2)*ri_wheel;
    tr = cos(tooth_ang/2)*ri_wheel;
    th = re_wheel - tr;
    
    difference(){
        
        union(){
            // M12 ring
            translate([0,0,w_thick/2])
            cylinder(h=w_thick, r=ri_wheel, $fn=100, center =true);
            
            // gear teeth
            for(ang = [0:tooth_ang:end_ang]){
            rotate([0,0,ang])
            translate([0,tr,w_thick/2])
            linear_extrude(height = w_thick, center = true, convexity = 2, twist = 0)
            polygon(points=[[tw,0],[-tw,0],[0,th]]);
            }
            /*
    // in this case the spikes starts from center.            polygon(points=[[0,-re_wheel*3/4],[0,re_wheel*3/4],[re_wheel,0]]);
            }
            */
                
        // M12 ring
        translate([0,0,aperture_h/2])
        cylinder(h=aperture_h, r=M12_re, $fn=100, center =true);
        }
        // central hole
        translate([0,0,w_thick/2])
        cylinder(h=aperture_h*1.5, r=M12_ri, $fn=100, center =true); 
/*
intersection(){
    translate([0,0,w_thick/2]) 
    linear_extrude(height = total_h, center = true, convexity = 10, twist = 0,$fn = 100)
circle(M12_re-1);
                      translate([0,0,w_thick/2]) 
        clam_space(M12_re, free_M12 ,total_h, angles_M12);
}
*/
    }
}


module clamp(){

    difference(){
linear_extrude(height = h, center = true, convexity = 10, twist = 0,$fn = 100)
circle(re);

        linear_extrude(height = h*1.1, center = true, convexity = 10, twist = 0,$fn = 100)

circle(ri);
                                                translate([0,0,h/2-h_clam*(1-thick_frac) - h_clam*thick_frac/2])  
        clam_space(re*1.5, free_clam_space ,h_clam*thick_frac, angles1);
        
        translate([0,0,h/2- h_clam/2]) 
           intersection() {                         
        clam_space(re*1.5, free_clam_space ,h_clam, angles1);
                             
        clam_space(re*1.5, free_clam_space ,h_clam, angles2);
       
}            
    }

}


module WS_camera(){
    difference(){
        //translate([0,0,w_thick/2]) 
        wheel();
        translate([0,0,-h/2+h_clam]) 
        clamp();
    }
}

///////////////////////////
// Create the focus knob //
///////////////////////////

// Uncomment to generate the different versions of the module

//WS_camera();
