import uvicorn
import json
import os
import aiofiles
from fastapi import FastAPI, File, UploadFile, Request, HTTPException
from fastapi.responses import JSONResponse, FileResponse
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import Optional, List, Dict, Any

# --- Configuration ---
DATA_DIR = "data"
MUSIC_DIR = "music"
APP_DATA_FILE = os.path.join(DATA_DIR, "app_data.json")

# Create directories if they don't exist
os.makedirs(DATA_DIR, exist_ok=True)
os.makedirs(MUSIC_DIR, exist_ok=True)

# This is the DEFAULT_STATE from your index.html, converted to Python
DEFAULT_STATE = {
    'userName': 'Student',
    'dailyFocus': '',
    'focusIsSet': False,
    'dailyStudyGoal': 50,
    'theme': 'light',
    'tasks': [],
    'tasksViewMode': 'kanban',
    'tasksListSort': {'column': 'dueDate', 'direction': 'asc'},
    'tasksCalendarMonth': {'year': 2024, 'month': 10}, # Will be updated by JS on load
    'courses': [],
    'flashcardDecks': [],
    'currentDeckId': None,
    'studyMode': {
        'active': False,
        'deckId': None,
        'currentCardIndex': 0,
        'showingBack': False,
        'answerChecked': False
    },
    'pomodoroSettings': {
        'work': 25,
        'shortBreak': 5,
        'longBreak': 15
    },
    'pomodoro': {
        'mode': 'work',
        'remainingSeconds': 1500,
        'isRunning': False,
        'startTime': None,
        'timerInterval': None
    },
    'studyHistory': [],
    'quickLinks': [
        {'id': 'link1', 'name': 'Google Scholar', 'url': 'https://scholar.google.com', 'icon': '📚'},
        {'id': 'link2', 'name': 'GitHub', 'url': 'https://github.com', 'icon': '💻'},
        {'id': 'link3', 'name': 'YouTube', 'url': 'https://youtube.com', 'icon': '🎥'},
        {'id': 'link4', 'name': 'Stack Overflow', 'url': 'https://stackoverflow.com', 'icon': '❓'}
    ],
    'unlockedAchievements': [],
    'musicPlaylist': [], # Added for storing music
    'chartView': 'daily',
    'currentModule': 'dashboard',
    'currentCourseId': None,
    'lastSaved': 0
}

# --- FastAPI App ---
app = FastAPI()

# --- CORS Middleware ---
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allows all origins (e.G., localhost:3000, file://, etc.)
    allow_credentials=True,
    allow_methods=["*"],  # Allows all methods (GET, POST, etc.)
    allow_headers=["*"],  # Allows all headers
)

# --- API Endpoints ---

@app.post("/api/save-data")
async def save_data(request: Request):
    """Saves the entire application state to a JSON file."""
    try:
        data = await request.json()
        # Add a server-side timestamp
        data['lastSaved'] = int(DEFAULT_STATE['lastSaved']) # Use a consistent timestamp format
        async with aiofiles.open(APP_DATA_FILE, "w", encoding="utf-8") as f:
            await f.write(json.dumps(data, indent=2))
        return {"status": "success", "message": "Data saved."}
    except Exception as e:
        return JSONResponse(status_code=500, content={"status": "error", "message": str(e)})

@app.get("/api/load-data")
async def load_data():
    """Loads the application state from the JSON file."""
    if os.path.exists(APP_DATA_FILE):
        try:
            async with aiofiles.open(APP_DATA_FILE, "r", encoding="utf-8") as f:
                content = await f.read()
                return JSONResponse(content=json.loads(content))
        except Exception as e:
            # If file is corrupt, return default
            return JSONResponse(content=DEFAULT_STATE)
    else:
        # If no file exists, return the default state
        return JSONResponse(content=DEFAULT_STATE)

@app.post("/api/upload-music")
async def upload_music(file: UploadFile = File(...)):
    """Handles music file uploads."""
    file_path = os.path.join(MUSIC_DIR, file.filename)
    
    # Basic security: prevent path traversal
    if ".." in file.filename:
        raise HTTPException(status_code=400, detail="Invalid filename.")
        
    try:
        async with aiofiles.open(file_path, "wb") as f:
            content = await file.read()
            await f.write(content)
            
        # Return the URL that the frontend can use to play the file
        file_url = f"/{MUSIC_DIR}/{file.filename}"
        return {"name": file.filename, "url": file_url}
        
    except Exception as e:
        return JSONResponse(status_code=500, content={"status": "error", "message": str(e)})

class DeleteRequest(BaseModel):
    filename: str

@app.post("/api/delete-music")
async def delete_music(item: DeleteRequest):
    """Deletes a music file from the server."""
    
    # --- FIX IS HERE ---
    # Create the full, absolute path to the file first
    file_path = os.path.abspath(os.path.join(MUSIC_DIR, item.filename))
    
    # Define the absolute path to the music directory
    abs_music_dir = os.path.abspath(MUSIC_DIR)
    
    # Security check:
    # 1. Check for ".." (path traversal)
    # 2. Check if the resolved file path (file_path) is truly inside the allowed music directory (abs_music_dir)
    if ".." in item.filename or not file_path.startswith(abs_music_dir):
        raise HTTPException(status_code=400, detail="Invalid filename or path.")
    # --- END FIX ---
        
    if os.path.exists(file_path):
        try:
            os.remove(file_path)
            return {"status": "success", "message": f"{item.filename} deleted."}
        except Exception as e:
            return JSONResponse(status_code=500, content={"status": "error", "message": str(e)})
    else:
        return JSONResponse(status_code=404, content={"status": "error", "message": "File not found."})


# --- Static File Serving ---

# Serve the music files
app.mount(f"/{MUSIC_DIR}", StaticFiles(directory=MUSIC_DIR), name="music")

# Serve the main index.html
@app.get("/")
async def get_index():
    return FileResponse('index.html')

if __name__ == "__main__":
    print("Starting FastAPI server...")
    print(f"Access the app at http://localhost:8000")
    uvicorn.run("main:app", host="localhost", port=8000, reload=True)