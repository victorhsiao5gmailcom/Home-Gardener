from flask import Blueprint, render_template, request, redirect, url_for, flash
import os

app = Blueprint('app', __name__)

def save_uploaded_file(uploaded_file):
    if uploaded_file:
        file_extension = os.path.splitext(uploaded_file.filename)[1]
        save_dir = "user_upload_files"

        os.makedirs(save_dir, exist_ok=True)
        save_path = os.path.join(save_dir, uploaded_file.filename)

        with open(save_path, "wb") as f:
            f.write(uploaded_file.read())

        return save_path
    return None

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        uploaded_image = request.files.get('image')
        if uploaded_image:
            image_path = save_uploaded_file(uploaded_image)
            if image_path:
                flash("File uploaded successfully!", "success")
            else:
                flash("Failed to upload file.", "warning")
        return redirect(url_for('app.index'))

    return render_template('index.html')