from fastapi import FastAPI, File, UploadFile, HTTPException
from fastapi.middleware.cors import CORSMiddleware
import shutil
import os

app = FastAPI(title="Own U Verification API")

# Allow the Android app to talk to this server
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"], 
    allow_methods=["*"],
    allow_headers=["*"],
)

# Create a folder to save the uploaded IDs
UPLOAD_DIR = "uploaded_ids"
os.makedirs(UPLOAD_DIR, exist_ok=True)

@app.post("/verify-id")
async def verify_id(file: UploadFile = File(...)):
    # 1. Check the file type
    if not file.content_type.startswith("image/"):
        raise HTTPException(status_code=400, detail="File must be an image.")
    
    # 2. Save the image to the server
    file_path = os.path.join(UPLOAD_DIR, file.filename)
    with open(file_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)
        
    # 3. In the future, we will run the AI verification here.
    # For now, we just return a success message.
    
    return {
        "status": "success",
        "message": f"ID received and saved as {file.filename}",
        "verified": True
    }

@app.get("/")
def read_root():
    return {"message": "Own U Verification Server is running."}