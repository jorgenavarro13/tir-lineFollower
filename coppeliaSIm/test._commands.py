from motor import init_client, set_wheel, set_both, set_speeds, stop
from ir import init_ir_sensors, read_ir_sensors
API_PATH = r"C:\Program Files\CoppeliaRobotics\CoppeliaSimEdu\programming\zmqRemoteApi\clients\python\src" #your path

WHEEL_R = 0.14

sim, lj, rj = init_client(API_PATH)

sim, ir_handles = init_ir_sensors(API_PATH)

set_both(sim, lj, rj, 0.1, WHEEL_R)

read_ir_sensors(sim, ir_handles, dt=0.01)