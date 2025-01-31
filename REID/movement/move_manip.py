import time
from spot_sdk import SpotClient

def distance_move():
    # Initialize Spot client and connect to robot
    spot = SpotClient()
    spot.connect()

    # Example of setting a sequence of movement commands (could involve moving in place, body adjustments, etc.)
    spot.move_body_forward(distance=0.1)  # Move the body forward slightly
    time.sleep(0.5)  # Pause for half a second
    spot.move_body_backward(distance=0.1)  # Move backward slightly
    time.sleep(0.5)  # Pause again

    # You can add more movements (side-to-side, rotating torso) here to add flair
    spot.move_body_rotate(angle=15)  # Rotate the torso by 15 degrees
    time.sleep(0.5)

    # Repeat or loop the movements to simulate the desired effect
    for _ in range(5):
        spot.move_body_forward(distance=0.1)
        spot.move_body_backward(distance=0.1)

    spot.disconnect()
