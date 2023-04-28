from flask import (
    Flask,
    Response,
    render_template,
    request,
    send_from_directory,
    send_file,
)

import cv2
import os
from dotenv import load_dotenv

from routes import drone_api

load_dotenv(".env")


app = Flask(__name__)
app.jinja_env.add_extension("pypugjs.ext.jinja.PyPugJSExtension")

app.register_blueprint(drone_api.drone)

camera_forward = cv2.VideoCapture(0)
camera_down = cv2.VideoCapture(1)


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


@app.route("/")
def index():
    return render_template("index.pug")


@app.route("/front_feed")
def front_feed():
    print("Handling front_feed request", flush=True)
    print(request.url)
    return Response(
        gen_frames(camera_forward), mimetype="multipart/x-mixed-replace; boundary=frame"
    )


@app.route("/down_feed")
def down_feed():
    print(request.url)
    return Response(
        gen_frames(camera_down), mimetype="multipart/x-mixed-replace; boundary=frame"
    )


@app.route("/public/<path:path>")
def public(path):
    return send_from_directory("public", path)


@app.route("/current_image")
def current_image(camera="down"):
    cam = camera_forward if camera == "front" else camera_down
    success, frame = camera.read()
    if success:
        return send_file(cam.imencode(".jpg", frame))


if __name__ == "__main__":
    app.run(host=os.getenv("HOST"), port=os.getenv("PORT"), debug=False, threaded=True)
