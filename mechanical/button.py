# SPDX-License-Identifier: MIT
"""Captive front button: one small print, retained by the existing lid.

Coordinates are assembly mm. The two side ears define the travel stops;
the narrow, bevel-backed boss contacts only the B3U actuator.
"""
import manifold3d as m


def box(size, center):
    return m.Manifold.cube(size, True).translate(center)


def build(p):
    z = p['front_button']['axis_z']
    # The face is deliberately 0.8mm proud of its surround at the forward stop.
    face_profile = m.CrossSection.square((6, 2), True).offset(1)
    face = face_profile.extrude(1.6).transform([[1, 0, 0, 0],
                                             [0, 0, 1, -45.6],
                                             [0, 1, 0, z]])
    ears = sum((box((1.6, .6, 4), (x, -43.7, z))
                for x in [-4.2, 4.2]), m.Manifold())
    # A 45-degree lower bevel prints the contact boss without support.
    profile = m.CrossSection([[(-44, z-1.4), (-43.05, z-.45),
                              (-43.05, z+.45), (-44, z+.45)]])
    # CrossSection coordinates are (Y,Z); extrusion becomes the X axis.
    # Construct this transform explicitly to avoid a hidden orientation offset.
    boss = profile.extrude(2).transform([[0, 0, 1, -1],
                                       [1, 0, 0, 0],
                                       [0, 1, 0, 0]])
    button = face + ears + boss

    surround = box((14, 4.6, 5.4), (0, -42.5, 4.5))
    # Open-top channel: drop in the cap, then the lid captures it.
    surround -= box((10.8, 1.2, 9), (0, -43.4, 6.9))
    surround -= box((8.8, 1.2, 9), (0, -44.5, 6.9))
    # Clear the switch body and PCB; retain side-ear stops at Y=-42.8.
    surround -= box((6.8, 5, 9), (0, -40.5, 6.9))
    surround -= box((3.2, 2.5, 2), (0, -42.4, z))
    roof = box((14, 4.6, 2.2), (0, -42.5, 8.3))
    return surround, roof, button
