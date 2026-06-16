import threading
import os
import uuid

_engine = None
_lock   = threading.Lock()

def _init_engine():
    import pyttsx3
    engine = pyttsx3.init()
    engine.setProperty("rate", 175)   # words-per-minute (default 200 is slightly fast)
    for voice in engine.getProperty("voices"):
        if "zira" in voice.name.lower():   # Microsoft Zira — Windows female voice
            engine.setProperty("voice", voice.id)
            break
    return engine

def _speak_gtts_fallback(text: str):
    """Used only if pyttsx3 fails (e.g. no SAPI5 voices installed)."""
    import pygame
    from gtts import gTTS
    pygame.mixer.init()
    temp = os.path.join(os.environ.get("TEMP", "."), f"friday_{uuid.uuid4().hex}.mp3")
    try:
        tts = gTTS(text=text, lang="en", slow=False)
        tts.save(temp)
        sound = pygame.mixer.Sound(temp)
        ch = pygame.mixer.find_channel(True)
        ch.play(sound)
        while ch.get_busy():
            pygame.time.Clock().tick(10)
    finally:
        try:
            os.remove(temp)
        except OSError:
            pass

def speak(text: str):
    global _engine
    print(f"[FRIDAY] {text}")

    with _lock:
        try:
            if _engine is None:
                _engine = _init_engine()
            _engine.say(text)
            _engine.runAndWait()
        except Exception as e:
            print(f"[pyttsx3 error — falling back to gTTS] {e}")
            _engine = None
            try:
                _speak_gtts_fallback(text)
            except Exception as e2:
                print(f"[gTTS fallback error] {e2}")
