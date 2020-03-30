
/*
    This code generates lens holder adaptors for RPI custom lenses (e.g. M12 lenses) with internal thread mount.
    
    The code uses this thread library:
    https://github.com/adrianschlatter/threadlib
    Please follow the isntruction there to install the library prior to run this code.
    
    The correction values let you adjust the system to the 3D printing accuracy (try and error experience).
    
    This is licensed under the Creative Commons - Attribution license (CC BY 4.0)
    Isaac Núñez 2020.
*/



use <threadlib/threadlib.scad>


//////////////////////
//Defined by the user
//////////////////////////////////////
// lens cylinder mount specifications
//////////////////////////////////////

specs = thread_specs("M12x0.5-int"); // choose the name from THREAD_TABLE.scad, this case the M12x0.5

P = specs[0]; // pitch
corr = 0.25;
D = specs[2]+corr;  // +0.2 correction
Rrotation = specs[1]-corr/2; 
Turns = 24;        // Define the turns number accord length of the camera tube
H = (Turns + 1) * P;
Cyl_thick = 2;

// create your own table with the new thread
MY_THREAD_TABLE = [
                   ["M12_fixed-int", [P, Rrotation, D, specs[3]]]];


///////////////////////////////
// Camera mount specifications
//////////////////////////////

x_sensor = 8.5;
z_sensor = 5;
y_cable = 7.5;
x_cable = 9;
z_cable = 1.5;
cable_sep = 1;

pcb_cam_x = 25;
hole_dist = 5;
p_hole_size = 2; // PCB hole size
s_hole_size = 1.5; // support hole size 

st = 1; // support_thick
sc = 0.5; // sensor clearance dist

z_screw_holders = 3;


/// computed parameters (don´t change)

diam_lens_cyl = D+2*Cyl_thick;

s_cube_x = diam_lens_cyl;
s_cube_y = diam_lens_cyl;
s_cube_z = z_sensor+sc+st;

c_cube_x = x_cable+cable_sep+2*sc+2*st;
c_cube_y = x_sensor/2 + y_cable+sc+2*st-s_cube_y/2;
c_cube_z = z_cable+sc+st;

x_screw_holders = hole_dist+p_hole_size/2 - (s_cube_x - x_sensor)/2;


module support_base(hole) {

difference(){
    union(){
        difference(){
difference(){
cube([s_cube_x,s_cube_y,s_cube_z], center = true);
    translate([0,0,-st])
cube([s_cube_x-2*st,s_cube_y-2*st,s_cube_z], center = true);
};
cylinder(h=z_sensor+sc+st, d=hole, center=true, $fn =50);
}

    translate([-(x_cable+cable_sep-x_sensor)/2,(s_cube_y+c_cube_y)/2-st,-(s_cube_z-c_cube_z)/2])
difference(){
cube([c_cube_x,c_cube_y,c_cube_z], center = true);
    translate([0,0,-st])
cube([c_cube_x-2*st,c_cube_y-2*st,c_cube_z], center = true);
}};
    translate([-(x_cable+cable_sep-x_sensor)/2,(s_cube_y-st)/2,-(s_cube_z-c_cube_z+2*st)/2])
cube([c_cube_x-2*st,3*st,c_cube_z], center = true);
}

}

module screw_holder() {
    
    linear_extrude(height = z_screw_holders, center = true, convexity = 10, twist = 0)
    difference(){
    union(){circle(d=s_hole_size+2*st, $fn=120);translate([0,-(s_hole_size/2+st)])square([x_screw_holders,s_hole_size+2*st]);};
    circle(d=s_hole_size+0.1, $fn=60); //0.1 error
}
    
}


// Create the lens mount

    translate([0,0,s_cube_z/2])
nut("M12_fixed", turns=Turns, Douter=diam_lens_cyl,higbee_arc=50,table=MY_THREAD_TABLE);


support_base(12+0.4);



translate([-(x_screw_holders)-s_cube_x/2,0,-(s_cube_z-z_screw_holders)/2])
screw_holder();


translate([(x_screw_holders)+s_cube_x/2,0,-(s_cube_z-z_screw_holders)/2])

rotate(180)

screw_holder();
