from PIL import Image
import io
import base64
import requests
import re
from urllib.request import urlopen

MAX_DIMENSION = 320
MIN_DIMENSION = 100

def is_base64(input_str):
    parts = input_str.split(',')
    if len(parts) != 2:
        return False
    
    # Check if the encoding is base64
    if ';base64' in parts[0]:
        try:
            # Attempt to decode the base64 encoded data
            base64.b64decode(parts[1])
            return True
        except:
            return False
    else:
        # If encoding is not specified or not base64, return false
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
        return resize_base64_image(input_data)
    elif is_url(input_data):
       return resize_image(input_data)
    elif input_data.startswith("blob:"):
        return
    else:
        raise ValueError("Input data is neither a base64 string nor a URL to an online image.")

def resize_base64_image(base64_image):
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


def convert_to_base64(image_url):
    try:
        # Fetch the blob data from the URL
        response = requests.get(image_url)
        
        # Check if the request was successful
        if response.status_code == 200:
            blob_data = response.content
            
            # Convert blob data to base64
            base64_string = base64.b64encode(blob_data).decode('utf-8')
            print("Converted blob to base64 successfully.")
            print(base64_string)
            return base64_string
        else:
            print("Error fetching blob data. Status code:", response.status_code)
            return None
    except Exception as e:
        print("Error converting blob to base64:", e)
        return None