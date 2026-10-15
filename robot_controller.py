import requests
import time

# ✅ Send command to specific robot IP
def send_command(command, value=None, ip=None):
    if not ip:
        print("❌ No IP provided for send_command.")
        return

    url = f"http://{ip}/{command}"
    if value is not None:
        if command in ["left", "right"]:
            url += f"?angle={value}"
        else:
            url += f"?cm={value}"

    for attempt in range(3):
        try:
            print(f"[➡️] Sending to {ip}: {url}")
            response = requests.get(url, timeout=10)
            print(f"[✅] Response from {ip}: {response.text}")
            break
        except Exception as e:
            print(f"❌ Attempt {attempt + 1}: Failed to send '{command}' to {ip}\n{e}")
            time.sleep(2)

# Optional utility functions (not strictly needed anymore)
def move_forward(cm, ip):
    send_command("forward", cm, ip)

def move_backward(cm, ip):
    send_command("backward", cm, ip)

def turn_left(degrees, ip):
    send_command("left", degrees, ip)

def turn_right(degrees, ip):
    send_command("right", degrees, ip)	

def stop_robot(ip):
    send_command("stop", ip=ip)


