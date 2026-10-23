from fastapi import FastAPI, File, UploadFile, HTTPException
from fastapi.middleware.cors import CORSMiddleware
import shutil
import os

app = FastAPI(title="Own U Verification API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"], 
    allow_methods=["*"],
    allow_headers=["*"],
)

UPLOAD_DIR = "uploaded_ids"
os.makedirs(UPLOAD_DIR, exist_ok=True)

@app.post("/verify-id")
async def verify_id(
    front_file: UploadFile = File(...),
    back_file: UploadFile = File(...)
):
    if not front_file.content_type.startswith("image/") or not back_file.content_type.startswith("image/"):
        raise HTTPException(status_code=400, detail="Files must be images.")
    
    # Save Front
    front_path = os.path.join(UPLOAD_DIR, f"front_{front_file.filename}")
    with open(front_path, "wb") as buffer:
        shutil.copyfileobj(front_file.file, buffer)
        
    # Save Back
    back_path = os.path.join(UPLOAD_DIR, f"back_{back_file.filename}")
    with open(back_path, "wb") as buffer:
        shutil.copyfileobj(back_file.file, buffer)
        
    return {
        "status": "success",
        "message": "Front and Back IDs received and saved.",
        "verified": True
    }

@app.get("/")
def read_root():
    return {"message": "Own U Verification Server is running."}