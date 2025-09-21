import numpy as np
from coppeliasim_zmqremoteapi_client import RemoteAPIClient
from keybrd import is_pressed, rising_edge

def init_motors():
    left_mtr = sim.getObject('/LineTracer/DynamicLeftJoint')
    right_mtr = sim.getObject('/LineTracer/DynamicRightJoint')
    return left_mtr, right_mtr

def init_sensors():
    base_name = "/LineTracer/lineSensor"
    cam_handles = []
    for i in range(8):
        path = f'{base_name}[{i}]'
        h = sim.getObject(path)
        cam_handles.append(h)
    return cam_handles

def get_sensor_values(threshold=0.2):
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

def set_motor_speed(mtr, rads):
    sim.setJointTargetVelocity(mtr, rads)

def diff_to_vels(throttle, steer):
    left = throttle + steer
    right = throttle - steer
    return left, right

client = RemoteAPIClient('localhost', 23000)
sim = client.getObject('sim')
left_mtr, right_mtr = init_motors()
cam_handles = init_sensors()

# Example usage
THROTTLE_MAX = 3.14 * 2.0  # Example max speed for motors
STEER_MAX = 3.14 * 0.5     # Example max steering adjustment
manual_mode = True
while True:
    sensor_values = get_sensor_values()
    print(sensor_values)

    # Mode toggle
    if rising_edge('m'):
        manual_mode = not manual_mode
        print(f"Mode: {'Manual' if manual_mode else 'Auto'}")
    
    if manual_mode:
        # Get normalized throttle and steering values (-1 to 1) based on WASD keys
        throttle = int(is_pressed('w')) - int(is_pressed('s'))
        steer = int(is_pressed('d')) - int(is_pressed('a'))
    else:
        Kp = -0.5
        sensors = get_sensor_values()
        error = (sensors[0] * -3.5 + sensors[1] * -2.5 + sensors[2] * -1.5 + sensors[3] * -0.5 +
                 sensors[4] *  0.5 + sensors[5] *  1.5 + sensors[6] *  2.5 + sensors[7] *  3.5)
        steer = Kp * error
        throttle = 0.5 # constant forward speed
    
    # Scale to max speeds
    throttle *= THROTTLE_MAX
    steer *= STEER_MAX

    # Set motor speeds
    left_speed, right_speed = diff_to_vels(throttle, steer)
    set_motor_speed(left_mtr, left_speed)
    set_motor_speed(right_mtr, right_speed)
