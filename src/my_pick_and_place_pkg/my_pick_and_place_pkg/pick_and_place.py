#!/usr/bin/env python3

import rclpy
from rclpy.node import Node

from geometry_msgs.msg import PoseStamped
from moveit_msgs.action import MoveGroup
from moveit_msgs.msg import Constraints, PositionConstraint, OrientationConstraint, BoundingVolume
from shape_msgs.msg import SolidPrimitive
from builtin_interfaces.msg import Duration

from rclpy.action import ActionClient


class PickAndPlaceNode(Node):
    def __init__(self):
        super().__init__('pick_and_place_node')
        self.get_logger().info("🚀 PickAndPlaceNode 시작됨")

        # MoveGroup ActionClient
        self._action_client = ActionClient(self, MoveGroup, '/move_action')

        # Timer로 연결 기다린 후 목표 pose 전송
        self.timer = self.create_timer(1.0, self.send_goal)

    def send_goal(self):
        self.timer.cancel()

        if not self._action_client.wait_for_server(timeout_sec=5.0):
            self.get_logger().error('❌ MoveGroup action server 연결 실패!')
            return

        self.get_logger().info("✅ MoveGroup action server 연결 성공!")

        # 목표 pose 설정
        target_pose = PoseStamped()
        target_pose.header.frame_id = 'base_link'
        target_pose.pose.position.x = 0.4
        target_pose.pose.position.y = 0.2
        target_pose.pose.position.z = 0.3
        target_pose.pose.orientation.w = 1.0  # 기본 방향

        goal_msg = MoveGroup.Goal()
        goal_msg.request.group_name = 'ur_manipulator'
        goal_msg.request.pose_target.append(target_pose)
        goal_msg.request.planner_id = ''
        goal_msg.request.num_planning_attempts = 5
        goal_msg.request.allowed_planning_time = 5.0
        goal_msg.request.max_velocity_scaling_factor = 1.0
        goal_msg.request.max_acceleration_scaling_factor = 1.0
        goal_msg.request.start_state.is_diff = True

        self.get_logger().info("📦 이동 목표 전송 중...")
        self._action_client.wait_for_server()
        self._action_client.send_goal_async(goal_msg, feedback_callback=self.feedback_cb).add_done_callback(self.goal_response_cb)

    def feedback_cb(self, feedback_msg):
        self.get_logger().info("📡 경로 계획 중...")

    def goal_response_cb(self, future):
        goal_handle = future.result()
        if not goal_handle.accepted:
            self.get_logger().error('❌ 경로 목표 거부됨')
            return

        self.get_logger().info('🟢 경로 목표 수락됨! 실행 중...')
        goal_handle.get_result_async().add_done_callback(self.result_cb)

    def result_cb(self, future):
        result = future.result().result
        self.get_logger().info(f'🎉 경로 실행 완료! 성공 여부: {result.error_code.val}')


def main():
    rclpy.init()
    node = PickAndPlaceNode()
    rclpy.spin(node)
    rclpy.shutdown()
