#!/usr/bin/env python

from time import sleep

import rospy

from ros_node import RosNode
from std_msgs.msg import String
from beginner_tutorials.srv import *


node = RosNode("test_ros_node")


@node.publisher("/test_pub", String, queue_size=1)
def test_publish():
    s = "test_publish_message"
    print("Publishing: '{0}'".format(s))
    return s


@node.publisher('/zak', String, queue_size=1)
def zak_func():
    return 'Zak'

@node.subscriber("test_pub", String)
def test_sub(data):
    s = data.data
    print("Received: '{0}'".format(s))

@node.service('test_service', AddTwoInts)
def add_two_ints(req):
    return AddTwoIntsResponse(req.a + req.b)

if __name__ == "__main__":
    while True:
        # test_publish()
        zak_func()

        rospy.wait_for_service('test_service')
        try:
            add_two_ints = rospy.ServiceProxy('test_service', AddTwoInts)
            resp = add_two_ints.call(1, 2)
            print('Service returned: {0}'.format(resp.sum))
        except rospy.ServiceException:
            print('Could not call service! Exiting...')
            exit(0)

        sleep(5)
