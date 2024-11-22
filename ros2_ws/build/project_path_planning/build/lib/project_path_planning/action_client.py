import rclpy
from rclpy.node import Node
from rcl_interfaces.msg import SetParametersResult
from nav2_msgs.action import NavigateToPose

class Navigation(Node):
    def __init__(self):
        super().__init__('move_to_spot')
        # Declare parameters dynamically using a dictionary for spot names and associated parameters
        self.declare_parameter('spot_name', rclpy.Parameter.Type.STRING)
        self.spots = {}  # Dictionary to store spots and their parameters
        self.add_on_set_parameters_callback(self.parameter_callback)
        self.timer_ = self.create_timer(0.5, self.timer_callback)
        self.assign = False

    def parameter_callback(self, params):
        for param in params:
            if param.name == 'spot_name':
                self.label = param.value
                self.assign = True
        return SetParametersResult(successful=True)

    def get_spot_parameters(self, spot_name):
        """Return a dictionary of parameters for a given spot."""
        keys = [
            'corner1.orientation.w', 'corner1.position.x', 'corner1.position.y',
            'corner2.orientation.w', 'corner2.position.x', 'corner2.position.y',
            'pedestrian.orientation.w', 'pedestrian.position.x', 'pedestrian.position.y'
        ]
        spot_data = {}
        for key in keys:
            param_name = f'spot_name.{spot_name}.{key}'
            spot_data[key] = self.get_parameter(param_name).value
        return spot_data

    def timer_callback(self):
        if self.assign:
            # Use the label to get the specific spot's parameters dynamically
            self.spots[self.label] = self.get_spot_parameters(self.label)
            self.assign = False
            self.get_logger().info(f"Spot data: {str(self.spots[self.label])}")

def main(args=None):
    rclpy.init(args=args)
    node = Navigation()
    rclpy.spin(node)
    node.destroy_node()
    rclpy.shutdown()
