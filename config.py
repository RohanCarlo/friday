import os
from dotenv import load_dotenv

load_dotenv()

GEMINI_API_KEY      = os.getenv("GEMINI_API_KEY", "")
OPENWEATHER_API_KEY = os.getenv("OPENWEATHER_API_KEY", "")
NEWS_API_KEY        = os.getenv("NEWS_API_KEY", "")
GROQ_API_KEY        = os.getenv("GROQ_API_KEY", "")
YOUR_CITY           = os.getenv("YOUR_CITY", "Bengaluru")

VOICE_LANGUAGE = "en"
VOICE_SPEED    = False

APPS = {
    "intellij"  : r"C:\Program Files\JetBrains\IntelliJ IDEA 2025.3.1.1\bin\idea64.exe",
    "vscode"    : r"C:\Users\admin\AppData\Local\Programs\Microsoft VS Code\bin\code",
    "chrome"    : r"C:\Program Files\Google\Chrome\Application\chrome.exe",
    "notepad"   : "notepad.exe",
    "spotify"   : r"C:\Users\%USERNAME%\AppData\Roaming\Spotify\Spotify.exe",
    "terminal"  : "cmd.exe",
    "explorer"  : "explorer.exe",
}
