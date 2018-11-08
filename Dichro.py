# TEST SCRIPT FOR SEEING IF IT IS POSSIBLE TO AUTOMATE A TOMO with 2 polarizations.
import numpy as np

# Filenames
file_name = 'F40N80F80BRot.txt'

# NUM OF TOMOS
# num_of_tomos = 1

# Tomo parameters;
# naming convention date_sampleName_JJoffset_angle_number.xrm
# FF naming convention date_sampleName_JJoffset_FF_number.xrm

date = '20180603'
sample_name_1 = 'F40N80F80BRot'

binning = 1  #set your binning, unit: field of view
exptime1 = 20  #set your exposure time, unit: second
exptime2 = 12
exptime3 = 10
exptimeFF = 3

# define energy
E = 707.4

# define sample & FF positions
X = -89.4
Y = -227.6
Z = -639.1
FF_Z = -1100
FF2_Z = Z #to come back to initial sample positions
FF_X = 1700
FF2_X = X #to come back to initiacl sample positions
#FF_Y = 100

# Define JJ_up & JJ_down
JJU_1 = 0.9 #UP
JJD_1 = -2.2 #UP
JJU_2 = -3.1 #DOWN
JJD_2 = -6.2 #DOWN
JJU_3 = 10 #to open after macro has finished
JJD_3 = -10 #to open after macro has finished
JJ_offset_1 = (JJU_1 + JJD_1) / 2.0
JJ_offset_2 = (JJU_2 + JJD_2) / 2.0

T0 = 0
Tini = -55.5
T_0 = -55
T_1 = -44
T_2 = -24
T_3 = 24
T_4 = 44
T_5 = 55

T_step1 = 1.0
T_step2 = 2.0
FF_T = -45
FF2_T = 0

# Zoneplate Values
ZPz_1 = -11309.1
ZPz_2 = -11307.6

#repetitions = 10
repetitions_FF = 50
wait_time_JJ = 80


###############################################################################
## Aux Functions DO NOT MODIFY
###############################################################################
file_name_collect = '{0}_collect.{1}'.format(*file_name.rsplit('.', 1))
file_name_ff = '{0}_ff.{1}'.format(*file_name.rsplit('.', 1))

# Function: Move select and target
def set_select_and_target(file, select, target):
    # Move select
    file.write('moveto prx %6.2f\n' % select)
    # Move target
    file.write('moveto pry %6.2f\n' % target)


# Function: Move jjs to position 1
def move_to_jj_1(file):
    file.write('moveto phy %6.2f\n' %JJD_1)
    file.write('moveto phx %6.2f\n' %JJU_1)
    file.write('moveto ZPz %6.2f\n' %ZPz_1)
    file.write('wait %d\n' % wait_time_JJ)

# Function: Move jjs to position 2
def move_to_jj_2(file):
    file.write('moveto phy %6.2f\n' %JJD_2)
    file.write('moveto phx %6.2f\n' %JJU_2)
    file.write('moveto ZPz %6.2f\n' %ZPz_2)
    file.write('wait %d\n' % wait_time_JJ)

# Function: Collection for a single angle
def collect_many_repetitions(file, T, counter, repetitions):
    file.write('moveto T %6.2f\n' %T)
    if counter % 2 == 0:
        for j in range(repetitions):
            file.write('collect {0}_{1}_{2}_{3}_{4}.xrm\n'.format(date, sample_name_1, JJ_offset_1, T, j))
        move_to_jj_2(file)
        for j in range(repetitions):
            file.write('collect {0}_{1}_{2}_{3}_{4}.xrm\n'.format(date, sample_name_1, JJ_offset_2, T, j))
    else:
        for j in range(repetitions):
            file.write('collect {0}_{1}_{2}_{3}_{4}.xrm\n'.format(date, sample_name_1, JJ_offset_2, T, j))
        move_to_jj_1(file)
        for j in range(repetitions):
            file.write('collect {0}_{1}_{2}_{3}_{4}.xrm\n'.format(date, sample_name_1, JJ_offset_1, T, j))
    set_select_and_target(file, 1, T)

# Function: Collection for a full angular region
def angular_region_collection(file, repetitions, exptime, T_initial, T_final, T_step):
    counter = 0
    move_to_jj_1(file)
    file.write('setexp ' + str(exptime) + '\n')
    for T in np.arange(T_initial, T_final, T_step):
        collect_many_repetitions(file, T, counter, repetitions)
        counter += 1

def collect_FF(file, extension="FF"):
    file.write('moveto T %6.2f\n' % T0)
    file.write('moveto T %6.2f\n' % FF_T)
    file.write('moveto Z %6.2f\n' % FF_Z)
    file.write('moveto X %6.2f\n' % FF_X)
    file.write('setexp ' + str(exptimeFF) + '\n')
    move_to_jj_1(file)
    for j in range(repetitions_FF):
        file.write('collect {0}_{1}_{2}_{3}_{4}.xrm\n'.format(date, sample_name_1, JJ_offset_1, extension, j))

    move_to_jj_2(file)
    for j in range(repetitions_FF):
        file.write('collect {0}_{1}_{2}_{3}_{4}.xrm\n'.format(date, sample_name_1, JJ_offset_2, extension, j))

###############################################################################



# Define regions to collect
with open(file_name_collect, 'w') as collect_file:
    # Move to Energy: important for preprocessing
    collect_file.write('moveto energy %6.2f\n' % E)
    #### Confirm Sample Position ####
    collect_file.write('moveto X %6.2f\n' % X)
    collect_file.write('moveto Y %6.2f\n' % Y)
    collect_file.write('moveto Z %6.2f\n' % Z)
    #### JU_1, JD_1 ###
    collect_file.write('setbinning ' + str(binning) + '\n')
    set_select_and_target(collect_file, 0, 0)
    collect_file.write('moveto T %6.2f\n' % Tini)
    # You can define new regions below
    angular_region_collection(collect_file, 25, exptime1, T_0, T_1 + T_step1, T_step1)
    angular_region_collection(collect_file, 20, exptime2, T_1 + T_step1, T_2 + T_step1, T_step1)
    angular_region_collection(collect_file, 18, exptime3, T_2 + T_step2, T_3 + T_step2, T_step2)
    angular_region_collection(collect_file, 20, exptime2, T_3 + T_step1, T_4 + T_step1, T_step1)
    angular_region_collection(collect_file, 25, exptime1, T_4 + T_step1, T_5 + T_step1, T_step1)




###############################################################################
## Create microscope collect files DO NOT MODIFY
###############################################################################

# Copy file_name_collect contents in file_name
with open(file_name, 'w') as outfile:
    with open(file_name_collect) as infile:
        outfile.write(infile.read())

# FF Acquisition
with open(file_name_ff, 'w') as ff_file:
    collect_FF(ff_file)

# Copy file_name_collect contents in file_name
with open(file_name, 'a') as outfile:
    with open(file_name_ff) as infile:
        outfile.write(infile.read())

with open(file_name_collect, 'a') as collect_file, open(file_name, 'a') as outfile:
    collect_FF(collect_file, "FF_END")

    collect_file.write('moveto X %6.2f\n' % FF2_X)
    outfile.write('moveto X %6.2f\n' % FF2_X)
    collect_file.write('moveto Z %6.2f\n' % FF2_Z)
    outfile.write('moveto Z %6.2f\n' % FF2_Z)
    collect_file.write('moveto T %6.2f\n' % FF2_T)
    outfile.write('moveto T %6.2f\n' % FF2_T)
    collect_file.write('moveto phy %6.2f\n' % JJD_3)
    outfile.write('moveto phy %6.2f\n' % JJD_3)
    collect_file.write('moveto phx %6.2f\n' % JJU_3)
    outfile.write('moveto phx %6.2f\n' % JJU_3)
###############################################################################
