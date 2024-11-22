from launch import LaunchDescription
from launch_ros.actions import Node 
from ament_index_python import get_package_share_directory  
import os

def generate_launch_description():
    
    map_file=os.path.join(get_package_share_directory('project_mapping'), 'maps', 'turtlebot_area.yaml')
    map_server=Node(
        package="nav2_map_server",
        executable="map_server",
        name="map_server",
        output="screen",
        parameters=[{'use_sim_time': True},{'yaml_filename': map_file}]
    )
    spot_recorder=Node(
        package="project_path_planning",
        executable="spot_recorder",
        name="spot_recorder",
        output="screen"
    )
    lifecycle_manager=Node(
        package="nav2_lifecycle_manager",
        executable="lifecycle_manager",
        name="spot_recorder_lifecycle",
        output="screen",
        parameters=[{'use_sim_timer': True}, {'autostart': True}, {'node_names': ['map_server']}]
        )
    return LaunchDescription([
        map_server,
        spot_recorder,
        lifecycle_manager
    ])