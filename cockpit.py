import cv2
import pyautogui
from flask import Flask, render_template, Response, request, jsonify
import numpy as np
import threading
import asyncio
import keyboard

app = Flask(__name__)
mfd_left=(1919,683,703,703)
mfd_right=(1919,1,703,703)
# Function to capture the first part of your screen
def capture_screen1():
    while True:
        screen = pyautogui.screenshot(region=mfd_left, allScreens=True)
        frame = cv2.cvtColor(np.array(screen), cv2.COLOR_RGB2BGR)
        ret, jpeg = cv2.imencode('.jpg', frame)
        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + jpeg.tobytes() + b'\r\n')

# Function to capture the second part of your screen
def capture_screen2():
    while True:
        # Modify the coordinates and dimensions as per your second screen region
        screen = pyautogui.screenshot(region=mfd_right, allScreens=True)
        frame = cv2.cvtColor(np.array(screen), cv2.COLOR_RGB2BGR)
        ret, jpeg = cv2.imencode('.jpg', frame)
        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + jpeg.tobytes() + b'\r\n')

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
    keys = [str(key_val[0]), str(key_val[1])]
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
