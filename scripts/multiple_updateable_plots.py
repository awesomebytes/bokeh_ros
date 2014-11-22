#! /usr/bin/env python
# -*- coding: utf-8 -*-
"""
Created on 22/11/14

@author: Sam Pfeiffer

"""

from bokeh.plotting import *
from bokeh.objects import Glyph
import random
import time


x_data = []
y_data = []

x_data2 = []
y_data2 = []

output_server("multiple_updateable_plots")

figure(title="First plot")
line(x_data, y_data,
    color="#0000FF",
    tools="pan,resize,wheel_zoom", width=1200,height=300, 
    title = 'First plot stuff',
    legend='value of thing')
xaxis()[0].axis_label = "Time"
yaxis()[0].axis_label = "Value"


figure(title="Second plot")
line(x_data2, y_data2, 
    color="#0000FF",
    tools="pan,resize,wheel_zoom", width=1200,height=300, 
    title = 'Second plot stuff',
    legend='value of thing2')
xaxis()[0].axis_label = "Time"
yaxis()[0].axis_label = "Value"

show()


renderers = curplot().select(dict(type=Glyph))
datasource = renderers[0].data_source
time_ref = 0
while True:
    datasource.data["x"] = x_data
    datasource.data["y"] = y_data
    datasource._dirty = True
    cursession().store_objects(datasource)
    # How to update data of each plot?
    # This updates the last one only
    
    x_data.append(time_ref)
    time_ref += 1
    y_data.append(random.random()) 
    time.sleep(0.1)
        

