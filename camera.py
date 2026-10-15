import cv2
import numpy as np

# Replace with your DroidCam URL
CAMERA_URL = "http://192.168.31.13:8080/video"

cap = cv2.VideoCapture(CAMERA_URL)
cap.set(cv2.CAP_PROP_FRAME_WIDTH, 1280)
cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 720)

def get_frame():
    ret, frame = cap.read()
    if not ret:
        return None
    return frame

# Example function to detect objects (replace with your YOLO/ArUco detection)
def detect_objects(frame):
    # For simplicity, mock detection: robot positions and object positions
    robots = [{"id": 1, "x": 100, "y": 150}, {"id": 2, "x": 200, "y": 250}]
    objects = [{"name": "scissor", "x": 500, "y": 400}]
    return robots, objects

