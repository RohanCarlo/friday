import speech_recognition as sr

recognizer = sr.Recognizer()
recognizer.energy_threshold        = 300
recognizer.pause_threshold         = 0.6   # shorter pause = faster end-of-phrase detection
recognizer.non_speaking_duration   = 0.4
recognizer.dynamic_energy_threshold = True

_calibrated = False

def calibrate_once():
    """Run at startup so every subsequent listen skips the 0.5s noise calibration."""
    global _calibrated
    if _calibrated:
        return
    print("[FRIDAY] Calibrating microphone...")
    with sr.Microphone() as source:
        recognizer.adjust_for_ambient_noise(source, duration=1.0)
    _calibrated = True
    print(f"[FRIDAY] Mic calibrated — energy threshold: {recognizer.energy_threshold:.0f}")

def listen_once(timeout=8, phrase_limit=10) -> str | None:
    """Listen for one phrase and return the text, or None if nothing heard."""
    if not _calibrated:
        calibrate_once()

    with sr.Microphone() as source:
        print("[FRIDAY] Listening...")
        try:
            audio = recognizer.listen(
                source,
                timeout=timeout,
                phrase_time_limit=phrase_limit
            )
        except sr.WaitTimeoutError:
            return None

    try:
        text = recognizer.recognize_google(audio, language="en-IN")
        print(f"[You said] {text}")
        return text.lower().strip()
    except sr.UnknownValueError:
        return None
    except sr.RequestError as e:
        print(f"[Voice Input Error] {e}")
        return None
