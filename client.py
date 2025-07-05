from google import genai
import base64

api_key = "AIzaSyCejGe7ewxpeiMGyHiY9c4tt1lWvakRhb4"  # Replace with your actual API key

def encode_file(file_path):
    """Encodes a file to base64."""
    with open(file_path, "rb") as file:
        return base64.b64encode(file.read()).decode("utf-8")


# --- 1. Prepare the Text Prompt ---
system_prompt = "You are a helpful assistant. Give answers as short as you can."
user_question = "identify the fruit in image and help me to cut it"
text_prompt = system_prompt + "\n" + user_question  # Combine prompt and question



# --- 2. Prepare the File Attachments ---
image_path = "docs/banana.png" #  Replace with the actual path to your image file (or other file)
document_path = "docs/doc.txt"  # Replace with path to your document

# Encode files to base64:
try:
    image_data = encode_file(image_path)
    document_data = encode_file(document_path)
except FileNotFoundError as e:
    print(f"Error: File not found: {e}")
    exit()


# --- 3. Create the Request Payload ---

contents = [
    {
        "role": "user",
        "parts": [
            {"text": text_prompt}, # your text prompt
        ],
    },
    {
        "role": "user",
        "parts": [
            {
                "inline_data": {
                    "mime_type": "image/jpeg",  #  Replace with the actual MIME type of your image
                    "data": image_data,
                }
            }
        ],
    },
    {
        "role": "user",
        "parts": [
            {
                "inline_data": {
                    "mime_type": "text/plain",  # Replace with the actual MIME type of your document
                    "data": document_data,
                }
            }
        ],
    },
]

# --- 4. Make the API Call ---
client = genai.Client(api_key=api_key)

try:
    response = client.models.generate_content(
        model="gemini-2.0-flash", contents=contents
    )
    print(response.text)

except Exception as e:
    print(f"API Error: {e}")