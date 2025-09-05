from motor import init_client, set_wheel, set_both, set_speeds, stop
from vision_sensors import init_cameras, read_cameras

API_PATH = r"/home/jose/Descargas/CoppeliaSim_Edu_V4_10_0_rev0_Ubuntu22_04/programming/zmqRemoteApi/clients/src" #your path

WHEEL_R = 0.14

# Initialize the client and get the simulation and joint handles
sim, lj, rj = init_client(API_PATH)
sim, cam_handles = init_cameras(API_PATH, host='localhost', port=23000, base_name='/LineTracer/lineSensor')

#Example of usage
read_cameras(sim, cam_handles, dt=0.1, threshold=0.2)


set_both(sim, lj, rj, 0.0, WHEEL_R)

