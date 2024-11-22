import rclpy
from rclpy.node import Node 
from geometry_msgs.msg import PoseWithCovarianceStamped
from custom_interfaces.srv import MyServiceMessage
from rclpy.qos import QoSProfile, ReliabilityPolicy, DurabilityPolicy
import os
class SpotRecorder(Node):
    def __init__(self):
        super().__init__('spot_recorder')
        self._service=self.create_service(MyServiceMessage,'/save_spot', self.srv_callback)
        self._subscriber=self.create_subscription(PoseWithCovarianceStamped, '/amcl_pose', self.subscriber_callback, QoSProfile(depth=10, reliability=ReliabilityPolicy.RELIABLE, durability=DurabilityPolicy.TRANSIENT_LOCAL))
        self.label= str
        self.position=PoseWithCovarianceStamped()
        self.orientation=PoseWithCovarianceStamped()
        self.label_list=[]
        self.position_list=[]
        self.orientation_list=[]        
    def subscriber_callback(self, msg):
        self.position=msg.pose.pose.position
        self.orientation=msg.pose.pose.orientation
    def srv_callback(self, request,response):
        self.label=request.label
        if self.label!="end":
            self.label_list.append(self.label)
            self.position_list.append(self.position)
            self.orientation_list.append(self.orientation)
            response.message=str(self.position)+str(self.orientation)
        config_directory=os.path.join(os.path.expanduser('~'),'ros2_ws/src/project_localization/config')
        spots_txt=os.path.join(config_directory, "spots.txt")
        if self.label=="end":
            with open(spots_txt, 'a') as file:
                for i in range(len(self.label_list)):
                    file.write("%s: \n %s \n %s \n" %(self.label_list[i], self.position_list[i], self.orientation_list[i]))
            response.message="coordinates saved successfully in spots.txt"
        response.navigation_successfull=True
        
        return response
def main(args=None):
    rclpy.init(args=args)
    rec=SpotRecorder()
    rclpy.spin(rec)
    rec.destroy_node()
    rclpy.shutdown()
