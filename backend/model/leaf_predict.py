import requests
import os

API_KEY = os.getenv("KINDWISE_API_KEY")  # Store your API key in .env

def predict_leaf_disease(image_path: str):
   def encode_image(image_path):
    with open(image_path, "rb") as image_file:
        return base64.b64encode(image_file.read()).decode('utf-8')

    client = Groq()

# Path to your local image file
    base64_image = encode_image(image_path)

    completion = client.chat.completions.create(
    model="meta-llama/llama-4-scout-17b-16e-instruct",
    messages=[
        {
            "role": "user",
            "content": [
                {
                    "type": "text",
                    "text": "You will be given an image of a plant? Your task is to return its specie and tell if its' suffering from any disease. "
                },
                {
                    "type": "image_url",
                    "image_url": {
                        "url": f"data:image/jpeg;base64,{base64_image}"
                    }
                }
            ]
        }
    ],
    temperature=1,
    max_completion_tokens=1024,
    top_p=1,
    stream=False,
    stop=None,
    )

    return completion.choices[0].message.content
