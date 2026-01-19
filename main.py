from fastapi import FastAPI, UploadFile, File
from fastapi.responses import HTMLResponse
import os
import google.generativeai as genai

# Konfigurasi Gemini API
genai.configure(api_key=os.environ.get("GEMINI_API_KEY"))

app = FastAPI()

@app.get("/", response_class=HTMLResponse)
def home():
    return """
    <html>
        <head><title>Video to Prompt</title></head>
        <body style="font-family:sans-serif;padding:20px">
            <h2>Video to Prompt (Viral Short)</h2>
            <input type="file" id="video" accept="video/*"/>
            <br><br>
            <button onclick="upload()">Generate Prompt</button>
            <pre id="result" style="margin-top:20px;"></pre>

            <script>
            async function upload(){
                const file = document.getElementById('video').files[0];
                const formData = new FormData();
                formData.append("file", file);

                document.getElementById("result").innerText = "Processing...";

                const res = await fetch("/upload", {
                    method: "POST",
                    body: formData
                });

                const data = await res.json();
                document.getElementById("result").innerText = data.prompt;
            }
            </script>
        </body>
    </html>
    """

@app.post("/upload")
async def upload_video(file: UploadFile = File(...)):
    model = genai.GenerativeModel("gemini-pro")

    prompt = f"""
You are a professional short video prompt creator.

Generate a viral short video prompt based on this video concept:
Filename: {file.filename}

Focus on:
- Hook
- Cinematic style
- Camera movement
- Lighting
- Mood
- Viral potential

Return ONLY the prompt in English.
"""

    response = model.generate_content(prompt)

    return {
        "filename": file.filename,
        "prompt": response.text
    }
