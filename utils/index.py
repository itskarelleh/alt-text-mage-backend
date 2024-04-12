from functools import lru_cache
from transformers import pipeline
from PIL import Image
import requests
import io
import base64
import re
from urllib.request import urlopen

MAX_DIMENSION = 320
MIN_DIMENSION = 100

#cache images
@lru_cache(maxsize=1000)
def generate_alt_text_cached(image_url):
    altTextGenerator = pipeline("image-to-text", model="Salesforce/blip2-opt-2.7b")
    example = altTextGenerator(image_url)
    alt_text = example[0]['generated_text']
    return alt_text

def is_base64(input_str):
    try:
        # Attempt to decode the input string as base64
        base64.b64decode(input_str)
        return True
    except:
        return False
    
def is_url(input_str):
    url_pattern = re.compile(
        r'^(?:http|ftp)s?://'  # http:// or https://
        r'(?:(?:[A-Z0-9](?:[A-Z0-9-]{0,61}[A-Z0-9])?\.)+(?:[A-Z]{2,6}\.?|[A-Z0-9-]{2,}\.?)|'  # domain...
        r'localhost|'  # localhost...
        r'\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})'  # ...or ip
        r'(?::\d+)?'  # optional port
        r'(?:/?|[/?]\S+)$', re.IGNORECASE)
    return re.match(url_pattern, input_str) is not None
    
def process_image(input_data):
    if is_base64(input_data):
        # Resize base64 image
        return resize_base64_image(input_data)
    elif(input_data.startswith("blob:")):
        # Extract base64 image data from the URL
        base64_data = input_data.split(":")[1]
        # Resize base64 image
        return resize_base64_image(base64_data)
    elif is_url(input_data):
       return resize_image(input_data)
    else:
        raise ValueError("Input data is neither a base64 string nor a URL to an online image.")

def resize_base64_image(base64_image):
    """Resizes a base64-encoded image if its width or height is greater than MAX_DIMENSION,
    ensuring the resized image is at least MIN_DIMENSION in both dimensions.

    Args:
        base64_image: The base64-encoded image string.

    Returns:
        The resized base64-encoded image string, or the original string if no resizing was needed.
    """

    try:
        # Decode the base64-encoded image
        img_bytes = base64.b64decode(base64_image)
        img = Image.open(io.BytesIO(img_bytes))

        # Check if resizing is needed
        if img.width > MAX_DIMENSION or img.height > MAX_DIMENSION:
            width, height = img.size
            ratio = min(MAX_DIMENSION / width, MAX_DIMENSION / height)  # Calculate resize ratio
            new_size = (int(width * ratio), int(height * ratio))

            # Ensure at least MIN_DIMENSION in both directions
            new_size = (max(MIN_DIMENSION, new_size[0]), max(MIN_DIMENSION, new_size[1]))
            resized_img = img.resize(new_size, Image.ANTIALIAS)  # Use anti-aliasing for smoother results

            # Encode the resized image back to base64
            buffered = io.BytesIO()
            resized_img.save(buffered, format=img.format)
            resized_base64_image = base64.b64encode(buffered.getvalue()).decode('utf-8')
            return resized_base64_image
        else:
            return base64_image  # No resizing needed, return the original base64 string

    except Exception as e:
        print(f"Error resizing base64 image: {e}")
        return base64_image  # Returning the original base64 string in case of errors


def resize_image(image_url):
  """Resizes an image from a URL if its width or height is greater than MAX_DIMENSION,
  ensuring the resized image is at least MIN_DIMENSION in both dimensions.

  Args:
      image_url: The URL of the image (must start with http or https).

  Returns:
      The resized base64-encoded image string, or None if there was an error.
  """

  try:
    # Check if URL starts with http or https
    if not image_url.startswith("http"):
      raise ValueError("Image URL must start with http or https")

    # Download image data
    response = urlopen(image_url)
    img_bytes = response.read()

    # Open image from downloaded bytes
    img = Image.open(io.BytesIO(img_bytes))

    # Check if resizing is needed
    if img.width > MAX_DIMENSION or img.height > MAX_DIMENSION:
      width, height = img.size
      ratio = min(MAX_DIMENSION / width, MAX_DIMENSION / height)  # Calculate resize ratio
      new_size = (int(width * ratio), int(height * ratio))

      # Ensure at least MIN_DIMENSION in both directions
      new_size = (max(MIN_DIMENSION, new_size[0]), max(MIN_DIMENSION, new_size[1]))
      resized_img = img.resize(new_size, Image.ANTIALIAS)  # Use anti-aliasing for smoother results

      # Encode the resized image back to base64
      buffered = io.BytesIO()
      resized_img.save(buffered, format=img.format)
      resized_base64_image = base64.b64encode(buffered.getvalue()).decode('utf-8')
      return resized_base64_image
    else:
      return None  # No resizing needed, return None

  except Exception as e:
    print(f"Error resizing image: {e}")
    return None  # Returning None in case of errors
