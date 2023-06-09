from flask import (
    Flask,
    Response,
    render_template,
    request,
    send_from_directory,
    send_file,
)
import logging
import numpy as np


log = logging.getLogger("werkzeug")
log.setLevel(logging.ERROR)
import cv2
import os
from dotenv import load_dotenv

from routes import drone_api
import threading

load_dotenv(".env")


app = Flask(__name__)
app.jinja_env.add_extension("pypugjs.ext.jinja.PyPugJSExtension")

app.register_blueprint(drone_api.drone)

# camera_forward = cv2.VideoCapture(0)
# camera_down = cv2.VideoCapture(1)


# def gen_frames(camera):
#     while True:
#         success, frame = camera.read()
#         if not success:
#             print("failed", flush=True)
#             break
#         else:
#             ret, buffer = cv2.imencode(".jpg", frame)
#             frame = buffer.tobytes()
#             yield (b"--frame\r\n" b"Content-Type: image/jpeg\r\n\r\n" + frame + b"\r\n")

camera_forward = cv2.VideoCapture(0)
camera_down = cv2.VideoCapture(1)


@app.route("/")
def index():
    return render_template("index.pug")


def gen_frames(camera):
    while True:
        success, frame = camera.read()
        if not success:
            print("failed", flush=True)
            break
        else:
            ret, buffer = cv2.imencode(".jpg", frame)
            frame = buffer.tobytes()
            yield (b"--frame\r\n" b"Content-Type: image/jpeg\r\n\r\n" + frame + b"\r\n")


@app.route("/front_feed")
def front_feed():
    print("Handling front_feed request", flush=True)
    print(request.url)
    return Response(
        gen_frames(camera_forward), mimetype="multipart/x-mixed-replace; boundary=frame"
    )


@app.route("/down_feed")
def down_feed():
    print("Handling down_feed request", flush=True)
    print(request.url)
    return Response(
        gen_frames(camera_down), mimetype="multipart/x-mixed-replace; boundary=frame"
    )


# start camera threads
def start_camera_threads():
    forward_thread = threading.Thread(target=gen_frames, args=(camera_forward,))
    down_thread = threading.Thread(target=gen_frames, args=(camera_down,))
    cv_thread = threading.Thread(target=generate_cv_frames, args=(camera_forward,))
    forward_thread.start()
    down_thread.start()
    cv_thread.start()


@app.route("/public/<path:path>")
def public(path):
    return send_from_directory("public", path)


@app.route("/current_image/<camera>")
def current_image(camera="down"):
    cam = camera_forward if camera == "front" else camera_down
    success, frame = cam.read()
    if success:
        return send_file(cam.imencode(".jpg", frame))


def generate_cv_frames(camera):
    while True:
        # Read a frame from the camera
        success, img = camera.read()
        if not success:
            break

        # Reduce the size of the frame
        img = cv2.resize(img, (640, 480))

        # Process the frame
        hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
        lower_blue = np.array([90, 50, 50])
        upper_blue = np.array([150, 255, 255])
        mask = cv2.inRange(hsv, lower_blue, upper_blue)
        contours, _ = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

        # Keep only the largest contour
        contours = sorted(contours, key=cv2.contourArea, reverse=True)[:1]

        cv2.drawContours(img, contours, -1, (0, 255, 0), 2)

        # Convert the processed frame to JPEG format
        ret, buffer = cv2.imencode(".jpg", img)
        frame = buffer.tobytes()

        # Yield the frame in a chunked MJPEG stream
        yield (b"--frame\r\n" b"Content-Type: image/jpeg\r\n\r\n" + frame + b"\r\n")


@app.route("/cv_feed")
def cv_feed():
    print("Handling cv_feed request", flush=True)
    print(request.url)
    return Response(
        generate_cv_frames(camera_forward),
        mimetype="multipart/x-mixed-replace; boundary=frame",
    )


if __name__ == "__main__":
    start_camera_threads()
    app.run(host=os.getenv("HOST"), port=os.getenv("PORT"), debug=False, threaded=True)
