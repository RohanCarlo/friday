# main.py - FRIDAY with auto-briefing + smart conversation flow

import time
import threading
from friday_gui   import FridayGUI
from voice_input  import listen_once, calibrate_once
from voice_output import speak as _speak
from wake_word    import wait_for_wake_word
from orchestrator import process_command
from agents.sports_agent import get_sports
from agents.news_agent   import get_news

gui = None
CONVERSATION_TIMEOUT = 20  # seconds to wait for follow-up before sleeping

def speak(text: str):
    if gui:
        gui.set_speaking(text)
    _speak(text)
    if gui:
        gui.set_sleeping()

def morning_briefing():
    """FRIDAY proactively tells you important updates on startup."""
    calibrate_once()   # warm up mic before we start speaking
    time.sleep(1.5)

    hour   = time.localtime().tm_hour
    period = "morning" if hour < 12 else "afternoon" if hour < 17 else "evening"

    speak(f"Good {period}. F.R.I.D.A.Y. systems online.")
    time.sleep(0.5)
    speak("Let me pull up your briefing.")
    time.sleep(0.5)

    # ── Barcelona news ───────────────────────────────────────────
    try:
        barca = process_command("Any recent news or updates about FC Barcelona football team?")
        speak(f"Barcelona update. {barca}")
        time.sleep(0.4)
    except:
        speak("Couldn't fetch Barcelona update right now.")

    # ── RCB IPL news ─────────────────────────────────────────────
    try:
        rcb = process_command("Latest news and scores about Royal Challengers Bangalore RCB in IPL?")
        speak(f"RCB update. {rcb}")
        time.sleep(0.4)
    except:
        speak("Couldn't fetch RCB update right now.")

    # ── Top news headlines ───────────────────────────────────────
    try:
        news = get_news(category="general", country="in")
        speak(f"Here are today's top stories. {news}")
        time.sleep(0.4)
    except:
        speak("Couldn't fetch top news right now.")

    speak("That's your briefing. Say Hi Friday anytime you need me.")

def conversation_window():
    """
    Once FRIDAY is awake, keep her awake and listening
    without needing 'Hi Friday' again for each message.
    Returns when user goes quiet or says goodbye.
    """
    while True:
        if gui:
            gui.set_listening()

        command = listen_once(timeout=CONVERSATION_TIMEOUT, phrase_limit=15)

        # Silence — go back to sleep
        if not command:
            speak("Going back to sleep. Say Hi Friday when you need me.")
            return

        if gui:
            gui.set_heard(command)
            gui.set_processing()

        # Exit phrases
        if any(w in command for w in [
            "goodbye", "shut down", "go to sleep",
            "bye friday", "sleep", "that's all", "thank you friday",
            "thanks friday", "see you"
        ]):
            speak("Alright, going to sleep. Say Hi Friday when you need me.")
            return

        # Process and respond
        response = process_command(command)
        speak(response)
        time.sleep(0.3)
        # Loop back — keep listening without requiring wake word again

def friday_loop():
    morning_briefing()

    while True:
        try:
            # ── Sleep: wait for wake word ─────────────────────────
            if gui:
                gui.set_sleeping()
            wait_for_wake_word()

            # ── Woken up ──────────────────────────────────────────
            speak("Yes?")

            # ── Stay in conversation until user goes quiet ────────
            conversation_window()

        except KeyboardInterrupt:
            speak("Shutting down. Goodbye.")
            if gui:
                gui.stop()
            break
        except Exception as e:
            print(f"[Error] {e}")
            speak("Something went wrong. Ready when you are.")
            continue

def main():
    global gui
    gui = FridayGUI()
    gui.set_sleeping()

    t = threading.Thread(target=friday_loop, daemon=True)
    t.start()

    gui.run()

if __name__ == "__main__":
    main()