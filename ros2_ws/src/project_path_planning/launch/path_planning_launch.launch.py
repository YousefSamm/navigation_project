from launch import LaunchDescription
from launch_ros.actions import Node
import os
from ament_index_python import get_package_share_directory, get_package_prefix

def generate_launch_description():
    
    nav2_yaml=os.path.join(get_package_share_directory('project_path_planning'),'config', 'planner_server.yaml')
    controller_yaml=os.path.join(get_package_share_directory('project_path_planning'), 'config', 'controller.yaml' )
    bt_navigator_yaml=os.path.join(get_package_share_directory('project_path_planning'), 'config', 'bt_navigator.yaml')
    recovery_yaml=os.path.join(get_package_share_directory('project_path_planning'), 'config', 'recovery.yaml')
    planner=Node(
        package='nav2_planner',
        executable='planner_server',
        name='planner_server',
        output='screen',
        parameters=[nav2_yaml]
        )
    controller=Node(
        package='nav2_controller',
        executable='controller_server',
        name='controller_server',
        output='screen',
        parameters=[controller_yaml]

    )
    bt_navigator=Node(
        package='nav2_bt_navigator',
        executable='bt_navigator',
        name='bt_navigator',
        output='screen',
        parameters=[bt_navigator_yaml]
    )
    recovery_behaviors=Node(
        package='nav2_behaviors',
        executable='behavior_server',
        name='recoveries_server',
        parameters=[recovery_yaml]
    
    )
    life_cycle_manager=Node(
        package="nav2_lifecycle_manager",
        executable='lifecycle_manager',
        name='path_planning_lifecycle_manager',
        parameters=[{'use_sim_time': True}, {'autostart': True}, {'node_names': ['planner_server', 'controller_server', 'bt_navigator', 'recoveries_server']}]
    )

    return LaunchDescription([
        planner,
        controller,
        bt_navigator,
        recovery_behaviors,
        life_cycle_manager
    
    ])
