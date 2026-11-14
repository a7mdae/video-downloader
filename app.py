import os
from flask import Flask, jsonify, render_template, request, send_from_directory
import yt_dlp

app = Flask(__name__)
DOWNLOAD_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), "downloads")

if not os.path.exists(DOWNLOAD_DIR):
  os.makedirs(DOWNLOAD_DIR)


@app.route("/")
def index():
  return render_template("index.html")


@app.route("/download", methods=["POST"])
def download():
  url = request.form.get("url")
  if not url:
    return jsonify({"status": "error", "message": "No URL provided."})

  # Force H.264 (avc1) video + AAC (mp4a) audio for universal iPhone/Android/PC compatibility
  ydl_opts = {
      "format": "bestvideo[vcodec^=avc1]+bestaudio[acodec^=mp4a]/best[ext=mp4]/best",
      "outtmpl": os.path.join(DOWNLOAD_DIR, "%(title)s.%(ext)s"),
      "noplaylist": True,
      "js_runtimes": {"deno": {"path": None}, "node": {"path": None}},
  }

  try:
    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
      info = yt_dlp.YoutubeDL({"quiet": True}).extract_info(
          url, download=False
      )
      # Fallback title cleaning for Windows filesystem
      title = info.get("title", "video")

      info = ydl.extract_info(url, download=True)
      filename = ydl.prepare_filename(info)

      base, _ = os.path.splitext(filename)
      final_filename = os.path.basename(base + ".mp4")
      if not os.path.exists(os.path.join(DOWNLOAD_DIR, final_filename)):
        final_filename = os.path.basename(filename)

      return jsonify({
          "status": "success",
          "message": "Video optimized and ready!",
          "filename": final_filename,
      })
  except Exception as e:
    return jsonify({"status": "error", "message": str(e)})


@app.route("/get-video/<path:filename>")
def get_video(filename):
  # Explicitly set video/mp4 mimetype so iOS Safari recognizes it instantly
  return send_from_directory(
      DOWNLOAD_DIR, filename, as_attachment=True, mimetype="video/mp4"
  )


if __name__ == "__main__":
  app.run(debug=True, port=5000)