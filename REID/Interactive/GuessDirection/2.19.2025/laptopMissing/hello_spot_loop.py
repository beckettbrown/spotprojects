import argparse
import os
import sys
import time

import bosdyn.client
import bosdyn.client.lease
import bosdyn.client.util
import bosdyn.geometry
from bosdyn.api import trajectory_pb2
from bosdyn.api.spot import robot_command_pb2 as spot_command_pb2
from bosdyn.client import math_helpers
from bosdyn.client.frame_helpers import GRAV_ALIGNED_BODY_FRAME_NAME, ODOM_FRAME_NAME, get_a_tform_b
from bosdyn.client.image import ImageClient
from bosdyn.client.robot_command import RobotCommandBuilder, RobotCommandClient, blocking_stand, blocking_sit
from bosdyn.client.robot_state import RobotStateClient
from bosdyn.util import seconds_to_duration


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

        # Commanding the robot to stand twice
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

        # Capture an image.
        # Spot has five sensors around the body. Each sensor consists of a stereo pair and a
        # fisheye camera. The list_image_sources RPC gives a list of image sources which are
        # available to the API client. Images are captured via calls to the get_image RPC.
        # Images can be requested from multiple image sources in one call.
        image_client = robot.ensure_client(ImageClient.default_service_name)
        sources = image_client.list_image_sources()
        image_response = image_client.get_image_from_sources(['frontleft_fisheye_image'])
        _maybe_display_image(image_response[0].shot.image)
        if config.save or config.save_path is not None:
            _maybe_save_image(image_response[0].shot.image, config.save_path)


def _maybe_display_image(image, display_time=3.0):
    """Try to display image, if client has correct deps."""
    try:
        import io

        from PIL import Image
    except ImportError:
        logger = bosdyn.client.util.get_logger()
        logger.warning('Missing dependencies. Can\'t display image.')
        return
    try:
        image = Image.open(io.BytesIO(image.data))
        image.show()
        time.sleep(display_time)
    except Exception as exc:
        logger = bosdyn.client.util.get_logger()
        logger.warning('Exception thrown displaying image. %r', exc)


def _maybe_save_image(image, path):
    """Try to save image, if client has correct deps."""
    logger = bosdyn.client.util.get_logger()
    try:
        import io

        from PIL import Image
    except ImportError:
        logger.warning('Missing dependencies. Can\'t save image.')
        return
    name = 'hello-spot-img.jpg'
    if path is not None and os.path.exists(path):
        path = os.path.join(os.getcwd(), path)
        name = os.path.join(path, name)
        logger.info('Saving image to: %s', name)
    else:
        logger.info('Saving image to working directory as %s', name)
    try:
        image = Image.open(io.BytesIO(image.data))
        image.save(name)
    except Exception as exc:
        logger = bosdyn.client.util.get_logger()
        logger.warning('Exception thrown saving image. %r', exc)


def main():
    """Command line interface."""
    parser = argparse.ArgumentParser()
    bosdyn.client.util.add_base_arguments(parser)
    parser.add_argument(
        '-s', '--save', action='store_true', help=
        'Save the image captured by Spot to the working directory.'
    )
    parser.add_argument(
        '--save-path', default=None, nargs='?', help=
        'Save the image captured by Spot to the provided directory.'
    )
    options = parser.parse_args()
    try:
        jarvis_squats(options)  # Call the function to make Spot stand and sit twice
        return True
    except Exception as exc:  # Error handling
        logger = bosdyn.client.util.get_logger()
        logger.error('Hello, Spot! threw an exception: %r', exc)
        return False


if __name__ == '__main__':
    if not main():
        sys.exit(1)
