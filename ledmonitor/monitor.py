#!/usr/bin/env python

##
## ledmonitor
##
##
## Positons:
## 7 - Enviroment (gateway, development, test, production)
##   6 - Role (web, application, server, database)
##     5 - Managed (Yes, No)
##       4 - Storage Load (low, nominal, concern, trouble)
##         3 - Memory Load (low, nominal, concern, trouble)
##           2 - Swap Load (low, nominal, concern, trouble)
##             1 - CPU Load (low, nominal, concern, trouble)
##               0 - Temperature Load (low, nominal, concern, trouble)
##
## Environment state is read from a file in the ledmonitor directory called environment
##      Values include: gateway, development, test, production
##          gateway     - blue
##          development - green
##          test        - yellow
##          production  - purple
##      All other strings will be considered in error and cause the LED to be set to red
##
## Role state is read from a file in the ledmonitor directory called role
##      Values include: web, application, server, database
##          web         - blue
##          application - green
##          server      - yellow
##          database    - purple
##      All other strings will be considered in error and cause the LED to be set to red
##
## Managed state is read from a file in the ledmonitor directory called manage
##      Values include: managed, unmanaged
##          managed     - white
##          unmanaged   - black (off)
##      All other strings will be considered in error and cause the LED to be set to black (off)
##
## RGB Color Values (r, g, b)
## White    255, 255, 255
## Red      255, 0, 0
## Orange   255, 128, 0
## Yellow   255, 255, 0
## Green    0, 255, 0
## Blue     0, 0, 255
## Purple   127, 0, 255
## Pink     255, 0, 255
## Black    0, 0, 0
##      Useful color value information: http://www.rapidtables.com/web/color/RGB_Color.htm

## Set verbose flag to true for LED information to be printed on stdout
##  else set it to False
verbose = False

import time
from subprocess import PIPE, Popen
try:
    import psutil
except ImportError:
    exit("This script requires the psutil module\nInstall with: sudo pip install psutil")

from blinkt import set_clear_on_exit, set_brightness, set_pixel, show, clear

# Make sure that we turn off all the LEDs on exit.
set_clear_on_exit()

## Turn off any LEDs that may be set
clear()

# Brightness is a range from 0 to 1.
# Full brightness is very bright, so we'll set it to its lowest.
set_brightness(0.1)

## Function to set the temperature LED - far right, position 0
## Thermal limit is 85C
##      Low <50% of thermal limit (green)
##      Nominal >50% <70% of thermal limit (yellow)
##      Caution >70% <90% of thermal limit (orange)
##      Danger >90% of thermal limit (red)
def set_temperature_led():
    lp = 0
    process = Popen(['vcgencmd', 'measure_temp'], stdout=PIPE)
    output, _error = process.communicate()
    t = float(output[output.index('=') + 1:output.rindex("'")])
    if t < (85*.5):
        if verbose:
            state = "Low (Green)"
        set_pixel(lp, 0, 255, 0)
    if t > (85*.5) and t < (85*.7):
        if verbose:
            state = "Nominal (Yellow)"
        set_pixel(lp, 255, 255, 0)
    if t > (85*.7) and t < (85*.9):
        if verbose:
            state = "Concern (Orange)"
        set_pixel(lp, 255, 128, 0)
    if t > (85*.9):
        if verbose:
            state = "Trouble (Red)"
        set_pixel(lp, 255, 0, 0)
    if verbose:
        print "CPU Temperature: ", t, "-", state
    return

## Function to set the CPU Load LED - position 1
##      Low <20% of max CPU (green)
##      Nominal >20% <70% of max CPU (yellow)
##      Caution >70% <90% of max CPU (orange)
##      Danger >90% of max CPU(red)
def set_cpu_load_led():
    lp = 1
    cpu_load = psutil.cpu_percent()
    if cpu_load < (100*.2):
        if verbose:
            state = "Low (Green)"
        set_pixel(lp, 0, 255, 0)
    if cpu_load > (100*.2) and cpu_load < (100*.7):
        if verbose:
            state = "Nominal (Yellow)"
        set_pixel(lp, 255, 255, 0)
    if cpu_load > (100*.7) and cpu_load < (100*.9):
        if verbose:
            state = "Concern (Orange)"
        set_pixel(lp, 255, 128, 0)
    if cpu_load > (100*.9):
        if verbose:
            state = "Trouble (Red)"
        set_pixel(lp, 255, 0, 0)
    if verbose:
        print "CPU Load: ", cpu_load, "-", state
    return

## Function to set the SWAP Load LED - position 2
##      Low <10% of max swap (green)
##      Nominal >10% <50% of max swap (yellow)
##      Caution >50% <90% of max swap (orange)
##      Danger >90% of max swap (red)
def set_swap_load_led():
    lp = 2
    swap_load = psutil.swap_memory().percent
    if swap_load < (100*.1):
        if verbose:
            state = "Low (Green)"
        set_pixel(lp, 0, 255, 0)
    if swap_load > (100*.1) and swap_load < (100*.5):
        if verbose:
            state = "Nominal (Yellow)"
        set_pixel(lp, 255, 255, 0)
    if swap_load > (100*.5) and swap_load < (100*.9):
        if verbose:
            state = "Concern (Orange)"
        set_pixel(lp, 255, 128, 0)
    if swap_load > (100*.9):
        if verbose:
            state = "Trouble (Red)"
        set_pixel(lp, 255, 0, 0)
    if verbose:
        print "SWAP Load: ", swap_load, "-", state
    return

## Function to set the MEMORY Load LED - position 3
##      Low <10% of max memory (green)
##      Nominal >10% <50% of max memory (yellow)
##      Caution >50% <90% of max memory (orange)
##      Danger >90% of max memory (red)
def set_memory_load_led():
    lp = 3
    memory_load = psutil.virtual_memory().percent
    if memory_load < (100*.1):
        if verbose:
            state = "Low (Green)"
        set_pixel(lp, 0, 255, 0)
    if memory_load > (100*.1) and memory_load < (100*.5):
        if verbose:
            state = "Nominal (Yellow)"
        set_pixel(lp, 255, 255, 0)
    if memory_load > (100*.5) and memory_load < (100*.9):
        if verbose:
            state = "Concern (Orange)"
        set_pixel(lp, 255, 128, 0)
    if memory_load > (100*.9):
        if verbose:
            state = "Trouble (Red)"
        set_pixel(lp, 255, 0, 0)
    if verbose:
        print "Memory Load: ", memory_load, "-", state
    return

## Function to set the STORAGE Load LED - position 4
##      Low <20% of max storage (green)
##      Nominal >20% <70% of max storage (yellow)
##      Caution >70% <90% of max storage (orange)
##      Danger >90% of max storage (red)
def set_storage_load_led():
    lp = 4
    storage_load = psutil.disk_usage('/').percent
    if storage_load < (100*.2):
        if verbose:
            state = "Low (Green)"
        set_pixel(lp, 0, 255, 0)
    if storage_load > (100*.2) and storage_load < (100*.7):
        if verbose:
            state = "Nominal (Yellow)"
        set_pixel(lp, 255, 255, 0)
    if storage_load > (100*.7) and storage_load < (100*.9):
        if verbose:
            state = "Concern (Orange)"
        set_pixel(lp, 255, 128, 0)
    if storage_load > (100*.9):
        if verbose:
            state = "Trouble (Red)"
        set_pixel(lp, 255, 0, 0)
    if verbose:
        print "Storage Load: ", storage_load, "-", state
    return

## Function to set the MANAGE state LED - position 5
##      managed (white)
##      unmanaged (black - off)
##
##      Any other values or a missing file are an error and will be shown as red
def set_manage_state_led():
    lp = 5
    try:
        contents = open('./manage.state', 'r').read()
    except:
        contents = "error"
    if contents.strip() == "managed":
        set_pixel(lp, 255, 255, 255)
        if verbose:
            state = "Managed (White)"
    elif contents.strip() == "unmanaged":
        set_pixel(lp, 0, 0, 0)
        if verbose:
            state = "Unmanaged (Black)"
    else:
        state = "Error (Red)"
        set_pixel(lp, 255, 0, 0)
    if verbose:
        print "Managed state: ", state
    return

## Function to set the ROLE state LED - position 6
##          web         (blue)
##          application (green)
##          server      (yellow)
##          database    (purple)
##
##      Any other values or a missing file are an error and will be shown as red
def set_role_state_led():
    lp = 6
    try:
        contents = open('./role.state', 'r').read()
    except:
        contents = "error"
    if contents.strip() == "web":
        set_pixel(lp, 0, 0, 255)
        if verbose:
            state = "Web (Blue)"
    elif contents.strip() == "application":
        set_pixel(lp, 0, 255, 0)
        if verbose:
            state = "application (Green)"
    elif contents.strip() == "server":
        set_pixel(lp, 255, 255, 0)
        if verbose:
            state = "server (Yellow)"
    elif contents.strip() == "database":
        set_pixel(lp, 127, 0, 255)
        if verbose:
            state = "database (Purple)"
    else:
        state = "Error (Red)"
        set_pixel(lp, 255, 0, 0)
    if verbose:
        print "Role state: ", state
    return

## Function to set the ENVIRONMENT state LED - position 7
##          gateway     (blue)
##          development (green)
##          test        (yellow)
##          production  (purple)
##
##      Any other values or a missing file are an error and will be shown as red
def set_environment_state_led():
    lp = 7
    try:
        contents = open('./environment.state', 'r').read()
    except:
        contents = "error"
    if contents.strip() == "gateway":
        set_pixel(lp, 0, 0, 255)
        if verbose:
            state = "Gateway (Blue)"
    elif contents.strip() == "development":
        set_pixel(lp, 0, 255, 0)
        if verbose:
            state = "Development (Green)"
    elif contents.strip() == "test":
        set_pixel(lp, 255, 255, 0)
        if verbose:
            state = "Test (Yellow)"
    elif contents.strip() == "production":
        set_pixel(lp, 127, 0, 255)
        if verbose:
            state = "Production (Purple)"
    else:
        state = "Error (Red)"
        set_pixel(lp, 255, 0, 0)
    if verbose:
        print "Environment state: ", state
    return

## Main loop
while True:
    if verbose:
        print
    set_temperature_led()
    set_cpu_load_led()
    set_swap_load_led()
    set_memory_load_led()
    set_storage_load_led()
    set_manage_state_led()
    set_role_state_led()
    set_environment_state_led()

    show()
    time.sleep(1)
