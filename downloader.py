import os
import yt_dlp


def download_video(url, output_dir="downloads"):
  if not os.path.exists(output_dir):
    os.makedirs(output_dir)

  ydl_opts = {
      "format": "bestvideo[ext=mp4]+bestaudio[ext=m4a]/best[ext=mp4]/best",
      "outtmpl": os.path.join(output_dir, "%(title)s.%(ext)s"),
      "noplaylist": True,
      # Explicitly allow node runtime if deno isn't used
      "js_runtimes": {"deno": {"path": None}, "node": {"path": None}},
  }

  try:
    print(f"\n[+] Connecting to link...")
    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
      info = ydl.extract_info(url, download=True)
      filename = ydl.prepare_filename(info)
      print(f"\n[SUCCESS] Downloaded successfully!")
      print(f"Saved to: {os.path.abspath(filename)}")
  except Exception as e:
    print(f"\n[ERROR] Failed to download: {e}")


if __name__ == "__main__":
  print("=== Universal Video Downloader ===")
  video_url = input("Paste your video link here: ").strip()

  if video_url:
    download_video(video_url)
  else:
    print("[ERROR] No URL provided.")