import sys
import time
import numpy as np
import cv2
from coppeliasim_zmqremoteapi_client import RemoteAPIClient

def init_cameras(api_path, host='localhost', port=23000, base_name='/LineTracer/lineSensor'):
    sys.path.insert(0, api_path)
    client = RemoteAPIClient(host, port)
    sim = client.getObject('sim')

    # Start the simulation if it is currently stopped
    if sim.getSimulationState() == 0:
        sim.startSimulation()
        time.sleep(0.5)

    # Get the 8 camera handles
    cam_handles = []
    for i in range(8):
        path = f'{base_name}[{i}]'
        h = sim.getObject(path)
        cam_handles.append(h)

    return sim, cam_handles


#Reads the 8 vision sensors, prints 0/1 for each one,
#and opens debug windows showing what each sensor sees if activated.
def read_cameras(sim, cam_handles, dt=0.1, threshold=0.2):
    
    
    print("[INFO] Reading 8 Vision Sensors (Ctrl+C to stop)")
    try:
        while True:
            states = []
            for i, h in enumerate(cam_handles):
                img, res = sim.getVisionSensorImg(h)
                w, hres = int(res[0]), int(res[1])

                # Convert the buffer into a numpy array
                if isinstance(img, (bytes, bytearray)):
                    buf = np.frombuffer(img, dtype=np.uint8)
                    scale255 = True
                else:
                    buf = np.asarray(img, dtype=np.float32)
                    scale255 = False

                # Reconstruct the image: RGB or grayscale
                if buf.size == w * hres * 3:
                    if scale255:
                        frame = buf.reshape(hres, w, 3).astype(np.float32) / 255.0
                    else:
                        frame = (buf.reshape(hres, w, 3) + 1.0) / 2.0
                    gray = frame.mean(axis=2)
                elif buf.size == w * hres:
                    if scale255:
                        frame = buf.reshape(hres, w).astype(np.float32) / 255.0
                    else:
                        frame = (buf.reshape(hres, w) + 1.0) / 2.0
                    gray = frame
                else:
                    print(f"[WARN] Unexpected buffer size for sensor {i}")
                    continue

                # Binary detection: 1 if black (line), 0 if white (background)
                detected = 1 if gray.mean() < threshold else 0
                states.append(str(detected))

                # Show debug window for each sensor
                #debug_img = (gray * 255).astype(np.uint8)
                #cv2.imshow(f"Sensor {i}", debug_img)

            print("Vision:", " ".join(states), flush=True)

            # Press 'q' to close windows and stop
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break

            time.sleep(dt)

    except KeyboardInterrupt:
        print("\n[INFO] Camera reading stopped.")
    finally:
        cv2.destroyAllWindows()
