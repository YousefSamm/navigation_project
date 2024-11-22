import rclpy
from rclpy.node import Node 
from geometry_msgs.msg import PoseWithCovarianceStamped
from rclpy.qos import QoSProfile, ReliabilityPolicy
import os
import yaml
from ament_index_python import get_package_share_directory
class SpotRecoreder(Node):
    def __init__(self):
        super().__init__("spot_recorder")
        self.subscrier_=self.create_subscription(PoseWithCovarianceStamped, '/initialpose',
            self.recorder_callback, QoSProfile(depth=10, reliability=ReliabilityPolicy.RELIABLE))
        self.file=os.path.join(os.path.expanduser('~'),'ros2_ws/src/project_path_planning/config', 'project_params.yaml')
        self.label=["corner1","corner2","pedestrian"]
        self.index=0
        self.data = {'ros__parameters': {}}
    def recorder_callback(self, msg):
        self.position = {
            'x': msg.pose.pose.position.x,
            'y': msg.pose.pose.position.y,
            'z': msg.pose.pose.position.z
        }
        self.orientation = {
            'x': msg.pose.pose.orientation.x,
            'y': msg.pose.pose.orientation.y,
            'z': msg.pose.pose.orientation.z,
            'w': msg.pose.pose.orientation.w
        }
        self.data['ros__parameters'][self.label[self.index]] = {
            'position': self.position,
            'orientation': self.orientation
        }
        self.index+=1
        if self.index >= len(self.label):
            with open(self.file, 'w') as file:
                yaml.dump(self.data, file, default_flow_style=False)
            self.get_logger().info("All positions recorded to project_params.yaml")
            rclpy.shutdown()  # Shutdown after writing data
def main(args=None):
    rclpy.init(args=args)
    node=SpotRecoreder()
    rclpy.spin(node)
    node.destroy_node()
    rclpy.shutdown()


