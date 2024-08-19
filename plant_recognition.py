from pathlib import Path
import google.generativeai as genai


def upload_to_gemini(path, mime_type=None):
  """Uploads the given file to Gemini.

  See https://ai.google.dev/gemini-api/docs/prompting_with_media
  """
  file = genai.upload_file(path, mime_type=mime_type)
  print(f"Uploaded file '{file.display_name}' as: {file.uri}")
  return file


def plt_recog_dis_dect(image, api):
  genai.configure(api_key=api)

  # Set up the model
  generation_config = {
    "temperature": 1,
    "top_p": 0.95,
    "top_k": 64,
    "max_output_tokens": 8192,
  }

  safety_settings = [
    {
      "category": "HARM_CATEGORY_HARASSMENT",
      "threshold": "BLOCK_MEDIUM_AND_ABOVE"
    },
    {
      "category": "HARM_CATEGORY_HATE_SPEECH",
      "threshold": "BLOCK_MEDIUM_AND_ABOVE"
    },
    {
      "category": "HARM_CATEGORY_SEXUALLY_EXPLICIT",
      "threshold": "BLOCK_MEDIUM_AND_ABOVE"
    },
    {
      "category": "HARM_CATEGORY_DANGEROUS_CONTENT",
      "threshold": "BLOCK_MEDIUM_AND_ABOVE"
    },
  ]

  model = genai.GenerativeModel(model_name="gemini-1.5-flash",
                                generation_config=generation_config,
                                safety_settings=safety_settings)

  files = [
    upload_to_gemini(image, mime_type="image/jpeg"),
  ]

  response = model.generate_content([
    "Identify the main plant; Short Response; Output: Binomial Name, Common Name, Disease Name (0 if not present)",
    "image ",
    files[0],
    "Species_Name: , Common_Name: , Disease: ",
  ])
  

  text = response.text

  text = text.replace("Species_Name: ", "")
  text = text.replace(", ", ",")
  text = text.replace("Common_Name: ", "")
  text = text.replace("Disease: ", "")
  text = text.replace("\n", "")
  text = text.replace("0 ", "0")

  response_processed = text.split(",")

  # Splitting at index 1 (after the second term)
  plant = response_processed[:2]
  disease = response_processed[2:]

  return(plant, disease)