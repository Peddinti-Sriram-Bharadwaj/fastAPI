from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import yt_dlp

app = FastAPI()

class VideoRequest(BaseModel):
    url: str

@app.post("/summarize-youtube")
async def summarize_youtube(request: VideoRequest):
    url = request.url

    try:
        ydl_opts = {
            'format': 'bestaudio/best',
            'outtmpl': 'downloads/%(id)s.%(ext)s',
        }
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info_dict = ydl.extract_info(url, download=False)
            audio_url = info_dict['formats'][0]['url']
            return {"audio_url": audio_url}
    except Exception as e:
        print(f"Error: {e}")  # This will log the exact error to the console
        raise HTTPException(status_code=400, detail=f"Error downloading video: {e}")
