import time

from renvros2_demo_msgs.action import Fibonacci

import rclpy
from rclpy.action import ActionServer, CancelResponse, GoalResponse
from rclpy.callback_groups import ReentrantCallbackGroup
from rclpy.executors import MultiThreadedExecutor
from rclpy.node import Node


class MinimalActionServer(Node):

    def __init__(self):
        super().__init__('minimal_action_server')

        self._sequence = []
        
        self._action_server = ActionServer(
            self,
            Fibonacci,
            'fibonacci',
            execute_callback=lambda x,self_=self:self_.execute_callback(x),
            callback_group=ReentrantCallbackGroup(),
            goal_callback=lambda x, self_=self:self_.goal_callback(x),
            cancel_callback=lambda x,self_=self:self_.cancel_callback(x))

    def destroy(self):
        self._action_server.destroy()
        super().destroy_node()

    def goal_callback(self, goal_request):
        """Accepts or rejects a client request to begin an action."""
        # This server allows multiple goals in parallel
        self.get_logger().info('Received goal request')
        return GoalResponse.ACCEPT

    def cancel_callback(self, goal_handle):
        """Accepts or rejects a client request to cancel an action."""
        self.get_logger().info('Received cancel request')
        return CancelResponse.ACCEPT

    async def execute_callback(self, goal_handle):
        """Executes a goal."""
        self.get_logger().info('Executing goal...')

        # Append the seeds for the Fibonacci sequence
        feedback_msg = Fibonacci.Feedback()
        self._sequence = [0, 1]

        # Start executing the action
        for i in range(1, goal_handle.request.order):
            if goal_handle.is_cancel_requested:
                goal_handle.canceled()
                self.get_logger().info('Goal canceled')
                return Fibonacci.Result()

            # Update Fibonacci sequence
            #feedback_msg.sequence.append(feedback_msg.sequence[i] + feedback_msg.sequence[i-1])
            self._sequence.append(self._sequence[i] + self._sequence[i-1])

            #self.get_logger().info('Publishing feedback: {0}'.format(feedback_msg.sequence))
            self.get_logger().info('Publishing feedback: {0}'.format(self._sequence))

            feedback_msg.value = self._sequence[-1]

            # Publish the feedback
            goal_handle.publish_feedback(feedback_msg)

            # Sleep for demonstration purposes
            time.sleep(1)

        goal_handle.succeed()

        # Populate result message
        result = Fibonacci.Result()
        result.result = self._sequence[-1] if len(self._sequence) > 0 else 1

        #self.get_logger().info('Returning result: {0}'.format(result.sequence))
        self.get_logger().info('Returning result: {0}'.format(result.result))

        return result


def main(args=None):
    rclpy.init(args=args)

    minimal_action_server = MinimalActionServer()

    # Use a MultiThreadedExecutor to enable processing goals concurrently
    executor = MultiThreadedExecutor()

    rclpy.spin(minimal_action_server, executor=executor)

    minimal_action_server.destroy()
    rclpy.shutdown()


if __name__ == '__main__':
    main()
