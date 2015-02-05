#! /usr/bin/env python
# -*- coding: utf-8 -*-
"""
Created on 22/11/14

@author: Sam Pfeiffer

"""

from bokeh.plotting import *
import random
import time
from bokeh.models.renderers import GlyphRenderer
import sys

MAX_DATA = 200

if len(sys.argv) < 2:
    num_plots = 2
else:
    num_plots = int(sys.argv[1])

print "Going to generate " + str(num_plots) + " dynamically updated plots."

# We will store the data here
plot_dicts = []
for i in range(num_plots):
    mydict = {}
    mydict['x_data'] = []
    mydict['y_data'] = []
    plot_dicts.append(mydict)


output_server("multiple_independent_updateable_plots")

for idx, myplot in enumerate(plot_dicts):
    # Set up plot
    myplot['title'] = "Plot #" + str(idx + 1)
    print "Setting up: " + myplot['title']
    myplot['figure'] = figure(title=myplot['title'])
    myplot['figure'].line(
                          myplot['x_data'],
                          myplot['y_data'],
                          color="#0000FF",
                          tools="pan,resize,wheel_zoom",
                          width=1200,
                          height=300,
                          legend='value of thing'
                          )

# Show plots!
show()

# Set up renderers and datasources
for myplot in plot_dicts:
    print "Setting up renderer for: " + myplot['title']
    myplot['renderer'] = myplot['figure'].select(dict(type=GlyphRenderer))
    myplot['data_source'] = myplot['renderer'][0].data_source

# Set up the dynamic plotting
initial_time = time.time()
last_time = None
while True:

    time_ref = (time.time() - initial_time) % 60
    for idx, myplot in enumerate(plot_dicts):
        if last_time == None:
            last_time = time.time()
        else:
            this_update_time = time.time()
            time_dif = this_update_time - last_time
            last_time = time.time()
            print "Update cycle time: " + str(time_dif) + " seconds."
        print "Updating data for: " + myplot['title']
        myplot['data_source'].data["x"] = myplot['x_data']
        myplot['data_source'].data["y"] = myplot['y_data']
        myplot['data_source']._dirty = True
        # This call is the slowest one
        cursession().store_objects(myplot['data_source'])
        
        # Plotting only the last MAX_DATA samples
        if len(myplot['x_data']) > MAX_DATA:
            myplot['x_data'].pop(0)
            myplot['y_data'].pop(0)
        myplot['x_data'].append(time_ref + idx * 5.0)
        myplot['y_data'].append(random.random())
    time.sleep(0.01)

