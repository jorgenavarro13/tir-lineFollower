import numpy as np
from coppeliasim_zmqremoteapi_client import RemoteAPIClient
from keybrd import is_pressed, rising_edge
import time

class PID:
    def __init__(self, Kp, Ki, Kd, output_limit=None, integral_limit=None):
        self.Kp = Kp
        self.Ki = Ki
        self.Kd = Kd
        self.prev_error = 0.0
        self.integral = 0.0
        self.output_limit = output_limit
        self.integral_limit = integral_limit

    def compute(self, error, dt):
        if dt <= 0:
            return 0.0
        # integral (with anti-windup)
        self.integral += error * dt
        if self.integral_limit is not None:
            self.integral = max(min(self.integral, self.integral_limit), -self.integral_limit)

        derivative = (error - self.prev_error) / dt
        out = self.Kp * error + self.Ki * self.integral + self.Kd * derivative
        self.prev_error = error

        if self.output_limit is not None:
            out = max(min(out, self.output_limit), -self.output_limit)
        return out

def compute_error(sensors, positions):
    s_sum = sum(sensors)
    if s_sum == 0:
        return None
    return sum(p * v for p, v in zip(positions, sensors)) / s_sum




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

        # PID tunning (valores iniciales; ajusta)
        pid = PID(Kp=0.12, Ki=0.0, Kd=0.08, output_limit=0.35, integral_limit=1.0)

        base_speed = 0.30          # reduce para curvas cerradas
        positions = [-3.5, -2.5, -1.5, -0.5, 0.5, 1.5, 2.5, 3.5]  # mejor resolución central

        # filtros y límites
        error_filtered = 0.0
        alpha = 0.3                # factor de suavizado exponencial (0-1) → menor = más suavizado
        last_time = time.time()
        left_speed = right_speed = 0.0
        max_delta = 0.1            # límite de cambio por iteración (slew rate)
        last_known_direction = 0   # -1 left, 1 right, 0 unknown

        while sim.getSimulationState() != sim.simulation_stopped:
            now = time.time()
            dt = now - last_time
            if dt <= 0:
                dt = 1e-3
            last_time = now

            sensors = get_sensor_values()  # [0/1] * 8
            raw_error = compute_error(sensors, positions)

            if raw_error is None:
                # Línea perdida: gira suavemente hacia última dirección conocida en vez de corrección brusca
                if last_known_direction == 0:
                    correction = 0.0
                else:
                    # aplicar pequeña corrección sostenida para buscar la línea
                    correction = 0.15 * last_known_direction
            else:
                # actualiza dirección conocida
                last_known_direction = -1 if raw_error < 0 else (1 if raw_error > 0 else last_known_direction)
                # filtro exponencial para suavizar saltos
                error_filtered = alpha * raw_error + (1 - alpha) * error_filtered
                correction = pid.compute(error_filtered, dt)

            # aplica correccion al par de motores
            target_left = base_speed + correction
            target_right = base_speed - correction

            # limita rangos -1..1
            target_left = max(min(target_left, 1.0), -1.0)
            target_right = max(min(target_right, 1.0), -1.0)

            # slew rate limiter: no cambiar más rapido que max_delta por ciclo
            left_speed = left_speed + max(min(target_left - left_speed, max_delta), -max_delta)
            right_speed = right_speed + max(min(target_right - right_speed, max_delta), -max_delta)

            set_motor_speeds(left_speed, right_speed)

            # pequeña pausa estable; ajusta según performance del simulador
            time.sleep(0.02)

    finally:
        sim.stopSimulation()
