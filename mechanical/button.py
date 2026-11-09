# SPDX-License-Identifier: MIT
"""Broad side paddle with twin guides, independent stops and foam return.

All coordinates are assembly millimetres. The raised face clears a fingertip
above the desk. Print face down with local support beneath the outboard ears.
"""
import manifold3d as m


def box(size, center):
    return m.Manifold.cube(size, True).translate(center)


def build(p):
    button = p['front_button']
    cap = button['printed_cap']
    z = button['axis_z']
    top, height = cap['rail_top_z_mm'], cap['rail_height_mm']
    rail_z = top - height / 2
    clearance = cap['minimum_slide_clearance_mm']
    width, face_height = cap['face_width_mm'], cap['face_height_mm']
    radius = cap['face_corner_radius_mm']
    profile = m.CrossSection.square(
        (width - 2 * radius, face_height - 2 * radius), True
    ).offset(radius)
    face = profile.extrude(cap['face_thickness_mm']).transform(
        [[1, 0, 0, 0], [0, 0, 1, cap['face_front_y']],
         [0, 1, 0, cap['face_center_z_mm']]]
    )
    # A shallow dish identifies the press area; retain >=0.8mm at its centre.
    dish_radius = 14
    face -= m.Manifold.sphere(dish_radius, 128).translate(
        (0, cap['face_front_y'] - dish_radius + cap['thumb_dish_depth_mm'],
         cap['press_center_z_mm'])
    )
    front, rear = cap['rail_front_y_mm'], cap['rail_rear_y_mm']
    arms = sum((box((cap['rail_width_mm'], rear - front, height),
                    (x, (front + rear) / 2, rail_z))
                for x in cap['rail_centers_x_mm']), m.Manifold())
    ear_width = cap['ear_outer_x_mm'] - cap['ear_inner_x_mm']
    ear_x = (cap['ear_outer_x_mm'] + cap['ear_inner_x_mm']) / 2
    ears = sum((box((ear_width, cap['ear_depth_mm'], height),
                    (sign * ear_x, cap['ear_center_y_mm'], rail_z))
                for sign in [-1, 1]), m.Manifold())
    back = cap['face_front_y'] + cap['face_thickness_mm'] - .1
    tip = cap['rest_tip_y']
    boss_profile = m.CrossSection([[(back, z - .8), (tip, z - .45),
                                   (tip, z + .45), (back, z + .45)]])
    boss = boss_profile.extrude(2).transform(
        [[0, 0, 1, -1], [1, 0, 0, 0], [0, 1, 0, 0]]
    )
    paddle = face + arms + ears + boss

    floor_top = top - height - clearance
    wall_top = top + clearance
    floor_z = floor_top - .4
    wall_height = wall_top - (floor_top - .8)
    wall_z = wall_top - wall_height / 2
    ear_front = cap['ear_center_y_mm'] - cap['ear_depth_mm'] / 2
    ear_back = cap['ear_center_y_mm'] + cap['ear_depth_mm'] / 2
    inward_stop = ear_back + cap['nominal_max_travel_mm']
    pad = button['return_pads']
    backing = pad['backing_front_y_mm']
    assert abs(backing - ear_back - pad['rest_cavity_mm']) < 1e-8
    surround = m.Manifold()
    for sign in [-1, 1]:
        surround += box((7.6, 8.0, .8), (sign * 7.2, -38.6, floor_z))
        surround += box((.8, 6.2, wall_height),
                        (sign * 3.4, -39.1, wall_z))
        surround += box((.8, 2.8, wall_height),
                        (sign * 7.0, -40.9, wall_z))
        # Outward retention, inward stop and foam backing are independent.
        surround += box((4.4, .8, wall_height),
                        (sign * 8.8, ear_front - .4, wall_z))
        surround += box((2.8, .8, wall_height),
                        (sign * 5.2, inward_stop + .4, wall_z))
        surround += box((2.4, .8, wall_height),
                        (sign * 8.8, backing + .4, wall_z))
        surround += box((.8, 4.8, wall_height),
                        (sign * 10.8, -36.9, wall_z))
    # Retain clearance around the existing front PCB capture pads and feet.
    for x, y in p['pcb_capture']['front_pad_centers']:
        surround -= m.Manifold.cylinder(10, 1.6, 1.6, 96).translate((x, y, 0))
    surround ^= m.Manifold.cylinder(
        10, p['base_diameter'] / 2 - .2, p['base_diameter'] / 2 - .2, 192
    )
    # Stay below the bearing outer race: this stationary roof must not touch it.
    roof = box((23.0, 7.7, .8), (0, -38.45, wall_top + .4))
    roof ^= m.Manifold.cylinder(
        20, p['base_diameter'] / 2 - .35, p['base_diameter'] / 2 - .35, 192
    )
    return surround, roof, paddle


def return_pad_solids(p, travel=0):
    """Installed compressed foam and adhesive; front face follows the ear."""
    pad = p['front_button']['return_pads']
    layers = pad['layers_per_pad']
    adhesive = pad['adhesive_per_layer_mm']
    cavity = pad['rest_cavity_mm'] - travel
    foam_depth = cavity / layers - adhesive
    assert foam_depth > 0
    start = pad['backing_front_y_mm'] - cavity
    foam, bonds = m.Manifold(), m.Manifold()
    for x in pad['centers_x_mm']:
        for layer in range(layers):
            y = start + layer * (foam_depth + adhesive)
            foam += box((pad['pad_width_mm'], foam_depth, pad['pad_height_mm']),
                        (x, y + foam_depth / 2, pad['center_z_mm']))
            bonds += box((pad['pad_width_mm'], adhesive, pad['pad_height_mm']),
                         (x, y + foam_depth + adhesive / 2, pad['center_z_mm']))
    return foam, bonds


def return_budget(p):
    pad = p['front_button']['return_pads']
    travel = p['front_button']['printed_cap']['nominal_max_travel_mm']
    free = pad['layers_per_pad'] * pad['layer_thickness_mm']
    adhesive = pad['layers_per_pad'] * pad['adhesive_per_layer_mm']
    error = pad['relative_cavity_error_mm']
    free_min = free * (1 - pad['layer_thickness_tolerance_fraction'])
    free_max = free * (1 + pad['layer_thickness_tolerance_fraction'])
    minimum_preload = free_min + adhesive - pad['adhesive_total_tolerance_mm'] - pad['rest_cavity_mm'] - error
    maximum_compression = 1 - (pad['rest_cavity_mm'] - travel - error - adhesive - pad['adhesive_total_tolerance_mm']) / free_max
    assert minimum_preload > 0, 'Both return pads must remain in contact at rest'
    assert maximum_compression < .60, 'Keep the return foam below the project 60% compression criterion'
    return {
        'minimum_rest_precompression_mm': round(minimum_preload, 4),
        'nominal_rest_compression_percent': round(100 * (1 - (pad['rest_cavity_mm'] - adhesive) / free), 3),
        'nominal_pressed_compression_percent': round(100 * (1 - (pad['rest_cavity_mm'] - travel - adhesive) / free), 3),
        'maximum_tolerance_compression_percent': round(100 * maximum_compression, 3),
        'basis': 'Thickness +/-10%, cavity +/-0.1mm and combined adhesive +/-0.02mm. Compression criterion is an engineering choice, not force/life certification.',
        'physical_return_force_and_life_verified': False,
    }
