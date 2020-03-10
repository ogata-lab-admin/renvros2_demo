#!/usr/bin/python
import logging

import rclpy
from rclpy.action import ActionClient
from rclpy.node import Node
import rclpy
import renvros2

from renvros2_demo_msgs.action import GoalPose
from nav2_msgs.action import NavigateToPose

#from renvros2_demo_msgs.action import Fibonacci

#host = "192.168.1.24:8080"
host = "localhost:8080"
#host = "192.168.170.219:8080"
#host = "192.168.128.157:8080"
#host = "192.168.180.15:8080"
typeId = "RENVROS.TEST.DEVICE5"
name   = "renvros2-tester5"
version = "1.0.0"
device_uuid = None
deviceName = "DEVICE5"

class MobileAction(renvros2.RenvNode):
    def __init__(self):
        super().__init__('movile_act_device')
        logger = logging.getLogger(__name__)
        logging.basicConfig(filename=__name__ + '.log', level=logging.INFO)
        self.init_renv(typeId, name, version, device_uuid, deviceName, logger)

        def goal_conv(p):
            goal = NavigateToPose.Goal()
            goal.pose.header.frame_id = p.frame_id
            goal.pose.pose.position.y = p.y
            goal.pose.pose.position.x = p.x
            goal.pose.pose.orientation.z = p.th
            return goal

        def feed_conv(f):
            print('feedback is ', f)
            feed = NavigateToPose.Feedback()
            return feed

        def result_conv(r):
            print('result is ', r)
            result = GoalPose.Result()
            return result
        
        self._action_client = renvros2.RenvActionClient(self, NavigateToPose, '/NavigateToPose',
                                                        action_type_for_renv=GoalPose,
                                                        goal_converter=goal_conv,
                                                        feedback_converter=feed_conv,
                                                        result_converter=result_conv)
        self.connect(host)
        
        
        
def main(args=None):
    rclpy.init(args=args)
    a = MobileAction()
    renvros2.spin(a)
    n.destroy_node()
    rclpy.shutdown()

if __name__ == '__main__':
    main()
