# 🏎️ Gesture Racing Game

Control a racing car with your hand through your webcam. MediaPipe tracks your hand, Pygame runs the game.

---

## 🎮 Controls

| Input | Action |
| ----- | ------ |
| Open palm (5 fingers) | Accelerate |
| Fist | Brake |
| Tilt hand left/right | Steer |
| `C` | Calibrate (hold your hand in a neutral pose first) |
| `T` | Switch theme |
| `V` | Show/hide the camera preview |
| `R` | Restart after game over |
| `ESC` | Quit |

No hand in view means the car brakes.

---

## ✨ Features

* Real-time hand tracking (MediaPipe Hand Landmarker)
* Gesture steering with calibration and a dead zone
* Endless scrolling road: the car wraps from one side to the other
* Obstacles (barriers and cones) that move with the road, with spacing so the road is never blocked
* Difficulty ramp: starts with 3 obstacles, adds one every 5 points, up to 10
* 3 lives, score for every obstacle dodged, game over and restart
* Top speed cap, speed lines and road speed that follow the car
* 5 switchable themes: Night City, Desert Day, Grassland, Neon Synthwave, Snow
* Small webcam preview with hand landmarks

---

## 🏗️ Project Structure

```
Gesture-Racing-Game/
├── game/
│   ├── main.py              # Entry point and game loop
│   ├── car.py               # Car movement and physics
│   ├── obstacles.py         # Obstacles
│   ├── road.py              # Dashes, asphalt, curbs, speed lines
│   ├── scenery.py           # Themed scrolling background
│   ├── themes.py            # Theme colours and settings
│   ├── hand_tracker.py      # MediaPipe hand detection
│   ├── gestures.py          # Finger and steering logic
│   └── hand_landmarker.task # MediaPipe model file
├── images/
│   └── car1.png
└── README.md
```

---

## ⚙️ Installation

Use Python 3.13 (pygame has no prebuilt wheel for 3.14 yet).

```bash
py -3.13 -m pip install opencv-python mediapipe pygame numpy
```

`game/hand_landmarker.task` must be present. If it is missing, download it:

```
https://storage.googleapis.com/mediapipe-models/hand_landmarker/hand_landmarker/float16/1/hand_landmarker.task
```

---

## ▶️ Running

```bash
py -3.13 game/main.py
```

Connect your webcam, press `C` with your hand in a neutral pose, then play.

---

## 🧠 How It Works

1. The webcam frame goes to the MediaPipe hand landmarker.
2. `gestures.py` counts raised fingers (accelerate/brake) and measures the wrist-to-middle-finger angle against the calibrated angle (steering).
3. `main.py` applies this to the car, scrolls the road, scenery and obstacles at a speed based on the car's speed, and checks pixel-perfect collisions.

---

## 🚧 Ideas for Later

* High score saved to a file
* Pause and a start countdown
* Sound effects and music
* Gesture smoothing, crash effects, speedometer

---

## ⚠️ Notes

* Works best in good lighting with your hand clearly visible
* Avoid fast erratic movements

---

## 👨‍💻 Author

Ayush Sharma
B.E. CSE (AI/ML)
