#!/usr/bin/env python

import roslib
roslib.load_manifest('visualization_marker_tutorials')
from std_msgs.msg import UInt8MultiArray
from visualization_msgs.msg import Marker
from visualization_msgs.msg import MarkerArray
import rospy
import math
import bitstring as bs


def main():
    topic = 'visualization_marker_array'
    publisher = rospy.Publisher(topic, MarkerArray)

    count = 0

    def callback(data):
        nonlocal count, MARKERS_MAX, markerArray
        bits = bs.BitArray(data.data)
        angle = bits[32+11:32+20].int
        rng = bits[32+21:32+31].uint
        if ((data.data[1] == ord('\x05')) & (data.data[0] != ord('@'))):
            #rospy.loginfo("I heard %s %s", angle * 0.1, rng * 0.1)
            marker = Marker()
            marker.header.frame_id = "/world"
            marker.id = data.data[0]
            marker.type = marker.SPHERE
            marker.action = marker.ADD
            marker.scale.x = 0.1
            marker.scale.y = 0.1
            marker.scale.z = 0.1
            marker.color.a = 1.0
            marker.color.r = 1.0
            marker.color.g = 1.0
            marker.color.b = 0.0
            marker.pose.orientation.w = 1.0
            marker.pose.position.x = rng * math.cos(angle * 0.1 * math.pi / 180.0) * 0.1
            marker.pose.position.y = rng * math.sin(angle * 0.1 * math.pi / 180.0) * 0.1
            marker.pose.position.z = 0

            # We add the new marker to the MarkerArray, removing the oldest
            # marker from it when necessary
            # if (count > MARKERS_MAX):
            #     markerArray.markers.pop(0)
            if(data.data[0] < 64):
                markerArray.markers[data.data[0]] = marker

            # Renumber the marker IDs
            # id = 0
            # for m in markerArray.markers:
            #     m.id = id
            #     id += 1

            # count += 1


    

    markerArray = MarkerArray()

    for i in range(64):
        marker = Marker()
        markerArray.markers.append(marker)

    count = 0
    MARKERS_MAX = 64

    sub_can = rospy.Subscriber('/can/msgs', UInt8MultiArray, callback)
    rospy.init_node('register')
    while not rospy.is_shutdown():

        # Publish the MarkerArray
        publisher.publish(markerArray)

        rospy.sleep(0.01)

if __name__ == '__main__':
    main()
