import sys
from coppeliasim_zmqremoteapi_client import RemoteAPIClient

def init_client(api_path,
                host='localhost', port=23000,
                left_joint_path='/DynamicLeftJoint',
                right_joint_path='/DynamicRightJoint'):
    if api_path not in sys.path:
        sys.path.insert(0, api_path)
    client = RemoteAPIClient(host, port)
    sim = client.getObject('sim')
    left_joint  = sim.getObject(left_joint_path)
    right_joint = sim.getObject(right_joint_path)
    return sim, left_joint, right_joint

def _clamp(v, vmin, vmax):
    return max(vmin, min(vmax, v))

def _mps_to_rads(v_mps, wheel_radius_m):
    if wheel_radius_m <= 0:
        raise ValueError("wheel_radius_m must be > 0")
    return v_mps / wheel_radius_m

# side 0 = left, 1 = right
# left_sign/right_sign: change to -1 if a wheel is reversed
# v_mps: desired linear speed in m/s (saturated to vmax_mps)
def set_wheel(sim, left_joint, right_joint,
              side, v_mps,
              wheel_radius_m,
              vmax_mps=1.2,
              left_sign=1.0, right_sign=1.0):
    v = _clamp(float(v_mps), -vmax_mps, vmax_mps)
    w = _mps_to_rads(v, wheel_radius_m)
    if side == 0:
        sim.setJointTargetVelocity(left_joint,  left_sign * w)
    elif side == 1:
        sim.setJointTargetVelocity(right_joint, right_sign * w)
    else:
        raise ValueError("Side must be 0 (left) or 1 (right)")
    return v  # returns the applied speed

# Sends the same value to both wheels (m/s)
def set_both(sim, left_joint, right_joint,
             v_mps,
             wheel_radius_m,
             vmax_mps=1.2,
             left_sign=1.0, right_sign=1.0):
    v = _clamp(float(v_mps), -vmax_mps, vmax_mps)
    w = _mps_to_rads(v, wheel_radius_m)
    sim.setJointTargetVelocity(left_joint,  left_sign * w)
    sim.setJointTargetVelocity(right_joint, right_sign * w)
    return v

# Sends different values to each wheel (m/s)
def set_speeds(sim, left_joint, right_joint,
               v_left_mps, v_right_mps,
               wheel_radius_m,
               vmax_mps=1.2,
               left_sign=1.0, right_sign=1.0):
    vL = _clamp(float(v_left_mps),  -vmax_mps, vmax_mps)
    vR = _clamp(float(v_right_mps), -vmax_mps, vmax_mps)
    sim.setJointTargetVelocity(left_joint,  left_sign  * _mps_to_rads(vL, wheel_radius_m))
    sim.setJointTargetVelocity(right_joint, right_sign * _mps_to_rads(vR, wheel_radius_m))
    return vL, vR

# Stops both motors
def stop(sim, left_joint, right_joint):
    sim.setJointTargetVelocity(left_joint,  0.0)
    sim.setJointTargetVelocity(right_joint, 0.0)
