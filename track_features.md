# Line Follower Competition Rules

## Track Features

### Nominal Line
**Description:** Standard track line with no added challenge; used in straight or curved sections between other features.
**Key Specs (Max / Min):** Width: 20 mm; Continuous, high-contrast black line on white surface

![Nominal Line](images/nominal_line.png)

---

### Start Box
**Description:** Designated starting area where the wheelbase of the robot must be fully placed before the run begins. Ensures consistent positioning and fair starts for all teams.
**Key Specs (Max / Min):** Rectangular outline, 250 mm wide × 100 mm long; nominal line runs through the center.

![Start Box](images/start.png)

---

### Stop Box
**Description:** The official end of the track. Robots must detect the filled black area and come to a complete stop with their entire chassis fully contained within the box. This feature tests stopping accuracy, overshoot control, and final stability.
**Key Specs (Max / Min):** Solid black rectangle, 250 mm wide × 400 mm long; positioned at the end of the nominal line.

![Stop Box](images/stop.png)

---

### Turns
**Description:** Curved path sections of varying angles, from gentle arcs to sharp bends.
**Key Specs (Max / Min):** Min radius: 0.25 m (measured at centerline); Angle: any (e.g., 90°, 135°, 180°).

![Turns](images/turn.png)

---

### Variable Line Width
**Description:** Straight sections where the track line changes thickness, affecting how many sensors detect it at once.
**Key Specs (Max / Min):** Width: 15–25 mm (nominal ~20 mm).

![Variable Line Width](images/variable_line_width_0.png)
![Variable Line Width](images/variable_line_width_1.png)

---

### Line Discontinuities
**Description:** Line broken into dashes and gaps along a straight section.
**Key Specs (Max / Min):** Gap (space) ≤ 40 mm; Dash (line) ≥ 40 mm.

![Line Discontinuities](images/line_discontinuities.png)

---

### Wide Gap Crossing
**Description:** Gap in the line followed by a lateral shift before it resumes.
**Key Specs (Max / Min):** Gap (space) ≤ 40 mm; Lateral offset: 15–30 mm.

![Wide Gap Crossing](images/wide_gap.png)

---

### Fork Path Intersection
**Description:** Straight line with one or more perpendicular branches; only one path continues smoothly.
**Key Specs (Max / Min):** Branch angle: 90°; May appear left, right, or both. Branch length: 80 mm (from center line).

![Fork Path Intersection](images/fork_path_0.png)
![Fork Path Intersection](images/fork_path_1.png)

---

### Fake Parallel Lines
**Description:** Short false lines placed near the main one to mislead sensors.
**Key Specs (Max / Min):** Offset: 25–40 mm from true line; Length: 100 mm; Only on straights.

![Fake Parallel Lines](images/fake_parallel.png)

---

### Squiggly Line
**Description:** A wavy line oscillating left–right in a repeating pattern.
**Key Specs (Max / Min):** Amplitude: 60 mm; Period: 60 mm; Max length: 1.0 m; Width: 20 mm.

![Squiggly Line](images/squiggly_line.png)

---
