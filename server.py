from flask import Flask
import flask

app = Flask(__name__, static_folder='.', static_url_path='')

@app.route('/')
def index():
    return flask.jsonify({
        "status": "I'm alive!"
    })

@app.route("/eye")
def send_eyedata():

    eye_data = {"right": 0.5,"left":0.5}
    return flask.jsonify({
        "eyes": eye_data
    })


if __name__ == "__main__":
    app.run(port=9090, debug=True)