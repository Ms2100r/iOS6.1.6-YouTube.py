from flask import Flask, redirect, abort
from yt_dlp import YoutubeDL
import os
import threading
import time

app = Flask(__name__)
VIDEO_PATH = "video.mp4"

def download(video_id):
    # 既存ファイルを確実に消してから開始
    if os.path.exists(VIDEO_PATH):
        try:
            os.remove(VIDEO_PATH)
        except:
            pass

    ydl_opts = {
        "format": "best[ext=mp4][height<=720]/best",
        "outtmpl": VIDEO_PATH,
        "quiet": False, # 進行状況を確認するため一時的にTrueから変更推奨
        "noplaylist": True,
    }

    try:
        with YoutubeDL(ydl_opts) as ydl:
            # ここでダウンロード完了までブロック（待機）される
            ydl.download([f"https://www.youtube.com/watch?v={video_id}"])
        
        # ダウンロード直後はファイルがロックされている場合があるため、わずかに待機
        time.sleep(1) 
        return os.path.exists(VIDEO_PATH)
    except Exception as e:
        print(f"Download Error: {e}")
        return False

def delete_later():
    time.sleep(90)
    try:
        if os.path.exists(VIDEO_PATH):
            os.remove(VIDEO_PATH)
    except:
        pass

@app.route("/api/video/<video_id>")
def watch(video_id):
    # 1. ダウンロードを実行（完了するまでここで止まる）
    success = download(video_id)

    if success:
        # 2. 削除予約スレッド開始
        threading.Thread(target=delete_later).start()
        # 3. ファイルが存在することを確認してリダイレクト
        return redirect("http://192.168.11.27/v")
    else:
        abort(500)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=2025, threaded=True)
