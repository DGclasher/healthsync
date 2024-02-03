import os
import json
import requests
from decouple import config

def analyze_symptoms(symptoms):
    endpoint = "https://api-inference.huggingface.co/models/timpal0l/mdeberta-v3-base-squad2"
    headers = {
        "Authorization": f"Bearer {config('AI_API_KEY')}",
    }
    context_path = os.path.join(os.getcwd(), 'app', 'context.txt')
    with open(context_path, 'r') as f:
        context = f.read()
    payload = {
        "inputs": {
            "question": symptoms,
            "context": context
        }
    }
    res = requests.post(endpoint, headers=headers, json=payload)
    return json.loads(res.text)

def analyze_image(image):
    endpoint = "https://api-inference.huggingface.co/models/Salesforce/blip-image-captioning-large"
    headers = {
        "Authorization": f"Bearer {config('AI_API_KEY')}",
    }
    res = requests.post(endpoint, headers=headers, data=image)
    res = json.loads(res.text)
    generated_text = res[0]["generated_text"]
    return generated_text

def analyze_image_only(image):
    image_res = analyze_image(image)
    symptoms_res = analyze_symptoms(image_res)
    return symptoms_res

def analyze_both(image, symptoms):
    image_res = analyze_image(image)
    res = analyze_symptoms(image_res + " " + symptoms)
    return res