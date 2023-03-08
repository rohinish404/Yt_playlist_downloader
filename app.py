from queue import Queue
from pytube import YouTube, Playlist
import subprocess
import threading
from flask import Flask, render_template, request, send_file
import os
import zipfile
import ssl
ssl._create_default_https_context = ssl._create_unverified_context

app = Flask(__name__)

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/download", methods=["POST"])
def download():
    # Get the playlist URL from the form data
    url = request.form["url"]

    # Download the videos using multi-threading
    filenames = download_playlist(url)

    # Write the list of filenames to a file
    with open("file_list.txt", "w") as f:
        for filename in filenames:
            f.write(f"file '{filename}'\n")

    # Concatenate the videos
    output_path = "output.mp4"
    concatenate_videos(filenames, output_path)

    for filename in filenames:
        if filename != output_path:
            os.remove(filename)
    # Send the concatenated video file as a download
    return send_file(output_path, as_attachment=True)
    os.remove(output_path)
def download_video(url, filename_queue):
    # Download the video and put the filename in the queue
    video = YouTube(url)
    filename = video.streams.get_highest_resolution().download()
    filename_queue.put(filename)

def download_playlist(url):
    p = Playlist(url)
    filenames = []
    filename_queue = Queue()

    # Start a thread for each video to download it concurrently
    threads = []
    for video in p.videos:
        thread = threading.Thread(target=download_video, args=(video.watch_url, filename_queue))
        threads.append(thread)
        thread.start()

    # Wait for all threads to finish and get the filenames
    for thread in threads:
        thread.join()

    while not filename_queue.empty():
        filenames.append(filename_queue.get())

    return filenames

def concatenate_videos(filenames, output_path):
    # Use FFMPEG to concatenate the videos
    command = ["ffmpeg", "-y", "-f", "concat", "-safe", "0", "-i", "file_list.txt", "-c", "copy", output_path]
    subprocess.call(command)

@app.route("/downloadZip", methods=["POST"])
def downloadZip():
    # Get the playlist URL from the form data
    url = request.form["url"]

    # Download all the videos in the playlist using multithreading
    playlist = Playlist(url)
    if not os.path.exists('videos'):
        os.makedirs('videos')

    def download_video(video):
        video.streams.get_highest_resolution().download(output_path='videos')

    threads = []
    for video in playlist.videos:
        thread = threading.Thread(target=download_video, args=(video,))
        thread.start()
        threads.append(thread)

    for thread in threads:
        thread.join()

    # Compress all the downloaded videos into a zip file
    zip_path = "videos.zip"
    zip_file = zipfile.ZipFile(zip_path, 'w')
    for foldername, subfolders, filenames in os.walk('videos'):
        for filename in filenames:
            file_path = os.path.join(foldername, filename)
            zip_file.write(file_path, os.path.relpath(file_path, 'videos'), compress_type=zipfile.ZIP_DEFLATED)
    zip_file.close()

    # Remove the videos directory after zipping
    os.system('rm -rf videos')

    # Send the zip file as a download
    return send_file(zip_path, as_attachment=True)
    os.remove(zip_path)
if __name__ == "__main__":
    app.run()
