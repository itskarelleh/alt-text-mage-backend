from transformers import pipeline
from functools import lru_cache

model_id = "Salesforce/blip-image-captioning-large"
altTextGenerator = pipeline("image-to-text", model_id, max_new_tokens=200)

def generate_alt_text(image_url):
    print("Generating alt text for image URL:", image_url)
    result = altTextGenerator(image_url)
    alt_text = result[0]['generated_text']
    
    print(result)

    return alt_text

@lru_cache(maxsize=1024)
def generate_alt_text_cached(image_url):
# Generate alt text for the image URL
    result = altTextGenerator(image_url)
    alt_text = result[0]['generated_text']

    print(result)

    return alt_text

