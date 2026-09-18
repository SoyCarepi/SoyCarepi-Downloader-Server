from app.platforms import detect_platform

def test_supported_platforms():
    assert detect_platform("https://www.tiktok.com/@x/video/123") == "tiktok"
    assert detect_platform("https://www.instagram.com/reel/abc/") == "instagram"
    assert detect_platform("https://www.facebook.com/watch/?v=123") == "facebook"
    assert detect_platform("https://youtu.be/abc") == "youtube"

def test_unknown_platform():
    assert detect_platform("https://example.com/video") is None
