from flask import Flask, request, jsonify, send_from_directory
from werkzeug.utils import secure_filename
import os
import uuid
from ppg_extractor import extract_ppg

app = Flask(__name__)
UPLOAD_FOLDER = "uploads"
RESULT_FOLDER = "results"
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
os.makedirs(RESULT_FOLDER, exist_ok=True)

@app.route("/upload", methods=["POST"])
def upload():
    if 'video' not in request.files:
        return jsonify({"error": "No video uploaded"}), 400

    file = request.files['video']
    filename = secure_filename(str(uuid.uuid4()) + ".mp4")
    filepath = os.path.join(UPLOAD_FOLDER, filename)
    file.save(filepath)

    try:
        result_path = extract_ppg(filepath, RESULT_FOLDER)
        return jsonify({
            "status": "success",
            "graph_url": request.host_url + "results/" + os.path.basename(result_path)
        })
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route("/results/<filename>")
def result_file(filename):
    return send_from_directory(RESULT_FOLDER, filename)

if __name__ == "__main__":
    app.run(debug=True)
