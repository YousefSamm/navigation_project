import rclpy
from rclpy.node import Node 
from rcl_interfaces.msg import SetParametersResult
from nav2_msgs.action import NavigateToPose

class Navigation(Node):
    def __init__(self):
        super().__init__('move_to_spot')
        self.declare_parameter('spot_name', rclpy.Parameter.Type.STRING)
        self.declare_parameter('spot_name.corner1.orientation.w', rclpy.Parameter.Type.DOUBLE)
        self.declare_parameter('spot_name.corner1.position.x', rclpy.Parameter.Type.DOUBLE)
        self.declare_parameter('spot_name.corner1.position.y', rclpy.Parameter.Type.DOUBLE)
        self.declare_parameter('spot_name.corner2.orientation.w', rclpy.Parameter.Type.DOUBLE)
        self.declare_parameter('spot_name.corner2.position.x', rclpy.Parameter.Type.DOUBLE)
        self.declare_parameter('spot_name.corner2.position.y', rclpy.Parameter.Type.DOUBLE)        
        self.declare_parameter('spot_name.pedestrian.orientation.w', rclpy.Parameter.Type.DOUBLE)
        self.declare_parameter('spot_name.pedestrian.position.x', rclpy.Parameter.Type.DOUBLE)
        self.declare_parameter('spot_name.pedestrian.position.y', rclpy.Parameter.Type.DOUBLE)        
        self.add_on_set_parameters_callback(self.parameter_callback)
        self.timer_=self.create_timer(0.5, self.timer_callback)
        self.label=None
        self.data={}
        self.values=[]
        self.assign=False
    def parameter_callback(self, params):
        for param in params:
            if param.name=='spot_name':
                self.label=param.value
                self.assign=True
        return SetParametersResult(successful=True)
    def timer_callback(self):
        if self.assign:
            # Use a dictionary to map the parameters
            keys = [
                'orientation.w', 'position.x', 'position.y'
            ]
            
            # Use the label to form keys for the parameters dynamically
            for key in keys:
                param_name = f'spot_name.{self.label}.{key}'
                self.data[key] = self.get_parameter(param_name).value

            self.assign = False
            self.get_logger().info(f"Data: {str(self.data)}")
def main(args=None):
    rclpy.init(args=args)
    node=Navigation()
    rclpy.spin(node)
    node.destroy_node()
    rclpy.shutdown()
