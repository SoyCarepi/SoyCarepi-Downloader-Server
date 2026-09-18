from urllib.parse import urlparse

def detect_platform(url: str):
    host = (urlparse(url).hostname or "").lower().removeprefix("www.")
    if host == "tiktok.com" or host.endswith(".tiktok.com"):
        return "tiktok"
    if host in {"instagram.com", "instagr.am"} or host.endswith(".instagram.com"):
        return "instagram"
    if host == "facebook.com" or host == "fb.watch" or host.endswith(".facebook.com"):
        return "facebook"
    if host in {"youtube.com", "youtu.be"} or host.endswith(".youtube.com"):
        return "youtube"
    return None
