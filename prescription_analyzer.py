# pyrefly: ignore [missing-import]
from google import genai
from pydantic import BaseModel
import os
import json
from dotenv import load_dotenv

load_dotenv()

class MedicationInfo(BaseModel):
    medication_name: str
    use_case: str
    side_effects: list[str]

class PrescriptionAnalysis(BaseModel):
    medications: list[MedicationInfo]

class PrescriptionAnalyzer:
    def __init__(self, api_key=None, model_name='gemini-3.6-flash'):
        """
        Initializes the Prescription Analyzer using Google's Gemini API.
        Ensure you have your API key set in the GEMINI_API_KEY environment variable,
        or pass it directly to this constructor.
        """
        if api_key is None:
            api_key = os.environ.get("GEMINI_API_KEY")
            if not api_key:
                raise ValueError("API Key must be provided or set as GEMINI_API_KEY environment variable.")
        
        self.client = genai.Client(api_key=api_key)
        self.model_name = model_name
    
    def analyze_text(self, ocr_text: str) -> dict:
        """
        Takes messy OCR text from a medical prescription and returns a structured dictionary
        containing the medications, use cases, and side effects.
        """
        prompt = f"""
        You are an expert medical AI assistant.
        I will provide you with messy extracted text from a handwritten medical prescription.
        Your task is to:
        1. Identify the names of any prescribed medications.
        2. Provide the common use case for each medication.
        3. List the common side effects for each medication.
        
        Here is the extracted text:
        {ocr_text}
        """
        
        response = self.client.models.generate_content(
            model=self.model_name,
            contents=prompt,
            config=genai.types.GenerateContentConfig(
                response_mime_type="application/json",
                response_schema=PrescriptionAnalysis,
            ),
        )
        
        return json.loads(response.text)

if __name__ == "__main__":
    # Example usage script
    # Run: python prescription_analyzer.py
    
    print("Initializing Prescription Analyzer...")
    try:
        # Defaults to using GEMINI_API_KEY from environment variables
        analyzer = PrescriptionAnalyzer()
        
        sample_text = "Rx: Amoxicillin 500mg take twice daily for 7 days. Ibuprofen 400mg as needed for pain."
        print(f"Sample Input Text: {sample_text}\n")
        
        result = analyzer.analyze_text(sample_text)
        print("Analysis Result:")
        print(json.dumps(result, indent=2))
    except ValueError as e:
        print("Error:", e)
        print("Please set your GEMINI_API_KEY in your environment variables.")
        print("Example: $env:GEMINI_API_KEY=\"your-api-key\"")
