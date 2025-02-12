import argparse
import os
import sys
import time
import threading

import tkinter as tk
from tkinter import messagebox

import bosdyn.client
import bosdyn.client.lease
import bosdyn.client.util
import bosdyn.geometry
from bosdyn.api.spot import robot_command_pb2 as spot_command_pb2
from bosdyn.client import math_helpers
from bosdyn.client.frame_helpers import GRAV_ALIGNED_BODY_FRAME_NAME, ODOM_FRAME_NAME, get_a_tform_b
from bosdyn.client.robot_command import RobotCommandBuilder, RobotCommandClient, blocking_stand, blocking_sit
from bosdyn.client.robot_state import RobotStateClient


class SpotControlApp:
    def __init__(self, master):
        self.master = master
        self.master.title("Spot Robot Control")
        self.master.geometry("400x300")

        # Label to show the current status
        self.status_label = tk.Label(master, text="Robot Status: Idle", font=("Helvetica", 14))
        self.status_label.pack(pady=20)

        # Buttons for control
        self.start_button = tk.Button(master, text="Start Standing/Sitting", command=self.start_actions)
        self.start_button.pack(pady=10)

        self.stop_button = tk.Button(master, text="Stop Robot", command=self.stop_robot, state=tk.DISABLED)
        self.stop_button.pack(pady=10)

        # Robot connection variables
        self.robot = None
        self.command_client = None
        self.running_thread = None

    def connect_to_spot(self, hostname, username, password):
        """Connect to the Spot robot."""
        sdk = bosdyn.client.create_standard_sdk('SpotControlClient')
        robot = sdk.create_robot(hostname)

        bosdyn.client.util.authenticate(robot, username, password)
        robot.time_sync.wait_for_sync()

        self.robot = robot
        self.command_client = robot.ensure_client(RobotCommandClient.default_service_name)

    def start_actions(self):
        """Start the standing and sitting actions in a separate thread."""
        self.start_button.config(state=tk.DISABLED)
        self.stop_button.config(state=tk.NORMAL)
        self.status_label.config(text="Robot Status: Standing/Sitting")

        # Start the actions in a background thread
        self.running_thread = threading.Thread(target=self.run_actions)
        self.running_thread.start()

    def run_actions(self):
        """Run the standing and sitting actions."""
        # Ensure that the robot is connected before issuing commands
        if self.robot is None or self.command_client is None:
            self.status_label.config(text="Robot not connected")
            return

        try:
            # Power on the robot (if not already powered on)
            self.robot.power_on(timeout_sec=20)
            assert self.robot.is_powered_on(), 'Robot power on failed.'

            # Perform stand and sit actions in a loop
            for _ in range(2):  # Two iterations
                # Command the robot to stand
                blocking_stand(self.command_client, timeout_sec=10)
                time.sleep(2)

                # Command the robot to sit
                blocking_sit(self.command_client, timeout_sec=10)
                time.sleep(2)

            # Power off the robot
            self.robot.power_off(cut_immediately=False, timeout_sec=20)
            assert not self.robot.is_powered_on(), 'Robot power off failed.'

            # Update GUI when done
            self.status_label.config(text="Robot Status: Idle")
            self.start_button.config(state=tk.NORMAL)
            self.stop_button.config(state=tk.DISABLED)

        except Exception as e:
            self.status_label.config(text="Robot Error")
            messagebox.showerror("Error", f"An error occurred: {str(e)}")

    def stop_robot(self):
        """Stop the robot."""
        if self.running_thread and self.running_thread.is_alive():
            # Stop the robot actions by powering it off immediately
            self.robot.power_off(cut_immediately=True, timeout_sec=10)
            self.status_label.config(text="Robot Status: Idle")
            self.start_button.config(state=tk.NORMAL)
            self.stop_button.config(state=tk.DISABLED)
            self.running_thread.join()


def main():
    """Set up and start the Tkinter GUI application."""
    # Create the main application window
    root = tk.Tk()

    # Create an instance of the SpotControlApp class
    app = SpotControlApp(root)

    # Configure Spot connection details (e.g., IP, username, password)
    hostname = '192.168.80.3'  # Change this to the actual IP of your Spot
    username = 'user'  # Enter your username
    password = 'asicf7znb6j8'  # Enter your password

    # Connect to the robot (this will run in the background)
    app.connect_to_spot(hostname, username, password)

    # Run the Tkinter main loop
    root.mainloop()


if __name__ == '__main__':
    main()
