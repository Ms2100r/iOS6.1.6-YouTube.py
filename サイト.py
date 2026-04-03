# server.py
from flask import Flask, send_file
from waitress import serve

app = Flask(__name__)


@app.route("/")
def serve_music():
    return send_file("./index.html", conditional=True)

@app.route("/v")
def serve_v():
    return send_file("./video.html", conditional=True)

@app.route("/video")
def serve_v2():
    return send_file("./video.mp4", conditional=True)

if __name__ == "__main__":
    # 全インターフェースで待ち受け（LAN内でiOS6からアクセス可能）
    serve(app, host="0.0.0.0", port=80)
