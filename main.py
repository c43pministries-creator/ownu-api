from fastapi import FastAPI, File, UploadFile, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import shutil
import os
import requests

app = FastAPI(title="Own U Verification & Generation API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"], 
    allow_methods=["*"],
    allow_headers=["*"],
)

UPLOAD_DIR = "uploaded_ids"
os.makedirs(UPLOAD_DIR, exist_ok=True)

# PASTE YOUR KAGGLE NGROK URL HERE
KAGGLE_URL = "https://sternum-ferocity-matador.ngrok-free.dev/generate"

class GenerateRequest(BaseModel):
    prompt: str

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

@app.post("/generate-tryon")
def generate_tryon(request: GenerateRequest):
    # We use the user's exact request, but we force the framing
    full_prompt = f"full body shot, head to toes visible, a realistic fashion photo of a person standing, wearing {request.prompt}, photorealistic, high quality clothing, studio lighting."
    
    try:
        # Send the request to the Kaggle GPU
        response = requests.post(KAGGLE_URL, json={"prompt": full_prompt}, timeout=120)
        response.raise_for_status()
        data = response.json()
        
        return {"status": "success", "image_base64": data["image_base64"]}
    except Exception as e:
        print(f"Kaggle Error: {e}")
        raise HTTPException(status_code=500, detail="Image generation failed.")
@app.get("/")
def read_root():
    return {"message": "Own U Server is running."}
