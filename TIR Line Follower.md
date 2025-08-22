# Line Follower Competition Rules

---

## Supersession Clause
This document supersedes all previous versions of the rules for the Line Follower category.  
In case of any discrepancies, the latest version published by the organizers shall prevail.  
In all cases, the general event rules take precedence over category-specific rules.

---

## 1. Introduction and Objective

The Line Follower category challenges teams to design and program a robot that can follow a black line on a white surface, navigating through a series of track elements and obstacles. Unlike other robotics competitions where participants bring their own hardware, here all competitors must use the **official robot kit** provided by the organizers.  

The kit is supplied as a set of components which teams must solder and assemble themselves. All schematics, design files, and datasheets are open-source and available through the official GitHub repository. This ensures that while the hardware is standardized, participants are encouraged to learn the details of every component in order to make informed programming decisions.  

A simulator is also provided, based on **CoppeliaSim** and programmed in Python, so that teams can begin experimenting with control strategies before their hardware is ready. Once assembled, the robot is programmed using an **ESP32-C6 development board**, typically through the Arduino IDE, though other environments (ESP-IDF, MicroPython) are also acceptable.  

The competition is structured around multiple tracks of varying complexity. Each track is divided into distinct challenge elements, and points are awarded for successfully completing them. Teams may earn partial points by clearing some challenges even if they cannot complete the full track. The final element of every track is a **stop box**, which must be reached and occupied fully by the robot to be considered complete.  

Points accumulate across all qualifying tracks, and the top-performing teams advance to the finals. Additional points are awarded to the fastest teams per track, ranked by placement.  

Competitors are encouraged to design **robust control strategies** that can adapt to varied tracks and conditions, rather than attempting to memorize a single layout. Not only is memorization impractical given the discrete sensor bar and variability of tracks, but in practice teams with solid control systems will always outperform attempts to game the layout.

---

## 2. The Robot

### 2.1 Dimensions
The robot kit has approximate fixed dimensions of **120 mm width by 180 mm length**, with a ground clearance of about 20 mm. The wheels extend slightly beyond these bounds. No modifications to the chassis, wheelbase, or motors are allowed.  

### 2.2 Mobility
The robot uses **two rear metal gear motors with encoders** and a passive front caster. Differential drive is required for all motion. The encoders provide AB channel Hall-effect outputs that teams must interpret to estimate wheel speed and distance.  

### 2.3 Sensors
At the front of the robot is a sensor bar of **eight infrared emitter/receiver pairs**, spaced 14 mm apart in a shallow arc. These sensors are connected through a comparator system with a single trimpot to adjust sensitivity, and their digital outputs are multiplexed for the microcontroller to read sequentially.  

Teams must carefully calibrate the trimpot under varying lighting conditions. The discrete nature of the array means that narrow lines may occasionally fall between sensors, requiring filtering and robust control algorithms.  

### 2.4 Power
The robot is powered by two **18650 Li-ion batteries** (3.7 V nominal each). These are not included in the kit due to shipping restrictions and must be sourced separately. Batteries feed through an undervoltage protection circuit, and regulated 3.3 V and 5 V rails power the components. Teams are responsible for safe handling and charging.  

### 2.5 Assembly
The kit includes primarily through-hole components, with a handful of surface-mount devices. Teams are strongly encouraged to practice soldering beforehand. The kit is sold **as is**, without warranty, though spare parts may be obtained via the organizers or from suppliers listed in the bill of materials.  

Teams may decorate or cosmetically modify their robot (e.g., 3D-printed shells), but may not alter the electronics, motors, sensors, or power system in any way. The only permitted functional modification is an optional **bumper or shade** in front of the sensor bar to mitigate lighting effects.  

### 2.6 Control Electronics
The main controller is an **ESP32-C6 development board**. It may be programmed with the Arduino IDE, ESP-IDF, or MicroPython, at the team’s discretion.  

A **start button** is included to initiate runs, and a DIP switch provides up to eight configurable profiles that teams can map to different control parameters. This allows rapid adjustment between runs without reprogramming the microcontroller.  

During competition runs, all **wireless functionality** of the ESP32-C6 (Wi-Fi, Bluetooth, or any other radio) must be strictly disabled. Any use of wireless communication during an official run will result in **immediate disqualification from the competition**.  
Outside of official runs—during practice or debugging—teams may freely use wireless features for logging, control, or development.

---

## 3. Track Specifications and Challenge Elements

### 3.1 Track Environment
The competition arena consists of large vinyl mats (at least 15 m × 15 m total) with tracks printed as black vinyl lines on a white background. Multiple tracks may be set up in parallel. The black line may reflect light, so teams must calibrate their sensors appropriately.  

Each day, new tracks will be presented. Early rounds use simpler tracks with fewer elements, while later rounds introduce more complex layouts. Teams are encouraged to build their own practice mats using the templates that may be shared via the Discord channel.  

### 3.2 Line Specifications
- **Width:** between 15 mm and 25 mm, with 20 mm as the most common value.  
- **Color:** always black line on white background.  
- **Spacing:** parallel tracks are separated by at least 25 cm, ensuring that robots only see one line at a time.  

Once calibrated during the first day, the line specifications remain consistent across all official tracks.  

### 3.3 Track Challenge Elements
Tracks are built from a standard set of challenge elements. During qualifying rounds, these appear individually or in straightforward combinations. **Hybrid challenges** (e.g., discontinuities inside curves) will not be used in the qualifying rounds but may appear in the **finals** to raise difficulty for top teams.  

Competitors should consult **Appendix A**, which contains diagrams and dimensions for each element.  

**List of challenge elements:**
- Variable Line Widths  
- Turns (Minimum Radius 0.25 m, up to 180°)  
- Squiggly Sections (Amplitude 60 mm, Period 60 mm, Length up to 1 m)  
- Discontinuities (Gaps up to 40 mm, with line segments of at least 40 mm between gaps)  
- Wide Gap Crossings with Lateral Offsets (gap of 40 mm, reappearing line shifted 15–30 mm center-to-center)  
- Fork Path Intersections (T or X-shapes, correct path = continuous curvature)
- Fake Short Parallel Lines (25–40 mm offset, length up to 100 mm, only on straight sections)  
- Stop Box (25 cm × 40 cm rectangle; robot must fully enter and stop)  

### 3.4 Lighting Conditions
The competition takes place indoors under mixed lighting (LED, halogen, natural light from windows). Lighting is not deliberately varied but may change slightly throughout the event. Teams may use bumper shades to guarantee uniform illumination of the sensors. External lighting devices on robots are forbidden.

---

## 4. Competition Rules, Scoring, Execution of Rounds & Jury

### 4.1 General Rules
Robots must be placed at the start area, indicated by two wheel placement marks printed on the track. Both rear wheels must be positioned within this area, but teams may orient the robot as they wish.  

The run begins when the team presses the robot’s start button, which simultaneously starts the official timer. Teams may not touch or intervene with the robot during the run. Any touch by a team member immediately counts as a reset attempt. Touches by judges (e.g., for safety reasons) do not count against the team.  

Each team has **three attempts per track**, with the best result recorded. Restarts always begin from the start zone, and the clock resets.  

During qualifying rounds, each track has a defined maximum time (e.g., 3–5 minutes depending on length). This will be announced at the start of each day. Teams must present themselves within one minute of being called or forfeit that track.  

### 4.2 Scoring System
Each track is composed of a series of challenge elements, each with an associated difficulty level (easy, medium, hard). Difficulty levels are described in Appendix A and determine the relative point values of challenges. Exact scoring for each track will be announced on the day of competition.  

Points are awarded only if the robot passes the **checkpoint** immediately after a challenge. Partial attempts without passing the checkpoint do not earn points. The stop box counts as the final challenge, requiring the robot to fully enter and stop.  

The fastest five teams to complete a track are awarded **bonus points**, equal to half the value of the highest-scoring challenge in that track. Rankings are relative, not absolute time differences.  

### 4.3 Penalties
A run is declared invalid if any of the following occur:
- The robot cuts across the track to skip a section.  
- The robot stops or fails to recover the line within a reasonable time (judge’s discretion).  
- The time limit expires.  
- Unauthorized hardware modifications are detected.  
- A team member interferes with the robot during the run.  
- The robot starts before the judge’s signal.  
- The robot communicates externally during the run, including any wireless connection.  

Attempting to modify the robot hardware in violation of Section 2 results in immediate **disqualification from the competition**.  

For safety reasons, the jury may also disqualify a robot if it exhibits dangerous behavior such as overheating, sparking, or uncontrolled motion.  

### 4.4 Execution of Rounds
During the qualifying phase, all teams compete on multiple tracks, accumulating points. No eliminations occur before finals. The five teams with the highest point totals advance to the finals.  

In the finals, tracks are longer and may include hybrid challenge elements. Teams again receive three attempts per track, with the best result recorded.  

Schedules and time limits are announced at the start of each day. Teams must monitor the official communication channels (website, email, Discord) for updates.  

### 4.5 Jury and Appeals
Each run is supervised by at least one jury member. Category managers are present in the arena. Final decisions are made by the jury, but teams may appeal to the managers and jury collectively. Once a joint decision is reached, it is final.  

Jury members are external robotics professionals or professors with no conflict of interest. All runs may be recorded; video evidence may be used to review disputes if available.  

---

## 5. Participation Requirements

### 5.1 Eligibility
Participation is open to all **university and high school students**. Teams may consist of up to five students and must register a single robot kit. Teams may optionally include a mentor, though this is not required. Proof of enrollment will be required.  

### 5.2 Registration
Teams must register for the overall event and separately purchase the official robot kit. Registration is per student; the kit is purchased once per team.  

The kit is sold **as is**. Minor flaws may occur; teams are responsible for assembly and operation. Spare parts can be obtained from suppliers listed in the bill of materials or purchased from organizers.  

Deadlines, fees, and procedures are published on the official event website. Teams must monitor website and email updates for changes.  

### 5.3 Team Preparation
Teams are expected to:  
- Assemble the kit.  
- Practice soldering beforehand.  
- Study schematics and datasheets.  
- Use the simulator to develop control strategies before hardware arrives.  

### 5.4 Equipment and Logistics
Organizers provide workstations with power outlets. Teams must bring laptops, batteries, chargers, and any tools needed. Separate event norms will govern workshop and arena use.  

Requests for accommodations may be submitted via Discord. While not guaranteed, common requests will be considered.  

### 5.5 Code of Conduct
Teams must follow the **general code of conduct** of the event, which is published separately. Failure to comply may result in disqualification regardless of category performance.  

The rules in this document apply only to the Line Follower category, but the general event rules always take precedence.

---

## Appendix A – Challenge Element Diagrams
(To be published separately with figures and exact dimensions.)

## Appendix B – Robot Bill of Materials & Datasheets
(To be published separately on GitHub and linked from the event website.)
