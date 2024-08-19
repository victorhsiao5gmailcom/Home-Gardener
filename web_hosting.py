from plant_recognition import plt_recog_dis_dect
from growing_condition import gen_rec
from disease_management import dis_man
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
st.title("Home Gardener")
  
# Allow image upload
uploaded_image = st.file_uploader("Upload an image of your plant:")

while True:
  if uploaded_image is not None:
    image_path = save_uploaded_file(uploaded_image)
    break


# Call functions with uploaded image path
plt_ide_dis_dec = plt_recog_dis_dect(image_path, api)
plant = plt_ide_dis_dec[0]
disease = plt_ide_dis_dec[1]

species_name = plant[0]
common_name = plant[1]

growing_condition = gen_rec(species_name, api)
pests_management = dis_man(species_name, disease, api)
  
if "0" not in disease:
  pests_management = dis_man(plant[0], disease, api)
else:
  pests_management = "There is no disease present"

# Display results
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
st.write(growing_condition.replace("**Growing Conditions**", ""))

st.subheader("Disease Management")
st.write(pests_management)

# remove temp file
os.remove(image_path)