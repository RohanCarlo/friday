import speech_recognition as sr
from voice_input import calibrate_once, recognizer

WAKE_PHRASES = [
    "hi friday", "hey friday", "friday",
    "hi frieda", "high friday", "hey frieda",
    "okay friday", "ok friday", "wake up friday",
]

def wait_for_wake_word():
    """
    Listens in short 2-second bursts until it hears a wake phrase.
    Mic is calibrated once on first call so no per-burst overhead.
    """
    calibrate_once()
    print("[FRIDAY] Sleeping... say 'Hi Friday' to wake me up.")

    while True:
        try:
            with sr.Microphone() as source:
                audio = recognizer.listen(
                    source,
                    timeout=2,
                    phrase_time_limit=2
                )

            heard = recognizer.recognize_google(audio, language="en-IN").lower().strip()
            print(f"[Heard] {heard}")

            if any(phrase in heard for phrase in WAKE_PHRASES):
                print("[FRIDAY] Wake word detected!")
                return

        except sr.WaitTimeoutError:
            pass
        except sr.UnknownValueError:
            pass
        except sr.RequestError:
            pass
        except Exception as e:
            print(f"[Wake Word Error] {e}")
