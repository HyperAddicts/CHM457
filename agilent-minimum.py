# Minimal-ish sample program for Agilent DVM (34405 or 34410).  Made for an ac voltage input;
# reports rms voltage and frequency.

import visa  #sets up PyVISA

################# Establish communications  #########

# This version assumes that the Agilent DVM is the only instrument attached.
# If that's not true, the warranty is void!

rm = visa.ResourceManager()  # make a resource manager
devlist = rm.list_resources()  # get a list of resources (instruments)
dvm =  rm.open_resource(devlist[0])  # make an object named 'dvm' to represent first instrument
dvm.timeout = 3000 # specify 3-second timeout limit
instr_id = dvm.query('*IDN?')  # ask the instrument for its ID
print instr_id  # show it to user

##########  Configure device  ################

# configure for AC voltage readings, 10V range, 0.1 mV resolution
dvm.write('CONF:VOLT:AC 10,0.0001')

###########  Make measurements   ###############
# Read one voltage as already configured
result = dvm.query('READ?')
print "voltage = ", float(result), " Vrms"

# now make frequency measurement, letting instrument self-configure
result = dvm.query('MEAS:freq?')
print "frequency = ", float(result), " Hz"

############  End communication  ##########
dvm.close()



