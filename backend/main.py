import logging
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from fastapi.middleware.cors import CORSMiddleware
from agents import GeneratorAgent, ReviewerAgent

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

app = FastAPI(title="Eklavya AI Assessment Pipeline")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"], 
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class GenerateRequest(BaseModel):
    grade: int
    topic: str

generator = GeneratorAgent()
reviewer = ReviewerAgent()

@app.post("/api/generate-lesson")
async def generate_lesson(request: GenerateRequest):
    try:
        logger.info(f"Starting Generation Pipeline | Grade: {request.grade} | Topic: '{request.topic}'")
        
        initial_draft = generator.generate(grade=12, topic=request.topic)
        
        review_result = reviewer.review(grade=request.grade, generator_output=initial_draft)
        status = review_result.get("status")
        feedback = review_result.get("feedback", [])
        
        logger.info(f"Review Agent Evaluation Status: {status.upper()}")
        
        if status == "pass":
            return {
                "initial_draft": initial_draft,
                "feedback": [],
                "final_draft": None,
                "status": "pass"
            }
            
        logger.info("Triggering refinement loop based on Reviewer feedback.")
        refined_draft = generator.generate(
            grade=request.grade, 
            topic=request.topic, 
            previous_feedback=feedback
        )
        
        return {
            "initial_draft": initial_draft,
            "feedback": feedback,
            "final_draft": refined_draft,
            "status": "refined"
        }
        
    except Exception as e:
        logger.error(f"Pipeline Execution Error: {str(e)}", exc_info=True)
        raise HTTPException(status_code=500, detail="An error occurred during the AI generation pipeline.")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)