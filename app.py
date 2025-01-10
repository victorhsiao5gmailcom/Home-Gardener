from flask import Flask, render_template, request, redirect, url_for
import os
from plant_recognition import plt_recog_dis_dect
from growing_condition import gen_rec
from disease_management import dis_man

api_list = ["AIzaSyCgpMSPT1RLLYhRtEoLin40U1A2ayopV5g", "AIzaSyBL-2h7CT3ODJhHqujwViK8cz5iOjaeiWc", "AIzaSyBL-2h7CT3ODJhHqujwViK8cz5iOjaeiWc"]
app = Flask(__name__, template_folder='/home/CoffeeTesVh/HomeGardener/App/templates', static_folder='/home/CoffeeTesVh/HomeGardener/App/static')

def save_uploaded_file(uploaded_file):
    if uploaded_file:
        file_extension = os.path.splitext(uploaded_file.filename)[1]
        save_dir = "HomeGardener/App/static/user_upload_files"

        try:
            os.makedirs(save_dir, exist_ok=True)
            print(f"Directory {save_dir} created successfully or already exists.")
        except Exception as e:
            print(f"Failed to create directory {save_dir}: {e}")
            return None

        save_path = os.path.join(save_dir, uploaded_file.filename)

        try:
            uploaded_file.save(save_path)
            print(f"File saved successfully at {save_path}")
            return save_path
        except Exception as e:
            print(f"Failed to save file {uploaded_file.filename}: {e}")
            return None
    return None

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        uploaded_image = request.files.get('image')
        if uploaded_image:
            image_path = save_uploaded_file(uploaded_image)
            print(image_path)
            if image_path:
                image_filename = os.path.basename(image_path)
                for api in api_list:
                    try:
                        plt_ide_dis_dec = plt_recog_dis_dect(image_path, api)
                        print(plt_ide_dis_dec)
                        if not plt_ide_dis_dec or len(plt_ide_dis_dec) < 2:
                            raise ValueError("Invalid response from plant_recognition API")

                        plant = plt_ide_dis_dec[0]
                        disease = plt_ide_dis_dec[1]
                        species_name = plant[0]
                        common_name = plant[1]

                        growing_condition = gen_rec(species_name, api)
                        if "0" not in disease:
                            disease_management = dis_man(species_name, disease, api)
                        else:
                            disease_management = "There is no disease present"

                        return render_template('index.html', success=True, image_filename=image_filename, species_name=species_name, common_name=common_name, growing_condition=growing_condition, disease_management=disease_management)
                    except Exception as e:
                        print(f"API key {api} failed: {e}")
                        continue
    return render_template('index.html', success=False)

if __name__ == '__main__':
    app.run(debug=True)