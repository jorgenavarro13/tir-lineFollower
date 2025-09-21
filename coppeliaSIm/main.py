from time import sleep
from motor import init_client, set_wheel, set_both, set_speeds, stop, set_speeds_rad
from vision_sensors import init_cameras, read_cameras, get_sensor_values

API_PATH = r"/home/jose/Descargas/CoppeliaSim_Edu_V4_10_0_rev0_Ubuntu22_04/programming/zmqRemoteApi/clients/src" #your path

WHEEL_R = 0.14

# Initialize the client and get the simulation and joint handles
sim, lj, rj = init_client(API_PATH)
sim, cam_handles = init_cameras(API_PATH, host='localhost', port=23000, base_name='/LineTracer/lineSensor')

def diff_mix(throttle, turn):
    #L = t - s;
    #R = t + s;

    left = throttle - turn
    right = throttle + turn
    return left, right

from keybrd import is_pressed, is_toggled
while True:
    sensors = get_sensor_values(sim, cam_handles, threshold=0.2)
    print("Sensors:", sensors)
    
    if not is_toggled('m'): # Manual mode
        throttle = (int(is_pressed('w')) - int(is_pressed('s'))) * 3.14 * 2
        turn = (int(is_pressed('a')) - int(is_pressed('d'))) * 3.14 * 0.25
    else:
        # Simple proportional controller
        Kp = 0.3
        error = (sensors[0] * -3.5 + sensors[1] * -2.5 + sensors[2] * -1.5 + sensors[3] * -0.5 +
                 sensors[4] *  0.5 + sensors[5] *  1.5 + sensors[6] *  2.5 + sensors[7] *  3.5)
        turn = Kp * error
        throttle = 1.0 # constant forward speed

    left, right = diff_mix(throttle, turn)

    set_speeds_rad(sim, lj, rj, left_rad_s=left, right_rad_s=right)
    sleep(0.1)
