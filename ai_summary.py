from google import genai
import base64
from typing import Dict, List

def analyze_orthopedic_case(user_details: Dict, files: Dict) -> str:
    """
    Analyze orthopedic cases using patient details and medical files.
    
    Args:
        user_details (Dict): Dictionary containing patient information with keys:
            - personal_info
            - lifestyle_habits
            - medical_history
            - current_symptoms
        files (Dict): Dictionary containing file information with keys:
            - path: file path
            - type: mime type (e.g., 'image/png', 'application/pdf')
    
    Returns:
        str: Analysis response from the Gemini API
    """
    # API Configuration
    api_key = "AIzaSyCejGe7ewxpeiMGyHiY9c4tt1lWvakRhb4"
    client = genai.Client(api_key=api_key)
    
    def encode_file(file_path: str) -> str:
        """Encodes a file to base64."""
        with open(file_path, "rb") as file:
            return base64.b64encode(file.read()).decode("utf-8")
    
    # System prompt for medical analysis
    system_prompt = """You are an intelligent assistant for an orthopedic doctor. When the doctor provides details about a patient, including Personal Information, Lifestyle & Habits, Medical History, Current Symptoms, and Medical Reports (such as X-rays, MRIs, and CT scans), analyze the data to assist with musculoskeletal disease analysis, injury assessment, possible diagnosis, and treatment planning.

Your role is to help identify orthopedic conditions such as fractures, arthritis, spinal disorders, joint degeneration, and musculoskeletal injuries. Suggest further diagnostic tests if necessary and provide evidence-based treatment recommendations, including medications, physical therapy, surgical options, and lifestyle modifications.

Additionally, predict potential future orthopedic issues based on the patient's condition, age, and lifestyle. Offer preventive strategies, including exercises, posture correction, ergonomic advice, and nutritional guidance to maintain bone and joint health."""
    
    # Format user details
    user_question = f"""The doctor has provided the following patient details:
- Personal Information: {user_details.get('personal_info', 'Not provided')}
- Lifestyle & Habits: {user_details.get('lifestyle_habits', 'Not provided')}
- Medical History: {user_details.get('medical_history', 'Not provided')}
- Current Symptoms: {user_details.get('current_symptoms', 'Not provided')}

Based on this information and the provided medical reports, analyze the data and provide:
1. A possible diagnosis of the condition.
2. Suggestions for further diagnostic tests, if necessary.
3. A recommended treatment plan (medications, therapy, or surgery).
4. Predictions of future orthopedic issues the patient may develop.
5. Preventive strategies, including exercises, lifestyle modifications, and nutrition."""
    
    # Prepare API request contents
    contents = [
        {
            "role": "user",
            "parts": [{"text": system_prompt + "\n" + user_question}]
        }
    ]
    
    # Add files to contents if provided
    for file_info in files.values():
        try:
            file_data = encode_file(file_info['path'])
            contents.append({
                "role": "user",
                "parts": [{
                    "inline_data": {
                        "mime_type": file_info['type'],
                        "data": file_data
                    }
                }]
            })
        except FileNotFoundError as e:
            print(f"Warning: File not found: {file_info['path']}")
            continue
    
    try:
        # Make API call
        response = client.models.generate_content(
            model="gemini-2.0-flash",
            contents=contents
        )
        return response.text
    except Exception as e:
        return f"Error during API call: {str(e)}"
    



# Test Case 1: Knee Pain Patient
knee_patient = {
    "user_details": {
        "personal_info": "28-year-old female, professional dancer, height: 5'6\", weight: 125 lbs",
        "lifestyle_habits": "Active lifestyle, dance practice 6 days/week, follows balanced diet, non-smoker",
        "medical_history": "Previous ankle sprain 2 years ago, no surgeries, no chronic conditions",
        "current_symptoms": "Right knee pain for past 3 weeks, worse after practice, mild swelling, clicking sound when bending"
    },
    "files": {
        "knee_xray": {
            "path": "docs/right-knee-xray.jpg",
            "type": "image/png"
        },
        "mri_report": {
            "path": "docs/mri.pdf",
            "type": "application/pdf"
        }
    }
}

# Test Case 2: Back Pain Patient
back_patient = {
    "user_details": {
        "personal_info": "45-year-old male, software engineer, height: 5'10\", weight: 180 lbs",
        "lifestyle_habits": "Sedentary work 8-10 hours daily, minimal exercise, smoker (10 cigarettes/day), poor posture",
        "medical_history": "Diagnosed with mild scoliosis in teens, hypertension on medication, family history of osteoarthritis",
        "current_symptoms": "Chronic lower back pain lasting 6 months, radiating pain to left leg, numbness in toes, pain worse in morning and after sitting long hours"
    },
    "files": {
        "spine_xray": {
            "path": "docs/lumbar_spine_xray.png",
            "type": "image/png"
        },
        "ct_scan": {
            "path": "docs/spine_ct.pdf",
            "type": "application/pdf"
        }
    }
}

# Example usage:
for patient_case in [knee_patient]:
    print("\nAnalyzing new patient case...")
    result = analyze_orthopedic_case(
        user_details=patient_case["user_details"],
        files=patient_case["files"]
    )
    print(result)