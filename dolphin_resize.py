#! /usr/bin/env python
# -*- coding: Utf-8 -*-
# resize dolphin window according to number of files in current location

### SETTINGS ###
SMOOTHNESS = False
MAX_SMOOTH_CHANGE = 100*100;

MAX_FILES_COUNT   = 55

MAX_ROWS_COUNT    = 6 # limited by screen dimensions
MIN_COLUMNS_COUNT = 4 # comfort

MIN_WIDTH         = 50
MIN_HEIGHT        = 150

COLUMN_WIDTH      = 115
ROW_HEIGHT        = 90

### IMPORTS ###
from sys import argv
from os import popen as bashexec
from commands import getoutput as bashget
from math import sqrt

### FUNCTIONS ###
# concatenate list elements to str
def list_to_str(list_, sep=''):
    _ = str();
    for element in list_:
        _ += element + sep
    return _;

# resize window
def resizew(window_properties, new_width=0, new_height=0, maximum=False, smooth=False):
    #pre
    if new_width == window_properties['width'] and new_height == window_properties['height']:
        print "Window is already the correct size."
        return;
    #/pre
    
    # full size 
    if maximum:
        bashexec("xdotool windowsize $(xdotool getactivewindow) 100% 100%");
        print "Max'd";
        return;
    
    if not smooth:
        bashexec("wmctrl -r ':ACTIVE:' -e 0,%d,%d,%d,%d" % (window_properties['x'], window_properties['y'], new_width, new_height) )
        # TODO rough resizing
    if smooth:
        print "Smooth resizing...";
        old_width = window_properties['width'];
        old_height = window_properties['height'];
        for w in xrange(old_width, new_width, (new_width-old_width+1)/abs(new_width-old_width+1)): # +1/+1 to avoid ZeroDivisionError #ugly
            resizew(window_properties, w, old_height, smooth=False);
        for h in xrange(old_height, new_height, (new_height-old_height)/abs(new_height-old_height)):
            resizew(window_properties, new_width, h, smooth=False);

### ASSIGNMENTS ###
# get the active window
active_id = int(bashget('xdotool getactivewindow'));

active_id_hex = "0x" + str(hex(active_id)).split("0x")[-1].zfill(8);

active_properties_raw = bashget("wmctrl -lxpG | grep %s" % active_id_hex);

#if not dolphin window : exit
if active_properties_raw.find('dolphin.dolphin') < 0: exit(0);

active_properties_list = [ p for p in active_properties_raw.split(' ') if p]

active_properties = {
    'id':active_properties_list[0],
    'gravity':int(active_properties_list[1]),
    'pid':int(active_properties_list[2]),
    'x':int(active_properties_list[3]),
    'y':int(active_properties_list[4]),
    'width':int(active_properties_list[5]),
    'height':int(active_properties_list[6]),
    'pname':active_properties_list[7],
    'n/a':active_properties_list[8],
    'wname_list':active_properties_list[9:]
    }

active_properties['current_uri'] = list_to_str(list_to_str(active_properties['wname_list'], ' ').split('\xe2\x80\x94')[:-1], ' ').rstrip();

files_count = int(bashget('ls -l "%s" | wc -l' % active_properties['current_uri'])) - 1;


### MAIN ###

# Too much files: fullscreen && exit
if files_count > MAX_FILES_COUNT: resizew(active_properties, maximum=True); print "A lot of files (%d), window has been maximised" % files_count; exit(0);

if files_count < 1 : print "No file in here."; exit(0);

#rows_count = int(float(files_count + MIN_COLUMNS_COUNT - 1) / MIN_COLUMNS_COUNT); # FIXME max is MAX_ROWS_COUNT
rows_count = int(sqrt(files_count));
rows_count = min([rows_count, MAX_ROWS_COUNT]);

columns_count = int(float(files_count) / rows_count + 1); # FIXME min is MIN__COLUMNS_COUNT

print "There are %d files in %s. They will be displayed as %d columns and %d rows." % (files_count, active_properties['current_uri'], columns_count, rows_count);

# compute new window size
width = MIN_WIDTH + COLUMN_WIDTH * columns_count;

height = MIN_HEIGHT +  ROW_HEIGHT * rows_count;


change_in_dimension = abs(width-active_properties['width'])*abs(height-active_properties['height']);

if argv[-1] == 'smooth' or change_in_dimension < MAX_SMOOTH_CHANGE : SMOOTHNESS = True;


resizew(active_properties, width, height, smooth=SMOOTHNESS);

exit(0);
