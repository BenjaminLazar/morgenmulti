import streamlit as st
from PIL import Image
import requests
import base64
import io
import json

# Streamlit UI setup
st.image("todai 1.png")

# Text input
user_text = st.text_input("Add thoughts or notes for the questions here:")


# Image input
uploaded_file = st.file_uploader("Choose Image", type=["jpg", "jpeg", "png"])
if uploaded_file is not None:
    image = Image.open(uploaded_file)
    st.image(image, caption='Uploaded Image.', use_column_width=True)

def encode_image(image):
    img_format = image.format if image.format in ['JPEG', 'PNG'] else 'JPEG'  # Default to JPEG if format is not JPEG or PNG
    buffered = io.BytesIO()
    image.save(buffered, format=img_format)
    img_str = base64.b64encode(buffered.getvalue()).decode()
    return img_str

if uploaded_file is not None:
    base64_image = encode_image(image)

# Function to send data to ChatGPT Vision
def send_to_chatgpt_vision(text, image_base64):
    api_key = st.secrets["OPENAI_API_KEY"]
    extra_prompt = "You help participents at a talk to generate questions with the help of an image of the talk. Todays talk is about large multimodal AI models. Its a talk that makes a simple explenation on what multimodality is and what these models are, and then focusses on what uses cases that exists in everyday buisness tasks. Generate questions for this talk based on what you know, the image, and some extra notes that comes here: "
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {api_key}"
    }
    payload = {
        "model": "gpt-4-vision-preview",
        "messages": [
            {
                "role": "user",
                "content": [
                    {
                        "type": "text",
                        "text": extra_prompt + text
                    },
                    {
                        "type": "image_url",
                        "image_url": {
                            "url": f"data:image/jpeg;base64,{image_base64}"
                        }
                    }
                ]
            }
        ],
        "max_tokens": 300
    }
    response = requests.post("https://api.openai.com/v1/chat/completions", headers=headers, json=payload)
    return response.json()

# Button to send request
if st.button('Generate Questions'):
    if user_text and uploaded_file is not None:
        response = send_to_chatgpt_vision(user_text, base64_image)
        st.write(response['choices'][0]['message']['content'])
    else:
        st.write("Please input both text and an image.")
