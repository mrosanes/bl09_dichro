# TEST SCRIPT FOR SEEING IF IT IS POSSIBLE TO AUTOMATE A TOMO with 2 polarizations.

import numpy as np

# Filenames
file_name = 'dichro.txt'
file_name_collect = '{0}_collect.{1}'.format(*file_name.rsplit('.', 1))
file_name_ff = '{0}_ff.{1}'.format(*file_name.rsplit('.', 1))
# NUM OF TOMOS
# num_of_tomos = 1

# TODO Why this naming convention? it does not follow manytomos naming
# Tomo parameters;
# naming convention date_sampleName_JJoffset_angle_number.xrm
# FF naming convention date_sampleName_JJoffset_FF_number.xrm

date = '20180531'
sample_name_1 = 'name'

binning = 1  # set your binning, unit: field of view
exptime1 = 8  # set your exposure time, unit: second
exptime2 = 8
exptime3 = 10
exptimeFF = 3

# define energy
E = 707.4

# define sample & FF positions
X = 22
Y = 435.3
Z = -600
FF_Z = -1000
FF2_Z = Z  # to come back to initial sample positions
FF_X = 1700
FF2_X = X  # to come back to initiacl sample positions
# FF_Y = 100

# Define JJ_up & JJ_down
JJU_1 = 0.9  # UP
JJD_1 = -2.1  # UP
JJU_2 = -3.2  # DOWN
JJD_2 = -6.2  # DOWN
JJU_3 = 10  # to open after macro has finished
JJD_3 = -10  # to open after macro has finished
JJ_offset_1 = (JJU_1 + JJD_1) / 2.0
JJ_offset_2 = (JJU_2 + JJD_2) / 2.0

T0 = 0
Tini = -55
T_0 = -54
T_1 = -40
T_2 = 40
T_3 = 54
T_step = 2.0
FF_T = -45
FF2_T = 0

repetitions = 10
repetitions_FF = 10


def set_select_and_target(file, select, target):
    # Move select
    file.write('moveto prx %6.2f\n' % select)
    # Move target
    file.write('moveto pry %6.2f\n' % target)


with open(file_name_collect, 'w') as f:
    # Move to Energy: important for preprocessing
    f.write('moveto energy %6.2f\n' % E)

    #### Confirm Sample Position ####
    f.write('moveto X %6.2f\n' % X)
    f.write('moveto Y %6.2f\n' % Y)
    f.write('moveto Z %6.2f\n' % Z)

    #### JU_1, JD_1 ###

    f.write('setbinning ' + str(binning) + '\n')

    set_select_and_target(f, 0, 0)
    f.write('moveto T %6.2f\n' % Tini)

    for T in np.arange(T_0, T_1 + T_step, T_step):
        f.write('setexp ' + str(exptime1) + '\n')
        f.write('moveto T %6.2f\n' % T)
        f.write('moveto phy %6.2f\n' % JJU_1)
        f.write('moveto phx %6.2f\n' % JJD_1)
        f.write('wait 80\n')
        for j in range(repetitions):
            f.write('collect {0}_{1}_{2}_{3}_{4}.xrm\n'.format(date, sample_name_1, JJ_offset_1, T, j))
        f.write('moveto phy %6.2f\n' % JJU_2)
        f.write('moveto phx %6.2f\n' % JJD_2)
        f.write('wait 80\n')
        for j in range(repetitions):
            f.write('collect {0}_{1}_{2}_{3}_{4}.xrm\n'.format(date, sample_name_1, JJ_offset_2, T, j))
        set_select_and_target(f, 1, T)

    for T in np.arange(T_1 + T_step, T_2 + T_step, T_step):
        f.write('setexp ' + str(exptime2) + '\n')
        f.write('moveto T %6.2f\n' % T)
        f.write('moveto phy %6.2f\n' % JJU_1)
        f.write('moveto phx %6.2f\n' % JJD_1)
        f.write('wait 80\n')
        for j in range(repetitions):
            f.write('collect {0}_{1}_{2}_{3}_{4}.xrm\n'.format(date, sample_name_1, JJ_offset_1, T, j))
        f.write('moveto phy %6.2f\n' % JJU_2)
        f.write('moveto phx %6.2f\n' % JJD_2)
        f.write('wait 80\n')
        for j in range(repetitions):
            f.write('collect {0}_{1}_{2}_{3}_{4}.xrm\n'.format(date, sample_name_1, JJ_offset_2, T, j))
        set_select_and_target(f, 1, T)

    for T in np.arange(T_2 + T_step, T_3 + T_step, T_step):
        f.write('setexp ' + str(exptime3) + '\n')
        f.write('moveto T %6.2f\n' % T)
        f.write('moveto phy %6.2f\n' % JJU_1)
        f.write('moveto phx %6.2f\n' % JJD_1)
        f.write('wait 80\n')
        for j in range(repetitions):
            f.write('collect {0}_{1}_{2}_{3}_{4}.xrm\n'.format(date, sample_name_1, JJ_offset_1, T, j))
        f.write('moveto phy %6.2f\n' % JJU_2)
        f.write('moveto phx %6.2f\n' % JJD_2)
        f.write('wait 80\n')
        for j in range(repetitions):
            f.write('collect {0}_{1}_{2}_{3}_{4}.xrm\n'.format(date, sample_name_1, JJ_offset_2, T, j))
        set_select_and_target(f, 1, T)

# Copy file_name_collect contents in file_name
with open(file_name, 'w') as outfile:
    with open(file_name_collect) as infile:
        outfile.write(infile.read())

# FF Acquisition
with open(file_name_ff, 'w') as ff_file:
    # TODO is it need?
    ff_file.write('moveto T %6.2f\n' % T0)
    ff_file.write('moveto T %6.2f\n' % FF_T)
    ff_file.write('moveto Z %6.2f\n' % FF_Z)
    ff_file.write('moveto X %6.2f\n' % FF_X)
    ff_file.write('setexp ' + str(exptimeFF) + '\n')
    for j in range(repetitions_FF):
        ff_file.write('collect {0}_{1}_{2}_{3}_{4}.xrm\n'.format(date, sample_name_1, JJ_offset_2, "FF", j))

    ff_file.write('moveto phy %6.2f\n' % JJU_1)
    ff_file.write('moveto phx %6.2f\n' % JJD_1)
    ff_file.write('wait 80\n')
    for j in range(repetitions_FF):
        ff_file.write('collect {0}_{1}_{2}_{3}_{4}.xrm\n'.format(date, sample_name_1, JJ_offset_1, "FF", j))

# Copy file_name_collect contents in file_name
with open(file_name, 'a') as outfile:
    with open(file_name_ff) as infile:
        outfile.write(infile.read())

# TODO is it need?
with open(file_name_collect, 'a') as collect_file, open(file_name, 'a') as outfile:
    collect_file.write('moveto X %6.2f\n' % FF2_X)
    outfile.write('moveto X %6.2f\n' % FF2_X)
    collect_file.write('moveto Z %6.2f\n' % FF2_Z)
    outfile.write('moveto Z %6.2f\n' % FF2_Z)
    collect_file.write('moveto T %6.2f\n' % FF2_T)
    outfile.write('moveto T %6.2f\n' % FF2_T)
    collect_file.write('moveto phy %6.2f\n' % JJU_3)
    outfile.write('moveto phy %6.2f\n' % JJU_3)
    collect_file.write('moveto phx %6.2f\n' % JJD_3)
    outfile.write('moveto phx %6.2f\n' % JJD_3)
