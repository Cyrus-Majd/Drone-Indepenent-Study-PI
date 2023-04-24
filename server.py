from flask import Flask, Response, render_template, request
import cv2
import os

app = Flask(__name__)
if os.environ.get('WERKZEUG_RUN_MAIN') or Flask.debug is False:
    print('init cameras',flush=True)
    camera_forward = cv2.VideoCapture(0)
    camera_down = cv2.VideoCapture(1)

def gen_frames(camera):
    while True:
        success, frame = camera.read()
        if not success:
            print('failed',flush=True)
            break
        else:
            ret, buffer = cv2.imencode('.jpg', frame)
            frame = buffer.tobytes()
            yield (b'--frame\r\n'
                   b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/front_feed')
def front_feed():
    print("Handling front_feed request", flush=True)
    print(request.url)
    return Response(gen_frames(camera_forward), mimetype='multipart/x-mixed-replace; boundary=frame')

@app.route('/down_feed')
def down_feed():
    print(request.url)
    return Response(gen_frames(camera_down), mimetype='multipart/x-mixed-replace; boundary=frame')

if __name__ == '__main__':
    app.run(host='10.72.102.58', port=5000, debug=True)
