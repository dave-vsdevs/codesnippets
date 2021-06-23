import sys
import time

import pexpect
import re
import os
import random


MODES=[     "Atomic swirl",
            "Blue mood blobs",
            "Breath",
            "Candle",
            "Cinema brighten lights",
            "Cinema dim lights",
            "Cold mood blobs",
            "Collision",
            "Color traces",
            "Double swirl",
            "Fire",
            "Flags Germany/Sweden",
            "Full color mood blobs",
            "Green mood blobs",
            "Knight rider",
            "Led Test",
            "Light clock",
            "Lights",
            "Notify blue",
            "Pac-Man",
            "Plasma",
            "Police Lights Single",
            "Police Lights Solid",
            "Rainbow mood",
            "Rainbow swirl",
            "Rainbow swirl fast",
            "Random",
            "Red mood blobs",
            "Sea waves",
            "Snake",
            "Sparks",
            "Strobe red",
            "Strobe white",
            "System Shutdown",
            "Trails",
            "Trails color",
            "Warm mood blobs",
            "Waves with Color",
            "X-Mas"]




SLEEP_SEC  = .5 # Amount of time to sleep between loop iterations.


# Get bulb address from command parameters.
if len(sys.argv) != 2:
    print('Error must specify flip address as parameter!')
    print('Usage: sudo python flip_facet.py <address>')
    print('Example: sudo python flip_facet.py 0C:61:CF:C7:8B:F3')
    sys.exit(1)
flip = sys.argv[1]

# Run gatttool interactively.
gatt = pexpect.spawn('gatttool -I')
gatt.logfile_read = sys.stdout.buffer

# Connect to the device.
gatt.sendline('connect {0}'.format(flip))
gatt.expect('Connection successful')

# Setup range of hue value and start at minimum hue.

gatt.sendline('char-write-req 0x0025 303030303030')
gatt.expect('Characteristic value was written successfully')
time.sleep(1)
gatt.sendline('char-write-req 0x001a 0100')
gatt.expect('Characteristic value was written successfully')

picked={}

# Enter main loop.
print('Press Ctrl-C to quit.')
last = time.time()
while True:
    # Get amount of time elapsed since last update, then compute hue delta.
    now = time.time()
    #gatt.sendline('char-read-uuid F1196F52-71A4-11E6-BDF4-0800200C9A66')
    try:
        gatt.expect('Notification handle = .*')
        #print(str(gatt.before))
        print('+------------')
        print(str(gatt.after))
        m=re.search(r"value:.(0[0-9a-fA-F])",gatt.after.decode("utf-8") )
        print(m.group(1))

        facet=m.group(1)
            
        if(facet=="03"):
            os.system('/usr/bin/hyperion-remote --clearall')
        else:
            try:
                mode=picked[facet]
            except:
                mode=random.choice(MODES)
                picked[facet]=mode
                
            os.system('/usr/bin/hyperion-remote --effect "%s"' % mode)
            
        print('-------------')
    except pexpect.exceptions.TIMEOUT:
        pass
        # IF we want to not block
    
    # Wait a short period of time and setup for the next loop iteration.
    time.sleep(SLEEP_SEC)
    last = now
