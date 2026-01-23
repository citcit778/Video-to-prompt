from fastapi import FastAPI, UploadFile, File
from fastapi.responses import HTMLResponse

app = FastAPI()

@app.get("/", response_class=HTMLResponse)
async def home():
    return """
    <html>
        <head>
            <title>Video to Prompt</title>
        </head>
        <body style="font-family: Arial; padding: 20px;">
            <h2>Upload Short Video</h2>
            <form action="/upload" method="post" enctype="multipart/form-data">
                <input type="file" name="file" required>
                <br><br>
                <button type="submit">Generate Prompt</button>
            </form>
        </body>
    </html>
    """

@app.post("/upload")
async def upload_video(file: UploadFile = File(...)):
    return {
        "filename": file.filename,
        "prompt": "Cinematic viral short video prompt with smooth camera movement, strong hook in first 3 seconds, soft lighting, shallow depth of field, dynamic motion, high engagement style."
    }
