#! /usr/bin/env python
# -*- coding: utf-8 -*-
"""
Created on 22/11/14

@author: Sam Pfeiffer

Script that tries to show all joints of joint states
in a bokeh web plot
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
        self.max_points = 999999999#1000
        self.last_js = None
        self.x_data = []
        self.y_data = []
        
        # TODO: Get one message and get all joint names
        # For every joint name get its upper and lower limit
        # For every joint create a plot with its name
        
        rospy.Subscriber(JS_TOPIC, JointState, self.js_cb)
        output_server("joint_states_continuous")
        
        figure(title="Line example for joint states")
        line(self.x_data, self.y_data, 
            y_range=self.get_joint_limits('arm_left_1_joint'),
            color="#0000FF", #x_axis_type = "datetime", 
            tools="pan,resize,wheel_zoom", width=1200,height=300, 
            title = 'Joint states for arm_left_1_joint',
            legend='joint value')
        xaxis()[0].axis_label = "Time"
        yaxis()[0].axis_label = "Joint pos"
        # Testing random stuff to get more plots to work
        #p1 = curplot()
        figure(title="Line example for joint states again")
        line(self.x_data, self.y_data, 
            y_range=self.get_joint_limits('arm_left_1_joint'),
            color="#0000FF", #x_axis_type = "datetime", 
            tools="pan,resize,wheel_zoom", width=1200,height=300, 
            title = 'Joint states for arm_left_1_joint again',
            legend='joint value')
        xaxis()[0].axis_label = "Time"
        yaxis()[0].axis_label = "Joint pos"
        p2 = curplot()
        #gp = GridPlot(children=[[p1,p2]])
#         show(gp)
        show()
        rospy.loginfo("Plotted!")

    def get_joint_limits(self, joint_name):
        lower_limit = -4.0
        upper_limit = 4.0
        # Do magic to get limits with urdf_parser_py
        return [lower_limit, upper_limit]


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
        """Initial test that just does one plot with some values of joint states"""
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
        line(x_data, y_data, y_range=[-1.0, 3.0], color="#0000FF", x_axis_type = "datetime", 
            tools="pan,resize", width=1200,height=300, 
            title = 'Joint states for arm_left_1_joint',
            legend='joint value')
         
        xaxis()[0].axis_label = "Time"
        yaxis()[0].axis_label = "Joint pos"
        show()
        rospy.loginfo("Plotted!")
        
    def run_continuous(self):
        #renderers = [r for r in curplot().renderers if isinstance(r, Glyph)]
        renderers = curplot().select(dict(type=Glyph))
        print "Renderer is:"
        print renderers
        print len(renderers)
        datasource = renderers[0].data_source
        print "datasource.column_names:"
        print datasource.column_names
        #datasource2 = renderers[1].data_source
        while not rospy.is_shutdown():
            #rospy.logwarn("x_data: " + str(self.x_data))
            datasource.data["x"] = self.x_data
            datasource.data["y"] = self.y_data
            datasource._dirty = True
            cursession().store_objects(datasource)
#             datasource2.data["x"] = self.x_data / 10.0
#             datasource2.data["y"] = self.y_data / 10.0
#             datasource2._dirty = True
#             cursession().store_objects(datasource2)
            rospy.sleep(0.01)
            # TODO: Know if we can make bokeh-server go faster as it's updating the graph quite slowly
        

if __name__ == '__main__':
    rospy.init_node('joint_states_plotter')

    node = JointStatesPlotter()
    #node.run_example()
    node.run_continuous()