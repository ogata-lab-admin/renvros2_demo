#!/usr/bin/env python
import logging
import rclpy
import renvros2

from turtlesim.srv import Spawn


host = "192.168.1.24:8080"
typeId = "RENVROS.TEST.DEVICE4"
name   = "renvros2-tester4"
version = "1.0.0"
device_uuid = None
deviceName = "DEVICE4"

class TurtleSpawnDevice(renvros2.RenvNode):
    def __init__(self):
        super().__init__('turtle_spawn')

        logger = logging.getLogger(__name__)
        logging.basicConfig(filename='turtle_spawn.log',level=logging.INFO)
        self.init_renv(typeId, name, version, device_uuid, deviceName, logger)
        self._cli = self.create_renv_client(Spawn, '/spawn')
        self.connect(host)
        
def main(args=None):
    rclpy.init(args=args)
    n = TurtleSpawnDevice()
    renvros2.spin(n)
    n.destroy_node()
    rclpy.shutdown()

if __name__ == '__main__':
    main()
