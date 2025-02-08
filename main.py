from fastapi import FastAPI, HTTPException
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
import json
from pydantic import BaseModel
from typing import List

app = FastAPI()

# Serve static files (HTML)
app.mount("/static", StaticFiles(directory="."), name="static")

# Pydantic models for request/response
class Answer(BaseModel):
    question: str
    selected_answer: str

class TestSubmission(BaseModel):
    level: str
    answers: List[Answer]

# Load test data
def load_test_data(level: str):
    try:
        with open(f"{level.lower()}.json", "r") as f:
            return json.load(f)
    except FileNotFoundError:
        raise HTTPException(status_code=404, detail="Level not found")

@app.get("/")
async def read_root():
    return FileResponse("index.html")

@app.get("/api/test/{level}")
async def get_test(level: str):
    return load_test_data(level)

@app.post("/api/submit")
async def submit_test(submission: TestSubmission):
    # Load correct test data
    test_data = load_test_data(submission.level)
    
    # Calculate score
    correct_answers = 0
    for i, answer in enumerate(submission.answers):
        if answer.selected_answer == test_data["questions"][i]["correct_answer"]:
            correct_answers += 1
    
    # Determine next level based on score
    current_level = submission.level
    levels = ["A1", "A2", "B1", "B2", "C1", "C2"]
    current_index = levels.index(current_level)
    
    if correct_answers <= 3:
        # Go down one level if possible
        next_level = levels[current_index - 1] if current_index > 0 else current_level
    elif correct_answers >= 8:
        # Go up one level if possible
        next_level = levels[current_index + 1] if current_index < len(levels) - 1 else current_level
    else:
        # Stay at current level
        next_level = current_level
    
    return {
        "score": correct_answers,
        "next_level": next_level,
        "stay_current": next_level == current_level
    }