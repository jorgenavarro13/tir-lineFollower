import numpy as np
from coppeliasim_zmqremoteapi_client import RemoteAPIClient
from keybrd import is_pressed, rising_edge

# --- Functions you can use (don't change) --- #
def get_sensor_values(threshold=0.2):
    """
    Read the 8 vision sensors and return a list of 0/1 values
    (1 = line detected, 0 = no line)
    Example: [0, 0, 1, 1, 0, 0, 0, 0]
    """

    states = []
    for h in cam_handles:
        img, res = sim.getVisionSensorImg(h)
        w, hres = int(res[0]), int(res[1])

        # Convert the buffer into a numpy array
        buf = np.frombuffer(img, dtype=np.uint8)

        # Reconstruct the image: RGB or grayscale
        frame = buf.reshape(hres, w, 3).astype(np.float32) / 255.0
        gray = frame.mean(axis=2)

        # Binary detection: 1 if black (line), 0 if white (background)
        detected = 1 if gray.mean() < threshold else 0
        states.append(detected)  # Store as integer, not string
    
    return states

def set_motor_speeds(norm_left, norm_right):
    """
    Set both wheel speeds using normalized values (-1 to 1)
    -1 = full speed backward, 0 = stop, 1 = full speed forward
    
    Args:
        norm_left: normalized speed for left wheel (-1 to 1)
        norm_right: normalized speed for right wheel (-1 to 1)
    """
    # Clamp to [-1, 1] range
    norm_left = max(-1.0, min(1.0, norm_left))
    norm_right = max(-1.0, min(1.0, norm_right))
    
    # Convert to linear velocities in m/s
    left_linear_velocity = norm_left * MAX_SPEED
    right_linear_velocity = norm_right * MAX_SPEED
    
    # Convert to angular velocities in rad/s
    left_angular_velocity = left_linear_velocity / (WHEEL_D / 2)
    right_angular_velocity = right_linear_velocity / (WHEEL_D / 2)
    
    # Set the motor velocities
    client.setStepping(True)
    sim.setJointTargetVelocity(left_mtr, left_angular_velocity)
    sim.setJointTargetVelocity(right_mtr, right_angular_velocity)
    client.setStepping(False)

# --- Initialization code (don't change) --- #
WHEEL_D = 0.05  # Wheel diameter in meters
MAX_SPEED = 1.2 # m/s
client = RemoteAPIClient('localhost', 23000)
sim = client.getObject('sim')
left_mtr = sim.getObject('/LineTracer/DynamicLeftJoint')
right_mtr = sim.getObject('/LineTracer/DynamicRightJoint')
cam_handles = [sim.getObject(f"/LineTracer/lineSensor[{i}]") for i in range(8)]

# --- Your code starts here --- #
# Example usage
if __name__ == "__main__":
    try:
        sim.startSimulation()
        while sim.getSimulationState() != sim.simulation_stopped:
            sensors = get_sensor_values()                       # This will be a list of 0s or 1s. For example: [0, 0, 1, 1, 0, 0, 0, 0]
            print(sensors)

            deviation = sum(sensors[:4]) - sum(sensors[4:])     # This will be a value from -4 to +4
            steering_strength = 0.1                             # Adjust this value to change steering sensitivity
            norm_left = 0.5 + steering_strength * deviation     # This will be a value from 0 to 1
            norm_right = 0.5 - steering_strength * deviation    # This will be a value from 0 to 1
            set_motor_speeds(norm_left, norm_right)

    finally:
        sim.stopSimulation()
