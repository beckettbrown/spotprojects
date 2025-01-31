# control_leg.py
# A simple ROS node to control one of Spot's legs

from spot_sdk import SpotClient
from std_msgs.msg import String
import time

class SpotLegControl:
    def __init__(self):
        # Initialize the Spot client and connect to the robot
        self.spot = SpotClient()
        self.spot.connect()

    def control_leg(self, leg_name):
        """
        Move one leg at a time. Example for moving front left leg.
        Modify for other legs by changing 'leg_name'.
        """
        # Define the leg's joint names (e.g., for front left leg)
        if leg_name == "front_left":
            leg_joints = ['front_left_upper', 'front_left_lower', 'front_left_foot']
        elif leg_name == "front_right":
            leg_joints = ['front_right_upper', 'front_right_lower', 'front_right_foot']
        elif leg_name == "rear_left":
            leg_joints = ['rear_left_upper', 'rear_left_lower', 'rear_left_foot']
        elif leg_name == "rear_right":
            leg_joints = ['rear_right_upper', 'rear_right_lower', 'rear_right_foot']
        else:
            rospy.logerr(f"Invalid leg name: {leg_name}")
            return

        # Control each joint of the selected leg
        rospy.loginfo(f"Controlling {leg_name} leg...")
        for joint in leg_joints:
            self.move_joint(joint)

    def move_joint(self, joint_name):
        """
        Moves a single joint of the specified leg.
        """
        rospy.loginfo(f"Moving joint {joint_name}...")
        # Here, send position or velocity commands to each joint (replace with actual Spot SDK commands)
        # Example: Positioning the joint at a specific angle
        # Replace this with a real command using the Spot SDK's method for setting joint position.
        self.spot.set_joint_position(joint_name, 0.1)  # Adjust the value as necessary
        time.sleep(1)  # Adjust the sleep time to ensure the movement is completed

    def run(self):
        try:
            # Test controlling the front left leg (example)
            self.control_leg("front_left")
            rospy.loginfo("Leg control test complete.")
        except rospy.ROSInterruptException:
            rospy.logerr("ROS Interrupted, shutting down...")
        finally:
            # Disconnect from Spot once finished
            self.spot.disconnect()

if __name__ == '__main__':
    rospy.init_node('spot_leg_control_node', anonymous=True)
    control = SpotLegControl()
    control.run()
