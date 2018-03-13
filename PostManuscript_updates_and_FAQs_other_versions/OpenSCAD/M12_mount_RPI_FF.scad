/*
    This code uses modified code from Vaqueram ( https://www.thingiverse.com/thing:1963856) for the base.
    Lens holder and internal thread built from 
    A new thread module was used. The correction value makes the system fit perfectly with M12 lenses.
    This is licensed under the Creative Commons - Attribution license (CC BY 4.0)
    Fernán Federici 2017.
*/

use <threads.scad>

wall=3;
base_xy=16;
base_h=6;
M12_r=12/2;
mount_h = 10;
screw_d=21;//distance between screw holes
screw_r=2/2;
screw_hold_r=2;
corr=0.2;
sensor_h=2; //space for sensor
sensor_x=8.5;
wall_M12=1.5;
cyl_r=15;
baseM12();
$fn=100;

module baseM12() {
    difference() {
			union() {
                translate([0,0,mount_h/2 + base_h]) 
                color("Blue")   cylinder (r= cyl_r/2, h= mount_h, center=true);
				translate([0,0,base_h/2])
					color("Red")  cube([base_xy, base_xy, base_h], center = true);
				translate([screw_d/2, 0, 0])
					cylinder(r = screw_hold_r, h = base_h/2);
				translate(-[screw_d/2, 0, 0])
					cylinder(r = screw_hold_r, h = base_h/2);
					translate([0,0,base_h/2/2])
						cube([screw_d, 4, base_h/2], center = true);
			}
		translate([0,0,base_h/2])
			color("Green") cube([base_xy - wall*2, base_xy - wall*2, base_h], center = true);
		translate([screw_d/2, 0, 0])
			cylinder(r = screw_r, h = base_h);
		translate([-screw_d/2, 0, 0])
			cylinder(r = screw_r, h = base_h);
		translate([0, base_xy / 4, sensor_h/2])
			cube([sensor_x, base_xy / 2, sensor_h], center = true);
        translate([0, 0, base_h-corr])     english_thread (diameter=(((M12_r*2)+(corr*3))/25.4), threads_per_inch=50.8, length=mount_h*3/25.4,internal=true, n_starts=1, thread_size=-1, groove=true,square=false, rectangle=0, angle=30, taper=0, leadin=1);
	}
}


