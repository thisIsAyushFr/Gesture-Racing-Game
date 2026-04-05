# 🏎️ Gesture Racing Game

Control a racing car using just your hand gestures through your webcam. This project combines computer vision with game development to create a fun, interactive experience where your hand becomes the steering wheel.

---

## 🚀 Overview

This project uses **MediaPipe Hand Tracking** to detect hand movements and translates them into real-time controls in a racing game built with **Pygame**.

Instead of keyboard input:

* Tilt your hand → steer the car
* Make a fist → brake
* Show an open palm → accelerate

---

## 🎮 Features

* ✋ Real-time hand tracking using webcam
* 🏎️ Gesture-based car control
* 🛣️ Basic racing environment with boundaries
* 🚧 Obstacles for collision interaction
* 💨 Smooth movement with optional drifting physics
* ⚡ Lightweight and runs on CPU

---

## 🧠 Gesture Controls

| Gesture              | Action     |
| -------------------- | ---------- |
| Tilt Hand Left/Right | Steering   |
| Fist                 | Brake      |
| Open Palm            | Accelerate |

---

## 🏗️ Project Structure

```
gesture_racing/
│
├── main.py                # Entry point
├── hand_tracking.py       # MediaPipe hand detection
├── gesture_logic.py       # Gesture interpretation
│
├── game/
│   ├── car.py             # Car behavior
│   ├── physics.py         # Movement + drift logic
│   ├── track.py           # Track rendering
│   └── obstacles.py       # Obstacles system
│
├── assets/
│   ├── car.png
│   ├── track.png
│
└── README.md
```

---

## ⚙️ Installation

### 1. Clone the repository

```bash
git clone https://github.com/your-username/gesture-racing-game.git
cd gesture-racing-game
```

### 2. Install dependencies

```bash
pip install opencv-python mediapipe pygame numpy
```

---

## ▶️ Running the Project

```bash
python main.py
```

Make sure your webcam is connected and accessible.

---

## 🧩 How It Works

1. Webcam captures video frames
2. MediaPipe detects hand landmarks
3. Gesture logic interprets:

   * Hand angle → steering
   * Finger states → actions
4. Game engine updates:

   * Car speed
   * Direction
   * Position
5. Frame is rendered using Pygame

---

## 💨 Physics System

* Acceleration increases speed gradually
* Braking reduces speed smoothly
* Steering adjusts car angle
* Optional drifting adds inertia for realistic movement

---

## 🚧 Future Improvements

* 🏁 Lap system and scoring
* 🎵 Sound effects and background music
* 🌍 Multiple tracks and difficulty levels
* 🧠 AI opponents
* 📊 Performance optimization (CPU vs GPU experiments)
* 🎮 Menu and UI enhancements

---

## 🧪 Use Cases

* Computer vision + game dev project
* Human-computer interaction demo
* Mini research project (gesture-based control systems)
* Portfolio project for internships/research

---

## ⚠️ Notes

* Works best in good lighting conditions
* Keep hand clearly visible in frame
* Avoid fast erratic movements for better tracking

---

## 🤝 Contributing

Pull requests are welcome. For major changes, open an issue first to discuss what you'd like to improve.

---

## 📜 License

This project is open-source and available under the MIT License.

---

## 👨‍💻 Author

Ayush Sharma
B.E. CSE (AI/ML)

---

## 🌟 If you like this project

Give it a ⭐ on GitHub and share it with others!
