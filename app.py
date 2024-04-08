import os
# Use a pipeline as a high-level helper
from transformers import pipeline
from typing import Union
from fastapi.middleware.cors import CORSMiddleware

import requests
from fastapi import FastAPI, Request
from pydantic import BaseModel

app = FastAPI()

app_port = os.environ.get("PORT", 8000)

origins = [
    "*"
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class ImageUrl(BaseModel):
    imageUrl: str

@app.post("/generate-alt-text")
async def generate_alt_text(request_body: ImageUrl):
    print("Request_body.imageUrl:", request_body.imageUrl)
    
    altTextGenerator = pipeline("image-to-text", model="Salesforce/blip-image-captioning-large")
    
    try:
        # Generate alt text for the image URL
        example = altTextGenerator(request_body.imageUrl)
        alt_text = example[0]['generated_text']
        print("Generated Alt Text:", alt_text)
        return {"alt_text": alt_text}
    except Exception as e:
        print("Error generating alt text:", e)
        return {"error": "Failed to generate alt text"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.1", port=app_port)