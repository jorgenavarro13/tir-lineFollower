# TIR Line Follower

This repository contains all the resources needed to design, assemble, and test the **Line Follower Robot** for the competition. Both hardware and software components are included so teams can prepare thoroughly.

---

## 📂 Repository Structure

### 🔧 Hardware  
The `hardware/` folder contains:
- **Photos** of the PCB and assembled robot.  
- **Datasheets** for all key components.  
- **Schematics** and design files for the printed circuit board (PCB).  

All schematics and design files are open-source and align with the official competition kit.

---

### 🏁 Track Composer  
The `trackComposer/` directory includes **track templates**.  
- These files can be used to **print and build practice tracks**. You can download some examples [HERE](https://drive.google.com/drive/folders/1T4SW41VzTQQqG8hMeqaypMbbVBZAvxJS?usp=sharing), and probably find more in the Discord Community.
- A video tutorial explaining how to construct to-scale tracks for the simulator and which you can print too.
- Templates cover a variety of challenge elements (curves, forks, discontinuities, stop box, etc.) consistent with competition rules.  

This allows teams to test their robots on layouts similar to official competition tracks.  

---

### 🤖 CoppeliaSim  
The `coppeliaSIm/` directory contains all the files required to run the **official simulator**:  
- Pre-built robot model.  
- Simulation environment.  
- Python-based control interface.  

The simulator enables teams to **experiment with control strategies before the physical hardware is assembled**, helping with algorithm development and debugging.  


#### 📑 Components
- **`main.py`**  
  Entry point of the simulation.  
  - Initializes the simulation client.  
  - Loads the 8 vision sensors from the robot.  
  - Demonstrates how to read sensor states (0 = background, 1 = line).  
  - Provides an example of motor control using `set_both`.  

- **`motor.py`**  
  Functions to control the robot’s wheels.  
  - `init_client`: connects to CoppeliaSim and retrieves wheel joint handles.  
  - `set_wheel`: sets velocity for one wheel.  
  - `set_both`: sets the same velocity for both wheels (forward motion).  
  - `set_speeds`: sets different velocities for left and right wheels (turning).  
  - `stop`: stops both wheels.  

- **`vision_sensors.py`**  
  Functions to read the robot’s vision sensors.  
  - `init_cameras`: loads the 8 line sensors placed at the robot’s front.  
  - `read_cameras`: reads the sensor images, applies a threshold, and returns binary values (`0` or `1`).  
  - Optionally, debug windows can be opened with OpenCV to visualize what each sensor is detecting.  

#### ⚙️ How it Works
1. **Simulation Environment**  
   - The robot is equipped with **8 vision sensors** aligned at the front.  
   - Each sensor detects if it is over the **black line (1)** or **white background (0)**.  
   - These binary values simulate the typical behavior of IR sensors on a real line follower robot.  

2. **Motor Control**  
   - The wheels are controlled via velocity commands.  
   - By combining the vision sensor outputs with the motor functions, you can implement a line-following algorithm (e.g., proportional or PID control).  

3. **Debugging**  
   - Each sensor can open an OpenCV window showing its captured view.  
   - This helps validate whether thresholds are correctly distinguishing the line from the background.  
   - Example console output:  
     ```text
     Vision: 0 0 1 1 1 0 0 0
     ```  
     Here, the middle sensors detect the line, while the others see the background.  

#### ▶️ Running the Simulator
1. Make sure **CoppeliaSim** is installed and the **ZMQ Remote API** is enabled.  
2. Update the `API_PATH` variable inside `main.py` with the correct path to your `zmqRemoteApi/clients/python` folder.  
3. Start CoppeliaSim and load the robot scene (included in this repository).  
4. Run the script:  
   ```bash
   pip install numpy pandas opencv-python coppeliasim-zmqremoteapi-client
   python3 main.py
   ```
---

#### ✍️ Author

This code, simulation and environment setup were developed by **Jose Luis Urquieta Aguilar** as part of the TIR Line Follower project.  
Feel free to use, modify, and improve it.  


---

## 🚀 Getting Started

1. Clone this repository:  
   ```bash
   git clone [https://github.com/<your-org>/tir-lineFollower.git](https://github.com/IRS-tecMty/tir-lineFollower.git)
   cd tir-lineFollower
   ```
2. Explore the `hardware/` directory to familiarize yourself with the robot design.  
3. Use `trackComposer/` to print and set up practice tracks.  
4. Run the simulator from `coppeliaSIm/` to begin testing control algorithms.  

---

## 📜 License
All hardware schematics, datasheets, and design files are **open-source**. You are free to use, modify, and redistribute them in accordance with the competition guidelines.
