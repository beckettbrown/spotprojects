import argparse #argument parsing
import os   #operating system
import sys #system information
import time #time access


import bosdyn.client #establish a client
import bosdyn.client.lease #establish a lease
import bosdyn.client.util # access Client Untility
import bosdyn.geometry # access geometry
from bosdyn.api import trajectory_pb2 #access trajectory access
from bosdyn.api.spot import robot_command_pb2 as spot_command_pb2 #api commands
from bosdyn.client.robot_command import RobotCommandBuilder, RobotCommandClient, blocking_stand, blocking_sit #access builder,stand,sit
from bosdyn.client.robot_state import RobotStateClient #access robot state
from bosdyn.util import seconds_to_duration # access by seconds


def jarvis_squats(config):
    """A simple example of using the Boston Dynamics API to command a Spot robot."""

    # The SDK object is the primary entry point to the Boston Dynamics API.
    sdk = bosdyn.client.create_standard_sdk('HelloSpotClient')
    robot = sdk.create_robot(config.hostname)

    # Authenticate with the robot
    bosdyn.client.util.authenticate(robot)

    # Establish time sync with the robot
    robot.time_sync.wait_for_sync()

    # Verify the robot is not estopped
    assert not robot.is_estopped(), 'Robot is estopped.'

    # The robot state client will allow us to get the robot's state information
    robot_state_client = robot.ensure_client(RobotStateClient.default_service_name)

    # Lease to acquire robot control
    lease_client = robot.ensure_client(bosdyn.client.lease.LeaseClient.default_service_name)
    with bosdyn.client.lease.LeaseKeepAlive(lease_client, must_acquire=True, return_at_exit=True):
        # Power on the robot
        robot.logger.info('Powering on robot...')
        robot.power_on(timeout_sec=20)
        assert robot.is_powered_on(), 'Robot power on failed.'
        robot.logger.info('Robot powered on.')

   # Commanding the robot
    command_client = robot.ensure_client(RobotCommandClient.default_service_name)