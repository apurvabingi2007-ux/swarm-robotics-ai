import time
import os
import cv2

# ✅ Import shared get_image from image_tools
from image_tools import get_image

# === TOOL DEFINITIONS ===

def move_forward_tool():
    return {
        "type": "function",
        "function": {
            "name": "move_forward",
            "description": "Move the robot forward by a given distance in centimeters",
            "parameters": {
                "type": "object",
                "properties": {
                    "cm": {
                        "type": "integer",
                        "description": "Distance to move forward in centimeters"
                    }
                },
                "required": ["cm"]
            }
        }
    }

def move_backward_tool():
    return {
        "type": "function",
        "function": {
            "name": "move_backward",
            "description": "Move the robot backward by a given distance in centimeters",
            "parameters": {
                "type": "object",
                "properties": {
                    "cm": {
                        "type": "integer",
                        "description": "Distance to move backward in centimeters"
                    }
                },
                "required": ["cm"]
            }
        }
    }

def turn_left_tool():
    return {
        "type": "function",
        "function": {
            "name": "turn_left",
            "description": "Turn the robot to the left by a specified number of degrees",
            "parameters": {
                "type": "object",
                "properties": {
                    "degrees": {
                        "type": "integer",
                        "description": "Degrees to turn left"
                    }
                },
                "required": ["degrees"]
            }
        }
    }

def turn_right_tool():
    return {
        "type": "function",
        "function": {
            "name": "turn_right",
            "description": "Turn the robot to the right by a specified number of degrees",
            "parameters": {
                "type": "object",
                "properties": {
                    "degrees": {
                        "type": "integer",
                        "description": "Degrees to turn right"
                    }
                },
                "required": ["degrees"]
            }
        }
    }

def stop_robot_tool():
    return {
        "type": "function",
        "function": {
            "name": "stop_robot",
            "description": "Stop the robot immediately",
            "parameters": {
                "type": "object",
                "properties": {}
            }
        }
    }

def get_image_tool():
    return {
        "type": "function",
        "function": {
            "name": "get_image",
            "description": "Capture an image from the robot's camera and return the file path, robot position, detected objects, and pixel-to-cm calibration.",
            "parameters": {
                "type": "object",
                "properties": {}
            }
        }
    }

# === TOOL DEFINITIONS LIST ===

tool_definitions = [
    get_image_tool(),
    move_forward_tool(),
    move_backward_tool(),
    turn_left_tool(),
    turn_right_tool(),
    stop_robot_tool()
]

# === MOVEMENT FUNCTIONS ===

def move_forward(cm):
    print(f"Moving forward {cm}cm")

def move_backward(cm):
    print(f"Moving backward {cm}cm")

def turn_left(degrees):
    print(f"Turning left {degrees}°")

def turn_right(degrees):
    print(f"Turning right {degrees}°")

def stop_robot():
    print("Stopping robot")

# === FUNCTION MAPPING ===

function_map = {
    "get_image": get_image,  # ✅ Uses the shared fast camera
    "move_forward": move_forward,
    "move_backward": move_backward,
    "turn_left": turn_left,
    "turn_right": turn_right,
    "stop_robot": stop_robot
}
