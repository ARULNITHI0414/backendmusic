from flask import Flask, request, jsonify
import yt_dlp

app = Flask(__name__)

def get_mp3_url(video_id):
    ydl_opts = {
    'format': 'bestaudio/best',
    'extractaudio': True,  # Download audio only
    'audioformat': 'mp3',  # Specify audio format
    'noplaylist': True,
    'proxy': None,
    'quiet': True,
    }

    # Construct the video URL from the video ID
    video_url = f"https://www.youtube.com/watch?v={video_id}"

    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        try:
            # Extract audio information directly from the video URL
            audio_info = ydl.extract_info(video_url, download=False)
            for format_info in audio_info['formats']:
                if format_info['ext'] in ['webm', 'm4a', 'mp3']:
                    return format_info['url']

        except Exception as e:
            print(f"Error extracting MP3 URL: {e}")

    return None

@app.route('/get_mp3_url', methods=['GET'])
def get_mp3():
    video_id = request.args.get('video_id')
    if not video_id:
        return jsonify({"error": "No video ID provided"}), 400

    mp3_url = get_mp3_url(video_id)
    if mp3_url:
        return jsonify({"mp3_url": mp3_url})
    else:
        return jsonify({"error": "Video not found or no audio available"}), 404

if __name__ == '__main__':
    app.run()  # Ensure to use a production server for deployment
