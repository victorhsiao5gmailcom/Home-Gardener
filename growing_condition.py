import os
import google.generativeai as genai

def gen_rec(plant, api):
  genai.configure(api_key=api)

  generation_config = {
    "temperature": 1,
    "top_p": 0.95,
    "top_k": 64,
    "max_output_tokens": 8192,
    "response_mime_type": "text/plain",
  }

  model = genai.GenerativeModel(
    model_name="gemini-1.5-flash",
    generation_config=generation_config,
  )

  response = model.generate_content([
    "You are an expert in horticulture and an experienced home gardener; without title, species name, common name; without heading; Please give specific growing conditions (not wordy, easy to comprehense) based on the species of plant.",
    f"species_name: {plant}",
    "Lighting, Soil, Watering, Fertilizer, Temperature, Humidity: ",
  ])

  return(response.text)