# F.R.I.D.A.Y. — AI Voice Assistant

A personal Iron Man-inspired voice assistant for Windows. Uses Groq (LLaMA) for fast AI responses, Google Speech Recognition for voice input, and a JARVIS-style Tkinter GUI.

## Features

- **Wake word** — say "Hi Friday" to activate
- **Persistent memory** — remembers facts about you across sessions (`memory.json`)
- **Conversation context** — keeps the last 3 exchanges in memory during a session
- **Morning briefing** — auto-fetches Barcelona news, RCB scores, and top headlines on startup
- **Weather** — real-time via OpenWeatherMap
- **News** — top headlines via NewsAPI (India)
- **Sports** — IPL / TheSportsDB scores
- **App launcher** — open VS Code, Chrome, IntelliJ, Spotify, and more by voice
- **System info** — CPU and RAM usage on demand
- **JARVIS-style GUI** — animated rings, visualizer bars, conversation log

## Setup

### 1. Clone and install dependencies

```bash
git clone https://github.com/your-username/friday.git
cd friday
pip install -r requirements.txt
```

> **Windows note:** `pyaudio` often needs a wheel — install it with:
> ```bash
> pip install pipwin && pipwin install pyaudio
> ```

### 2. Configure API keys

Copy `.env.example` to `.env` and fill in your keys:

```bash
cp .env.example .env
```

| Key | Where to get it |
|-----|----------------|
| `GROQ_API_KEY` | [console.groq.com](https://console.groq.com) — free |
| `OPENWEATHER_API_KEY` | [openweathermap.org](https://openweathermap.org/api) — free tier |
| `NEWS_API_KEY` | [newsapi.org](https://newsapi.org) — free tier |
| `GEMINI_API_KEY` | [aistudio.google.com](https://aistudio.google.com) — free |

### 3. Update app paths (optional)

Edit `config.py` → `APPS` dict to match your installed application paths.

### 4. Run

```bash
python main.py
```

Or double-click `start_friday.bat`.

## Voice commands

| Say | What happens |
|-----|-------------|
| "Hi Friday" | Wake up |
| "What's the weather?" | Current weather for your city |
| "Top news" | Today's headlines |
| "Open Chrome" | Launches Chrome |
| "IPL scores" / "RCB update" | Latest cricket results |
| "System info" | CPU and RAM usage |
| "Goodbye" / "Go to sleep" | Back to sleep mode |

### Memory commands

| Say | What happens |
|-----|-------------|
| "Remember I like dark coffee" | Saves the fact to `memory.json` |
| "Don't forget my sister's birthday is March 15" | Saves with a descriptive key |
| "What do you know about me?" | Speaks all stored memories |
| "Do you remember my coffee preference?" | Searches memories for "coffee" |
| "Forget my coffee preference" | Deletes that entry |

FRIDAY uses stored memories **automatically** — if you've told her your city, she'll factor that into recommendations without being asked.

## Project structure

```
friday/
├── main.py              # Entry point, conversation loop
├── orchestrator.py      # LLM routing + tool dispatch + session context
├── voice_input.py       # Speech recognition (calibrates mic once at startup)
├── voice_output.py      # Text-to-speech (pyttsx3 + gTTS fallback)
├── wake_word.py         # Wake phrase detection
├── friday_gui.py        # Tkinter animated GUI
├── config.py            # Loads settings from .env
├── agents/
│   ├── weather_agent.py
│   ├── news_agent.py
│   ├── sports_agent.py
│   ├── system_agent.py
│   └── memory_agent.py  # Persistent memory (read/write memory.json)
├── memory.json          # Auto-created; stores your facts (gitignored)
├── .env                 # Your API keys (never committed)
└── .env.example         # Template for new users
```

## Requirements

- Windows 10/11
- Python 3.10+
- Microphone
- Internet connection (for speech recognition, news, weather, Groq API)
