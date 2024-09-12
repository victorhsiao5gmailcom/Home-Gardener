from plant_recognition import plt_recog_dis_dect
from growing_condition import gen_rec
from disease_management import dis_man
from translator import translate
import streamlit as st
import os


def save_uploaded_file(uploadedfile):
    """
    Saves the uploaded file to the specified directory.

    Args:
        uploadedfile: The uploaded file object.
    """

    if uploadedfile is not None:
        # Get the file extension
        file_extension = os.path.splitext(uploadedfile.name)[1]

        # Select the save location
        save_dir = "user_upload_files"

        if save_dir:
            # Create the directory if it doesn't exist
            os.makedirs(save_dir, exist_ok=True)

            # Construct the save path
            save_path = os.path.join(save_dir, uploadedfile.name)
            

            # Save the file
            with open(save_path, "wb") as f:
                f.write(uploadedfile.getbuffer())

            st.success("File uploaded successfully!")
            return save_path
        else:
            st.warning("Failed to upload.")
            return None
    

api = "AIzaSyCgpMSPT1RLLYhRtEoLin40U1A2ayopV5g"
language = "English"
lang_list = ["English", "繁體中文", "Español"]

col1, col2 = st.columns([5,1])
with col1: st.title("Home Gardener")
with col2: language = st.selectbox("Language", lang_list, 0)
print(f"Language Selected: {language}")


# Allow image upload
uploaded_image = st.file_uploader("Upload an image of your plant:")

while True:
  if uploaded_image is not None:
    image_path = save_uploaded_file(uploaded_image)
    break


# Dictionary
eng_chn = {
  "Plant Information": "植物資訊",
  "Plant Image": "植物圖片",
  "Plant Info": "植物資料",
  "Growing Condition": "生長條件",
  "Disease Management": "疾病控制",
  "Species Name": "學名",
  "Common Name": "常見名",
  "There is no disease present": "該植物沒有發現疾病"

}

eng_esp = {
  "Plant Information": "Información de la Planta",
  "Plant Image": "Imagen de la Planta",
  "Plant Info": "Información de la Planta",
  "Growing Condition": "Condiciones de Cultivo",
  "Disease Management": "Manejo de Enfermedades",
  "Species Name": "nombre cientifico",
  "Common Name": "nombre común",
  "There is no disease present": "No hay ninguna enfermedad presente"
}

# Call functions with uploaded image path
plt_ide_dis_dec = plt_recog_dis_dect(image_path, api)
print("Plant Identified")
plant = plt_ide_dis_dec[0]
disease = plt_ide_dis_dec[1]
species_name = plant[0]
common_name = plant[1]

if language != "English":
  common_name = translate(plant[1], language, api)

  growing_condition = translate(gen_rec(species_name, api), language, api)
  pests_management = translate(dis_man(species_name, disease, api), language, api)
  print("Translation Completed")
else:
  growing_condition = gen_rec(species_name, api)
  pests_management = dis_man(species_name, disease, api)
  print("Growing Condition Proccessed")
  
if "0" not in disease:
  pests_management = translate(dis_man(plant[0], disease, api), language, api)
else:
  if language == "English":
    pests_management = "There is no disease present"
  elif language == "繁體中文":
    pests_management = eng_chn["There is no disease present"]
  else:
    pests_management = eng_esp["There is no disease present"]
print("Pests Management Proccessed")


# Display results
print("Displaying Results")

# English
if language == "English":
  st.header("Plant Information")
  col1, col2 = st.columns([3, 1])
  with col1:
    st.header("Plant Image")
    st.image(image_path)
  with col2:
    st.header("Plant Info")
    st.subheader(f"{species_name}\nSpecies Name")
    st.subheader(f"{common_name}\nCommon Name")

  st.subheader("Growing Condition")
  st.write(growing_condition)

  st.subheader("Disease Management")
  st.write(pests_management)
else:
  if language == "繁體中文":
     dict = eng_chn
  else:
     dict = eng_esp

  st.header(dict["Plant Information"])
  col1, col2 = st.columns([3, 1])
  with col1:
    st.header(dict["Plant Image"])
    st.image(image_path)
  with col2:
    st.header("Plant Info")
    st.subheader(species_name)
    st.write(dict["Species Name"])
    st.subheader(common_name)
    st.write(dict["Common Name"])

  st.subheader(dict["Growing Condition"])
  st.write(growing_condition)

  st.subheader(dict["Disease Management"])
  st.write(pests_management)

print("Result Displayed")

# remove temp file
os.remove(image_path)