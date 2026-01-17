from fastapi import FastAPI, UploadFile, File
from fastapi.responses import HTMLResponse
import subprocess, os, uuid, base64
import google.generativeai as genai

genai.configure(api_key=os.environ.get("GEMINI_API_KEY"))

app = FastAPI()

UPLOAD_DIR = "uploads"
os.makedirs(UPLOAD_DIR, exist_ok=True)

@app.get("/", response_class=HTMLResponse)
def home():
    return open("index.html").read()

@app.post("/upload")
async def upload_video(file: UploadFile = File(...)):
    video_id = str(uuid.uuid4())
    video_path = f"{UPLOAD_DIR}/{video_id}.mp4"

    with open(video_path, "wb") as f:
        f.write(await file.read())

    # extract frames
    frame_pattern = f"{UPLOAD_DIR}/{video_id}_%03d.jpg"
    subprocess.run([
        "ffmpeg", "-i", video_path,
        "-vf", "fps=1",
        frame_pattern
    ])

    frames = []
    for f in sorted(os.listdir(UPLOAD_DIR)):
        if f.startswith(video_id) and f.endswith(".jpg"):
            with open(f"{UPLOAD_DIR}/{f}", "rb") as img:
                frames.append(base64.b64encode(img.read()).decode())

        if len(frames) >= 5:
            break

    model = genai.GenerativeModel("gemini-pro-vision")

    prompt = """
Analyze these video frames and generate a viral short video prompt.
Focus on cinematic style, hook, lighting, camera angle, motion, and mood.
Return ONLY the prompt in English.
"""

    response = model.generate_content(
        [{"mime_type": "image/jpeg", "data": f} for f in frames] + [prompt]
    )

    return response.text
