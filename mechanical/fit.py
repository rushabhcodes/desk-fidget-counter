# SPDX-License-Identifier: MIT
"""Engineering fit budget using catalogue facts and user-authorized estimates."""
import math

def evaluate(p):
    b=p['bearing'];m=p['bearing_mount'];f=p['fit_budget'];c=p['pcb_capture']
    diameter_error=f['printed_fit_diameter_error']+f['bearing_diameter_error']
    inner=b['id']-p['bearing_stem_od'];outer=p['bearing_pocket_id']-b['od']
    eccentricity=(inner+outer+2*diameter_error)/2
    print_xy=eccentricity+f['lid_alignment_error']+2*f['printed_surface_error']
    pcb_play=(2.7+f['pcb_hole_diameter_error']-(c['peg_diameter']-f['printed_fit_diameter_error']))/2
    pcb_xy=eccentricity+f['lid_alignment_error']+f['printed_surface_error']+pcb_play+f['smt_position_error']
    gap_min=c['compressed_pad_height']-f['pcb_thickness_error']-f['relative_print_z_error']
    gap_max=c['compressed_pad_height']+f['pcb_thickness_error']+f['relative_print_z_error']
    foam_min=c['uncompressed_pad_height']*(1-c['pad_thickness_tolerance_fraction'])
    foam_max=c['uncompressed_pad_height']*(1+c['pad_thickness_tolerance_fraction'])
    compression_min=foam_min-gap_max+c['adhesive_thickness']-.01
    compression_max=foam_max-gap_min+c['adhesive_thickness']+.01
    sagitta=p['encoder']['track_radius']-math.sqrt(p['encoder']['track_radius']**2-2**2)
    radial_slot=(3-p['encoder']['track_thickness'])/2-pcb_xy-sagitta
    margin_width=f['bearing_width_error']+f['relative_print_z_error']
    values={
      'PCB_peg_min_diametral_clearance_mm':2.7-f['pcb_hole_diameter_error']-c['peg_diameter']-f['printed_fit_diameter_error'],
      'maximum_bearing_radial_eccentricity_mm':eccentricity,
      'fixed_print_to_rotor_xy_budget_mm':print_xy,
      'PCB_to_rotor_xy_budget_mm':pcb_xy,
      'PCB_maximum_in_plane_play_mm':pcb_play,
      'bezel_to_rotor_remaining_radial_clearance_mm':.8-print_xy,
      'optical_fork_remaining_radial_clearance_mm':radial_slot,
      'optical_slot_remaining_vertical_beam_margin_mm':.9-.1-.15-f['pcb_thickness_error']-f['relative_print_z_error']-f['moving_z_check'],
      'screen_glass_remaining_axial_clearance_mm':p['display']['glass_relief_mm']-.1-f['relative_print_z_error'],
      'foam_minimum_compression_mm':compression_min,
      'foam_maximum_compression_percent':100*compression_max/foam_max,
      'foam_nominal_compression_percent':100*(c['uncompressed_pad_height']-c['compressed_pad_height']+c['adhesive_thickness'])/c['uncompressed_pad_height'],
      'USB_plug_to_rotor_min_vertical_clearance_mm':p['knob_bottom_z']-f['moving_z_hardware_check']-p['usb_access']['axis_z']-p['usb_access']['plug_height_mm']/2,
    }
    for key,value in values.items():assert value>0,(key,value)
    assert values['foam_maximum_compression_percent']<60,'Engineering compression criterion, not a supplier operating rating'
    assert print_xy<=f['moving_xy_print_check']+1e-8
    assert pcb_xy<=f['moving_xy_pcb_check']+1e-8
    assert abs(f['moving_z_print_check']-f['bearing_width_error']-f['relative_print_z_error'])<1e-8
    assert abs(f['moving_z_hardware_check']-f['bearing_width_error']-f['pcb_thickness_error']-f['relative_print_z_error'])<1e-8
    return {'basis':'Catalogue boundaries plus explicitly accepted engineering approximations; calibrated print target, not measured process capability.','assumptions':f,'results':{k:round(v,4) for k,v in values.items()},'all_running_margins_positive':True,'push_fit':{'nominal_stem_clearance_mm':inner,'nominal_pocket_clearance_mm':outer,'diameter_uncertainty_mm':diameter_error,'calibration_required':True,'physical_retention_verified':False},'physical_tests':'Not performed; first-build checks remain documented in validation/BRINGUP.md.'}
