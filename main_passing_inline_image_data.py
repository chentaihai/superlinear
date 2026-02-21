from google import genai
from google.genai import types

with open('/Users/taihaichen.acl/Documents/IMG_9083.jpg', 'rb') as f:
    image_bytes = f.read()

client = genai.Client()
response = client.models.generate_content(
  model='gemini-3-flash-preview',
  contents=[
    types.Part.from_bytes(
      data=image_bytes,
      mime_type='image/jpeg',
    ),
    'Caption this image. And describe the contents of the image in detail.'
  ]
)

print(response.text)