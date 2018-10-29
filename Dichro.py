# TEST SCRIPT FOR SEEING IF IT IS POSSIBLE TO AUTOMATE A TOMO with 2 polarizations.

import numpy as np

# Filenames
file_name = 'dichro.txt'  
file_name_jj_one = 'dichro_jj_one.txt'  
file_name_jj_two = 'dichro_jj_two.txt'  


# NUM OF TOMOS
#num_of_tomos = 1
  

# Tomo parameters; 
# naming convention date_sampleName_JJoffset_angle_number.xrm
# FF naming convention date_sampleName_JJoffset_FF_number.xrm

date = '20180531'  
sample_name_1 = 'name'

binning = 1  #set your binning, unit: field of view 
exptime1 = 8  #set your exposure time, unit: second
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
FF2_Z = Z #to come back to initial sample positions
FF_X = 1700
FF2_X = X #to come back to initiacl sample positions
#FF_Y = 100

# Define JJ_up & JJ_down
JJU_1 = 0.9 #UP
JJD_1 = -2.1 #UP
JJU_2 = -3.2 #DOWN
JJD_2 = -6.2 #DOWN
JJU_3 = 10 #to open after macro has finished
JJD_3 = -10 #to open after macro has finished
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

f = open(file_name, 'w')

# Move to Energy: important for preprocessing
f.write('moveto energy %6.2f\n' %E)

#### Confirm Sample Position ####
f.write('moveto X %6.2f\n' %X) 
f.write('moveto Y %6.2f\n' %Y)
f.write('moveto Z %6.2f\n' %Z)

#### JU_1, JD_1 ###

f.write('setbinning ' + str(binning) + '\n')

f.write('moveto T %6.2f\n' %Tini)

for T in np.arange(T_0, T_1+T_step, T_step):
    f.write('setexp ' + str(exptime1) + '\n')
    f.write('moveto T %6.2f\n' %T)
    f.write('moveto phy %6.2f\n' %JJU_1)
    f.write('moveto phx %6.2f\n' %JJD_1)
    f.write('wait 80\n')
    for j in range(repetitions):
        f.write('collect {0}_{1}_{2}_{3}_{4}.xrm\n'.format(date, sample_name_1, JJ_offset_1, T, j))
    f.write('moveto phy %6.2f\n' %JJU_2)
    f.write('moveto phx %6.2f\n' %JJD_2)
    f.write('wait 80\n')
    for j in range(repetitions):
        f.write('collect {0}_{1}_{2}_{3}_{4}.xrm\n'.format(date, sample_name_1, JJ_offset_2, T, j)) 
    T = T + T_step

for T in np.arange(T_1+T_step, T_2+T_step, T_step):
    f.write('setexp ' + str(exptime2) + '\n')
    f.write('moveto T %6.2f\n' %T)
    f.write('moveto phy %6.2f\n' %JJU_1)
    f.write('moveto phx %6.2f\n' %JJD_1)
    f.write('wait 80\n')
    for j in range(repetitions):
        f.write('collect {0}_{1}_{2}_{3}_{4}.xrm\n'.format(date, sample_name_1, JJ_offset_1, T, j))
    f.write('moveto phy %6.2f\n' %JJU_2)
    f.write('moveto phx %6.2f\n' %JJD_2)
    f.write('wait 80\n')
    for j in range(repetitions):
        f.write('collect {0}_{1}_{2}_{3}_{4}.xrm\n'.format(date, sample_name_1, JJ_offset_2, T, j)) 
    T = T + T_step

for T in np.arange(T_2+T_step, T_3+T_step, T_step):
    f.write('setexp ' + str(exptime3) + '\n')
    f.write('moveto T %6.2f\n' %T)
    f.write('moveto phy %6.2f\n' %JJU_1)
    f.write('moveto phx %6.2f\n' %JJD_1)
    f.write('wait 80\n')
    for j in range(repetitions):
        f.write('collect {0}_{1}_{2}_{3}_{4}.xrm\n'.format(date, sample_name_1, JJ_offset_1, T, j))
    f.write('moveto phy %6.2f\n' %JJU_2)
    f.write('moveto phx %6.2f\n' %JJD_2)
    f.write('wait 80\n')
    for j in range(repetitions):
        f.write('collect {0}_{1}_{2}_{3}_{4}.xrm\n'.format(date, sample_name_1, JJ_offset_2, T, j)) 
    T = T + T_step

f.write('moveto T %6.2f\n' %T0)
   

# FF Acquisition
f.write('moveto T %6.2f\n' %FF_T)
f.write('moveto Z %6.2f\n' %FF_Z) 
f.write('moveto X %6.2f\n' %FF_X)
f.write('setexp ' + str(exptimeFF) + '\n')
for j in range(repetitions_FF):
    f.write('collect {0}_{1}_{2}_{3}_{4}.xrm\n'.format(date, sample_name_1, JJ_offset_2, "FF", j))

f.write('moveto phy %6.2f\n' %JJU_1)
f.write('moveto phx %6.2f\n' %JJD_1)
f.write('wait 80\n')
for j in range(repetitions_FF):
    f.write('collect {0}_{1}_{2}_{3}_{4}.xrm\n'.format(date, sample_name_1, JJ_offset_1, "FF", j))

f.write('moveto X %6.2f\n' %FF2_X)
f.write('moveto Z %6.2f\n' %FF2_Z)
f.write('moveto T %6.2f\n' %FF2_T)
f.write('moveto phy %6.2f\n' %JJU_3)
f.write('moveto phx %6.2f\n' %JJD_3)

f.close()





####### File necessary for preprocessing of second JJ positions: JJ_offset_1 ###

f = open(file_name_jj_one, 'w')

# Move to Energy: important for preprocessing
f.write('moveto energy %6.2f\n' %E)

#### Confirm Sample Position ####
f.write('moveto X %6.2f\n' %X) 
f.write('moveto Y %6.2f\n' %Y)
f.write('moveto Z %6.2f\n' %Z)
f.write('setbinning ' + str(binning) + '\n')

f.write('moveto T %6.2f\n' %Tini)

for T in np.arange(T_0, T_1+T_step, T_step):
    f.write('setexp ' + str(exptime1) + '\n')
    f.write('moveto T %6.2f\n' %T)
    f.write('moveto phy %6.2f\n' %JJU_1)
    f.write('moveto phx %6.2f\n' %JJD_1)
    for j in range(repetitions):
        f.write('collect {0}_{1}_{2}_{3}_{4}.xrm\n'.format(date, sample_name_1, JJ_offset_1, T, j))
    T = T + T_step

for T in np.arange(T_1+T_step, T_2+T_step, T_step):
    f.write('setexp ' + str(exptime2) + '\n')
    f.write('moveto T %6.2f\n' %T)
    f.write('moveto phy %6.2f\n' %JJU_1)
    f.write('moveto phx %6.2f\n' %JJD_1)
    for j in range(repetitions):
        f.write('collect {0}_{1}_{2}_{3}_{4}.xrm\n'.format(date, sample_name_1, JJ_offset_1, T, j))
    T = T + T_step

for T in np.arange(T_2+T_step, T_3+T_step, T_step):
    f.write('setexp ' + str(exptime3) + '\n')
    f.write('moveto T %6.2f\n' %T)
    f.write('moveto phy %6.2f\n' %JJU_1)
    f.write('moveto phx %6.2f\n' %JJD_1)
    for j in range(repetitions):
        f.write('collect {0}_{1}_{2}_{3}_{4}.xrm\n'.format(date, sample_name_1, JJ_offset_1, T, j))
    T = T + T_step

f.write('moveto T %6.2f\n' %T0)

# FF Acquisition
f.write('moveto T %6.2f\n' %FF_T)
f.write('moveto Z %6.2f\n' %FF_Z) 
f.write('moveto X %6.2f\n' %FF_X)
f.write('setexp ' + str(exptimeFF) + '\n')
f.write('moveto phy %6.2f\n' %JJU_1)
f.write('moveto phx %6.2f\n' %JJD_1)
for j in range(repetitions_FF):
    f.write('collect {0}_{1}_{2}_{3}_{4}.xrm\n'.format(date, sample_name_1, JJ_offset_1, "FF", j))

f.close()



####### File necessary for preprocessing of second JJ positions: JJ_offset_2 ###

f = open(file_name_jj_two, 'w')

# Move to Energy: important for preprocessing
f.write('moveto energy %6.2f\n' %E)

#### Confirm Sample Position ####
f.write('moveto X %6.2f\n' %X) 
f.write('moveto Y %6.2f\n' %Y)
f.write('moveto Z %6.2f\n' %Z)
f.write('setbinning ' + str(binning) + '\n')

f.write('moveto T %6.2f\n' %Tini)

for T in np.arange(T_0, T_1+T_step, T_step):
    f.write('setexp ' + str(exptime1) + '\n')
    f.write('moveto T %6.2f\n' %T)
    f.write('moveto phy %6.2f\n' %JJU_2)
    f.write('moveto phx %6.2f\n' %JJD_2)
    for j in range(repetitions):
        f.write('collect {0}_{1}_{2}_{3}_{4}.xrm\n'.format(date, sample_name_1, JJ_offset_2, T, j)) 
    T = T + T_step

for T in np.arange(T_1+T_step, T_2+T_step, T_step):
    f.write('setexp ' + str(exptime2) + '\n')
    f.write('moveto T %6.2f\n' %T)
    f.write('moveto phy %6.2f\n' %JJU_2)
    f.write('moveto phx %6.2f\n' %JJD_2)
    for j in range(repetitions):
        f.write('collect {0}_{1}_{2}_{3}_{4}.xrm\n'.format(date, sample_name_1, JJ_offset_2, T, j)) 
    T = T + T_step

for T in np.arange(T_2+T_step, T_3+T_step, T_step):
    f.write('setexp ' + str(exptime3) + '\n')
    f.write('moveto T %6.2f\n' %T)
    f.write('moveto phy %6.2f\n' %JJU_2)
    f.write('moveto phx %6.2f\n' %JJD_2)
    for j in range(repetitions):
        f.write('collect {0}_{1}_{2}_{3}_{4}.xrm\n'.format(date, sample_name_1, JJ_offset_2, T, j)) 
    T = T + T_step

f.write('moveto T %6.2f\n' %T0)

# FF Acquisition
f.write('moveto T %6.2f\n' %FF_T)
f.write('moveto Z %6.2f\n' %FF_Z) 
f.write('moveto X %6.2f\n' %FF_X)
f.write('setexp ' + str(exptimeFF) + '\n')
f.write('moveto phy %6.2f\n' %JJU_2)
f.write('moveto phx %6.2f\n' %JJD_2)
for j in range(repetitions_FF):
    f.write('collect {0}_{1}_{2}_{3}_{4}.xrm\n'.format(date, sample_name_1, JJ_offset_2, "FF", j))

f.close()


