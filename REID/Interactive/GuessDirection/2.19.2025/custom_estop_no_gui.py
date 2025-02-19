import logging
import signal
import sys
import threading
from bosdyn.client import create_standard_sdk
from bosdyn.client.estop import EstopClient, EstopEndpoint, EstopKeepAlive
from bosdyn.client.lease import LeaseClient, LeaseKeepAlive

def setup_estop(robot):
    # Create an Estop Client
    estop_client = EstopClient(robot)
    
    # Set up the Estop Endpoint
    estop_endpoint = EstopEndpoint(estop_client)

    # Set up the Estop KeepAlive to keep the endpoint alive
    estop_keepalive = EstopKeepAlive(estop_endpoint)

    # Start the keep-alive process in a separate thread
    estop_keepalive_thread = threading.Thread(target=estop_keepalive.run)
    estop_keepalive_thread.daemon = True
    estop_keepalive_thread.start()
    
    return estop_client, estop_endpoint, estop_keepalive

def main():
    logging.basicConfig(level=logging.INFO)

    # Connect to the robot (replace 'robot_name' with your robot's name or IP address)
    sdk = create_standard_sdk('EstopClient')
    robot = sdk.create_robot('robot_name')

    # Authenticate and connect to the robot
    robot.authenticate('username', 'password')

    # Set up Estop
    estop_client, estop_endpoint, estop_keepalive = setup_estop(robot)

    # Perform operations with Estop here
    try:
        # Add any operations you need with Estop control (e.g., activate Estop, check status)
        print("Estop is now active and running.")
        signal.pause()  # Keep the main program running until interrupted
    except KeyboardInterrupt:
        print("Exiting program.")
        estop_client.stop()  # Stop Estop if interrupted

if __name__ == "__main__":
    main()
