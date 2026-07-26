# Eklavya AI Assessment: Agent-Based Educational Content Generator

A full-stack, AI-driven application that utilizes a multi-agent pipeline to generate, review, and dynamically refine age-appropriate educational content for students.

##  Architecture Overview

This project implements a lightweight, zero-downtime AI agent pipeline:
1. **Generator Agent:** Drafts an initial lesson explanation and MCQs based on the requested Grade Level and Topic.
2. **Reviewer Agent:** Strictly evaluates the draft for age-appropriateness, conceptual accuracy, and clarity.
3. **Refinement Loop:** If the Reviewer issues a `FAIL` status, the feedback is instantly fed back into the Generator for a single-pass refinement to produce a simplified, corrected final draft.

##  Tech Stack
* **Frontend:** React (Vite), CSS3 (Component-driven architecture)
* **Backend:** Python, FastAPI, Pydantic
* **AI Integration:** Groq API (Llama-3.3-70b-versatile model)

##  Setup Instructions

### Backend (FastAPI)
1. Navigate to the backend directory:
   ```bash
   cd backend