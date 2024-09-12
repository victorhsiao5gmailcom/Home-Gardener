import os
import google.generativeai as genai

def translate(text, language, api_key):
    genai.configure(api_key=api_key)

    # Create the model
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
    system_instruction=f"Tranlate the text into the desired language: {language}",
    )

    chat_session = model.start_chat(
    history=[
    ]
    )

    response = chat_session.send_message(text)
    print(text)
    print(response.text)

    return(response.text)