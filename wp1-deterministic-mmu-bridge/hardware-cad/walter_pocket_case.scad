// SPDX-License-Identifier: AGPL-3.0-only
// Parametric fit-test concept; dimensions are assumptions, not a verified PCB fit.
inner_x = 65;
inner_y = 42;
inner_z = 20;
wall = 2;
clearance = 0.4;
button_diameter = 8;
$fn = 48;
assert(inner_x > 30 && inner_y > 25 && inner_z > 8 && wall >= 1);
// Open tray. Rounded tactile guards distinguish the two placeholder button holes.
difference() {
    cube([inner_x + 2*wall, inner_y + 2*wall, inner_z + wall]);
    translate([wall, wall, wall]) cube([inner_x, inner_y, inner_z + 1]);
    for (x = [inner_x/3, 2*inner_x/3])
        translate([x, -1, inner_z/2]) rotate([-90, 0, 0])
            cylinder(h=wall+2, d=button_diameter+clearance);
}
for (x = [inner_x/3, 2*inner_x/3])
    translate([x, 0, inner_z/2 + button_diameter]) rotate([90, 0, 0])
        cylinder(h=1.5, d=(x < inner_x/2 ? 3 : 5));
// Separate flat lid for fit tests; fastening, antenna keepout, battery safety and
// ingress/thermal/drop testing remain engineering work.
translate([inner_x + 3*wall + 5, 0, 0])
    cube([inner_x + 2*wall, inner_y + 2*wall, wall]);
