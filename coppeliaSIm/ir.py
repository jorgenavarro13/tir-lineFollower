import sys
import time
from coppeliasim_zmqremoteapi_client import RemoteAPIClient

def init_ir_sensors(api_path, host='localhost', port=23000, base_name='/LineTracer'):
    sys.path.insert(0, api_path)
    client = RemoteAPIClient(host, port)
    sim = client.getObject('sim')

    # Start the simulation if it is stopped
    if sim.getSimulationState() == 0:
        sim.startSimulation()
        time.sleep(0.5)

    # Get the 8 handles
    ir_handles = []
    for i in range(8):
        path = f'{base_name}/proximitySensor[{i}]'
        handle = sim.getObject(path)
        ir_handles.append(handle)

    return sim, ir_handles

# Reads the IR sensors and displays their state
# Returns a list with the state of each sensor (0 or 1)
def read_ir_sensors(sim, ir_handles, dt=0.1):
    print("[INFO] Reading IR sensors (Ctrl+C to stop)")
    try:
        while True:
            states = []
            for h in ir_handles:
                ret = sim.readProximitySensor(h)
                detected = 1 if ret[0] else 0
                states.append(str(detected))
            print('IR:', ' '.join(states), flush=True)
            time.sleep(dt)
    except KeyboardInterrupt:
        print("\n[INFO] Sensor reading stopped.")
