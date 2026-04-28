 Driver Safety Monitoring System

Real-time AI-based system for detecting driver drowsiness and seatbelt usage using computer vision.

---

📌 Overview

A real-time driver safety system that detects:

- 🚨 Drowsiness
- ⚠️ Seatbelt Violation (No Seatbelt)

Using:

- YOLOv8 for seatbelt detection
- MediaPipe for drowsiness detection
- Streamlit WebRTC for real-time interface

---

🎯 Features

- ✅ Real-time webcam monitoring
- ✅ YOLO-based seatbelt detection ("best.pt")
- ✅ EAR-based drowsiness detection
- ✅ Threaded beep alert system (non-blocking)
- ✅ Clean and interactive Streamlit UI

---

🧠 System Architecture

Webcam → WebRTC → Frame Processing
        → YOLO (Seatbelt Detection)
        → MediaPipe (Drowsiness Detection)
        → Decision Engine
        → Alert System → UI Output

---

⚙️ Tech Stack

- Python
- Streamlit
- streamlit-webrtc
- Ultralytics YOLOv8
- OpenCV
- MediaPipe
- NumPy

---

📂 Project Structure

driver_safety_monitoring/
│── app.py
│── seat_belt.py
│── drowsy_detection.py
│── best.pt
│── requirements.txt
│── README.md

---

🚀 Installation

git clone https://github.com/MadhuShrivastava/driver_safety_monitoring.git
cd driver_safety_monitoring
pip install -r requirements.txt

---

▶️ Run

streamlit run app.py

Open in browser:
http://localhost:8501

---

🧪 How It Works

🔹 Seatbelt Detection

- YOLOv8 model detects:
  - "seatbelt"
  - "no_seatbelt"

---

🔹 Drowsiness Detection

- MediaPipe face landmarks
- EAR (Eye Aspect Ratio) calculation
- Threshold-based alert system

---

🔊 Alert System

- Thread-based (non-blocking)
- Cross-platform:
  - Windows → "winsound.Beep()"
  - Others → system beep via subprocess

---

📊 Dataset

This project uses a seatbelt detection dataset from Roboflow Universe:

🔗 https://universe.roboflow.com/madhus-workspace-bbugf/seatbelt-detection-lb1ec-ciwse/dataset/1

Details:

- Classes: "seatbelt", "no_seatbelt"
- Type: Object Detection
- Split: 2442 train / 698 validation / 349 test

The dataset includes annotated images under diverse real-world conditions, enabling robust model training.

---

⚠️ Limitations

- Performance depends on lighting conditions
- Webcam quality affects accuracy
- Real-time inference may lag on low-end systems

---

📈 Future Scope

- Mobile usage detection
- Performance optimization
- Smart vehicle integration
- Advanced behavior tracking

---

🤝 Contributing

Pull requests are welcome.

---

⭐ Show your support

If you like this project, consider giving it a ⭐ on GitHub!

---

«This project demonstrates a real-time safety monitoring pipeline combining deep learning and computer vision for practical applications.»