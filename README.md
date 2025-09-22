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


### 🏁 Track Specifications and Track Composer
You can find more about the track features, specifications and measurements in the [official website and rules](https://www.larc-lars2025.org/tir-line-follower).

The `trackComposer/` directory includes **track templates**.  
- These files can be used to **print and build practice tracks**. You can download some examples [HERE](https://drive.google.com/drive/folders/1T4SW41VzTQQqG8hMeqaypMbbVBZAvxJS?usp=sharing), and probably find more in the Discord Community.  
- A **video tutorial** explaining how to construct to-scale tracks for the simulator and which you can print too.  
- Templates cover a variety of challenge elements (curves, forks, discontinuities, stop box, etc.) consistent with competition rules.  

This allows teams to test their robots on layouts similar to official competition tracks.  

---

### 🤖 CoppeliaSim2  
The `coppeliaSIm2/` directory contains all the files required to run the **official simulator**:  
- Pre-built robot model.  
- Simulation environment.  
- Python control script.  

The simulator enables teams to **experiment with control strategies before the physical hardware is assembled**, helping with algorithm development and debugging.  

---

# ⚡ Quick Start Guide for Simulator

1. Clone this repository:  
   ```bash
   git clone [https://github.com/<your-org>/tir-lineFollower.git](https://github.com/IRS-tecMty/tir-lineFollower.git)
   cd tir-lineFollower
   ```
2. Explore the `hardware/` directory to familiarize yourself with the robot design.  
3. Use `trackComposer/` to print and set up practice tracks.  
4. Run the simulator from `coppeliaSIm2/` to begin testing control algorithms.  


Follow these steps to set up and run the line follower simulation:
1. **Download and Install CoppeliaSim Edu Edition**  
   [CoppeliaSim Edu Edition](https://www.coppeliarobotics.com/)

2. **Install Python**  
   Make sure [Python](https://www.python.org/downloads/) is installed on your system.

3. **Download the Repository**  
   [tir-lineFollower GitHub Repository](https://github.com/IRS-tecMty/tir-lineFollower)

4. **Install Required Python Libraries**  
   Run the following command in your terminal:
   ```bash
   pip install coppeliasim_zmqremoteapi_client numpy pynput
   ```

5. **Open the Simulation File in CoppeliaSim**  
   Open:
   ```
   tir-lineFollower\CoppeliaSim2\linefollower.ttt
   ```

6. **Run the Python Script**  
   Execute:
   ```
   tir-lineFollower\CoppeliaSim2\line_follower.py
   ```
   The robot should now start moving in the CoppeliaSim window.

---

# 📑 Example Code: Components & How it Works  

The `line_follower.py` script has two main parts:  

---

### 🔧 Fixed Code (System Setup)  

This part is required to make the simulator run.  

- **What it does**:  
  - Connects to CoppeliaSim.  
  - Sets up the **8 sensors** and **2 motors**.  
  - Defines wheel radius and max speed.  

- **Key functions you’ll actually use**:  
  - `get_sensor_values(threshold=0.2)` → gives you 8 binary values (`0 = background`, `1 = line`).  
  - `set_motor_speeds(norm_left, norm_right)` → commands left and right wheels (normalized: `-1` = full reverse, `0` = stop, `1` = full forward).  

- **Other details**: wheel radius, max speed, and API setup are included here.  

- **Important note**:  
  - Do **not modify this section** — it is part of how the system is built.  
  - You don’t need to fully understand every line, just what the two main functions do — because **those are your tools** for building the control logic.  

---

### 🧪 Custom Code (Where You Take Control 🚀)  

This is **your playground** — where you design the robot’s brain.  

In the file, look for this section:  

```python
if __name__ == "__main__":
    try:
        sim.startSimulation()
        while sim.getSimulationState() != sim.simulation_stopped:
            sensors = get_sensor_values()
            print(sensors)

            deviation = sum(sensors[:4]) - sum(sensors[4:])
            steering_strength = 0.1
            norm_left = 0.5 + steering_strength * deviation
            norm_right = 0.5 - steering_strength * deviation
            set_motor_speeds(norm_left, norm_right)
```

👉 **This `while` loop is the part you’ll change!**  

Right now, it contains a very simple example:  

- Reads the sensors.  
- Prints them to the console.  
- Computes a crude *bang-bang* style deviation (left vs. right).  
- Sends basic motor commands so the robot wiggles its way along the track.  

---

### 💡 Why this Example Exists  

- To prove the simulator is running correctly.  
- To show how the two key functions (sensors + motors) work together.  
- To give you a minimal “hello world” for robot control.  

---

### 🚀 What You Should Do Next  

- Run the code as-is once to confirm your setup works.  
- Then **replace the inside of the `while` loop** with your own strategy.  
  - Want smoother turns? Try proportional control.  
  - Want competition-ready precision? Implement PID control.  
  - Curious about alternatives? Experiment!  

This is where your creativity goes. The **fixed code** gets the robot talking to the simulator, but the **custom code** is where you make it intelligent.  

---

### 🎮 Alternative Example: `wasd_example.py`  

We also provide a second example called **`wasd_example.py`**.  

- This script imports the sensor and motor functions from `line_follower.py`.  
- Instead of automatic control, you **manually drive the robot** using the keyboard:  
  - `W` = forward  
  - `S` = backward  
  - `A` = turn left  
  - `D` = turn right  

Here’s the core loop from the file:  

```python
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
```

👉 Run this script to test your simulator setup and **control the robot with your keyboard**.  
This is another example of how to build your own code on top of the fixed functions.  

---

## 📜 License
All hardware schematics, datasheets, and design files are **open-source**. You are free to use, modify, and redistribute them in accordance with the competition guidelines.  
