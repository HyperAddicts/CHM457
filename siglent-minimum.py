# minimum example for controlling Siglent SDG function generator from Python
# though it's 'minimum', it does accommodate multiple instruments connected to USB and selects
# the SDG function generator; if it doesn't find one, it exits nicely
# G. McBane, 28 Jan 2024


#############   Establish communication   ###############

import visa  #sets up PyVISA for connection through USB
rm = visa.ResourceManager()  # make a resource manager; newer versions might need pyvisa.Res... instead
devlist = rm.list_resources()  # get a list of resources (instruments)
for  s in devlist:  # look through all devices in the list; s will represent each signature in turn
    if s.find('SDG')>-1:  # does one of them have 'SDG' in its device signature?
        funcgen =  rm.open_resource(s)  #if so, make a "device" object called funcgen to represent it
        break  # found what we wanted; leave loop, skipping over 'else' section
else:  # will only arrive here if we never found an SDG device
    print 'Failed to find device on USB connection'  # print error mesage
    exit()   # and quit

# we'll arrive here if we have found a function generator and set it up
# presuming it just woke up, its output will be turned off.  Set up our
# desired waveform before turning it on.

################# Configure Device  ################

funcgen.write('c1:bswv wvtp,sine')  # use 'basic wave' command to set Channel 1 wavetype to sine wave 
# important possibilities for wavetype are square, sine, ramp, dc

funcgen.write('c1:bswv frq,2000') # use 'basic wave' to set frequency to 2 kHz

#################  Start operation  ######################

funcgen.write('C1:outp on')  # turn Channel 1 on
