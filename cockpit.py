import cv2
import pyautogui
from flask import Flask, render_template, Response, request, jsonify
import numpy as np
import threading
import asyncio
import keyboard
from PIL import Image
from io import BytesIO
app = Flask(__name__)
mfd_left=(1919,683,703,703)
mfd_right=(1919,1,703,703)
# Function to capture the first part of your screen
def capture_screen1():
    while True:
        screen = pyautogui.screenshot(region=mfd_left, allScreens=True)
        # Convert PIL Image to numpy array
        frame = np.array(screen)
        # Convert RGB image to BGR (OpenCV format)
        frame_bgr = cv2.cvtColor(frame, cv2.COLOR_RGB2BGR)
        # Convert numpy array to PIL Image
        image = Image.fromarray(frame_bgr)
        # Convert image to WebP format
        with BytesIO() as output:
            image.save(output, format='WEBP')
            frame_webp = output.getvalue()
        yield (b'--frame\r\n'
               b'Content-Type: image/webp\r\n\r\n' + frame_webp + b'\r\n')

# Function to capture the second part of your screen
def capture_screen2():
    while True:
        
        screen = pyautogui.screenshot(region=mfd_right, allScreens=True)
        # Convert PIL Image to numpy array
        frame = np.array(screen)
        # Convert RGB image to BGR (OpenCV format)
        frame_bgr = cv2.cvtColor(frame, cv2.COLOR_RGB2BGR)
        # Convert numpy array to PIL Image
        image = Image.fromarray(frame_bgr)
        # Convert image to WebP format
        with BytesIO() as output:
            image.save(output, format='WEBP')
            frame_webp = output.getvalue()
        yield (b'--frame\r\n'
               b'Content-Type: image/webp\r\n\r\n' + frame_webp + b'\r\n')

# Route to stream the first part of the screen
@app.route('/video_feed1')
def video_feed1():
    return Response(capture_screen1(), mimetype='multipart/x-mixed-replace; boundary=frame')

# Route to stream the second part of the screen
@app.route('/video_feed2')
def video_feed2():
    return Response(capture_screen2(), mimetype='multipart/x-mixed-replace; boundary=frame')

# Route to render the index.html page
@app.route('/')
def index():
    return render_template('index.html')

# Asynchronous function to process keyboard shortcuts
async def process_keyboard_shortcut(keys):
    key_val = keys.split('_')
    keys = key_val
    for key in keys:
        keyboard.press(key)
        await asyncio.sleep(0.1)  # You may adjust the delay as needed
    for key in keys:
        keyboard.release(key)

# Route to receive keyboard shortcuts
@app.route('/send-keyboard-shortcut', methods=['POST'])
def receive_keyboard_shortcut():
    data = request.json
    shortcut = data.get('shortcut')
    threading.Thread(target=asyncio.run, args=(process_keyboard_shortcut(shortcut),)).start()
    return jsonify({'message': 'Shortcut received and will be executed asynchronously'})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, threaded=True, debug=True)
