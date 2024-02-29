# first demonstration program for controlling Siglent SDG function generator from Python
# G. McBane, 28 Jan 2024
import time  # get functions to make program wait
import visa  #sets up PyVISA for connection through USB


rm = visa.ResourceManager()  # make a resource manager; newer versions might need pyvisa.Res... instead
devlist = rm.list_resources()  # get a list of resources (probably instruments)
print 'VISA resource list:'
print devlist   # and print it.

for  s in devlist:  # look through all devices in the list; s will represent each signature in turn
    print 'checking ', s
    if s.find('SDG')>-1:  # does one of them have 'SDG' in its device signature?
        funcgen =  rm.open_resource(s)  #if so, make a "device" object called funcgen to represent it
        print("Instrument ID:")
        print funcgen.query('*IDN?')  # print device's description of itself
        break  # found what we wanted; leave loop, skipping over 'else' section
else:  # will only arrive here if we never found an SDG device
    print 'Failed to find device on USB connection'  # print error mesage
    exit()   # and quit

# we'll arrive here if we have found a function generator and set it up
# presuming it just woke up, its output will be turned off.  Set up our
# desired waveform before turning it on.

funcgen.write('c1:bswv wvtp,sine')  # use 'basic wave' command to set Channel 1 wavetype to sine wave 
# important possibilities for wavetype are square, sine, ramp, dc

funcgen.write('c1:bswv frq,2000') # use 'basic wave' to set frequency to 2 kHz

# to set amplitude, rather than typing it right in the command, I show how to use a variable and
# insert its value in the command string
ppamp =  2.5 # make a variable to hold amplitude, in volts peak-to-peak
command = 'c1:bswv amp,%5.3f' % ppamp  # the %5.3f will be replaced with the value from ppamp, formatted
# as a 5-space floating point number with 3 digits after the decimal point, like 2.500
print "about to send command: ", command  # should say "about to send command:  c1:bswv amp,2.500"
funcgen.write(command)  # send the command to the device 

# now turn Channel 1 on
funcgen.write('C1:outp on')
# to turn off, use 'outp off' 
print "sine wave should appear"

# At this point a 2.5V peak-to-peak, 2 kHz  sine wave should be appearing at the Channel 1 output.

time.sleep(5)  # wait 5 seconds

funcgen.write('c1:bswv wvtp,square')  # use 'basic wave' to switch to square wave
print "now should be square wave"
time.sleep(5)  # wait 5 seconds
print "Going to end the program now"

# At this point I just let the program end.  The generator should keep running with its square wave output.



