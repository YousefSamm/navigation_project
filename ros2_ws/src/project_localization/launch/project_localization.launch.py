from launch import LaunchDescription
from launch_ros.actions import Node
from ament_index_python.packages import get_package_share_directory
import os

def generate_launch_description():
    map_file=os.path.join(get_package_share_directory('project_mapping'), 'maps', 'turtlebot_area.yaml')
    nav2_yaml=os.path.join(get_package_share_directory('project_localization'), 'config', 'amcl_config.yaml')

    map_server=Node(
        package='nav2_map_server',
        executable='map_server',
        name="map_server",
        output='screen',
        parameters=[{'use_sim_time': True},{'yaml_filename': map_file}]
    )

    amcl_node=Node(
        package='nav2_amcl',
        executable='amcl',
        name='amcl',
        output='screen',
        parameters=[nav2_yaml]

    )

    lifecycle_manager=Node(
        package='nav2_lifecycle_manager',
        executable='lifecycle_manager',
        name='lifecycle_manager_localization',
        output='screen',
        parameters=[{'use_sim_time': True},{'autostart':True}, {'node_names': ['map_server', 'amcl']}]
    )
    self_localizer=Node(
        package='project_localization',
        executable='self_localization',
        name='self_localizer',
        output='screen'
    
    )
    spot_recorder=Node(
            package='project_localization',
            executable='spots_to_file',
            name='spot_recorder',
            output='screen'

    )
    return LaunchDescription([
    map_server,
    amcl_node,
    lifecycle_manager,
    self_localizer,
    spot_recorder
    
    
    ])