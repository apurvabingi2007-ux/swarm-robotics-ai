
import cv2
import math
import time
import threading
from azure.cognitiveservices.vision.computervision import ComputerVisionClient
from msrest.authentication import CognitiveServicesCredentials

# ==== Azure Computer Vision Setup ====
AZURE_ENDPOINT = "YOUR_AZURE_ENDPOINT"
AZURE_KEY = "YOUR_AZURE_KEY"

computervision_client = ComputerVisionClient(
    AZURE_ENDPOINT, CognitiveServicesCredentials(AZURE_KEY)
)

# ==== Camera setup ====
CAMERA_IP = "http://192.168.31.13:8080/video"
cap = cv2.VideoCapture(CAMERA_IP, cv2.CAP_FFMPEG)
cap.set(cv2.CAP_PROP_FRAME_WIDTH, 1280)
cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 720)

if not cap.isOpened():
    print(f"❌ Failed to open camera: {CAMERA_IP}")
else:
    print("✅ Camera opened successfully")

# ==== ArUco setup ====
try:
    aruco_dict = cv2.aruco.getPredefinedDictionary(cv2.aruco.DICT_4X4_50)
    if hasattr(cv2.aruco, "DetectorParameters_create"):
        aruco_params = cv2.aruco.DetectorParameters_create()
    else:
        aruco_params = cv2.aruco.DetectorParameters()
    if hasattr(aruco_params, "cornerRefinementMethod"):
        aruco_params.cornerRefinementMethod = cv2.aruco.CORNER_REFINE_SUBPIX

    TRACK_IDS = [1, 2, 3]
except AttributeError:
    print("❌ cv2.aruco not found. Install opencv-contrib-python")
    aruco_dict = None
    aruco_params = None
    TRACK_IDS = []

# ==== Frame handling ====
frame_lock = threading.Lock()
latest_frame = None
last_robot_info = {}
last_objects = []

# ==== Threaded camera capture ====
def camera_thread():
    global latest_frame
    while True:
        ret, frame = cap.read()
        if ret:
            with frame_lock:
                latest_frame = frame
        else:
            print("⚠️ Failed to grab frame from camera")
        time.sleep(0.01)

thread = threading.Thread(target=camera_thread, daemon=True)
thread.start()

# ==== Robot detection ====
def detect_robots(frame):
    detected = {}
    if aruco_dict is None or aruco_params is None:
        return detected

    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    corners, ids, _ = cv2.aruco.detectMarkers(gray, aruco_dict, parameters=aruco_params)

    if ids is not None:
        ids = ids.flatten()
        for marker_id, corner in zip(ids, corners):
            if marker_id not in TRACK_IDS:
                continue
            pts = corner.reshape((4, 2))
            tl, tr, br, bl = pts
            cx = int((tl[0] + br[0]) / 2)
            cy = int((tl[1] + br[1]) / 2)
            top_mid = (tl + tr) / 2.0
            bot_mid = (bl + br) / 2.0
            vec = top_mid - bot_mid
            angle = (math.degrees(math.atan2(vec[1], vec[0])) + 360) % 360
            detected[marker_id] = {"pos": (cx, cy), "angle": round(angle, 2)}

            # Debug overlay
            cv2.aruco.drawDetectedMarkers(frame, [corner])
            cv2.circle(frame, (cx, cy), 6, (0, 255, 0), -1)
            cv2.putText(frame, f"ID {marker_id} θ={round(angle)}°",
                        (cx + 10, cy - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.5,
                        (255, 255, 255), 2)
    return detected

# ==== Object detection (Azure) ====
def detect_objects_azure(frame):
    detected_objects = []

    # Convert frame to JPEG bytes
    _, img_bytes = cv2.imencode(".jpg", frame)
    img_bytes = img_bytes.tobytes()

    try:
        results = computervision_client.detect_objects_in_stream(img_bytes)
        for obj in results.objects:
            detected_objects.append({
                "object": obj.object_property.lower(),
                "confidence": obj.confidence,
                "rectangle": {
                    "x": int(obj.rectangle.x),
                    "y": int(obj.rectangle.y),
                    "w": int(obj.rectangle.w),
                    "h": int(obj.rectangle.h)
                }
            })
    except Exception as e:
        print("❌ Azure detection error:", e)

    return detected_objects

# ==== Main capture function ====
def get_image():
    global last_robot_info, last_objects

    with frame_lock:
        frame = None if latest_frame is None else latest_frame.copy()
    if frame is None:
        print("⚠️ No frame available yet")
        return None, {}, []

    # Robot detection
    last_robot_info = detect_robots(frame)

    # Object detection
    last_objects = detect_objects_azure(frame)

    cv2.imshow("Robot View", cv2.resize(frame, (900, 600)))
    cv2.waitKey(1)

    return frame, last_robot_info, last_objects

# ==== Extract object position ====
def extract_object_position(detected_objects, target_object, min_confidence=0.5):
    for obj in detected_objects:
        if obj.get("object", "").lower() == target_object.lower() and obj.get("confidence", 0) >= min_confidence:
            x = obj["rectangle"]["x"] + obj["rectangle"]["w"] // 2
            y = obj["rectangle"]["y"] + obj["rectangle"]["h"] // 2
            return (x, y)
    return None

