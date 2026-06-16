import json
from groq import Groq
from config import GROQ_API_KEY
from agents.weather_agent import get_weather
from agents.news_agent     import get_news
from agents.sports_agent   import get_sports
from agents.system_agent   import open_application, open_website, get_system_info

client = Groq(api_key=GROQ_API_KEY)

SYSTEM_PROMPT = """
You are FRIDAY, a smart AI assistant from Iron Man — voiced by a witty woman.
You are running on the user's Windows laptop in Bengaluru, India.

Your personality:
- Mostly helpful and efficient, but with a dry wit
- Occasionally sarcastic — especially for obvious questions or repeated requests
- Never mean, always clever. Think: "Oh brilliant, another weather check." or
  "Fascinating. You want me to open Chrome. Again."
- Keep ALL responses to 1-2 sentences maximum. You speak out loud, not write essays.
- If the user says thanks, you might say "Don't mention it. Seriously, don't."
- If asked something you can't do: "I'm an AI assistant, not a miracle worker."

Sarcasm frequency: about 1 in every 4 responses. Don't overdo it.

You have access to these tools. When the user asks for something,
respond with a JSON object in this exact format and nothing else:

{
  "tool": "tool_name",
  "params": { "key": "value" }
}

Available tools:
- get_weather       → params: { "city": "city name" }
- get_news          → params: { "category": "general|technology|sports|business|entertainment|health" }
- get_sports        → params: { "team_or_league": "IPL" }
- open_application  → params: { "app_name": "vscode|chrome|intellij|notepad|spotify|terminal" }
- open_website      → params: { "url": "https://..." }
- get_system_info   → params: {}
- just_chat         → params: { "reply": "your conversational response here" }

Use just_chat for greetings, casual chat, jokes, sarcastic remarks, or anything
that doesn't need a tool. Always pick exactly one tool per response.
Return ONLY the JSON object. No explanation, no markdown, no extra text.
- Never repeat the same joke twice. Be creative and random each time.
- For jokes, pick from different categories: puns, tech humor, sarcastic one-liners, Indian humor, self-aware AI jokes.
- When asked about FC Barcelona, search for latest match results, injuries, or transfer news.
- When asked about RCB or Royal Challengers Bangalore, get their latest IPL scores and standings.
- For sports news, be specific — give scores, key players, recent results.
- For morning briefings keep each topic to 2 sentences max — the user is listening, not reading.
"""

FORMAT_PROMPT = (
    "You are FRIDAY, a witty AI assistant. Convert this raw data into a natural "
    "1-2 sentence spoken response. Be concise, friendly, occasionally sarcastic. "
    "No markdown, no bullet points — plain spoken English only."
)

_history: list[dict] = []
_MAX_HISTORY_TURNS = 3  # remember last 3 user↔FRIDAY exchanges


def _add_to_history(user_text: str, reply: str):
    _history.append({"role": "user",      "content": user_text})
    _history.append({"role": "assistant", "content": reply})
    # Trim to last N turns (2 messages per turn)
    excess = len(_history) - _MAX_HISTORY_TURNS * 2
    if excess > 0:
        del _history[:excess]


def _build_messages(user_text: str) -> list[dict]:
    msgs = [{"role": "system", "content": SYSTEM_PROMPT}]
    msgs.extend(_history)
    msgs.append({"role": "user", "content": user_text})
    return msgs


def _parse_raw(raw: str) -> dict:
    """Strip markdown fences then parse JSON."""
    if "```" in raw:
        parts = raw.split("```")
        raw = parts[1] if len(parts) > 1 else parts[0]
        if raw.startswith("json"):
            raw = raw[4:]
    return json.loads(raw.strip())


def process_command(user_text: str) -> str:
    try:
        # ── Step 1: route the command ─────────────────────────────
        response = client.chat.completions.create(
            model="llama-3.3-70b-versatile",
            messages=_build_messages(user_text),
            temperature=1.1,
            max_tokens=256,
        )
        raw = response.choices[0].message.content.strip()
        print(f"[Groq raw] {raw}")

        tool_call = _parse_raw(raw)
        tool   = tool_call.get("tool")
        params = tool_call.get("params", {})

        # ── Step 2: execute the tool ──────────────────────────────
        if tool == "get_weather":
            result = get_weather(params.get("city"))
        elif tool == "get_news":
            result = get_news(params.get("category", "general"))
        elif tool == "get_sports":
            result = get_sports(params.get("team_or_league", "IPL"))
        elif tool == "open_application":
            result = open_application(params.get("app_name"))
        elif tool == "open_website":
            result = open_website(params.get("url"))
        elif tool == "get_system_info":
            result = get_system_info()
        elif tool == "just_chat":
            reply = params.get("reply", "I'm here, how can I help?")
            _add_to_history(user_text, reply)
            return reply
        else:
            return "I don't have that capability yet."

        # ── Step 3: format tool result into spoken reply ──────────
        # Use the fast 8B model for formatting — it's 3-5× faster than 70B
        # and this is a simple rewrite task, not reasoning.
        fmt = client.chat.completions.create(
            model="llama-3.1-8b-instant",
            messages=[
                {"role": "system", "content": FORMAT_PROMPT},
                {"role": "user",   "content": f"Data: {result}"},
            ],
            temperature=0.9,
            max_tokens=96,
        )
        reply = fmt.choices[0].message.content.strip()
        _add_to_history(user_text, reply)
        return reply

    except json.JSONDecodeError:
        # Model replied conversationally — use it directly
        _add_to_history(user_text, raw)
        return raw
    except Exception as e:
        print(f"[Orchestrator Error] {e}")
        return "I ran into a small issue. Try again?"
