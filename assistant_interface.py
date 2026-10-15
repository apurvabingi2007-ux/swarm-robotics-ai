
import time
from image_tools import get_image, extract_object_position
from robot_controller import send_command

STEP_CM = 1
MIN_CONFIDENCE = 0.5
PROXIMITY_CM_THRESHOLD = 3

ROBOT_IPS = {
    1: "192.168.31.46",
    2: "192.168.31.213",
    3: "192.168.31.65"
}

def move_one_step(direction, robot_id):
    ip = ROBOT_IPS.get(robot_id)
    if not ip:
        print(f"❌ IP not found for Robot {robot_id}")
        return
    value = STEP_CM if direction in ["forward", "backward"] else 90
    print(f"[➡️] Sending '{direction}' ({value}) to Robot {robot_id} @ {ip}")
    send_command(direction, value, ip)

def heuristic_direction(dx, dy, heading):
    if abs(dx) >= abs(dy):
        if dx > 0:
            if 315 <= heading or heading < 45:
                return "forward"
            elif 135 < heading < 225:
                return "backward"
            else:
                return "right" if 45 <= heading <= 135 else "left"
        else:
            if 135 < heading < 225:
                return "forward"
            elif 315 <= heading or heading < 45:
                return "backward"
            else:
                return "left" if 45 <= heading <= 135 else "right"
    else:
        if dy > 0:
            if 45 <= heading <= 135:
                return "forward"
            elif 225 <= heading <= 315:
                return "backward"
            else:
                return "right" if heading < 180 else "left"
        else:
            if 225 <= heading <= 315:
                return "forward"
            elif 45 <= heading <= 135:
                return "backward"
            else:
                return "left" if heading < 180 else "right"

def distance_cm(p1, p2):
    dx = p1[0] - p2[0]
    dy = p1[1] - p2[1]
    # Approximate distance in pixels (no real cm conversion)
    return (dx ** 2 + dy ** 2) ** 0.5

def main():
    print("🤖 Object-reaching assistant started")
    target_object = "scissors"
    reached = {rid: False for rid in ROBOT_IPS.keys()}

    while not all(reached.values()):
        frame, robot_info, detected_objects = get_image()
        if frame is None:
            time.sleep(0.5)
            continue

        obj_pos = extract_object_position(detected_objects, target_object, MIN_CONFIDENCE)
        if not robot_info or not obj_pos:
            print("⚠️ Robot or target not detected. Retrying...")
            time.sleep(1)
            continue

        for robot_id, info in robot_info.items():
            if reached.get(robot_id, True):
                continue
            robot_pos = info["pos"]
            heading_angle = info["angle"]
            dist = distance_cm(robot_pos, obj_pos)
            print(f"📏 Robot {robot_id} is {dist:.2f} pixels from target")

            if dist < PROXIMITY_CM_THRESHOLD:
                print(f"✅ Robot {robot_id} reached target!")
                reached[robot_id] = True
            else:
                dx = obj_pos[0] - robot_pos[0]
                dy = obj_pos[1] - robot_pos[1]
                command = heuristic_direction(dx, dy, heading_angle)
                move_one_step(command, robot_id)

        time.sleep(1)

    print("🎉 All robots reached the scissors")

if __name__ == "__main__":
    main()

