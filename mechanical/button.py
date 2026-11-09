# SPDX-License-Identifier: MIT
"""Captive front button: one small print, retained by the existing lid.

Coordinates are assembly mm. A fork reaches over the switch to internal
retaining ears. Only the moving face and contact boss project through the wall.
"""
import manifold3d as m


def box(size, center):
    return m.Manifold.cube(size, True).translate(center)


def build(p):
    z = p['front_button']['axis_z']
    cap = p['front_button']['printed_cap']
    # The 8x4mm face stands 1.8mm beyond the circular base, without an outer pod.
    face_profile = m.CrossSection.square((6, 2), True).offset(1)
    face = face_profile.extrude(.8).transform([[1, 0, 0, 0],
                                             [0, 0, 1, cap['face_front_y']],
                                             [0, 1, 0, z]])
    arms = sum((box((1.6, 5.4, 1.2), (x, -40.9, 6.6))
                for x in [-3.2, 3.2]), m.Manifold())
    ears = sum((box((2.4, .8, 1.2), (x, -38.6, 6.6))
                for x in [-4.1, 4.1]), m.Manifold())
    # Positive overlap avoids separate shells at floating-point face seams.
    back = cap['face_front_y'] + .7
    tip = cap['rest_tip_y']
    profile = m.CrossSection([[(back, z-.8), (tip, z-.45),
                              (tip, z+.45), (back, z+.45)]])
    # CrossSection coordinates are (Y,Z); extrusion becomes the X axis.
    # Construct this transform explicitly to avoid a hidden orientation offset.
    boss = profile.extrude(2).transform([[0, 0, 1, -1],
                                       [1, 0, 0, 0],
                                       [0, 1, 0, 0]])
    button = face + arms + ears + boss

    # Open-top guides behind the switch: 0.4mm nominal running clearance.
    # Ears hit Y=-39.0 at rest and Y=-37.6 after 0.6mm inward travel.
    surround = m.Manifold()
    for sign in [-1, 1]:
        surround += box((4.5, 5.8, .8), (sign*4.25, -39.7, 5.2))
        surround += box((.8, 3, 2), (sign*6.1, -38.3, 6.6))
        surround += box((.8, 2.2, 2), (sign*1.6, -37.9, 6.6))
        surround += box((2.1, .8, 2), (sign*5.45, -39.4, 6.6))
        surround += box((4.5, .8, 2), (sign*4.25, -37.2, 6.6))
    # No fixed part of the button mechanism may bulge outside the case wall.
    surround ^= m.Manifold.cylinder(10, p['base_diameter']/2-.2,
                                    p['base_diameter']/2-.2, 192)
    roof = box((13, 2.8, 1.2), (0, -38.2, 8.2))
    return surround, roof, button
