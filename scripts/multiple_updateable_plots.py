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

MAX_DATA = 20

# We will store the data here
x_data = []
y_data = []

x_data2 = []
y_data2 = []

output_server("multiple_updateable_plots")

# Set up first plot
p1 = figure(title="First plot")
p1.line(x_data, y_data,
    color="#0000FF",
    tools="pan,resize,wheel_zoom", width=1200,height=300,
    legend='value of thing')

# Set up second plot
p2 = figure(title="Second plot")
p2.line(x_data2, y_data2, 
    color="#00FFFF",
    tools="pan,resize,wheel_zoom", width=1200,height=300,
    legend='value of thing')

# Show plots!
show()

# Set up the dynamic plotting
renderer1 = p1.select(dict(type=GlyphRenderer))
renderer2 = p2.select(dict(type=GlyphRenderer))
ds1 = renderer1[0].data_source
ds2 = renderer2[0].data_source
while True:
    time_ref = time.time() % 60
    ds1.data["x"] = x_data
    ds1.data["y"] = y_data
    ds1._dirty = True
    cursession().store_objects(ds1)
    ds2.data["x"] = x_data2
    ds2.data["y"] = y_data2
    ds2._dirty = True
    cursession().store_objects(ds2)
    
    # Plotting only the last MAX_DATA samples
    if len(x_data) > MAX_DATA:
        x_data.pop(0)
        y_data.pop(0)
        x_data2.pop(0)
        y_data2.pop(0)
    x_data.append(time_ref)
    x_data2.append(time_ref + 10.0)

    y_data.append(random.random())
    y_data2.append(random.random()) 
    time.sleep(0.1)

