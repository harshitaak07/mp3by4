from flask import Flask, request, jsonify
import cv2  # Make sure to import OpenCV
import numpy as np
import os

app = Flask(__name__)

# # Import your video processing functions
# from video_processing import getvideofile  # Adjust import as necessary
# from video_processing import processvideofile  # Adjust import as necessary

# @app.route('/capture_video', methods=['POST'])
# def capture_video_route():
#     try:
#         getvideofile()  # Call your video capture function
#         return jsonify({'message': 'Video captured successfully'}), 200
#     except Exception as e:
#         return jsonify({'error': str(e)}), 500

# @app.route('/process_video', methods=['POST'])
# def process_video_route():
#     try:
#         processvideofile()  # Call your video processing function
#         return jsonify({'message': 'Video processed successfully'}), 200
#     except Exception as e:
#         return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)