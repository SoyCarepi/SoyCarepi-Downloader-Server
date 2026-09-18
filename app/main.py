from fastapi import FastAPI, HTTPException, Query
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import StreamingResponse
from pydantic import BaseModel, HttpUrl
from urllib.parse import urlparse
from .platforms import detect_platform
import httpx

app = FastAPI(title="SoyCarepi Downloader API", version="1.0.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["POST", "GET"],
    allow_headers=["*"],
)

SUPPORTED = {"tiktok", "instagram", "facebook", "youtube"}

class ResolveRequest(BaseModel):
    url: HttpUrl

def extract(url: str):
    # Imported lazily so the API can start and URL tests can run even before
    # the server dependencies have been installed.
    import yt_dlp

    opts = {
        "quiet": True,
        "no_warnings": True,
        "noplaylist": True,
        "skip_download": True,
        "socket_timeout": 20,
    }
    with yt_dlp.YoutubeDL(opts) as ydl:
        return ydl.extract_info(url, download=False)

@app.get("/api/health")
def health():
    return {"ok": True, "service": "SoyCarepi Downloader API", "version": "1.0.0"}

@app.post("/api/resolve")
def resolve(req: ResolveRequest):
    url = str(req.url)
    platform = detect_platform(url)
    if platform not in SUPPORTED:
        raise HTTPException(400, detail={
            "error": "unsupported_url",
            "message": "Plataforma no compatible."
        })

    try:
        info = extract(url)
        formats = []
        seen = set()

        for f in info.get("formats", []):
            media_url = f.get("url")
            ext = f.get("ext")
            if not media_url or ext not in {"mp4", "m4a", "webm"}:
                continue

            has_video = f.get("vcodec") not in (None, "none")
            has_audio = f.get("acodec") not in (None, "none")
            if not (has_video or (platform == "youtube" and has_audio)):
                continue

            # Prefer common downloadable formats and avoid duplicate URLs.
            key = (media_url, ext)
            if key in seen:
                continue
            seen.add(key)

            if has_video:
                label = f.get("resolution") or f.get("format_note") or "Video"
            else:
                label = "Audio"

            formats.append({
                "format_id": f.get("format_id"),
                "label": label,
                "ext": ext,
                "url": media_url,
                "has_video": has_video,
                "has_audio": has_audio,
            })

        # Keep the response compact. Sort video formats roughly by height.
        formats.sort(key=lambda x: (not x["has_video"], x["label"]))
        formats = formats[:8]

        if not formats:
            raise RuntimeError("No downloadable format")

        return {
            "platform": platform,
            "title": info.get("title") or "Video",
            "thumbnail": info.get("thumbnail"),
            "formats": formats,
        }

    except Exception:
        raise HTTPException(502, detail={
            "error": "media_unavailable",
            "message": "No se pudo obtener un archivo descargable para este enlace."
        })

@app.get("/api/download")
async def download(url: str = Query(..., min_length=8)):
    """
    Streams a provider-supplied media URL through this server without
    permanently storing the media on disk.
    """
    parsed = urlparse(url)
    if parsed.scheme not in {"http", "https"} or not parsed.hostname:
        raise HTTPException(400, detail={"error": "invalid_url", "message": "URL inválida."})

    async def stream():
        async with httpx.AsyncClient(follow_redirects=True, timeout=30.0) as client:
            async with client.stream("GET", url) as response:
                response.raise_for_status()
                async for chunk in response.aiter_bytes(1024 * 256):
                    yield chunk

    return StreamingResponse(
        stream(),
        media_type="application/octet-stream",
        headers={"Content-Disposition": "attachment; filename=\"video.mp4\""},
    )
