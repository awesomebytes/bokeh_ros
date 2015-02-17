#! /usr/bin/env python

"""
Created on 17/02/15

@author: Sam Pfeiffer

Example made from:
https://github.com/bokeh/bokeh/blob/master/examples/plotting/server/scatter.py

And:
https://github.com/awesomebytes/bokeh_ros/blob/master/scripts/run_multiple_plots.py

(Which itself was based on: http://continuum.io/blog/painless_streaming_plots_w_bokeh)

"""

from bokeh.plotting import *
import random
import time
from bokeh.models.renderers import GlyphRenderer


TOOLS = "pan,wheel_zoom,box_zoom,reset,save,box_select"

# We will store the data here
x_data = []
y_data = []

# Setting up output server
output_server("simple_dynamic_scatter")

# Set up scatter plot
title = "Example simple dynamic scatter"
fig = figure(title=title)
fig.scatter(
              x_data,
              y_data,
              color="#0000FF",
              tools=TOOLS,
              width=1200,
              height=300,
              legend='value of thing'
            )

# Show plot!
show()

# Set up renderers and datasources
my_renderer = fig.select(dict(type=GlyphRenderer))
data_src = my_renderer[0].data_source

# Set up the dynamic plotting
while True:
    data_src.data["x"] = x_data
    data_src.data["y"] = y_data
    data_src._dirty = True
    cursession().store_objects(data_src)

    x_data.append(random.random())
    y_data.append(random.random())
    time.sleep(0.05)

