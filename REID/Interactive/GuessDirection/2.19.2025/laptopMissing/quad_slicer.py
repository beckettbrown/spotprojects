from spot_sdk import SpotSdk

spot = SPotSdk()

robot_state =  spot.get_robot_state()

orientation = robot_state.pose.orientation

print(f"Yaw: {orientation.yaw}",f"Pitch: {orientation.pitch}, Roll: {orientation.roll}")
