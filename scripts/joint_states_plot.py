#! /usr/bin/env python
# -*- coding: utf-8 -*-
"""
Created on 22/11/14

@author: Sam Pfeiffer
"""

import rospy
from sensor_msgs.msg import JointState

from bokeh.plotting import *

from bokeh.objects import Glyph

JS_TOPIC = '/joint_states'

class JointStatesPlotter():

    def __init__(self):
        # Some needed vars
        rospy.loginfo("Initializing JointStatesPlotter")
        self.max_points = 1000
        self.last_js = None
        self.x_data = []
        self.y_data = []
        rospy.Subscriber(JS_TOPIC, JointState, self.js_cb)
        output_server("joint_states_continuous")
        
        figure(title="Line example for joint states")
        line(self.x_data, self.y_data, color="#0000FF", x_axis_type = "datetime", 
            tools="pan,resize,wheel_zoom", width=1200,height=300, 
            title = 'Joint states for arm_left_1_joint',
            legend='joint value')
         
        xaxis()[0].axis_label = "Time"
        yaxis()[0].axis_label = "Joint pos"
        show()
        rospy.loginfo("Plotted!")

    def js_cb(self, data):
        rospy.logdebug("Got CB of JS")
        self.last_js = data
        if len(self.x_data) < self.max_points: # initial fill up
            self.x_data.append(data.header.stamp.secs)
            self.y_data.append(data.position[0])
        else: # get rid of initial value, and put at the end
            self.x_data.pop(0)
            self.x_data.append(data.header.stamp.secs)
            self.y_data.pop(0)
            self.y_data.append(data.position[0])
        
    def run_example(self):
        rospy.loginfo("Plotting!")
        js_msgs = []
        # Get 10 joint state messages
        NUM_JS = 100
        rospy.loginfo("Getting #" + str(NUM_JS) + " joint_state messages")
        for i in range(NUM_JS):
            js_msgs.append(rospy.wait_for_message(JS_TOPIC, JointState))
            #rospy.sleep(0.1)
        #js_msg = rospy.wait_for_message(JS_TOPIC, JointState)
        x_data = []
        y_data = []
        for i in range(NUM_JS):
            #js=JointState()
            x_data.append(js_msgs[i].header.stamp.secs) # put times in secs
            y_data.append(js_msgs[i].position[0]) # first joint arm_left_1_joint
        output_server("joint_states")
        
        figure(title="Line example for joint states")
        line(x_data, y_data, color="#0000FF", x_axis_type = "datetime", 
            tools="pan,resize", width=1200,height=300, 
            title = 'Joint states for arm_left_1_joint',
            legend='joint value')
         
        xaxis()[0].axis_label = "Time"
        yaxis()[0].axis_label = "Joint pos"
        show()
        rospy.loginfo("Plotted!")
        
    def run_continuous(self):
        renderer = [r for r in curplot().renderers if isinstance(r, Glyph)][0]
        print "Renderer is:"
        print renderer
        datasource = renderer.data_source
        while not rospy.is_shutdown():
            #rospy.logwarn("x_data: " + str(self.x_data))
            datasource.data["x"] = self.x_data
            datasource.data["y"] = self.y_data
            datasource._dirty = True
            cursession().store_objects(datasource)
            rospy.sleep(0.01)
        

if __name__ == '__main__':
    rospy.init_node('joint_states_plotter')

    node = JointStatesPlotter()
    #node.run_example()
    node.run_continuous()