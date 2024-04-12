import os
from transformers import pipeline
from typing import Union
from fastapi.middleware.cors import CORSMiddleware
from fastapi import FastAPI
from pydantic import BaseModel
from utils.index import generate_alt_text_cached, is_base64, is_url, process_image

app = FastAPI()

app_port = os.environ.get("PORT", 8000)
app_host = os.environ.get("HOST", "127.0.0.1")
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
    if(len(request_body.imageUrl) == 0):
        return {"error": "Invalid image URL"}

    image_url = process_image(request_body.imageUrl)

    alt_text = generate_alt_text_cached(image_url)

    if alt_text is None:
        # Cache miss, generate alt text and update cache
            altTextGenerator = pipeline("image-to-text", "Salesforce/blip-image-captioning-large", max_new_tokens=10)
            try:
                # Generate alt text for the image URL
                result = altTextGenerator(request_body.imageUrl)
                alt_text = result[0]['generated_text']
                print(result)
                return {"alt_text": alt_text}
            except Exception as e:
                print("Error generating alt text:", e)
                return {"error": "Failed to generate alt text"}

    return {"alt_text": alt_text}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host=app_host, port=app_port)