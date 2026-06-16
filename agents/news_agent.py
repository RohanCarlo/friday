# agents/news_agent.py

import requests
from config import NEWS_API_KEY

def get_news(category: str = "general", country: str = "in") -> str:
    url = (
        f"https://newsapi.org/v2/top-headlines"
        f"?country={country}&category={category}&pageSize=5&apiKey={NEWS_API_KEY}"
    )
    
    try:
        articles = requests.get(url, timeout=5).json().get("articles", [])
        
        if not articles:
            return "I couldn't find any news right now."
        
        headlines = [f"{i+1}. {a['title'].split(' - ')[0]}" for i, a in enumerate(articles[:5])]
        return "Here are today's top headlines. " + ". ".join(headlines)
    
    except Exception as e:
        return f"News service unavailable. Error: {e}"