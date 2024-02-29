# demo program showing programming of Agilent 34405/34410 multimeter

import visa  #sets up PyVISA
import time # get functions related to timekeeping ('sleep' is the one we need)

################# Establish communications  #########

rm = visa.ResourceManager()  # make a resource manager
# newer versions of PyVISA might need pyvisa.ResourceManager() instead
devlist = rm.list_resources()  # get a list of resources (instruments)
for  s in devlist:  # look through all devices in the list
    dev =  rm.open_resource(s)  # make a "device" object to represent this instrument
    instr_id = dev.query('*IDN?')  # ask the instrument for its ID
    print 'Found ', instr_id  # tell user what ID this one is
    if instr_id.find('Agilent')>-1 :  # is this the one we are looking for?
        print 'Happy with this instrument; going ahead.' # indicate success
        break  # found what we wanted; leave loop, skipping over 'else' section
    else : # (this else belongs to the 'if') some other instrument; close and try the next one
        print 'You are not my mother.  You are a SNORT.'
        dev.close() # end communication with this device and move to the next in the loop
else:  # (this else belongs to the 'for') will only arrive here if we never found the device we wanted
    print 'Failed to find device'  # print error mesage
    exit()   # and quit

##########  Configure device  ################

# configure for DC voltage readings, 10V range, 0.1 mV resolution
dev.write('CONF:VOLT:DC 10,0.0001')

###########  Make measurements   ###############

NMEAS = 10  # will make 10 voltage readings
WAITTIME = 1.0 # will wait 1 second between each reading

data = []  # make an empty list to hold the readings
for i in range(NMEAS) :
    result = float(dev.query('READ?'))  # make measurement;
    # "float" converts string return from query into real floating-point number
    data.append(result)  # add to data list
    print i, result  # print result on screen
    time.sleep(WAITTIME)  # wait until it's time for next reading

############  End communication with device  ############
dev.close()

######## Store results into a file

filename = raw_input('Enter output file name:  ')  # get name of file from user
log = open(filename,'w')  # open file
print >> log, 'i  \t  voltage '  # write a header line into file
for i in range(NMEAS) :  #  loop over elements of data list
    print >>log, ("%d\t %7.4f" % (i, data[i]))  # write number and then voltage,
    #  one line per data point; \t inserts tab character.  %d in format string produces
    # integer ('digit') format.  %7.4f produces 7-space floating point with 4 digits after decimal.

log.close()  # close file

