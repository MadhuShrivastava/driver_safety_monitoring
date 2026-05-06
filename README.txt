# Driver Safety Monitoring System

Ever felt your eyes getting heavy on a long drive? This project was built to help with exactly that — a real-time system that watches for drowsiness and seatbelt violations so drivers stay safe on the road.
Real-time AI-based system for detecting driver drowsiness and seatbelt usage using computer vision.

---

## 📌 Overview

A real-time driver safety system that detects:

- 🚨 Drowsiness
- ⚠️ Seatbelt Violation (No Seatbelt)

Using:

- YOLOv8 for seatbelt detection
- MediaPipe for drowsiness detection
- Streamlit WebRTC for real-time interface

---

## 🎯 Features

- ✅ Real-time webcam monitoring
- ✅ YOLO-based seatbelt detection (`best.pt`)
- ✅ EAR-based drowsiness detection
- ✅ Threaded alarm system using `pygame` (non-blocking, loops until eyes open)
- ✅ Browser audio fallback for Streamlit Cloud deployment
- ✅ Clean and interactive Streamlit UI

---

## 🧠 System Architecture

```
Webcam → WebRTC → Frame Processing
        → YOLO (Seatbelt Detection)
        → MediaPipe (Drowsiness Detection)
        → Decision Engine
        → Alert System (pygame / browser audio) → UI Output
```

---

## ⚙️ Tech Stack

- Python
- Streamlit
- streamlit-webrtc
- Ultralytics YOLOv8
- OpenCV
- MediaPipe
- NumPy
- pygame

---

## 📂 Project Structure

```
driver_safety_monitoring/
│── app.py
│── seat_belt.py
│── drowsy_detection.py
│── best.pt
│── alarm.mp3
│── requirements.txt
│── README.md
```

---

## 🚀 Installation

```bash
git clone https://github.com/MadhuShrivastava/driver_safety_monitoring.git
cd driver_safety_monitoring
pip install -r requirements.txt
```

---

## ▶️ Run

```bash
streamlit run app.py
```

Open in browser: `http://localhost:8501`

---

## 🧪 How It Works

### 🔹 Seatbelt Detection

- YOLOv8 model detects:
  - `seatbelt`
  - `no_seatbelt`

### 🔹 Drowsiness Detection

- MediaPipe face landmarks
- EAR (Eye Aspect Ratio) calculation
- Threshold-based alert system

---

## 🔊 Alert System

- Thread-based (non-blocking)
- Loops `alarm.mp3` until the driver opens their eyes
- Cross-platform:
  - **Local** → `pygame` plays `alarm.mp3` through system speakers
  - **Streamlit Cloud** → browser-side `<audio>` fallback (no server speakers needed)

---

## 📊 Dataset

This project uses a seatbelt detection dataset from Roboflow Universe:

🔗 [Seatbelt Detection Dataset](https://universe.roboflow.com/madhus-workspace-bbugf/seatbelt-detection-lb1ec-ciwse/dataset/1)

| Split      | Images |
|------------|--------|
| Train      | 2442   |
| Validation | 698    |
| Test       | 349    |

- Classes: `seatbelt`, `no_seatbelt`
- Type: Object Detection
- Diverse real-world conditions for robust training

---

## ⚠️ Limitations

- Performance depends on lighting conditions
- Webcam quality affects accuracy
- Real-time inference may lag on low-end systems

---

## 📈 Future Scope

- Mobile usage detection
- Performance optimization
- Smart vehicle integration
- Advanced behavior tracking

---

## 🤝 Contributing

Pull requests are welcome.

---

## ⭐ Show Your Support

If you like this project, consider giving it a ⭐ on GitHub!

---

> This project demonstrates a real-time safety monitoring pipeline combining deep learning and computer vision for practical applications.