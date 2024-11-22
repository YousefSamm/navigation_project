import rclpy
from rclpy.node import Node
from geometry_msgs.msg import PoseWithCovarianceStamped
from geometry_msgs.msg import PointStamped
from std_srvs.srv import Empty

class Localize(Node):
    def __init__(self):
        super().__init__('initial_pose_pub_node')
        self.publisher_ = self.create_publisher(PoseWithCovarianceStamped, '/initialpose', 1)
        self.subscriber_ = self.create_subscription(PointStamped, '/clicked_point', self.callback, 1)
        self.subscriber_  # prevent unused variable warning
        self._client = self.create_client(Empty, '/reinitialize_global_localization')
        if self._client.wait_for_service(timeout_sec=1.0):
            req = Empty.Request()
            self._client.call_async(req)
        else:
            self.get_logger().error('Service /reinitialize_global_localization not available')

    def callback(self, msg):
        self.get_logger().info('Received Data:\n X: %f \n Y: %f \n Z: %f' % (msg.point.x, msg.point.y, msg.point.z))
        self.publish(msg.point.x, msg.point.y)

    def publish(self, x, y):
        msg = PoseWithCovarianceStamped()
        msg.header.frame_id = 'map'
        msg.pose.pose.position.x = x
        msg.pose.pose.position.y = y
        msg.pose.covariance = [0.0] * 36  # Set zero covariance matrix
        
        self.get_logger().info('Publishing Initial Position\n X: %f \n Y: %f' % (x, y))
        self.publisher_.publish(msg)

        
def main(args=None):
    rclpy.init(args=args)
    node = Localize()
    rclpy.spin(node)
    node.destroy_node()
    rclpy.shutdown()

if __name__ == '__main__':
    main()
