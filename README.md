# SoyCarepi Downloader Server V1.1

FastAPI backend for the SoyCarepi Downloader APK. Uses yt-dlp for supported public media URLs and does not permanently store media.

Deploy on Render with build `pip install -r requirements.txt` and start `uvicorn app.main:app --host 0.0.0.0 --port $PORT`.
