import cv2
import numpy as np
from ultralytics import YOLO
import os

# Model loading

_MODEL_PATH = os.path.join(os.path.dirname(__file__), "best.pt")
_model = None


def _load_model():
    global _model
    if _model is None:
        if not os.path.exists(_MODEL_PATH):
            raise FileNotFoundError(
                f"YOLO weights not found at '{_MODEL_PATH}'. "
                "Place best.pt in the same directory as seat_belt.py."
            )
        _model = YOLO(_MODEL_PATH)

        print("Loaded model with classes:", _model.names)

    return _model


# Main function 

def detect_seatbelt(frame: np.ndarray, conf_threshold: float = 0.5) -> np.ndarray:
 
    model = _load_model()
    results = model(frame, verbose=False)[0]

    seatbelt_status = "unknown"  # default state

    no_seatbelt_detected = False
    seatbelt_detected = False
    
    # Detecting the seatbelt status
    if results.boxes is not None and len(results.boxes):
        for box in results.boxes:
            conf = float(box.conf[0])
            if conf < conf_threshold:
                continue

            cls_id = int(box.cls[0])
            label = model.names[cls_id].lower()

            # Bounding box
            x1, y1, x2, y2 = map(int, box.xyxy[0])

            if label == "no_seatbelt":
                no_seatbelt_detected = True
                color = (0, 0, 255)  # red

            elif label == "seatbelt":
                seatbelt_detected = True
                color = (0, 255, 0)  # green

            else:
                color = (255, 255, 0)  # unknown class

            # Draw box
            cv2.rectangle(frame, (x1, y1), (x2, y2), color, 2)

            # Label text
            cv2.putText(
                frame,
                f"{label} {conf:.2f}",
                (x1, max(y1 - 8, 0)),
                cv2.FONT_HERSHEY_SIMPLEX,
                0.6,
                color,
                2,
            )

    if no_seatbelt_detected:
        seatbelt_status = "off"
        text = "Seatbelt OFF"
        color = (0, 0, 255)

    elif seatbelt_detected:
        seatbelt_status = "on"
        text = "Seatbelt ON"
        color = (0, 255, 0)

    else:
        text = "Seatbelt: Unknown"
        color = (0, 255, 255)

    # Status display
    cv2.putText(
        frame,
        text,
        (10, 60),
        cv2.FONT_HERSHEY_SIMPLEX,
        0.7,
        color,
        2,
    )

    return frame