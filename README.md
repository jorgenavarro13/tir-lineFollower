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
