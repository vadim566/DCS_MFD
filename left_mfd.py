import cv2
import pyautogui
from flask import Flask, render_template, Response, request, jsonify
import numpy as np
import threading
import asyncio
import keyboard

app = Flask(__name__)

# Function to capture part of your screen
def capture_screen():
    while True:
        # Capture part of your screen using pyautogui
        screen = pyautogui.screenshot(region=(1906, 708, 710, 710), allScreens=True)

        # Convert the captured screenshot to a format suitable for streaming
        frame = cv2.cvtColor(np.array(screen), cv2.COLOR_RGB2BGR)

        # Convert the captured frame to JPG format
        ret, jpeg = cv2.imencode('.jpg', frame)

        # Yield the frame
        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + jpeg.tobytes() + b'\r\n')

# Route to stream the captured screen
@app.route('/')
def index():
    return render_template('index.html')

# Route to stream the captured screen
@app.route('/video_feed')
def video_feed():
    return Response(capture_screen(), mimetype='multipart/x-mixed-replace; boundary=frame')

# Asynchronous function to process keyboard shortcuts
# async def process_keyboard_shortcut(shortcut):
#     # Simulate keyboard input based on the received shortcut
#     # if shortcut == 'shift+1':
#     key_val=shortcut.split('_')
#     print(key_val)
#     # pyautogui.hotkey('shifctrl', str(key_val[1]))
#     # pyautogui.keyDown('shiftleft')
#     # pyautogui.keyDown(str(key_val[1]))
#     # pyautogui.keyUp(str(key_val[1]))
#     keyboard.send('left shift')
#     keyboard.send(str(key_val))
    
async def process_keyboard_shortcut(keys):
    key_val=keys.split('_')
    # for key in keys:
    keys=["shift",str(key_val[1])]
    print(keys)
    for key in keys:
        keyboard.press(key)
        await asyncio.sleep(0.1)  # You may adjust the delay as needed
    

    for key in keys:
        keyboard.release(key)    

        # Execute other actions here if needed



# Example: Simulate pressing left Shift + 'K' keys


# Route to receive keyboard shortcuts
@app.route('/send-keyboard-shortcut', methods=['POST'])
def receive_keyboard_shortcut():
    data = request.json
    shortcut = data.get('shortcut')
    print(shortcut)
    # Process the received shortcut asynchronously in a separate thread
    threading.Thread(target=asyncio.run, args=(process_keyboard_shortcut(shortcut),)).start()

    # Send a response back if needed
    return jsonify({'message': 'Shortcut received and will be executed asynchronously'})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, threaded=True, debug=True)
