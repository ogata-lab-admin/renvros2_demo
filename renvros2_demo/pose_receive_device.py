#!/usr/bin/python
import logging
import rclpy
import renvros2
from turtlesim.msg import Pose

#host = "192.168.128.157:8080"
#host = "192.168.170.237:8080"
host = "localhost:8080"
typeId = "RENVROS.TEST.DEVICE2"
name   = "renvros2-tester2"
version = "1.0.0"
device_uuid = None
deviceName = "DEVICE2"

class PoseSubscriber(renvros2.RenvNode):
    def __init__(self):
        super().__init__('pose_receive_device')
        logger = logging.getLogger(__name__)
        logging.basicConfig(filename='pose_receive_device.log',level=logging.INFO)
        self.init_renv(typeId, name, version, device_uuid, deviceName, logger)
        pub = self.create_renv_subscription(Pose,
                                            '/turtle1/pose',
                                            10)
        self.connect(host)

def main(args=None):
    rclpy.init(args=args)
    n = PoseSubscriber()
    renvros2.spin(n)
    n.destroy_node()
    rclpy.shutdown()


if __name__ == '__main__':
    main()
