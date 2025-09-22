from line_follower import get_sensor_values, set_motor_speeds, sim
from keybrd import is_pressed

try:
    sim.startSimulation()
    while sim.getSimulationState() != sim.simulation_stopped:
        sensors = get_sensor_values()
        print(sensors)

        throttle = int(is_pressed('w')) - int(is_pressed('s'))  # 1, 0, or -1
        turn = int(is_pressed('d')) - int(is_pressed('a'))      # 1, 0, or -1
        turn_strength = 0.2
        turn *= turn_strength
        set_motor_speeds(throttle + turn, throttle - turn)      # normalized speeds (-1 to 1)
finally:    
    sim.stopSimulation()