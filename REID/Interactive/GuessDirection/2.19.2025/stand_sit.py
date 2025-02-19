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
    sdk = bosdyn.client.create_standard_sdk('WakeUp Jarvis') # Change standard
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

    for i in range(5):  # Loop for standing action twice
            robot.logger.info(f'Commanding robot to stand, iteration {i + 1}...')
            blocking_stand(command_client, timeout_sec=10)
            robot.logger.info(f'Robot standing, iteration {i + 1}.')
            time.sleep(3)  # Optional: sleep for 3 seconds between iterations

            # Command the robot to sit after each standing action
            robot.logger.info(f'Commanding robot to sit, iteration {i + 1}...')
            blocking_sit(command_client, timeout_sec=10)
            robot.logger.info(f'Robot sitting, iteration {i + 1}.')
            time.sleep(3)  # Optional: sleep for 3 seconds after sitting
        
        # After the loop, power off the robot
    robot.logger.info('Powering off robot...')
    robot.power_off(cut_immediately=False, timeout_sec=20)
    assert not robot.is_powered_on(), 'Robot power off failed.'
    robot.logger.info('Robot safely powered off.')

def main():
    """Command line interface."""
    parser = argparse.ArgumentParser()
    bosdyn.client.util.add_base_arguments(parser)
    
    options = parser.parse_args()
    try:
        jarvis_squats(options)  # Call the function to make Spot stand and sit twice
        return True
    except Exception as exc:  # Error handling
        logger = bosdyn.client.util.get_logger()
        logger.error('Stand, Sit! threw an exception: %r', exc)
        return False


if __name__ == '__main__':
    if not main():
        sys.exit(1)
