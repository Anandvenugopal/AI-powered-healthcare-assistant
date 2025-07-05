from google import genai
import base64

api_key = "AIzaSyCejGe7ewxpeiMGyHiY9c4tt1lWvakRhb4"  # Replace with your actual API key

def encode_file(file_path):
    """Encodes a file to base64."""
    with open(file_path, "rb") as file:
        return base64.b64encode(file.read()).decode("utf-8")


# --- 1. Prepare the Text Prompt for Medical Analysis ---
system_prompt = "You are an intelligent assistant for an orthopedic doctor. When the doctor provides details about a patient, including Personal Information, Lifestyle & Habits, Medical History, Current Symptoms, and Medical Reports (such as X-rays, MRIs, and CT scans), analyze the data to assist with musculoskeletal disease analysis, injury assessment, possible diagnosis, and treatment planning.Your role is to help identify orthopedic conditions such as fractures, arthritis, spinal disorders, joint degeneration, and musculoskeletal injuries. Suggest further diagnostic tests if necessary and provide evidence-based treatment recommendations, including medications, physical therapy, surgical options, and lifestyle modifications.Additionally, predict potential future orthopedic issues based on the patient's condition, age, and lifestyle. Offer preventive strategies, including exercises, posture correction, ergonomic advice, and nutritional guidance to maintain bone and joint health."
user_question = (
    "The doctor has provided the following patient details: "
    "\n- **Personal Information:** [Provide details] "
    "\n- **Lifestyle & Habits:** [Provide details] "
    "\n- **Medical History:** [Provide details] "
    "\n- **Current Symptoms:** [Provide details] "
    "\n- **Medical Reports (X-ray, MRI, CT scans, etc.):** [Provide file attachments] "
    "\n\nBased on this information, analyze the data and provide: "
    "\n1. A possible diagnosis of the condition."
    "\n2. Suggestions for further diagnostic tests, if necessary."
    "\n3. A recommended treatment plan (medications, therapy, or surgery)."
    "\n4. Predictions of future orthopedic issues the patient may develop."
    "\n5. Preventive strategies, including exercises, lifestyle modifications, and nutrition."
)

text_prompt = system_prompt + "\n" + user_question  # Combine prompt and question

# --- 2. Prepare the File Attachments for Medical Analysis ---
# Example paths to different medical reports and scans (replace with actual paths)
image_path = "docs/fingerbroken.jpg"  # Replace with the actual path to your X-ray image file
# document_path = "docs/blood_report.pdf"  # Replace with the path to your blood report (PDF)

# Encode files to base64:
try:
    image_data = encode_file(image_path)
    # document_data = encode_file(document_path)
except FileNotFoundError as e:
    print(f"Error: File not found: {e}")
    exit()

# --- 3. Create the Request Payload ---
contents = [
    {
        "role": "user",
        "parts": [
            {"text": text_prompt},  # Medical report analysis prompt
        ],
    },
    {
        "role": "user",
        "parts": [
            {
                "inline_data": {
                    "mime_type": "image/png",  # Assuming X-ray image is in PNG format
                    "data": image_data,
                }
            }
        ],
    },
    # {
    #     "role": "user",
    #     "parts": [
    #         {
    #             "inline_data": {
    #                 "mime_type": "application/pdf",  # Assuming blood report is in PDF format
    #                 "data": document_data,
    #             }
    #         }
    #     ],
    # },
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
