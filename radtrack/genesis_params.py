# -*- coding: utf-8 -*-
u"""Mapping of rt_params to genesis_params.

:copyright: Copyright (c) 2015 Bivio Software, Inc.  All Rights Reserved.
:license: http://www.apache.org/licenses/LICENSE-2.0.html
"""
from __future__ import absolute_import, division, print_function, unicode_literals
from io import open

from pykern import pkarray
from pykern.pkdebug import pkdc, pkdp

def to_beam(params):
    '''Convert beam params to dict with Genesis keys'''
    res = dict()
    res['NPART']=params['num_particle']
    res['GAMMA0']=params['gamma']
    res['DELGAM']=params['rms_energy_spread']
    res['RXBEAM']=params['rms_horizontal_width']
    res['RYBEAM']=params['rms_vertical_width']
    res['EMITX']=params['rms_horizontal_emittance']
    res['EMITY']=params['rms_vertical_emittance']
    res['ALPHAX']=params['horizontal_alpha']
    res['ALPHAY']=params['vertical_alpha']
    res['XBEAM']=params['horizontal_coord']
    res['YBEAM']=params['vertical_coord']
    res['PXBEAM']=params['horizontal_angle']
    res['PYBEAM']=params['vertical_angle']
    res['CURPEAK']=params['peak_current']
    res['CUTTAIL']=params['cut_col']
    res['BUNCH']=params['bunch_factor']
    res['BUNCHPHASE']=params['bunch_phase']
    res['EMOD']=params['energy_modulation']
    res['EMODPHASE']=params['energy_modulation_phase']
    res['CONDITX']=params['conditx']
    res['CONDITY']=params['condity']
    
    return res
    
def to_undulator(params):
    '''Convert undulator params to dict with Genesis keys'''
    res = dict()
    res['AW0']=params['undulator_parameter']
    res['XLAMD']=params['period_len']
    res['IWITYP']=params['undulator_type']
    res['XKX']=params['horizontal_focus']
    res['XKY']=params['vertical_focus']
    res['FBESS0']=params['coupling_factor']
    res['NWIG']=params['num_periods']
    res['NSEC']=params['num_section']
    res['AWD']=params['virtual_undulator_parameter']
    res['WCOEFZ(1)']=params['taper_start']
    res['WCOEFZ(2)']=params['taper_field']
    res['WCOEFZ(3)']=params['taper_type']
    res['IERTYP']=params['error_type']
    res['DELAW']=params['error']
    res['ISEED']=params['rng_seed']
    res['AWX']=params['horizontal_misalignment']
    res['AWY']=params['vertical_misalignment']
    
    return res
    
def to_radiation(params):
    '''Convert radiation params to dict with Genesis keys'''    
    res = dict()
    res['XLAMDS']=params['resonant_wavelength']
    res['PRAD0']=params['input_power']
    res['ZRAYL']=params['rayleigh_length']
    res['ZWAIST']=params['rayleigh_waist']
    res['NHARM']=params['num_harmonic']
    res['IALLHARM']=params['all_harmonic']
    res['IHARMSC']=params['harmonic_coupling']
    res['PRADH0']=params['harmonic_power']
    
    return res

def to_particle_loading(params):
    '''Convert particle loading params to dict with Genesis keys'''
    res = dict()
    res['ILDPSI']=params['ham_particle_phase']
    res['ILDGAM']=params['ham_energy_distribution']
    res['ILDX']=params['ham_horizontal_distribution']
    res['ILDY']=params['ham_vertical_distribution']
    res['ILDPX']=params['ham_horizontal_angle']
    res['ILDPY']=params['ham_vertical_angle']
    res['IGAMGAUS']=params['energy_profile']
    res['ITGAUS']=params['trans_profile']
    res['INVERFC']=params['generate_gaus']
    res['IALL']=params['ham_all']
    res['IPSEED']=params['rng_sn_seed']
    res['NBINS']=params['num_bins']
    
    return res
    
def to_mesh(params):
    '''Convert mesh params to dict with Genesis keys'''
    res = dict()
    res['NCAR']=params['num_grid']
    res['LBC']=params['boundary']
    res['RMAX0']=params['auto_grid_size']
    res['DGRID']=params['direct_grid_size']
    res['NSCR']=params['azimuthal_modes']
    res['NPTR']=params['rad_grid']
    res['RMAX0SC']=params['rad_grid_size']
    res['ISCRKUP']=params['sc_calc']
    
    return res
    
def to_focusing(params):
    '''Convert focusing params to dict with Genesis keys'''
    res = dict()
    res['QUADF']=params['focus_strength']
    res['QUADD']=params['defocus_strength']
    res['FL']=params['focus_length']
    res['DL']=params['defocus_length']
    res['DRL']=params['drift_length']
    res['F1ST']=params['focus_length']*params['cell_start'].value
    res['QFDX']=params['max_horizontal_misalignment']
    res['QFDY']=params['max_vertical_misalignment']
    res['SOLEN']=params['solenoid_strength']
    res['SL']=params['solenoid_length']
    
    return res
    
def to_time(params):
    '''Convert time dependence params to dict with Genesis keys'''
    res=dict()
    res['ITDP']=params['set_time_dependent']
    res['CURLEN']=params['bunch_length']
    res['ZSEP']=params['slice_separation']
    res['NSLICE']=params['num_slice']
    res['NTAIL']=params['start_slice']
    res['SHOTNOISE']=params['shotnoise']
    res['ISNTYP']=params['shotnoise_algorithm']
    
    return res
    
def to_sim_control(params):
    '''Convert simulation control params to dict with Genesis keys'''
    res = dict()
    res['DELZ']=params['step_size']
    res['ZSTOP']=params['integration_length']
    res['IORB']=params['orbit_correct']
    res['ISRAVG']=params['energy_loss']
    res['ISRSIG']=params['energy_spread']
    res['ELOSS']=params['eloss']
    
    return res
    
def to_scan(params):
    '''Convert scan params to dict with Genesis keys'''
    res = dict()
    res['ISCAN']=params['scan_variable']
    res['NSCAN']=params['num_scan']
    res['SVAR']=params['scan_range']
    
    return res
    
def to_io_control(params):
    '''Convert io params to dict with Genesis keys'''
    res = dict()
    lout = []
    res['IPHSTY']= params['output_num_step']
    res['ISHSTY']=params['output_num_slice']
    res['IPPART']=params['particle_dist_num_step']
    res['ISPART']=params['particle_dist_num_slice']
    res['IPRADI']=params['field_dist_num_step']
    res['ISRADI']=params['field_dist_num_slice']
    res['IOTAIL']=params['time_window']
    res['OUTPUTFILE']=params['output_filename']
    res['MAGINFILE']=params['mag_input_filename']
    res['MAGOUTFILE']=params['mag_output_filename']
    res['IDUMP']=params['dump_all']
    res['IDMPFLD']=params['dump_field']
    res['IDMPPAR']=params['dump_particle']
    res['BEAMFILE']=params['beam_file']
    res['RADFILE']=params['rad_file']
    res['DISTFILE']=params['phase_file']
    res['NDCUT']=params['ndcut']
    res['FIELDFILE']=params['field_file']
    res['ALIGNRADF']=params['align_rad']
    res['OFFSETRADF']=params['offset_rad']
    res['PARTFILE']=params['part_dist_file']
    res['CONVHARM']=params['convharm']
    res['IBFIELD']=params['chicane_field']
    res['IMAGL']=params['chicane_mag_length']
    res['IDRIL']=params['chicane_drift']
    res['ILOG']=params['log']
    res['FFSPEC']=params['ff_spectrum']
    #res['TRAMA']=params['trama']
    
    #ITRAM TRANSLATOR LOOP THROUGH 36 ELEMENTS OF 6X6 MATRIX TO GENESIS FORM ITRAM##=VALUE
    #if bool(res['TRAMA']) is True:
    #    for i,v enumerate(params['trama']['itram']):
    #        for j,w enumerate(v):
    #            str_key = 'ITRAM'+str(i)+str(j)
    #            res[str_key]=w
                
    #LOOP THROUGH CHILDREN OF OUTPUT_PARAMS TO TURN INTO LIST 
    for key in params['output_parameters']:
        lout.append(int(params['output_parameters'][key]))
        
    res['LOUT']=lout
    
    return res
    
def to_genesis():
    res = dict()

    res['NPART']='num_particle'
    res['GAMMA0']='gamma'
    res['DELGAM']='rms_energy_spread'
    res['RXBEAM']='rms_horizontal_width'
    res['RYBEAM']='rms_vertical_width'
    res['EMITX']='rms_horizontal_emittance'
    res['EMITY']='rms_vertical_emittance'
    res['ALPHAX']='horizontal_alpha'
    res['ALPHAY']='vertical_alpha'
    res['XBEAM']='horizontal_coord'
    res['YBEAM']='vertical_coord'
    res['PXBEAM']='horizontal_angle'
    res['PYBEAM']='vertical_angle'
    res['CURPEAK']='peak_current'
    res['CUTTAIL']='cut_col'
    res['BUNCH']='bunch_factor'
    res['BUNCHPHASE']='bunch_phase'
    res['EMOD']='energy_modulation'
    res['EMODPHASE']='energy_modulation_phase'
    res['CONDITX']='conditx'
    res['CONDITY']='condity'
    res['AW0']='undulator_parameter'
    res['XLAMD']='period_len'
    res['IWITYP']='undulator_type'
    res['XKX']='horizontal_focus'
    res['XKY']='vertical_focus'
    res['FBESS0']='coupling_factor'
    res['NWIG']='num_periods'
    res['NSEC']='num_section'
    res['AWD']='virtual_undulator_parameter'
    res['WCOEFZ(1)']='taper_start'
    res['WCOEFZ(2)']='taper_field'
    res['WCOEFZ(3)']='taper_type'
    res['IERTYP']='error_type'
    res['DELAW']='error'
    res['ISEED']='rng_seed'
    res['AWX']='horizontal_misalignment'
    res['AWY']='vertical_misalignment'
    res['XLAMDS']='resonant_wavelength'
    res['PRAD0']='input_power'
    res['ZRAYL']='rayleigh_length'
    res['ZWAIST']='rayleigh_waist'
    res['NHARM']='num_harmonic'
    res['IALLHARM']='all_harmonic'
    res['IHARMSC']='harmonic_coupling'
    res['PRADH0']='harmonic_power'
    res['ILDPSI']='ham_particle_phase'
    res['ILDGAM']='ham_energy_distribution'
    res['ILDX']='ham_horizontal_distribution'
    res['ILDY']='ham_vertical_distribution'
    res['ILDPX']='ham_horizontal_angle'
    res['ILDPY']='ham_vertical_angle'
    res['IGAMGAUS']='energy_profile'
    res['ITGAUS']='trans_profile'
    res['INVERFC']='generate_gaus'
    res['IALL']='ham_all'
    res['IPSEED']='rng_sn_seed'
    res['NBINS']='num_bins'
    res['NCAR']='num_grid'
    res['LBC']='boundary'
    res['RMAX0']='auto_grid_size'
    res['DGRID']='direct_grid_size'
    res['NSCR']='azimuthal_modes'
    res['NPTR']='rad_grid'
    res['RMAX0SC']='rad_grid_size'
    res['ISCRKUP']='sc_calc'
    res['QUADF']='focus_strength'
    res['QUADD']='defocus_strength'
    res['FL']='focus_length'
    res['DL']='defocus_length'
    res['DRL']='drift_length'
    res['F1ST']='cell_start'
    res['QFDX']='max_horizontal_misalignment'
    res['QFDY']='max_vertical_misalignment'
    res['SOLEN']='solenoid_strength'
    res['SL']='solenoid_length'
    res['ITDP']='set_time_dependent'
    res['CURLEN']='bunch_length'
    res['ZSEP']='slice_separation'
    res['NSLICE']='num_slice'
    res['NTAIL']='start_slice'
    res['SHOTNOISE']='shotnoise'
    res['ISNTYP']='shotnoise_algorithm'
    res['DELZ']='step_size'
    res['ZSTOP']='integration_length'
    res['IORB']='orbit_correct'
    res['ISRAVG']='energy_loss'
    res['ISRSIG']='energy_spread'
    res['ELOSS']='eloss'
    res['ISCAN']='scan_variable'
    res['NSCAN']='num_scan'
    res['SVAR']='scan_range'
    res['IPHSTY']='output_num_step'
    res['ISHSTY']='output_num_slice'
    res['IPPART']='particle_dist_num_step'
    res['ISPART']='particle_dist_num_slice'
    res['IPRADI']='field_dist_num_step'
    res['ISRADI']='field_dist_num_slice'
    res['IOTAIL']='time_window'
    res['OUTPUTFILE']='output_filename'
    res['MAGINFILE']='mag_input_filename'
    res['MAGOUTFILE']='mag_output_filename'
    res['IDUMP']='dump_all'
    res['IDMPFLD']='dump_field'
    res['IDMPPAR']='dump_particle'
    res['BEAMFILE']='beam_file'
    res['RADFILE']='rad_file'
    res['DISTFILE']='phase_file'
    res['NDCUT']='ndcut'
    res['FIELDFILE']='field_file'
    res['ALIGNRADF']='align_rad'
    res['OFFSETRADF']='offset_rad'
    res['PARTFILE']='part_dist_file'
    res['CONVHARM']='convharm'
    res['IBFIELD']='chicane_field'
    res['IMAGL']='chicane_mag_length'
    res['IDRIL']='chicane_drift'
    res['ILOG']='log'
    res['FFSPEC']='ff_spectrum'
    res['LOUT']='output_parameters'
    
    return res
             
