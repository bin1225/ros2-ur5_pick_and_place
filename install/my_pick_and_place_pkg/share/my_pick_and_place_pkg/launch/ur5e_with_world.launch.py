from launch import LaunchDescription
from launch.actions import IncludeLaunchDescription, ExecuteProcess
from launch.launch_description_sources import PythonLaunchDescriptionSource
from ament_index_python.packages import get_package_share_directory
import os

def generate_launch_description():
    ur_pkg = get_package_share_directory('ur_simulation_gz')
    world_path = os.path.join(
        get_package_share_directory('my_pick_and_place_pkg'),
        'worlds',
        'pick_and_place_world.sdf'
    )

    return LaunchDescription([
        # Gazebo 직접 실행
        ExecuteProcess(
            cmd=['gazebo', world_path, '--verbose'],
            output='screen'
        ),

        # UR5e 스폰만 따로 실행
        IncludeLaunchDescription(
            PythonLaunchDescriptionSource(
                os.path.join(ur_pkg, 'launch', 'ur_spawner.launch.py')  # 로봇만 스폰하는 launch (예시)
            ),
            launch_arguments={
                'ur_type': 'ur5e'
            }.items()
        )
    ])
