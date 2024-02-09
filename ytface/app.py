import os
import datetime
import cv2
from flask import Flask, jsonify, request, render_template

import face_recognition

app = Flask(__name__)

# CREATE VARIABLE REGISTER
registered_data = {}

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/register", methods=["POST"])
def register():
    name = request.form.get("name")
    photo = request.files['photo']
    uploads_folder = os.path.join(os.getcwd(), "static", "uploads")

    if not os.path.exists(uploads_folder):
        os.makedirs(uploads_folder)

    today_date = datetime.date.today()
    file_name = f"{today_date}_{name}.jpg"
    photo.save(os.path.join(uploads_folder, file_name))
    registered_data[name] = file_name

    response = {"success": True, 'name': name}
    return jsonify(response)

@app.route("/login", methods=["POST"])
def login():
    photo = request.files['photo']
    uploads_folder = os.path.join(os.getcwd(), "static", "uploads")

    if not os.path.exists(uploads_folder):
        os.makedirs(uploads_folder)

    login_filename = os.path.join(uploads_folder, "login_face.jpg")
    photo.save(login_filename)

    login_image = face_recognition.load_image_file(login_filename)
    login_face_encodings = face_recognition.face_encodings(login_image)

    for name, filename in registered_data.items():
        registered_photo = os.path.join(uploads_folder, filename)
        registered_image = face_recognition.load_image_file(registered_photo)
        registered_face_encodings = face_recognition.face_encodings(registered_image)

        if len(registered_face_encodings) > 0 and len(login_face_encodings) > 0:
            matches = face_recognition.compare_faces(registered_face_encodings, login_face_encodings[0])
            print("matches", matches)

            if any(matches):
                response = {"success": True, "name": name}
                return jsonify(response)

    response = {"success": False}
    return jsonify(response)

@app.route("/success")
def success():
    user_name = request.args.get("user_name")
    return render_template("success.html", user_name=user_name)

if __name__ == "__main__":
    app.run(debug=True)
