from urllib.parse import urlparse

def detect_platform(url: str):
    host = urlparse(url).netloc.lower().split(":")[0]
    if host.endswith("tiktok.com") or host.endswith("tiktokv.com"): return "tiktok"
    if host.endswith("instagram.com") or host == "instagr.am": return "instagram"
    if host.endswith("facebook.com") or host.endswith("fb.watch"): return "facebook"
    if host.endswith("youtube.com") or host == "youtu.be": return "youtube"
    return None
    
