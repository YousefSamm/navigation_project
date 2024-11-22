from launch import LaunchDescription
from launch_ros.actions import Node 
from ament_index_python import get_package_share_directory  
import os

def generate_launch_description():
    
    map_file=os.path.join(get_package_share_directory('project_path_planning'), 'config', 'project_params.yaml')
    client=Node(
        package='project_path_planning',
        executable='move_to_spot',
        name='move_to_spot',
        output='screen',
        parameters=[map_file]
    )
    return LaunchDescription([
        client
    ])