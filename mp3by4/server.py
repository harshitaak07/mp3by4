from flask import Flask, request, jsonify, send_from_directory
import os
import asyncio
from summarize import summarize_text
from isolation import isolate_person, stitch_images_to_video
from flask_cors import CORS
from sentence_generate import extract_text_from_webpage, convert_text_to_speech, main as tts
from combiner import combine_audio_video 

app = Flask(__name__)
CORS(app)

# Set the static folder
app.static_folder = 'static'

@app.route('/summarize', methods=['POST'])
def summarize():
    data = request.get_json()
    input_text = data.get('text')

    if input_text:
        summary = summarize_text(input_text)
        return jsonify({"summary": summary}), 200
    else:
        return jsonify({"error": "No text provided"}), 400

@app.route('/generate_narration', methods=['POST'])
def generate_narration():
    data = request.get_json()
    url = data.get('url')  # Get the URL from the request

    if url:
        try:
            extracted_text = extract_text_from_webpage(url)
            if not extracted_text:
                return jsonify({"error": "Failed to extract text."}), 500

            mp3_filename = "output_audio.mp3"  # Define output file name
            saved_mp3 = convert_text_to_speech(extracted_text, mp3_filename)

            if saved_mp3:
                return jsonify({"narrative": extracted_text, "mp3_url": f"/static/{saved_mp3}"}), 200
            else:
                return jsonify({"error": "Failed to generate MP3."}), 500

        except Exception as e:
            return jsonify({"error": str(e)}), 500
    else:
        return jsonify({"error": "No URL provided."}), 400

@app.route('/static/<path:filename>', methods=['GET'])
def serve_file(filename):
    return send_from_directory(app.static_folder, filename, conditional=True)

@app.route('/process_and_combine', methods=['POST'])
async def process_and_combine():
    data = request.get_json()

    # Log the data to debug
    print(f"Received data: {data}")
    input_video = "19811797.mp4"
    url = data.get('url')
    print("INPUT DATA GOT")

    tts(url,'outputaudio.mp3')
    print("TTS COMPLETE")
    try:
        fps = isolate_person(input_video, 'output_frames')
        print("FPS COUNT ", fps)
        if fps == 0:
            raise ValueError("No frames were processed from the input video")
            
        stitch_images_to_video('output_frames', 'final123.mp4', fps)
        print("VIDEO STITCHED")
            
        combine_audio_video('final123.mp4', 'outputaudio.mp3', 'static/amongus.mp4')
        output_video = "amongus.mp4"
        return {"videoURL": f"/static/{output_video}"}
    except FileNotFoundError as e:
        print(f"File not found error: {str(e)}")
        return jsonify({"error": f"File not found: {str(e)}"}), 404
    except ValueError as e:
        print(f"Value error: {str(e)}")
        return jsonify({"error": str(e)}), 400
    except Exception as e:
        print(f"Unexpected error: {str(e)}")
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    app.run(host="0.0.0.0",port=5000)