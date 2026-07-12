"""bumble layout — 60 keys, Alice-style unibody split.

Geometry follows classic Alice-family spacing, anchored to plate-verified
reference boards (see LOG 5/6/9 for the measurement work): only the 4-column
alpha wedges rotate (±12°); outer columns stay straight and shear outward
~4.1 mm per row; the keys hugging the wedge boundary (2, -, P) are raised
slightly so the rotated corners clear; the spacebar row is dropped 1.5 mm;
apex 6->7 spacing is 1.48u, which is what fits the mirrored B (key #60).
Bottom row is bumble's own: corner mod pairs + 2.25|2.75 spacebars.

KEYS below is the hand-editable source of truth for placement — edit it
directly to iterate. Frame: key units, y down, origin = ` cap top-left
corner; angle sign is y-down (left wedge +12 = clockwise on screen).

Remaining geometry knobs:
  SPLIT_EXTRA — widens the apex gap by shifting the whole right half (RI+RO)
                horizontally, e.g. for the center screen bay.

placed() is the single geometry source for the keycap render and the plate.
"""

import math

SPLIT_EXTRA = 0.0        # u, extra apex gap on top of the reference spacing
KEY_INSET = 0.04         # u, visual keycap gap in renders

# Plate parameters (MX variant; Choc gets its own later)
UNIT_MM = 19.05
PLATE_MARGIN_MM = 6.0
PLATE_THICK_MM = 1.5
CUTOUT_MM = 14.0
PLATE_CORNER_R_MM = 3.0

# (legend, center_x_u, center_y_u, width_u, angle_deg, zone)
KEYS = [
    ('2', 2.4785, 0.3877, 1.0, -0.0, 'LO'),
    ('-', 11.9777, 0.3877, 1.0, -0.0, 'RO'),
    ('0', 10.9016, 0.4916, 1.0, -12.0, 'RI'),
    ('Bksp', 14.4674, 0.4998, 2.0, -0.0, 'RO'),
    ('`', 0.5000, 0.5000, 1.0, -0.0, 'LO'),
    ('1', 1.5000, 0.5000, 1.0, -0.0, 'LO'),
    ('=', 12.9556, 0.5000, 1.0, -0.0, 'RO'),
    ('3', 3.5546, 0.5955, 1.0, 12.0, 'LI'),
    ('9', 9.9234, 0.6995, 1.0, -12.0, 'RI'),
    ('4', 4.5327, 0.8034, 1.0, 12.0, 'LI'),
    ('8', 8.9453, 0.9074, 1.0, -12.0, 'RI'),
    ('5', 5.5109, 1.0114, 1.0, 12.0, 'LI'),
    ('7', 7.9671, 1.1153, 1.0, -12.0, 'RI'),
    ('6', 6.4890, 1.2193, 1.0, 12.0, 'LI'),
    ('P', 11.6963, 1.4444, 1.0, -0.0, 'RO'),
    ('W', 2.8575, 1.4696, 1.0, 12.0, 'LI'),
    ('Tab', 0.5315, 1.5000, 1.5, -0.0, 'LO'),
    ('Q', 1.7814, 1.5000, 1.0, -0.0, 'LO'),
    ('[', 12.6743, 1.5000, 1.0, -0.0, 'RO'),
    (']', 13.6743, 1.5000, 1.0, -0.0, 'RO'),
    ('\\', 14.9247, 1.5000, 1.5, -0.0, 'RO'),
    ('O', 10.6202, 1.5735, 1.0, -12.0, 'RI'),
    ('E', 3.8356, 1.6775, 1.0, 12.0, 'LI'),
    ('I', 9.6421, 1.7814, 1.0, -12.0, 'RI'),
    ('R', 4.8138, 1.8854, 1.0, 12.0, 'LI'),
    ('U', 8.6639, 1.9893, 1.0, -12.0, 'RI'),
    ('T', 5.7919, 2.0933, 1.0, 12.0, 'LI'),
    ('Y', 7.6858, 2.1972, 1.0, -12.0, 'RI'),
    ('Caps', 0.4431, 2.4998, 1.75, -0.0, 'LO'),
    ('Enter', 14.7738, 2.4998, 2.25, -0.0, 'RO'),
    ('S', 2.8942, 2.5000, 1.0, 12.0, 'LI'),
    ('A', 1.8181, 2.5000, 1.0, -0.0, 'LO'),
    (';', 12.1488, 2.5000, 1.0, -0.0, 'RO'),
    ("'", 13.1488, 2.5000, 1.0, -0.0, 'RO'),
    ('L', 11.0727, 2.5000, 1.0, -12.0, 'RI'),
    ('D', 3.8724, 2.7079, 1.0, 12.0, 'LI'),
    ('K', 10.0946, 2.7079, 1.0, -12.0, 'RI'),
    ('F', 4.8505, 2.9158, 1.0, 12.0, 'LI'),
    ('J', 9.1164, 2.9158, 1.0, -12.0, 'RI'),
    ('G', 5.8287, 3.1237, 1.0, 12.0, 'LI'),
    ('H', 8.1383, 3.1237, 1.0, -12.0, 'RI'),
    ('Shift', 0.4480, 3.4998, 2.25, -0.0, 'LO'),
    ('Shift', 14.9323, 3.4998, 2.75, -0.0, 'RO'),
    ('/', 12.8675, 3.5000, 1.0, -0.0, 'RO'),
    ('.', 11.8675, 3.5000, 1.0, -0.0, 'RO'),
    ('Z', 2.0990, 3.5000, 1.0, -0.0, 'LO'),
    ('X', 3.1751, 3.5819, 1.0, 12.0, 'LI'),
    (',', 10.7913, 3.5819, 1.0, -12.0, 'RI'),
    ('M', 9.8132, 3.7898, 1.0, -12.0, 'RI'),
    ('C', 4.1532, 3.7898, 1.0, 12.0, 'LI'),
    ('V', 5.1314, 3.9977, 1.0, 12.0, 'LI'),
    ('N', 8.8350, 3.9977, 1.0, -12.0, 'RI'),
    ('B', 7.8569, 4.2056, 1.0, -12.0, 'RI'),
    ('B', 6.1095, 4.2056, 1.0, 12.0, 'LI'),
    ('Ctrl', 0.1980, 4.4998, 1.25, -0.0, 'LO'),
    ('Cmd', 1.4480, 4.4998, 1.25, -0.0, 'LO'),
    ('Alt', 14.1823, 4.4998, 1.25, -0.0, 'RO'),
    ('Fn', 15.4323, 4.4998, 1.25, -0.0, 'RO'),
    ('', 4.7276, 5.0150, 2.25, 12.0, 'LI'),
    ('', 8.9389, 5.0788, 2.75, -12.0, 'RI'),
]


def _rot(px, py, deg, x, y):
    r = math.radians(deg)
    dx, dy = x - px, y - py
    return (px + dx * math.cos(r) - dy * math.sin(r),
            py + dx * math.sin(r) + dy * math.cos(r))


def placed():
    """Final geometry: list of dicts with legend, zone, x, y, w, angle,
    pivot (= key center), corners (4 rotated pts), center."""
    out = []
    for legend, cx, cy, w, angle, zone in KEYS:
        if zone in ("RI", "RO"):
            cx += SPLIT_EXTRA
        x, y = cx - w / 2, cy - 0.5
        corners = [_rot(cx, cy, angle, px, py)
                   for px, py in ((x, y), (x + w, y), (x + w, y + 1), (x, y + 1))]
        out.append(dict(legend=legend, zone=zone, x=x, y=y, w=w, angle=angle,
                        pivot=(cx, cy), corners=corners, center=(cx, cy)))
    return out
