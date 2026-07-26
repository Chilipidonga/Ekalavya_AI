import os
import json
import logging
from groq import Groq
from dotenv import load_dotenv

load_dotenv()

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

client = Groq(api_key=os.getenv("GROQ_API_KEY"))
MODEL_NAME = "llama-3.3-70b-versatile"

class GeneratorAgent:
    def generate(self, grade: int, topic: str, previous_feedback: list = None) -> dict:
        """
        Generates educational content and refines it if previous feedback is provided.
        """
        system_prompt = f"""You are an expert educational content creator for school students.
        Your task is to generate an educational explanation and multiple-choice questions (MCQs) for a Grade {grade} student about the topic: '{topic}'.
        
        CRITICAL INSTRUCTIONS:
        1. The language, tone, and complexity MUST be perfectly age-appropriate for Grade {grade}.
        2. Concepts must be factually correct.
        3. You MUST return the output as a valid JSON object matching this exact structure:
        
        {{
            "explanation": "A clear, engaging explanation of the topic appropriate for the grade.",
            "mcqs": [
                {{
                    "question": "Question text here",
                    "options": ["Option A", "Option B", "Option C", "Option D"],
                    "answer": "The exact string of the correct option"
                }}
            ]
        }}
        
        Generate exactly 3 MCQs. Output ONLY the JSON object and no other text.
        """

        prompt_payload = f"Create content for Topic: '{topic}', Grade: {grade}."
        
        if previous_feedback:
            prompt_payload += "\n\nWARNING: Your previous draft failed the review. You MUST rewrite the content to fix the following issues:\n"
            for issue in previous_feedback:
                prompt_payload += f"- {issue}\n"
                
        logger.info("Initiating Generator Agent draft creation.")
        
        response = client.chat.completions.create(
            model=MODEL_NAME,
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": prompt_payload}
            ],
            response_format={"type": "json_object"},
            temperature=0.7 
        )
        
        return json.loads(response.choices[0].message.content)

class ReviewerAgent:
    def review(self, grade: int, generator_output: dict) -> dict:
        """
        Evaluates the Generator's output against strict educational criteria.
        """
        system_prompt = f"""You are a strict educational reviewer. 
        Your task is to review educational content intended for a Grade {grade} student.
        
        EVALUATION CRITERIA:
        1. Age appropriateness: Is the vocabulary and tone suitable for a Grade {grade} student?
        2. Conceptual correctness: Are there any factual errors in the explanation or the MCQs?
        3. Clarity: Is the explanation easy to understand and are the MCQs well-framed without ambiguity?
        
        CRITICAL INSTRUCTIONS:
        You MUST return your evaluation as a valid JSON object matching this exact structure:
        
        {{
            "status": "pass" OR "fail",
            "feedback": ["String detailing specific issue 1", "String detailing specific issue 2"]
        }}
        
        - If the content meets all criteria perfectly, set status to "pass" and leave the feedback array empty.
        - If the content fails ANY of the criteria, set status to "fail" and provide specific, actionable feedback strings in the array.
        Output ONLY the JSON object and no other text.
        """
        
        prompt_payload = json.dumps(generator_output, indent=2)
        
        logger.info("Reviewer Agent is analyzing draft.")
        
        response = client.chat.completions.create(
            model=MODEL_NAME,
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": prompt_payload}
            ],
            response_format={"type": "json_object"}, 
            temperature=0.1 
        )
        
        return json.loads(response.choices[0].message.content)