from flask import Flask, request, jsonify, send_from_directory
import os
from summarize import summarize_text
from isolation import isolate_person, stitch_images_to_video
from flask_cors import CORS

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

@app.route('/isolate', methods=['POST'])
def isolate_video():
    input_video = "19811797.mp4"  # Replace with the input from request if needed
    output_folder = "output_frames"
    output_video = "final_output.mp4"

    # Process the video and create the isolated video
    original_fps = isolate_person(input_video, output_folder)
    stitch_images_to_video(output_folder, output_video, original_fps)

    # Return the URL of the processed video
    return {"videoURL": f"/static/{output_video}"}

@app.route('/static/<path:filename>', methods=['GET'])
def serve_video(filename):
    return send_from_directory(app.static_folder, filename)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
