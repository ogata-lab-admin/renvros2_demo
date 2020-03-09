#!/usr/bin/python
import logging

import rclpy
import renvros2

from renvros2_demo_msgs.action import Fibonacci

#host = "192.168.1.24:8080"
host = "192.168.170.219:8080"
typeId = "RENVROS.TEST.DEVICE3"
name   = "renvros2-tester3"
version = "1.0.1"
device_uuid = None
deviceName = "DEVICE3"

class FibonacciAction(renvros2.RenvNode):
    def __init__(self):
        super().__init__('fibonacci_act_device')
        logger = logging.getLogger(__name__)
        logging.basicConfig(filename='fibonacci_action_device.log',level=logging.INFO)
        self.init_renv(typeId, name, version, device_uuid, deviceName, logger)
        self.__action_client = renvros2.RenvActionClient(self, Fibonacci, 'fibonacci')
        self.connect(host)

def main(args=None):
    rclpy.init(args=args)
    n = FibonacciAction()
    renvros2.spin(n)
    n.destroy_node()
    rclpy.shutdown()

if __name__ == '__main__':
    main()
